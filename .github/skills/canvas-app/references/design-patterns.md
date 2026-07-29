# Canvas App 設計パターン

Canvas App で添付ファイルを扱い、Power Automate 中継で AI Builder / 外部処理へ渡すための
案件非依存の設計パターン。

## 1. PDF 添付パターン

### 1.1 AddMedia は PDF 添付の標準解ではない

- `AddMedia` は画像アップロード中心のため、PDF を含む任意ファイル添付には不向き。
- PDF を扱う要件では、**Canvas Form の Attachments コントロール** を優先する。

### 1.2 推奨構成

Canvas で PDF や画像を扱う場合は、次の構成が安定しやすい。

1. Canvas App では **Edit Form + Attachments** を使う
2. 一時置き場として **SharePoint リスト** を使う
3. `SubmitForm` 後の `LastSubmit.ID` を Flow に渡す
4. Flow 側で添付ファイルを取得して後続処理へ渡す

### 1.3 なぜこの構成がよいか

- Canvas 側のファイル型制約を回避できる
- Power Automate 側で添付取得や変換を一元化できる
- AI Builder や外部 API への受け渡しを Flow に閉じ込められる

## 2. Canvas から Flow / AI を呼ぶ設計

### 2.1 直接呼び出しより Flow 中継を優先する

- Canvas から Copilot Studio や AI 機能を **直接** 叩く方式は、要求形式や認証差分で不安定になりやすい。
- Power Automate を中継にすると、入力整形・例外処理・ログ記録・接続差分吸収をまとめられる。

### 2.2 Flow シグネチャの注意

- Power Apps V2 トリガーの引数定義を変更しても、Canvas 側に **古いシグネチャ** が残ることがある。
- 引数数不一致が出たら、Flow を再追加して接続メタデータを更新する。

### 2.3 Flow 表示名の注意

- Canvas 式中の Flow 参照名は内部名ではなく **表示名** になることがある。
- たとえば `MyFlow.Run(...)` と `マイフロー.Run(...)` のような差異が起こりうる。
- 接続し直した後は、式中の参照名を必ず実際の表示名に合わせる。

> [!TIP]
> 中継フローは ASCII 名で作ると Code Apps 連携・式参照ともに安定する。
> 日本語表示名は Canvas 式の参照名ズレやサニタイズ失敗の原因になりやすい。

## 3. SharePoint staging パターン

### 3.1 最小構成

- SharePoint の汎用リストを 1 つ用意する
- 添付ファイルを有効にする
- 必須列は最小にする

### 3.2 Canvas 側の基本式

1. Form の `DataSource` を staging リストにする
2. `Item` は `Defaults(<ListName>)` にする
3. 添付がある場合のみ `SubmitForm` する
4. `OnSuccess` で非表示の後続処理ボタンやロジックを呼ぶ

```powerfx
// 送信ボタン OnSelect の例
If(
    CountRows(EditForm1.Updates.'添付ファイル') > 0,
    SubmitForm(EditForm1)
)

// Form の Item
Defaults('StagingList')

// OnSuccess（後続の中継フロー呼び出し）
'ProcessAttachmentFlow'.Run(EditForm1.LastSubmit.ID)
```

### 3.3 Flow 側の基本処理

1. Power Apps から staging item ID を受け取る
2. `GetItemAttachments` で添付一覧を取得する
3. `GetAttachmentContent` で本体を読む
4. 必要に応じて保存・抽出・AI 呼び出しを行う

## 4. AI Builder 入力設計

### 4.1 実際に受けるパラメータだけ渡す

- AI Builder custom prompt では、**未定義パラメータを足すと保存や有効化に失敗** することがある。
- document 型入力では、定義済みのプロパティだけを渡す。

### 4.2 実装上の指針

- まず最小パラメータで動かす
- 動作確認後に拡張する
- 追加フィールドは prompt 側定義と厳密に一致させる

> [!NOTE]
> AI Builder 側の制約・PATCH 不可項目・base64 入力の注意は
> [ai-builder スキル](../../ai-builder/SKILL.md) と
> [power-automate-integration リファレンス](../../ai-builder/references/power-automate-integration.md) を参照。

## 5. Canvas App UI レビューの観点

Canvas App の画面をレビューするときは、個別の見た目の好みよりも、利用者が迷わず使えるかを先に確認する。

### 5.1 まず見る項目

- 画面タイトルが役割と一致しているか
- 主要 CTA が 1 つ目立ち、補助操作が埋もれていないか
- 文字切れ、部分的な欠け、変な縦バーが出ていないか
- アイコンや装飾が、意味ではなくノイズとして増えていないか
- 同じ画面内で装飾のトーンや密度がばらついていないか
- `ModernText` の `AutoHeight` が意図どおりか
- 横幅固定の選択肢が内部スクロールに閉じ込められていないか
- ギャラリーの `ShowScrollbar` と実際の行数が釣り合っているか

### 5.2 画面別の確認観点

- Home: 何をすべき画面か一目で分かるか、管理系操作が回答導線と混ざっていないか
- Response: 選択肢 1 つずつを見比べやすいか、ラジオや入力欄の高さが詰まりすぎていないか
- Completion: 完了メッセージと戻り先が明確か
- Admin: 一覧の密度が高すぎず、状態変更と公開切替が同じ行で扱いやすいか
- Aggregation: 集計値と内訳の関係が追いやすく、途中で切れたカードや行がないか

### 5.3 判断の基準

- まず情報の優先順位を揃える
- 次に余白と高さを整える
- 最後に装飾を足す。
- 迷ったら、見せたい情報を減らしてコントラストを上げる
