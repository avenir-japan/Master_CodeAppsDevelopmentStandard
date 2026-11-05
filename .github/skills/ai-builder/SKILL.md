---
name: ai-builder
description: "AI Builder の AI プロンプト（GPT Dynamic Prompt）を Dataverse API で作成し、Copilot Studio エージェントにツール（アクション）として追加する。Power Automate フローとの統合パターンも含む。"
category: ai
triggers:
  - "AI Builder"
  - "AI プロンプト"
  - "GPT Prompt"
  - "AIプロンプト作成"
  - "エージェントツール追加"
  - "msdyn_aimodel"
  - "InvokeAIBuilderModelTaskAction"
  - "プロンプトデプロイ"
  - "AI Prompt"
  - "aibuilderpredict"
  - "フロー AI Builder"
---

# AI Builder AI プロンプト構築スキル

AI Builder の **AI プロンプト（GPT Dynamic Prompt）** を Dataverse API で作成し、
Copilot Studio エージェントに **ツール（アクション）** として追加する。
Power Automate フローから **aibuilderpredict_customprompt** で呼び出すパターンも含む。

## 名称と利用経路を分けて確認する

| 用語 | 指すもの |
| --- | --- |
| AI Builder | プロンプトや OCR・文書処理等の AI モデルを含む機能群 |
| プロンプトビルダー | プロンプトを作成する画面 |
| プロンプトツール | エージェントから再利用可能なプロンプトを呼ぶ手段 |

名称の根拠は[プロンプトの概要](https://learn.microsoft.com/en-us/microsoft-copilot-studio/prompts-overview)（2026-10-30 確認）。[請求資料](https://learn.microsoft.com/en-us/microsoft-copilot-studio/requirements-messages-management)の「AI ツール」は料金区分の文脈で読み、すべてのエージェントツールや Instructions・生成回答と同義にしない。旧称「AI Builder プロンプト」や現行 UI 名が異なっても、検証済み API・スキーマ識別子（例: `AIModelPublish`、`InvokeAIBuilderModelTaskAction`、`aibuilderpredict_customprompt`）を名称合わせのために変更しない。

このスキルの API 実装は **Dataverse のプロンプトをエージェントへ直接追加したツール**または**クラウドフローのアクション**で利用する特定の経路を扱う。トピック内・エージェントフロー内のプロンプトも別経路として設計時に比較する。

- 各経路で利用可能な入力型・出力契約、接続・容量条件を確認する。エージェントフロー（「エージェントがフローを呼び出したとき」トリガー）を一般のクラウドフローと同一視しない。
- 方式選定は [architecture](../architecture/SKILL.md)、容量と公開後実行は[ライセンス確認ルール](../standard/references/license-requirements.md)を正本とする。

## AI Builder 採用後の実装方式選択

AI Builder の採用が決まったら、用途・入力形式・精度・運用負荷とライセンス・Credits 条件をそろえて比較する。

| 観点 | AI プロンプト（カスタムプロンプト） | プレビルトモデル（請求書処理モデル等） |
| --- | --- | --- |
| 用途・精度 | 請求書処理、ドキュメント情報抽出、分類、要約等で柔軟な抽出・分類・要約の候補 | 既存モデルの対応範囲と精度が要件を満たすか確認 |
| 入力・変更 | プロンプトテキスト + document/image 入力。プロンプト変更だけで出力形式・抽出項目を調整可能 | 対応する入力形式を要件と照合 |
| 導入・運用 | トレーニングデータ不要で即座にデプロイ・更新可能 | カスタムモデルを使う場合は学習データと運用負荷も評価 |

手書き文字の高精度 OCR が必須で AI プロンプトでは精度不足の場合、または既存のプレビルトモデルが組み込まれたワークフローを維持する必要がある場合は、プレビルトモデルを優先する。

## 前提: 設計フェーズ完了後に構築に入る（必須）

**AI プロンプトを構築する前に、プロンプト設計をユーザーに提示し承認を得ていること。**

設計提示時に含める内容:

| 項目               | 内容                                                 |
| ------------------ | ---------------------------------------------------- |
| プロンプト名       | 英語推奨（スキーマ名に使用される）                   |
| プロンプトテキスト | リテラルテキスト＋入力変数の組み合わせ               |
| 入力変数           | 名前・型（text / document / image）・説明・テスト値  |
| 出力形式           | text or json（JSON の場合はスキーマ＋サンプル）      |
| モデルパラメータ   | モデル種別（gpt-41-mini 等は例示であり採用方針ではない）・temperature |
| 利用先             | Copilot Studio ツール or Power Automate フロー       |
| shouldPromptUser   | 各入力変数をユーザーに自動的に尋ねるか（true/false） |

## AIModelPublish によるアクティブ化

**2026-04-15 検証済み**: 新規 Model は `msdyn_TemplateId@odata.bind` で作成し、プレフィックスなしの unbound action `AIModelPublish` で完全にアクティブ化する。`RunConfigurationId` に `model_id` を渡すと同じ ID の Run Config が生成され、Published Training（state=2, status=6）と Run Config（state=2, status=7）が自動作成されて Model は Active（state=1, status=1）になる。新規作成は 2 API コールで完了する（[呼び出しコード](references/build-reference.md#step-2-aimodelpublish-で1ステップ完全アクティブ化)）。

1. 新規: Model を作成し、`AIModelPublish` を呼ぶ。
2. 更新: 既存 Model の Active Run Config ID を取得し、`msdyn_customconfiguration` を PATCH する。再公開は不要（[更新手順](references/build-reference.md#既存-ai-プロンプトの更新パターン)）。

旧パターンとの違いや失敗時の対応は[構築リファレンスのトラブルシューティング](references/build-reference.md#トラブルシューティング)を参照する。

## Dataverse データ構造

AI プロンプト本体（`msdyn_aimodel`）、公開後の設定（`msdyn_aiconfiguration`）と、Copilot Studio 利用時のみ必要な `botcomponent` の構造・JSON / YAML 例および照合値は[構築リファレンス](references/build-reference.md#dataverse-データ構造)を参照する。

## 構築手順

設計承認後、[構築リファレンス](references/build-reference.md#構築手順)のコードと検証条件に従う。

1. `msdyn_TemplateId@odata.bind` とソリューションヘッダーで Model を作成する。
2. `AIModelPublish` でアクティブ化し、Active 状態を照合する。
3. Copilot Studio のツールとして使う場合のみ `botcomponent` を追加し、エージェントを再公開する。

## Power Automate フローからの AI Builder 呼び出し

AI Builder プロンプトを **Power Automate フロー内で呼び出す** パターン。
Copilot Studio ツールではなく、Dataverse トリガー等と組み合わせて自動実行する場合に使う。

デプロイ順序、動的パラメータと列追加後の確認は [Power Automate 連携リファレンス](references/power-automate-integration.md) を参照する。

## ファイル入力（Image or Document Input）の制限事項

- **エージェントへ直接追加したプロンプトツール**の画像・文書入力は未対応。テキストのプロンプト利用全般がフロー必須という意味ではない（[Microsoft Learn](https://learn.microsoft.com/en-us/microsoft-copilot-studio/add-inputs-prompt#limitations)、2026-10-30 確認）。
- ファイル形式（Code Interpreter の有無）、サイズ・ページ数・時間の上限と、フロー経由・変換時の検証条件は[構築リファレンス](references/build-reference.md#ファイル入力image-or-document-inputの制限事項)を参照する。

## .env 追加パラメータ

```env
# AI Builder AI Prompt 用（既存 .env に追加）
AI_PROMPT_NAME=AI Prompt Sample
AI_PROMPT_BOT_ID=https://copilotstudio.../bots/xxxxxxxx-xxxx-.../overview
# ↑ BOT_ID と異なるエージェントに追加する場合のみ指定
```

## デプロイ・トラブルシューティング

- [構築リファレンス](references/build-reference.md) — デプロイスクリプト・トラブルシューティング
- [Power Automate 連携リファレンス](references/power-automate-integration.md) — フロー統合パターン

## 関連スキル

| スキル                                       | 連携内容                                                                   |
| -------------------------------------------- | -------------------------------------------------------------------------- |
| [architecture](../architecture/SKILL.md)     | AI Builder を単独利用するか Copilot Studio / Flow と組み合わせるかを決める |
| [power-automate](../power-automate/SKILL.md) | フローから AI プロンプトを呼び出す                                         |
| [copilot-studio](../copilot-studio/SKILL.md) | AI プロンプトをエージェントのツールとして追加する                          |
| [code-apps](../code-apps/SKILL.md)           | Code Apps からフロー経由で AI 処理を利用する                               |
| [canvas-app](../canvas-app/SKILL.md)         | Canvas App の添付処理を Flow 経由で AI に渡す                              |
