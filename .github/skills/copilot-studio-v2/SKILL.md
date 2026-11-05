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

このスキルが向くのは、**Teams / Microsoft 365 Copilot 単独利用** のとき。ここでの「単独」はエージェントへの外部からの呼び出しや埋め込みが不要という意味であり、ナレッジやエージェント内部のツールを一切使わないという意味ではない。エージェントフローを使う場合は、選んだハーネスでその連携がサポートされるか別途確認する（[Microsoft Learn: エージェントフローをツールとして作成](https://learn.microsoft.com/en-us/microsoft-copilot-studio/advanced-flow-create) の手順は Standard ハーネス向け）。

| v2（本スキル）が向く                                    | v1（既存 `copilot-studio`）が向く                            |
| ------------------------------------------------------- | ------------------------------------------------------------ |
| Teams / M365 Copilot で単独利用し、外部から呼び出さない | Code Apps / Web サイト / 他システムから呼び出す              |
| 新アーキの構造を前提に保守したい                        | 外部公開、埋め込み、既存トリガー資産を使いたい               |
| Python スキルバンドル前提で構成したい                   | 会話開始、クイック返信、ニュース配信など v1 資産を流用したい |

> **致命的制約**: v2（cliagent）は **Code Apps から呼び出せず、Web 埋め込みにも向かない**。
> 外部連携や埋め込みがあるなら [../copilot-studio/SKILL.md](../copilot-studio/SKILL.md) を使う。

## このマスターでの既定フロー

1. [architecture](../architecture/SKILL.md) で v1 / v2 とフローの呼び出し元を選び、採用する重要経路の技術・ライセンス・Credits を [共通の実現可能性ゲート](../standard/references/power-platform-development-standard.md#開発着手前の実現可能性ゲート全案件必須)で判定する。エージェントフローを使う場合は選んだハーネスでの利用可否を確認し、[power-automate](../power-automate/SKILL.md) に入出力・接続・実行主体を渡す
2. ユーザーへ設計と未確認事項を提示し承認を得る。重要経路が未確認・不適合なら本実装を始めない
3. Copilot Studio UI で v2 エージェントを手動作成する
4. [手動作成チェックリスト](references/manual-creation-checklist.md) に沿って、作成直後の確認を行う
5. 設定変更や調査では **BotConfiguration JSON** と **botcomponents 構造** を前提に扱う
6. MCP サーバー追加前に `standard/scripts/check_mcp_client.py studio` で事前確認し、その後 UI で手動追加して **Confirm** と再公開まで行う
7. アイコン設定と公開前確認は [アイコンと公開の最小ガイド](references/icon-and-publish.md) と [外部入力と公開前チェック](../copilot-studio/references/external-input-release-check.md) を参照する
8. 異常時は本スキルの references を優先して切り分ける

## 事前検証スクリプト（推奨）

v2 の変更作業前後では、次の検証スクリプトを実行して設定整合を確認する。

- `scripts/verify_config.py`: BotConfiguration 構造、主要キー、必須設定の整合確認
- `scripts/verify_agent.py`: エージェント全体の運用観点チェック（公開前の最終確認）

UI で設定変更した場合も、これらは**設定の静的整合を確認する読み取り検証**として用いる。正常終了だけではツール接続、エージェントフローの実行、チャネルでの応答、公開後の利用権・Credits は確認できない。採用した入出力経路ごとに、顧客環境での実行条件と公開後の動作を別途確認する（[実行・確認テンプレート](references/verify-run-template.md)）。

## 設計確認テンプレート

エージェント名・目的・対象利用者、Teams / Microsoft 365 Copilot の利用チャネル、Instructions 全文、モデル・メモリ、MCP / 接続、公開情報と非対応事項を設計提示し、承認を得る。質問例と記入用テンプレートは [手動作成チェックリスト](references/manual-creation-checklist.md#設計確認の提示項目とテンプレート) を参照する。

## v1 との主な違い

v1 は UI 作成の GPT コンポーネント・PVA YAML・`aISettings.model.modelNameHint` を使う。v2 は UI 手動作成を既定とし、`bots.configuration` の BotConfiguration JSON・`CLICopilotRecognizer`・プレーン文字列の Instructions・`agentSettings.model.series` / `enableMemory` を使う。スキルはフラット Python バンドル、MCP は UI 手動追加と Confirm が必要（[構造と対比](references/new-architecture.md#v1旧アーキとの対比早見)）。

## 必須要件・落とし穴

- `configuration` を直接更新する場合は GET → ディープマージ → PATCH とし、モデル・メモリ等を保持する。モデルシリーズは固定せず対象環境の UI・公式資料で確認する（[BotConfiguration と構造](references/new-architecture.md#configurationbotconfiguration-json)）。v1 用 PVA YAML は使わない。
- v2 スキルは Python のフラットバンドル。JavaScript / pptxgenjs・サブフォルダ・同梱画像の直接読み込みを前提にせず、必要なら Base64 を使用する。`botcomponents` の type=9 は InlineAgentSkill / McpTool、type=14 は親スキルの同梱ファイル（[構造](references/new-architecture.md#botcomponents配下コンポーネント)）。
- MCP は API 自動追加せず、接続参照を確認して UI で追加 → Confirm → 再公開（[手順](references/mcp-servers.md)）。`missing connection reference` 等は [トラブルシューティング](references/troubleshooting.md) で切り分ける。
- アイコン・公開情報・UI 表示・MCP Confirm 状態を [アイコンと公開の最小ガイド](references/icon-and-publish.md) で確認する。

## サブリファレンス

| リファレンス                                                             | 内容                                                              |
| ------------------------------------------------------------------------ | ----------------------------------------------------------------- |
| [手動作成チェックリスト](references/manual-creation-checklist.md)        | v2 エージェントを UI 手動作成した直後に確認する項目               |
| [新アーキテクチャ構造](references/new-architecture.md)                   | cliagent の BotConfiguration / botcomponents の構造と v1 との差分 |
| [アイコンと公開の最小ガイド](references/icon-and-publish.md)             | アイコン準備、UI 反映確認、公開前後の最小確認項目                 |
| [公開時の説明文テンプレート](references/publish-description-template.md) | 短い説明、長い説明、開発元表示の文案テンプレート                  |
| [MCP サーバーの追加](references/mcp-servers.md)                          | Copilot Studio UI での手動追加手順と Confirm の注意点             |
| [verify 実行テンプレート](references/verify-run-template.md)             | AGENT_BOTID 指定と verify_config / verify_agent の実行例          |
| [トラブルシューティング](references/troubleshooting.md)                  | v2 で頻出するエラーと対処                                         |

## このマスターで意図的に含めていないもの

上流の `copilot-studio-v2` にある API 自動作成・自動公開スクリプト群は、
このマスターでは **現時点で取り込まない**。

必要になった場合は、次の条件で別途追加を検討する:

1. UI 手動作成より自動化メリットが明確に大きい
2. 環境差異を吸収する `.env` 設計まで合わせて取り込める
3. スキル添付や公開も含めた検証手順をセットで維持できる
