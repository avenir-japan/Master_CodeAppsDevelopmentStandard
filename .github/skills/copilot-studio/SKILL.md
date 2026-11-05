---
name: copilot-studio
description: "Copilot Studio の既存アーキテクチャ（v1）でエージェントを構築・設定する。生成オーケストレーション、ナレッジ、ツール、外部トリガーを採用条件の確認後に扱う。"
category: automation
triggers:
  - "Copilot Studio"
  - "エージェント作成"
  - "Bot"
  - "生成オーケストレーション"
  - "Instructions"
  - "指示"
  - "ナレッジ"
  - "MCP Server"
  - "PvaPublish"
  - "ボット設定"
  - "エージェント公開"
  - "Copilot Studio トリガー"
  - "メール受信"
  - "エージェント自動起動"
  - "ExternalTriggerComponent"
  - "ExecuteCopilot"
  - "Power Automate トリガー"
  - "Office 365 Outlook"
  - "OnNewEmailV3"
  - "メールトリガー"
  - "スケジュールトリガー"
  - "Work IQ MCP"
---

# Copilot Studio エージェント構築スキル

このスキルは **既存アーキテクチャ（v1）を採用したエージェント**の構築・設定を扱い、採用後の構成では生成オーケストレーション（Generative Orchestration）を使用する。Teams / Microsoft 365 Copilot 単独向けの新アーキテクチャ（cliagent）を採用する場合は [copilot-studio-v2](../copilot-studio-v2/SKILL.md) の制約と手順を優先し、v1 用の API・トピック操作を流用しない。
Microsoft 365 サブスクリプションに含まれる Copilot Studio for Teams プランでは生成オーケストレーションを利用できない。この方針を適用する前に、[ライセンス確認ガイド](../standard/references/license-requirements.md)に従って採用機能と作成者・利用者の利用権を確認し、不適合なら構築に進まず構成・追加ライセンスを相談する。
外部トリガーやニュース配信は要件がある場合のみ検討する。外部トリガーからエージェントを呼ぶ構成は標準案ではなく、ライセンス・Credits・実現可能性を確認して承認された例外案として扱う。

## サブリファレンス（必要に応じて参照）

| リファレンス                                                                         | 内容                                                                 |
| ------------------------------------------------------------------------------------ | -------------------------------------------------------------------- |
| [構築リファレンス](references/build-reference.md)                                    | 構築手順の詳細・Instructions テンプレート・スクリプトコード          |
| [ナレッジソースの選定](references/knowledge-source-selection.md)                     | ファイル直接登録・SharePoint サイト参照・Dataverse 取り込みの比較と検証導入パッケージの条件付き初期提案 |
| [外部トリガー](references/trigger.md)                                                | 承認済み例外案の UI 設定。後半の API フロー作成例は廃止・履歴用      |
| [トリガーパターン](references/trigger-patterns.md)                                   | トリガーの設定パターン集                                             |
| [トリガートラブルシューティング](references/trigger-troubleshooting.md)              | トリガー関連のトラブルシューティング                                 |
| [トラブルシューティング](references/troubleshooting.md)                              | トリガー以外を含む障害切り分け・復旧手順                             |
| [納品時制約](references/managed-solution-constraints.md)                             | マネージド / アンマネージド納品時の Copilot Studio 固有制約          |
| [ニュース配信エージェント](references/market-research-report.md)                     | RSS + Web検索 + Work IQ MCP によるニュース収集・配信エージェント構築 |
| [ニュース配信デプロイガイド（履歴）](references/market-research-deployment-guide.md) | 過去の案件固有構成の記録（実行禁止）                                 |
| [ニュース配信メールテンプレート](references/market-research-email-template.md)       | ニュース配信メールの HTML テンプレート                               |

> ニュース配信の上記 3 資料と `scripts/deploy_news_*`・`scripts/deploy_market_insight.py` は案件固有の履歴資料であり、通常の構築・実行手順ではない。`fix_email_*`・`setup_email_trigger.py`・`deploy_email_trigger.py` も事例別の復旧履歴で、一括適用しない。これらの実行は安全のため無効化している。削除せず記録として保持し、採用時は案件ごとの設計・検証・承認を経て新たに実装する。

## 前提: 設計フェーズ完了後に構築に入る（必須）

**エージェントを構築する前に、エージェント設計をユーザーに提示し承認を得ていること。** 既存エージェントの改修では、変更前にトピックの現状と依存関係を確認し、承認されていないトピックを削除しない（[改善時の確認手順](references/build-reference.md#既存エージェント改善パターン)）。

設計提示時に含める内容:

| 項目                     | 内容                                                                                                                                     |
| ------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------- |
| エージェント名・説明     | 名前と役割の説明                                                                                                                         |
| Instructions             | 指示テキストの全文案                                                                                                                     |
| 推奨プロンプト           | 3〜5 個のタイトル＋プロンプト文（GPT コンポーネントの conversationStarters）                                                             |
| 会話の開始のメッセージ   | エージェントに合った挨拶テキスト（ConversationStart トピックの SendActivity）                                                            |
| 会話の開始のクイック返信 | 3〜5 個のクイック返信テキスト（ConversationStart トピックの quickReplies）                                                               |
| 会話経路・既存トピック   | 新規では必要な会話経路を設計する。既存エージェントの改修ではトピックの用途・依存先・維持／変更／削除案を確認し、削除案は個別に承認を得る |
| ナレッジ                 | データソース（Dataverse テーブル / SharePoint / ファイル等）                                                                             |
| ツール                   | MCP Server の接続先・用途                                                                                                                |
| チャネル公開設定         | 簡単な説明・詳細な説明・背景色・開発者名（デフォルト値を提案）                                                                           |

```
フロー: 設計提示 → ユーザー承認 → アイコン画像提案 → ユーザー選択 → UI で Bot 作成 → スクリプトで設定適用
```

## アイコン画像提案（設計承認後・構築前）

> **アイコンの設計・生成・登録の詳細は `standard` スキルの [アイコン作成リファレンス](../standard/references/icon-creation.md) を参照。**
> ここではエージェント固有の手順のみ記載する。

エージェント設計が承認されたら、**Bot 作成前にアイコン画像を提案**する。
`standard` スキルの [アイコン作成リファレンス](../standard/references/icon-creation.md) のアイコン画像提案フローに従い、3〜4 パターンを提案 → ユーザー選択 → PNG 3 サイズ生成（240, 192, 32）→ `bots.iconbase64` + Teams マニフェストに API 登録。

## 大前提: 一つのソリューション内に開発

共通の `.env`、認証、ソリューション運用の正本は [standard スキル](../standard/SKILL.md) とする。

- Copilot Studio でも Dataverse テーブル、Code Apps、Power Automate フローと同じ `SOLUTION_NAME` / `PUBLISHER_PREFIX` を使う
- Bot 作成時（Copilot Studio UI）は対象ソリューションを明示的に選択する
- ソリューション外で作成したコンポーネントはリリース管理・環境間移行ができない

## 納品時の切り分け

- Copilot はナレッジ URL の変数化・差し替え対象、チャネル・認証の要件を整理し、スクリプトで設定値・補助文書を整える。顧客管理者は実 URL・資格情報・管理者同意、Teams / M365 Copilot / Web の実公開と SSO / OAuth を確認・実施する。
- ソリューション import と、公開・チャネル・認証・フロー稼働・実入力による実行成功は別々に判定する。マネージド案件では顧客側の直接編集を既定とせず再提供する。詳細は [納品時制約](references/managed-solution-constraints.md) を参照する。

## 絶対遵守ルール

- v1 Bot は Dataverse `bots` への直接 INSERT ではなく Copilot Studio UI で作成し、プロビジョニング完了後に設定する。
- GPT (`componenttype=15`) は UI 作成済みの `configuration.gPTSettings.defaultSchemaName` と照合して更新する。別コンポーネントの自動削除は禁止。既存設定を GET → ディープマージ → PATCH し、`optInUseLatestModels=False` と `aISettings` のモデル選択を保持する。
- Instructions / ConversationStart は PVA 固有のダブル改行 YAML を使い、`yaml.dump()` で書き戻さない。説明は `botcomponents.description` に publish 後に設定する。
- 更新コード、フォーマット例、例外と復旧条件は [構築リファレンス](references/build-reference.md#構築手順) を参照する。

## 構築手順

詳細な構築手順・スクリプトコードは [構築リファレンス](references/build-reference.md) を参照。

高レベルの手順:

- Copilot Studio のエージェントは作成時に標準ハーネスを選ぶ（理由は [license-requirements.md §1](../standard/references/license-requirements.md#1-基本方針)）。

1. **Step 0**: Copilot Studio UI で Bot 作成（ユーザー手動）
2. **Step 1-1.5**: Bot 検索 + プロビジョニング完了待ち
3. **Step 2**: 既存トピック・GPT コンポーネントの棚卸し。通常は保持し、個別承認のない削除をしない
4. **Step 3**: 生成オーケストレーション有効化
5. **Step 4-4.5**: Instructions + 会話の開始設定
6. **Step 5-6**: エージェント公開 + 説明設定
7. **Step 7-8**: Teams / Copilot チャネル公開設定
8. **Step 9**: ナレッジ・ツール・トリガーの手動追加案内

ナレッジ、MCP、トリガー、外部文書やユーザー入力を扱う場合は、公開・再公開前に[外部入力と公開前チェック](references/external-input-release-check.md)で権限・操作範囲と利用者視点の試験を確認する。

**完了判定**: 保存・公開済み（構成を読み戻し、公開状態を確認）と、稼働中（承認済み接続・トリガーで実入力から目的の出力／副作用が確認できる）は別の状態。デプロイ成功のログや公開だけでは稼働完了としない。チャネル到達性、接続認証、少数の実ケースと失敗時動作を承認された方法で検証し、未検証項目を明記する。

構造化 JSON を出力するエージェントは、実際の入力を使い、次のゲートを別々に確認する。

1. Instructions が保存・読み戻しできること（実行時の動作確認とは区別する）。
2. 出力が契約に適合すること。最上位キーだけでなく、配列要素のキー・型・必須項目も照合する。
3. 入力に確定メタデータがある場合、出力のファイル名などが元の値と完全一致すること。構造適合だけで合格にしない。

Instructions テンプレート・既存エージェント改善パターンは [構築リファレンス](references/build-reference.md#instructions-テンプレート) を参照。

## エージェントの評価

内容品質と処理成功を分け、固定の回帰ケースを複数回実行して変動を記録する。モデル比較は入力・Instructions・ナレッジ・ツール・出力契約・評価基準をそろえる（[評価の詳細](references/build-reference.md#評価と完了判定の補足)）。

## .env 必須項目

```env
DATAVERSE_URL=https://{org}.crm7.dynamics.com
SOLUTION_NAME=SolutionName
PUBLISHER_PREFIX=prefix
BOT_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
# scripts/deploy_agent.py の明示承認ゲートは URL ではなく完全一致する GUID のみ受け付ける
```

## 関連スキル

| スキル                                           | 連携内容                                           |
| ------------------------------------------------ | -------------------------------------------------- |
| [architecture](../architecture/SKILL.md)         | 対話型エージェントを入れるべきかを先に判断する     |
| [standard](../standard/SKILL.md)                 | 認証・ソリューション・共通運用の土台               |
| [power-automate](../power-automate/SKILL.md)     | 外部トリガーや補助処理をフローで担う               |
| [ai-builder](../ai-builder/SKILL.md)             | エージェントのツールとして AI プロンプトを追加する |
| [spec-to-markdown](../spec-to-markdown/SKILL.md) | エージェント要件やナレッジ元文書を事前整理する     |
