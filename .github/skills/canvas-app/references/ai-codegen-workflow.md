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
- 対象環境と Canvas App を編集できる組織アカウント
- Power Apps Studio で作成・保存済みの対象 App（新規の場合も空の App を先に保存する）
- coauthoring を有効にした Designer セッション
- Canvas Apps plugin の導入

plugin は最初の App レコードの作成や coauthoring の有効化はできない。接続後に、保存済みの空 App の画面や式を AI で作成できる。

### 2.1.1 GitHub Copilot を第一候補にした導入方針

この repo では、Canvas App の AI 編集は **まず GitHub Copilot で使う** 前提で整理する。

- GitHub Copilot in VS Code: VS Code 上で `canvas-apps` Agent Plugin と `canvas-authoring` MCP を使う
- Copilot CLI / Claude Code: plugin コマンドで `canvas-apps@power-platform-skills` を追加する

Copilot CLI / Claude Code で導入する場合の代表コマンド:

```text
/plugin marketplace add microsoft/power-platform-skills
/plugin install canvas-apps@power-platform-skills
```

> [!IMPORTANT]
> 上記コマンドは **この repo が提供するものではない**。
> 外部 plugin を開発端末へ導入するための入口であり、導入後の運用基準をこの repo が補完する。

### 2.1.2 VS Code Copilot と Copilot CLI / Claude Code の違い

| 利用形態                  | plugin の入口                                  | MCP 設定の考え方                                                      | この repo との関係                         |
| ------------------------- | ---------------------------------------------- | --------------------------------------------------------------------- | ------------------------------------------ |
| GitHub Copilot in VS Code | 拡張機能ビューの Agent Plugin / MCP Server     | plugin が登録する `canvas-authoring` に `configure-canvas-mcp` で接続 | この repo の標準運用と最も相性がよい       |
| Copilot CLI / Claude Code | `/plugin marketplace add` と `/plugin install` | plugin 側のセットアップフローで MCP を登録                            | 導入入口は異なるが、接続後の運用基準は同じ |

どちらの入口でも、最終的に必要なのは同じである。

1. Canvas Apps plugin が入っている
2. `canvas-authoring` が対象 app に向くよう設定されている
3. Power Apps Studio 側で coauthoring セッションが開いている

### 2.2 plugin が提供する代表機能

- `configure-canvas-mcp`
- `canvas-app`（空 App の画面生成と既存 App の編集）

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
4. `configure-canvas-mcp` に Designer の完全な編集 URL を渡して接続する
5. Designer タブを閉じずに維持する

### 3.0 ゼロから最初の疎通確認までの一本道

GitHub Copilot を使って **最初の `list_controls` 成功** まで到達する最短手順は次のとおり。

1. `dotnet --list-sdks` で `.NET 10 SDK` 以上を確認する
2. Canvas Apps plugin を導入する
3. 対象環境で App を作成・保存する（既存 App があればそれを開く）
4. Settings → Updates → Coauthoring を有効にする
5. Designer の完全な編集 URL を控え、タブを開いたままにする
6. `configure-canvas-mcp` にその URL を渡して接続する
7. `list_controls` を 1 回実行し、対象 App と整合することを確認する

この手順で `list_controls` が成功すれば、**MCP の最初の疎通確認は完了** とみなしてよい。

もし `list_controls` が `Not connected` で失敗したら、まず設定ミスよりも前に `connect` 未実行かセッション切れを疑う。

### 3.1 VS Code Copilot の接続

VS Code の拡張機能ビューで `@agentPlugins canvas apps` を検索し、Microsoft 発行の Canvas Apps plugin を導入する。
plugin は `canvas-authoring` MCP を登録するため、通常は `.vscode/mcp.json` にサーバーを手動登録しない。
Chat の Agent モードで `configure-canvas-mcp` を起動し、Power Apps Studio の編集画面のアドレスバーから完全な URL を渡す。
plugin は URL の `/e/` 配下から environment ID、URL デコードした `app-id` の末尾から app ID、ホスト名から `environment_category` を判定して `connect` する。
app player や Power Apps ホーム画面の URL は使わず、実際に開いている Designer の URL と対象環境を照合する。
接続が成功したら `list_controls` で疎通を確認する。

手動 MCP 設定や接続用 wrapper を使う場合は、導入済み plugin の現行仕様と `connect` の引数を確認してから設定する。旧来の `CANVAS_CLUSTER_CATEGORY` を含む固定設定例を流用しない。

> [!IMPORTANT]
> Designer タブは前面表示し続ける必要はないが、閉じると coauthoring セッションが切れる。

### 3.2 使える状態の判定基準

次を満たしたら、Canvas Authoring MCP は **使える状態** と判定してよい。

1. `connect` が成功する
2. `list_controls` が成功する
3. 返ってきた control 一覧が、今開いている対象 app と整合する

この 3 点を、この repo では Canvas App MCP 利用開始の **Definition of Done** とする。

逆に、`canvas-apps` や `canvas-authoring` がインストール済みに見えても、
上記 3 点を満たさない限りは **導入済みであっても利用開始完了ではない**。

## 4. 新規 App を作る流れ

1. 対象環境で空 App を作成・保存し、coauthoring を有効にして Designer を開いておく
2. 自然言語で要件を伝え、必要に応じて画面イメージ、利用者、デバイス、データソース前提を補足する
3. 接続後、専用作業ディレクトリへ初回同期し、AI が control / data source / API を確認しながら `pa.yaml` を生成する
4. `compile_canvas` で検証する
5. Designer 上で見た目と動作を確認する
6. Save、必要なら Publish する

## 5. 既存 App を編集する流れ

1. 対象 App を coauthoring セッションで開く
2. 専用作業ディレクトリへ `sync_canvas` で現在状態を初回同期する
3. 変更内容を自然言語で伝える
4. 生成・修正された `pa.yaml` を `compile_canvas` で検証する
5. Designer 上で結果を確認する
6. Save、必要なら Publish する

### 同期時の上書き防止

`sync_canvas` は同名のローカル `.pa.yaml` を **上書きする**。同期前に対象 App とディレクトリを確認し、未コミット・未退避のローカル変更がある場合は差分を確認して保護する。
最初の同期は App 専用ディレクトリで行い、同期時に `.pa.yaml` 以外のファイルを混在させない。リポジトリのルートや異なる App の作業領域を指定しない。
編集後の作業ディレクトリへ安易に再同期しない。サーバー側の状態を再確認するときは別の空ディレクトリへ同期し、作業コピーと差分を比較する。

### 接続と変更の安全確認

- 対象環境、Designer の App URL、`connect` の接続先、実行アカウントと編集権限を照合する。必要な権限だけを持つアカウントを使う。
- 利用する connector / data source が組織の DLP ポリシーとライセンス条件に適合するか確認する。接続の追加は [data source and connector boundary](data-source-and-connector-boundary.md) に従う。
- AI の提案する操作とツール引数を確認し、外部データから誘導された予期しない変更やアクセス要求は承認しない。
- パスワード、アクセストークン、接続文字列などをプロンプト、ログ、リポジトリへ記録しない。開発用 App で確認してから本番適用を判断する。

公式の前提・セキュリティ事項は [Canvas Apps plugin README](https://github.com/microsoft/power-platform-skills/tree/main/plugins/canvas-apps)、接続引数は [configure-canvas-mcp](https://github.com/microsoft/power-platform-skills/blob/main/plugins/canvas-apps/skills/configure-canvas-mcp/SKILL.md) を参照する。

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

## 7. 最初の疎通確認

接続設定後は、まず `connect` に続けて `list_controls` を実行し、対象 app に対して MCP が実際に触れていることを確認する。

もし `list_controls` が `Not connected` で失敗するなら、先に `connect` を実行し直す。これは設定不備よりも前提未実行で起きやすい。

この境界は [data source and connector boundary](data-source-and-connector-boundary.md) を参照。

## 8.1 Canvas Authoring MCP の薄い wrapper を作るとき

- `connect + compile_canvas`、`connect + sync_canvas` は、環境 ID・app ID・login hint・directoryPath を引数化した Node テンプレートにしておくと再利用しやすい。
- hardcode は極力避け、既定値は `.env` か CLI 引数で受ける。
- 特定案件向けの値を埋め込んだスクリプトは、master 側ではなく案件リポジトリに置く。

## 8. 検証の考え方

- `compile_canvas` は重要だが、それだけで完了とみなさない
- `compile_canvas` が通っても preview 崩れは残りうるので、Designer 上の目視確認と局所修正を別工程として扱う
- 広いレイアウト rewrite より、小さい可逆修正を優先する
- coauthoring 未接続時は false negative や connection 未解決が混ざることがある
- 最終確認は Designer 上で行う
- 保存の正本は Save / Publish 側にある

## 9. うまくいかないとき

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
