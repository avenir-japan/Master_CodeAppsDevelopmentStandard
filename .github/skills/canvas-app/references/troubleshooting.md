# Canvas App トラブルシューティング

Canvas App の AI 編集、coauthoring、single app / package、UI 調整で頻出する問題と対処法。

## 1. MCP / coauthoring の基本切り分け

### 1.1 まず確認すること

- `canvas-authoring` MCP が正しく設定されているか
- `.NET 10 SDK` が入っているか
- Power Apps Studio の対象 app で coauthoring が有効か
- Designer タブが開いたままか

接続確認の最短経路は、`connect` で対象 app に入ってから `list_controls` を 1 回実行すること。
`list_controls` が `Not connected` を返す場合は、設定ミスよりも前に `connect` 未実行を疑う。

再接続時は、前回成功したアカウントの `login_hint` を使うと認証のやり直しを減らしやすい。

セットアップ自体の流れは [ai-codegen-workflow](ai-codegen-workflow.md) を参照。

### 1.2 compile は通るが画面が変わらない

- compile が成功しても画面が変わらない場合は、まず **別の app を開いていないか** を疑う。
- `canvas-app.config.json` や手元メモの appId ではなく、**Designer の URL に含まれる app-id を正** として確認する。
- coauthoring live 反映では、Designer タブを前面表示し続ける必要はないが、**タブを閉じると反映経路が切れる**。

切り分け順:

1. Designer の URL の `app-id` が対象 app と一致しているか
2. いま見ている画面が本当にその app の Designer か
3. タブを閉じていないか、サインアウトしていないか、セッションが切れていないか

### 1.3 coauthoring セッション切れ

- `sync_canvas` や `compile_canvas` が通っても結果が不自然な場合は、coauthoring セッションが切れていることがある。
- その場合は、Designer を開き直して coauthoring を有効にした状態で再接続する。
- 最終的な保存の正本は Designer 側の **Save / Publish** であり、compile 成功だけで保存完了とみなさない。
- `422` が出た場合も、source 問題と決め打ちせず、まず Designer reopen と再接続を試す。

- 接続後すぐに `list_controls` を実行すると、内部のクラスタ解決や authoring endpoint 切り替え待ちが入ることがある。
- そのため、接続直後の数秒は結果未反映に見えても、まずは `connect` 完了を待ってから再試行する。

再接続時は、前回成功したアカウントの `login_hint` を使うと認証のやり直しを減らしやすい。

### 1.4 画面だけが不自然に崩れる

- 灰色の縦バー、テキスト切れ、謎の高さ崩れが出たら、まず `ModernText` の `AutoHeight` を確認する。
- 意図して固定高にしているのでなければ、`AutoHeight=true` を先に疑う。
- 特に見出し、説明文、カード内ラベルは、固定高のままだと preview 崩れの原因になりやすい。

### 1.5 blank-safe の基本

- `selected` 系や画面選択変数が `Blank()` になりうる場合は、`OnVisible` で初期化する。
- Gallery の空分岐は `Blank()` より `FirstN(collection, 0)` を優先する。
- 集計関数は、空集合で落ちないように `CountRows(...) = 0` を先に判定する。

### 1.6 ブラウザ制約

- 組織ポリシーで VS Code 内蔵ブラウザが使えない場合がある。
- その場合は最初から **外部ブラウザ前提の runbook** に切り替える。

## 2. PAC CLI 制約と非推奨ワークアラウンド

### 2.1 app 名指定 pull を優先する場面がある

- `canvas-app.config.json` の `appId` や `studioUrl` が **古い app を指す** ことがある。
- 正本確認や再取得では `pac canvas download --name "<AppName>"` が安全な場合がある。

```bash
# appId 指定より名前指定が安全なケース
pac canvas download --name "MyCanvasApp" --file-name current.msapp
```

### 2.2 pack / unpack は deprecated で、壊れる場合がある

- `pac canvas pack --layout SourceCode` は app によって `ValidateSources` で **FormatException** で失敗することがある。
- clean な unpack / repack でも再現する場合は、YAML 自体ではなく **PAC 側の問題** を疑う。
- そもそも `pack` / `unpack` は deprecated であり、標準運用にはしない。

### 2.3 回避策: msapp を ZIP として扱う

msapp は ZIP 形式なので、どうしても必要な場合だけ次の回避策が使える。

1. msapp を ZIP として展開する
2. `Src/*.pa.yaml` を編集する
3. ZIP として再封入し、拡張子を `.msapp` に戻す

> [!WARNING]
> Microsoft Learn では、source control の対象は `Src` 配下の `pa.yaml` のみであり、JSON は安定ソースではない。
> `Controls/*.json` の確認は、標準運用ではなく **最終手段の切り分け** として扱う。

具体的な取得・編集・再封入・import 手順は
[import / deploy runbook](import-deploy-runbook.md) を参照。

## 3. Attachments UI 崩れの直し方

### 3.1 崩れやすい原因

- Attachments コントロール本体の幅と高さが既定値のまま
- 親 DataCard の幅や高さが既定値のまま
- `DataCardKey` ラベルが表示されたまま
- AutoLayout 側の親コンテナ高さが不足している

### 3.2 最初に確認するポイント

1. 親コンテナの `Height`
2. ManualLayout コンテナの `Height`
3. Attachments データカードの `Width` / `Height` / `X`
4. `DataCardKey.Visible`
5. Attachments 本体の `Width` / `Height` / `X` / `Y`
6. `NoAttachmentsText` と `Tooltip`

### 3.3 実践ルール

- **本体だけでなく親 DataCard まで含めてサイズ調整** する
- 見出しラベルの既定表示は不要なら消す（`DataCardKey.Visible = false`）
- `Fill` と `HoverFill` を周辺カードと揃えて視覚ノイズを減らす

## 4. compile と検証の運用

### 4.1 coauthoring 未接続 compile の限界

- coauthoring 未接続の compile は **false negative** やコネクタ未解決エラーを出すことがある。
- 接続系エラーが多発する場合は、**Designer を開いた状態で最終確認** する。
