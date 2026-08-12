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

| 利用形態                  | plugin の入口                                  | MCP 設定の考え方                                                  | この repo との関係                         |
| ------------------------- | ---------------------------------------------- | ----------------------------------------------------------------- | ------------------------------------------ |
| GitHub Copilot in VS Code | 拡張機能ビューの Agent Plugin / MCP Server     | `.vscode/mcp.json` またはユーザー設定で `canvas-authoring` を登録 | この repo の標準運用と最も相性がよい       |
| Copilot CLI / Claude Code | `/plugin marketplace add` と `/plugin install` | plugin 側のセットアップフローで MCP を登録                        | 導入入口は異なるが、接続後の運用基準は同じ |

どちらの入口でも、最終的に必要なのは同じである。

1. Canvas Apps plugin が入っている
2. `canvas-authoring` が対象 app に向くよう設定されている
3. Power Apps Studio 側で coauthoring セッションが開いている

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

### 3.0 ゼロから最初の疎通確認までの一本道

GitHub Copilot を使って **最初の `list_controls` 成功** まで到達する最短手順は次のとおり。

1. `.NET 10 SDK` が入っていることを確認する
2. Canvas Apps plugin を導入する
3. Power Apps Studio で対象 app を開く
4. Settings → Updates → Coauthoring を有効にする
5. Designer の URL を控える
6. `configure-canvas-mcp` を実行するか、`.vscode/mcp.json` に `canvas-authoring` を登録する
7. Designer タブを閉じない
8. `connect` を実行する
9. `list_controls` を 1 回実行する

この 9 手順で `list_controls` が成功すれば、**MCP の最初の疎通確認は完了** とみなしてよい。

もし `list_controls` が `Not connected` で失敗したら、まず設定ミスよりも前に `connect` 未実行かセッション切れを疑う。

### 3.1 VS Code Copilot のローカル設定

VS Code Copilot では、Canvas Authoring MCP を `.vscode/mcp.json` に登録する運用が分かりやすい。
設定値は Designer の URL から取得した `environment ID`、`app ID`、`cluster category` を使う。

最小構成の例は次のとおり。

```json
{
  "servers": {
    "canvas-authoring": {
      "type": "stdio",
      "command": "dnx",
      "args": [
        "Microsoft.PowerApps.CanvasAuthoring.McpServer",
        "--yes",
        "--prerelease",
        "--source",
        "https://api.nuget.org/v3/index.json"
      ],
      "env": {
        "CANVAS_ENVIRONMENT_ID": "{ENVIRONMENT_ID}",
        "CANVAS_APP_ID": "{APP_ID}",
        "CANVAS_CLUSTER_CATEGORY": "{CLUSTER_CATEGORY}"
      }
    }
  }
}
```

そのまま流用しやすいテンプレート:

```json
{
  "servers": {
    "canvas-authoring": {
      "type": "stdio",
      "command": "dnx",
      "args": [
        "Microsoft.PowerApps.CanvasAuthoring.McpServer",
        "--yes",
        "--prerelease",
        "--source",
        "https://api.nuget.org/v3/index.json"
      ],
      "env": {
        "CANVAS_ENVIRONMENT_ID": "<ENVIRONMENT_ID>",
        "CANVAS_APP_ID": "<APP_ID>",
        "CANVAS_CLUSTER_CATEGORY": "<CLUSTER_CATEGORY>"
      }
    }
  }
}
```

置換が必要な値:

- `<ENVIRONMENT_ID>`: `make.powerapps.com/e/{environmentId}/...` の値
- `<APP_ID>`: Designer URL の `app-id` の GUID
- `<CLUSTER_CATEGORY>`: `configure-canvas-mcp` または Designer URL から得た cluster category

`environment ID` は `make.powerapps.com/e/{environmentId}/canvas/...` の `e/` 配下の値、`app ID` は `app-id` の末尾 GUID を使う。

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
