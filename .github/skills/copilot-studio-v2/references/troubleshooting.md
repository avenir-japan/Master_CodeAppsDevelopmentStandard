# copilot-studio-v2 — 異常系・よくあるエラー

新アーキテクチャ（cliagent）でのデプロイ・公開時に遭遇しやすいエラーと対処。
正常系の手順は [SKILL.md](../SKILL.md) を参照。

## よくあるエラー

| 症状 | 原因 | 対処 |
|---|---|---|
| `0x8004023b "Connection State is closed"` | Bot プロビジョニング直後で認可セッション未確立 | 数秒待って **リトライ**（一時エラー） |
| `undeclared property 'parentbotcomponentid'` | 親ナビ名が誤り | `ParentBotComponentId`（Pascalケース）を使う |
| `bot $select` で 400 | 新アーキに存在しない列を指定 | 全列取得してから必要列をフィルタ |
| `0x80040265`（bots 更新不可） | PATCH に `name` 列を含めていない | アイコン等の PATCH でも `name` を同送 |
| **UI の Model が「廃止されたモデル」になる** | `agentSettings.model.series` に旧命名（`Sonnet46` / `Sonnet5` / `Opus5`）を指定した | 現在利用可能なモデルと設定方法を Copilot Studio UI と公式情報で確認し、対象エージェントで変更後に再公開・動作確認する。未同梱のスクリプトや参照先を前提にしない |
| `Teams channel must be enabled`（上流の `set_app_details.py` 利用時の 404 / ErrorCode 7513） | Teams + Microsoft 365 チャネルが未有効 | このマスターでは UI の「チャネル」で利用可否と有効化を確認する。`set_app_details.py` は同梱していない |
| 公開時 `1 missing connection reference` | MCP サーバー追加後に接続参照が正しくバインドされていない | 対象 MCP サーバーを UI から削除→再追加→再公開（references/mcp-servers.md） |
| 公開後も MCP がエラー | UI の「確認(Confirm)」未実施 | UI で MCP サーバーを **Confirm**（再公開だけでは消えないことがある） |
| **UI の Confirm を押しても接続できない** | 接続参照バインドが古い状態で残っている（新 UI で頻発） | UI で対象 MCP サーバーを削除→再追加 → 再公開 → UI で再 Confirm（references/mcp-servers.md） |
| **設定を更新したら手動追加した MCP ツールが消えた** | `configuration` の丸ごと上書きや、名前で絞らない `componenttype eq 9` の削除（MCP ツールも type=9） | UI 更新を通常案とし、公開前にツール・接続参照を確認する。API 更新を例外的に採る場合は GET → deep-merge → PATCH とし、削除対象を名前で絞って前後差分を検査する。このマスターに `update_agent.py` や PATCH 前の自動ガードは同梱されていない |
| 更新のたびにエージェントが重複作成される | 新規作成と既存更新を取り違えた（上流の自動作成例を使用した場合） | このマスターでは [手動作成の正常系](../SKILL.md#このマスターでの既定フロー)に従い、運用中の既存エージェントを UI で確認してから更新する。上流の自動作成・更新スクリプトは同梱していない |
| 初期メッセージが既定文のまま | 初期メッセージ・会話スターターの設定漏れ | [手動作成チェックリスト](manual-creation-checklist.md)で UI の表示・公開後の文面を確認して修正する。このマスターに `set_prompts.py` 等の自動更新スクリプトは同梱していない |
| 日本語出力で `UnicodeEncodeError`（cp932） | Windows コンソール既定 | `sys.stdout.reconfigure(encoding="utf-8")` |
| 生成したファイルが UI 上でダウンロードできない | **同じファイル名**で複数回出力すると UI がダウンロードリンクを解決できない | Instructions（システムプロンプト）に「ファイルを出力する際は毎回異なるファイル名にする（例: 日時やUUIDを付与）」を明記する（[SKILL.md](../SKILL.md) の Instructions 設計を参照） |
