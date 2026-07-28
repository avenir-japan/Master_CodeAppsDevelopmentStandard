# Canvas App AI codegen workflow

Canvas Apps plugin、Canvas Authoring MCP、coauthoring を使って、Canvas App を **AI 主導で作成・編集** するための基準手順。

> [!IMPORTANT]
> この方式は preview を含む。
> 本番運用前提ではなく、必ず Designer 上で動作確認し、組織標準・セキュリティ・アクセシビリティ要件を別途確認する。

## 1. これは何のための方式か

この方式は、Canvas App を **今その場で作る / 直す** ためのライブ編集モードである。

- 新規 Canvas App を自然言語から作る
- 既存 App を同期して編集する
- 利用可能な control / API / data source を調べながら進める
- YAML を検証し、Power Apps Studio の coauthoring セッションへ反映する

source control や ALM の正本は別で考える。
履歴管理は [source code and Git integration](source-code-and-git-integration.md)、移送は [ALM and import options](alm-and-import-options.md) を参照。

## 2. 前提条件

### 2.1 必須要件

- `.NET 10 SDK` 以上
- Power Apps Studio で対象 App を開ける権限
- coauthoring を有効にした Designer セッション
- Canvas Apps plugin の導入

### 2.2 plugin が提供する代表機能

- `configure-canvas-mcp`
- `generate-canvas-app`
- `edit-canvas-app`

### 2.3 MCP 側の代表ツール

- `connect`
- `sync_canvas`
- `compile_canvas`
- `list_controls`
- `describe_control`
- `list_data_sources`
- `get_data_source_schema`
- `list_apis`
- `describe_api`

## 3. セットアップ手順

1. Power Apps Studio で対象 App を開く
2. Settings → Updates → Coauthoring を有効にする
3. Designer の URL を取得する
4. `configure-canvas-mcp` 相当の手順で environment ID / app ID / cluster を設定する
5. Designer タブを閉じずに維持する

> [!IMPORTANT]
> Designer タブは前面表示し続ける必要はないが、閉じると coauthoring セッションが切れる。

## 4. 新規 App を作る流れ

1. 自然言語で要件を伝える
2. 必要に応じて画面イメージ、利用者、デバイス、データソース前提を補足する
3. AI が control / data source / API を確認しながら `pa.yaml` を生成する
4. `compile_canvas` で検証する
5. Designer 上で見た目と動作を確認する
6. Save、必要なら Publish する

## 5. 既存 App を編集する流れ

1. 対象 App を coauthoring セッションで開く
2. `sync_canvas` で現在状態をローカルへ同期する
3. 変更内容を自然言語で伝える
4. 生成・修正された `pa.yaml` を `compile_canvas` で検証する
5. Designer 上で結果を確認する
6. Save、必要なら Publish する

## 6. 何を AI ができて、何をできないか

AI が得意なこと:

- 画面生成
- レイアウト修正
- Power Fx の修正
- control / API / schema の探索
- YAML の検証と再修正

AI が直接できないこと:

- Studio 内での data source 追加
- connection 作成
- connector の認証操作

この境界は [data source and connector boundary](data-source-and-connector-boundary.md) を参照。

## 7. 検証の考え方

- `compile_canvas` は重要だが、それだけで完了とみなさない
- coauthoring 未接続時は false negative や connection 未解決が混ざることがある
- 最終確認は Designer 上で行う
- 保存の正本は Save / Publish 側にある

## 8. うまくいかないとき

### 8.1 画面が変わらない

- 別の App を開いていないか
- app ID がずれていないか
- Designer タブを閉じていないか

### 8.2 MCP が応答しない

- `.NET 10 SDK` を確認する
- coauthoring が有効か確認する
- Designer セッションが切れていないか確認する
- 設定をやり直す

### 8.3 直近の変更を戻したい

- まず同期元の coauthoring 状態を確認する
- 直前の安定状態へ戻す
- 再度 compile と Designer 確認を行う

## 9. この方式を選ぶべきケース

- その場で App を作りたい
- 既存 App を会話しながら変えたい
- 画面や Power Fx を反復的に試したい

逆に、履歴管理が主目的なら Git Integration、環境移送が主目的なら solutions / single app / package を検討する。
