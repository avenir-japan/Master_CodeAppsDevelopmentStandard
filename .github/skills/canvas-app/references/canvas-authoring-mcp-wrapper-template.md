# Canvas Authoring MCP wrapper template

Canvas Authoring MCP を使うときの、案件横断で再利用しやすい薄い Node wrapper の考え方。

## 1. 目的

- `connect` の後に `compile_canvas` を実行する
- `connect` の後に `sync_canvas` を実行する
- 案件ごとの hardcode を減らす

## 2. 設計方針

- `environment_id` を環境変数または CLI 引数で受ける
- `app_id` を環境変数または CLI 引数で受ける
- `login_hint` を環境変数または CLI 引数で受ける
- `directoryPath` を環境変数または CLI 引数で受ける
- 失敗時は process exit code をそのまま返す

## 3. 使い分け

- compile 用と sync 用は、共通の接続初期化だけ切り出す
- 案件固有の固定値はテンプレートに埋め込まない
- 実運用の呼び出し側で、対象 app に応じた値を渡す

## 4. 参照先

- [Canvas App AI codegen workflow](ai-codegen-workflow.md)
- [Canvas App coauthoring limitations](coauthoring-limitations.md)