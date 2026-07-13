# 新アーキテクチャ（cliagent）構造リファレンス

Copilot Studio の **新アーキテクチャ（`cliagent`）** が Dataverse 上でどう保持されるかの要点。
このマスターでは **Bot の作成そのものは UI 手動前提** だが、作成後の調査・保守では以下の構造理解が必要になる。

## Bot 本体（`bots` テーブル）

| 列 | 役割 | 補足 |
| --- | --- | --- |
| `template` | 新アーキ識別子 | `cliagent-1.0.0` が目印 |
| `schemaname` | 内部一意名 | 環境ごとに異なる |
| `configuration` | 設定本体 | **BotConfiguration JSON** を文字列で保持 |
| `synchronizationstatus` | 同期状態 | UI 直後や変更直後に揺れることがある |
| `iconbase64` | アイコン | Bot アイコン画像 |

> v1 と最大に違うのは、設定の中心が GPT コンポーネントではなく **`bots.configuration`** に寄っている点。

## configuration（BotConfiguration JSON）

```json
{
  "$kind": "BotConfiguration",
  "channels": [
    { "$kind": "ChannelDefinition", "id": "MsTeams", "channelId": "MsTeams" }
  ],
  "recognizer": { "$kind": "CLICopilotRecognizer" },
  "agentSettings": {
    "$kind": "AgentSettings",
    "model": { "$kind": "ModelConfig", "series": "Sonnet46" },
    "instructions": {
      "$kind": "Instructions",
      "segments": [
        { "$kind": "StaticSegment", "value": "<エージェントの指示文>" }
      ]
    },
    "enableMemory": true
  }
}
```

| パス | 意味 |
| --- | --- |
| `recognizer.$kind` | 新アーキの認識器。`CLICopilotRecognizer` |
| `agentSettings.model.series` | モデル系列 |
| `agentSettings.instructions.segments[].value` | 指示文。プレーン文字列 |
| `agentSettings.enableMemory` | 会話メモリの有効化 |

### 改変時の原則

- `configuration` は **丸ごと上書きしない**
- 変更時は **GET → ディープマージ → PATCH** を前提にする
- v1 のような PVA ダブル改行 YAML を探しにいかない

## botcomponents（配下コンポーネント）

| componenttype | 種別 | 格納先 |
| --- | --- | --- |
| 9 | InlineAgentSkill または McpTool | `data` |
| 14 | FileAttachmentComponent | `filedata` |

### type=9 スキル（InlineAgentSkill）の data

```text
kind: InlineAgentSkill
content:
<!-- bic:bundle=crskill_<name>_zip_<hash> -->
```

### type=9 ツール（McpTool）の data

```text
kind: McpTool
connectorId: /providers/Microsoft.PowerApps/apis/...
authMode: Invoker
connectionReference: <prefix>.cr.<connector>.<guid>
operationId: mcp_<ServerName>
```

> MCP ツールは接続参照に依存するため、スキルより環境差異に弱い。
> このマスターで API 自動化せず UI 手動追加を正本にする理由はここにある。

### type=14 同梱ファイル

| 列 | 内容 |
| --- | --- |
| `name` | フラットなファイル名 |
| `schemaname` | ファイル用の一意名 |
| `filedata` | 実体バイト |
| `_parentbotcomponentid_value` | 親スキル(type=9) |

## v1 との対比早見

| 観点 | v1（classic / GPT コンポーネント） | v2（cliagent） |
| --- | --- | --- |
| 設定の中心 | botcomponents type=15 の YAML | `bots.configuration` の JSON |
| Instructions 形式 | PVA ダブル改行 YAML | プレーン文字列 segment |
| モデル指定 | `aISettings.model.modelNameHint` | `agentSettings.model.series` |
| スキル / ツール | ナレッジ・トピック中心 | type=9 InlineAgentSkill / McpTool |