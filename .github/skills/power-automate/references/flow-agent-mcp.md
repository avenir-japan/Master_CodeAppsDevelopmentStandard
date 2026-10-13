# FlowAgent MCP: フロー編集と失敗実行の診断

FlowAgent MCP はクラウドフローの編集・失敗 run の診断に使う**任意の経路**。
マスターの UI 雛形 / clone 定義 / 接続参照を正本とする方針を変更しない。
新規インストールや Azure CLI の認証は、作業対象・権限と利用条件を確認してから行う。

## 利用前のゲート

1. 対象環境・ソリューション・フロー・変更範囲、実行主体、使用する接続を特定する。
2. [MCP クライアント状態チェック](../../standard/SKILL.md#事前検証-mcp-クライアント状態チェック)で
   VS Code の MCP 利用可否を確認し、利用する FlowAgent プラグインの入手元とバージョンを確認する。
3. プラグインが要求する Node.js / Azure CLI 等と、対象環境に対する権限を確認する。
   `.vscode/mcp.json` にはシークレットを記載しない。FlowAgent 側の Azure CLI 認証と
   `auth_helper.py` のブラウザー認証は別であり、片方の成功を他方の成功と扱わない。
4. GitHub Copilot CLI / Claude Code 用の `.mcp.json` を VS Code にそのまま流用しない。
   プラグインの `server/mcp.mjs` を入手して VS Code の `.vscode/mcp.json` に stdio サーバーとして登録し、
   `MCP: List Servers` で起動を確認する。ソリューション名と環境は接続前に照合する。
5. 診断用ローカルログの保存先と保持期間を確認し、機密情報が残らない運用にする。
   MCP が利用できない場合は従来の UI / API と Power Automate の実行履歴で調査する。

## 編集時

編集前の定義と接続参照を保存し、対象フロー以外を変更しない。変更案・適用対象・影響を確認してから
MCP で編集し、取得した変更後の定義に対して[デプロイ前チェック](pre-deploy-checks.md)を実行する。
Designer 保存、公開または有効化、テスト実行を別々に確認する。

## 失敗 run の診断時

対象フローと run ID、開始時刻を特定し、MCP で失敗箇所と入出力の形を調べる。
複数 run の「最新」を無条件に今回の失敗とみなさない。ユーザーデータ、添付内容、トークンを
診断記録やリポジトリに残さない。修正案は失敗の証拠と対応付け、意図しない再実行や
有効化を行わず、再実行した場合は新しい run ID と結果で効果を確認する。

参照: [Microsoft Power Platform skills (Power Automate plugin)](https://github.com/microsoft/power-platform-skills/tree/main/plugins/power-automate)。
上流のセットアップ例をそのまま適用せず、プラグインの現在の要件と社内の認証制約を照合する。
公開 README と過去の上流手順で Node.js の最低バージョンが異なるため、固定値を標準化しない。
