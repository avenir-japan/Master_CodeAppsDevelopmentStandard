---
name: copilot-studio-v2
description: "Copilot Studio の新アーキテクチャ（cliagent）を、手動作成前提で安全に扱うための判断基準・制約・構造知識を整理する。Teams / Microsoft 365 Copilot 単独利用向け。"
category: automation
triggers:
  - "Copilot Studio v2"
  - "新しいアーキテクチャ"
  - "全く新しいアーキテクチャ"
  - "cliagent"
  - "CLICopilotRecognizer"
  - "BotConfiguration"
  - "agentSettings"
  - "enableMemory"
  - "フラット Python スキル"
  - "InlineAgentSkill"
  - "MCP サーバー Confirm"
  - "エージェント v2"
---

# Copilot Studio v2（新アーキテクチャ）運用スキル

Copilot Studio の **新アーキテクチャ（`cliagent`）** を、
このマスターでは **手動作成前提** で安全に扱うためのスキル。

上流では API による完全自動構築までカバーしているが、このマスターでは
**GitHub Copilot クレジット節約のため Bot 作成は UI 手動を既定** とし、
以下を正本として扱う:

- v1 / v2 の採用判断
- cliagent の構造理解
- v2 固有の制約と落とし穴
- MCP サーバーの手動追加手順
- 新 UI でのトラブルシューティング

## いつこのスキルを使うか

このスキルが向くのは、**Teams / Microsoft 365 Copilot 単独利用** のとき。

| v2（本スキル）が向く                                    | v1（既存 `copilot-studio`）が向く                            |
| ------------------------------------------------------- | ------------------------------------------------------------ |
| Teams / M365 Copilot で単独利用し、外部から呼び出さない | Code Apps / Web サイト / 他システムから呼び出す              |
| 新アーキの構造を前提に保守したい                        | 外部公開、埋め込み、既存トリガー資産を使いたい               |
| Python スキルバンドル前提で構成したい                   | 会話開始、クイック返信、ニュース配信など v1 資産を流用したい |

> **致命的制約**: v2（cliagent）は **Code Apps から呼び出せず、Web 埋め込みにも向かない**。
> 外部連携や埋め込みがあるなら [../copilot-studio/SKILL.md](../copilot-studio/SKILL.md) を使う。

## このマスターでの既定フロー

1. `architecture` スキルで v1 / v2 を選ぶ
2. ユーザーへ設計を提示し承認を得る
3. Copilot Studio UI で v2 エージェントを手動作成する
4. [手動作成チェックリスト](references/manual-creation-checklist.md) に沿って、作成直後の確認を行う
5. 設定変更や調査では **BotConfiguration JSON** と **botcomponents 構造** を前提に扱う
6. MCP サーバー追加前に `standard/scripts/check_mcp_client.py studio` で事前確認し、その後 UI で手動追加して **Confirm** と再公開まで行う
7. アイコン設定と公開前確認は [アイコンと公開の最小ガイド](references/icon-and-publish.md) を参照する
8. 異常時は本スキルの references を優先して切り分ける

## 事前検証スクリプト（推奨）

v2 の変更作業前後では、次の検証スクリプトを実行して設定整合を確認する。

- `scripts/verify_config.py`: BotConfiguration 構造、主要キー、必須設定の整合確認
- `scripts/verify_agent.py`: エージェント全体の運用観点チェック（公開前の最終確認）

UI で設定変更した場合も、最終的な成否判定はスクリプトの結果で機械的に確認する。

## 設計確認テンプレート

v2 を採用すると決まったら、実装前に少なくとも次の内容をユーザーへ提示して承認を取る。
このテンプレートは **Teams / Microsoft 365 Copilot 単独利用** を前提にしている。

### 確認項目

| 項目           | 何を決めるか                                       |
| -------------- | -------------------------------------------------- |
| エージェント名 | Teams / M365 Copilot 上での表示名                  |
| 役割           | 何を支援するエージェントか                         |
| 対象利用者     | 誰が使うか。社内限定か                             |
| 利用チャネル   | Teams / Microsoft 365 Copilot のどちらを主に使うか |
| Instructions   | 守るべきルール、回答方針、禁止事項                 |
| モデル方針     | どのモデル系列を使うか                             |
| メモリ利用     | 会話メモリを使うか                                 |
| MCP / ツール   | 何の MCP サーバーや接続を使うか                    |
| 公開情報       | アイコン、短い説明、長い説明、開発元名、各種 URL   |
| 非対応事項     | Code Apps 呼び出しや Web 埋め込みが不要であること  |

### 提示テンプレート

以下の形で、そのまま設計確認に使える。

```md
## Copilot Studio v2 エージェント設計案

- エージェント名:
- 目的:
- 主な利用者:
- 利用チャネル: Teams / Microsoft 365 Copilot
- v2 採用理由:
  - 単独利用であり、外部埋め込みや Code Apps 連携が不要
  - 新アーキ（cliagent）の構造で運用したい

### Instructions 案

<ここに指示文全文>

### モデル / メモリ

- モデル系列:
- 会話メモリ: 有効 / 無効

### 使うツール / MCP

- 利用する MCP サーバー:
- 接続準備の要否:
- Confirm が必要な対象:

### 公開情報

- 短い説明:
- 長い説明:
- 開発元名:
- Web サイト:
- 利用規約 URL:
- プライバシー URL:
- アイコン案:

### 非対応事項の確認

- Code Apps からの呼び出し: なし
- Web 埋め込み / SDK 連携: なし
- 既存 v1 トリガー資産の流用: 不要
```

### 設計確認時の質問テンプレート

ユーザーへの確認は、少なくとも次の 4 点を含める。

1. このエージェントは Teams / Microsoft 365 Copilot 単独利用で、外部からは呼び出しませんか。
2. Instructions に必ず守らせたい業務ルールや禁止事項は何ですか。
3. 使いたい MCP サーバーや接続先は何ですか。
4. 公開時に表示したい説明文、開発元名、リンク類は何ですか。

## v1 との主な違い

| 観点         | v1（`copilot-studio`）           | v2（本スキル）                                                 |
| ------------ | -------------------------------- | -------------------------------------------------------------- |
| Bot 作成     | UI 手動前提                      | 上流では API 作成可能。マスターでは UI 手動を既定              |
| 設定の保存先 | GPT コンポーネント + PVA YAML    | `bots.configuration` の **BotConfiguration JSON**              |
| recognizer   | クラシック PVA 系                | `CLICopilotRecognizer`                                         |
| Instructions | PVA ダブル改行 YAML              | `agentSettings.instructions.segments[].value` のプレーン文字列 |
| モデル指定   | `aISettings.model.modelNameHint` | `agentSettings.model.series`                                   |
| メモリ       | 個別設定                         | `agentSettings.enableMemory`                                   |
| スキル構成   | ナレッジ / トピック中心          | **フラット Python スキルバンドル**（type=9 + type=14）         |
| MCP 追加     | 既存資産あり                     | **Copilot Studio UI で手動追加** が正本                        |

## 必須要件・落とし穴

### configuration は BotConfiguration JSON

v2 では Instructions やモデル設定は GPT YAML ではなく、`bots.configuration` 内の JSON に入る。

```json
{
  "$kind": "BotConfiguration",
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

- v1 の PVA ダブル改行 YAML は不要
- 既存設定を変更するときは **GET → ディープマージ → PATCH** を前提にする
- `configuration` の丸ごと上書きはモデルやメモリ設定を壊しやすい

### スキルはフラット Python バンドル前提

新ランタイムでは次の制約を前提にする:

```
❌ JavaScript / pptxgenjs 前提
✅ Python ベースで実装する

❌ サブフォルダに依存したバンドル構成
✅ 同一階層のフラット構成でまとめる

❌ 同梱画像ファイルをそのまま読む前提
✅ 必要なら Base64 埋め込みで扱う
```

botcomponents の基本構造:

| componenttype | 役割                       | 格納先     |
| ------------- | -------------------------- | ---------- |
| 9             | InlineAgentSkill / McpTool | `data`     |
| 14            | スキル同梱ファイル         | `filedata` |

### MCP サーバーは UI 手動追加が正本

v2 の MCP サーバー追加は API 自動化しない。
接続参照の内部状態と **Confirm** 操作に依存するため、**Copilot Studio UI で手動追加 → Confirm → 再公開** を正常系とする。

手順は [references/mcp-servers.md](references/mcp-servers.md) を参照。

### アイコン設定と公開は v2 専用の確認観点で扱う

v2 では BotConfiguration だけ見ていれば十分ではない。
UI での見え方、MCP の Confirm 状態、再公開の要否も含めて確認する。

- 作成直後のチェックは [references/manual-creation-checklist.md](references/manual-creation-checklist.md)
- アイコン設定と公開前後の確認は [references/icon-and-publish.md](references/icon-and-publish.md)
- 公開時の説明文案は [references/publish-description-template.md](references/publish-description-template.md)

### よくある失敗

- `configuration` を丸ごと上書きしてモデルやメモリを消す
- MCP サーバー追加後に **Confirm** を押さず、公開だけで済ませる
- `missing connection reference` を API 不具合と誤認し、UI での再追加を試さない
- v2 を外部連携用途に選んでしまい、後から埋め込み不可に気づく

## サブリファレンス

| リファレンス                                                             | 内容                                                              |
| ------------------------------------------------------------------------ | ----------------------------------------------------------------- |
| [手動作成チェックリスト](references/manual-creation-checklist.md)        | v2 エージェントを UI 手動作成した直後に確認する項目               |
| [新アーキテクチャ構造](references/new-architecture.md)                   | cliagent の BotConfiguration / botcomponents の構造と v1 との差分 |
| [アイコンと公開の最小ガイド](references/icon-and-publish.md)             | アイコン準備、UI 反映確認、公開前後の最小確認項目                 |
| [公開時の説明文テンプレート](references/publish-description-template.md) | 短い説明、長い説明、開発元表示の文案テンプレート                  |
| [MCP サーバーの追加](references/mcp-servers.md)                          | Copilot Studio UI での手動追加手順と Confirm の注意点             |
| [verify 実行テンプレート](references/verify-run-template.md)             | AGENT_BOTID 指定と verify_config / verify_agent の実行例           |
| [トラブルシューティング](references/troubleshooting.md)                  | v2 で頻出するエラーと対処                                         |

## このマスターで意図的に含めていないもの

上流の `copilot-studio-v2` にある API 自動作成・自動公開スクリプト群は、
このマスターでは **現時点で取り込まない**。

必要になった場合は、次の条件で別途追加を検討する:

1. UI 手動作成より自動化メリットが明確に大きい
2. 環境差異を吸収する `.env` 設計まで合わせて取り込める
3. スキル添付や公開も含めた検証手順をセットで維持できる
