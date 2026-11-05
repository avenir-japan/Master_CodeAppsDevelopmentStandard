---
name: power-automate
description: "Power Automate クラウドフローをソリューション対応で作成・デプロイする。Dataverse workflows と Flow API の適用条件、接続参照、事前検証と有効化を扱う。"
category: automation
triggers:
  - "Power Automate"
  - "フロー作成"
  - "クラウドフロー"
  - "接続参照"
  - "Connection Reference"
  - "workflow"
  - "トリガー"
  - "アクション"
  - "フローデプロイ"
  - "フロー有効化"
  - "メール通知"
---

# Power Automate クラウドフロー構築スキル

ソリューション対応のクラウドフローを作成・デプロイする。既存スクリプトは Dataverse Web API（`workflows`）による作成・更新が主で、Flow API は環境解決・起動と一部のデプロイ経路に使用する（[経路と条件](references/code-first-flow-authoring.md#認証環境解決と接続参照)）。対象は通常のイベント／スケジュール、Canvas App や Copilot Studio からの呼び出し、クラウドフローからのエージェント起動など。**トリガー・実行主体・接続・課金条件を個別に確認**し、エージェントフローと断定したりクラウドフロー起点の Credits 判定を流用しない（[ライセンス確認ルール](../standard/references/license-requirements.md#1-基本方針)）。

既存フローの編集・失敗 run の診断に FlowAgent MCP を使う場合は、任意経路として[利用前のゲート](references/flow-agent-mcp.md)を確認する。UI 雛形 / clone 定義を正本とする方針は変えない。

## 核心原則: 接続参照（Connection Reference）が有効化成功の鍵

接続 ID を直接埋め込まず、ソリューション内の接続参照を定義から論理名で参照する。論理名だけでなく、環境側の接続 ID・コネクタ・接続状態まで検証し、有効化後に実行を確認する。`AzureResourceManagerRequestFailed` や `authenticatedUserObjectId` 不足の条件と JSON 形式は[接続参照の詳細](references/code-first-flow-authoring.md#認証環境解決と接続参照)を参照。

## 前提: 設計フェーズ完了後にデプロイに入る（必須）

デプロイ前にフロー名・目的、トリガー、条件分岐を含むアクション一覧、必要な接続、通知先・件名・本文の概要、[命名規則](references/naming-conventions.md)をユーザーへ提示し承認を得る。最初に作る最小単位は、Power Automate UI で保存可能な最小フローとその clone 定義。実装・デプロイは承認後に行う。

## 大前提: 一つのソリューション内に開発

`.env`・認証・ソリューション運用は[standard](../standard/SKILL.md)を正本とする。Dataverse `workflows` への作成には `MSCRM.SolutionUniqueName` ヘッダーを付け、接続参照も同じソリューションに含める。ソリューション外のフローは「マイフロー」に入り ALM 管理できない。接続の UI 事前作成と認証スコープは[実装ガイド](references/code-first-flow-authoring.md#認証環境解決と接続参照)を参照。

## 関連スキル

| スキル                                       | 連携内容                                         |
| -------------------------------------------- | ------------------------------------------------ |
| [architecture](../architecture/SKILL.md)     | Flow 単体か Copilot Studio 連携かを先に判断する  |
| [standard](../standard/SKILL.md)             | 認証・`.env`・ソリューション前提の共通ルール     |
| [dataverse](../dataverse/SKILL.md)           | トリガー元テーブル・更新対象テーブルの設計       |
| [code-apps](../code-apps/SKILL.md)           | Code Apps から呼ぶ PowerApps V2 フローを実装する |
| [canvas-app](../canvas-app/SKILL.md)         | Canvas App の staging 中継フローを作る           |
| [copilot-studio](../copilot-studio/SKILL.md) | 外部トリガーからエージェントを起動する           |
| [ai-builder](../ai-builder/SKILL.md)         | フロー内で AI プロンプトを呼び出す               |

## 絶対遵守ルール

- **方式**: まず既定アクションで MVP に必要な処理と検証を成立させる。Graph HTTP の使用条件、コネクタの責務境界と変数配置・式の制約は[実装ガイド](references/code-first-flow-authoring.md#アクション組み立て復旧時の注意)。
- **定義**: UI で保存可能な最小雛形を作り、pac / clone / export で取得した action 名・operationId・パラメータ形・接続参照を正本に拡張する。トリガー・アクション名は追加直後に `連番_処理内容（既定の日本語UIアクション名）` に固定し、式は取得済みの内部名を使う（[コードファースト](references/code-first-flow-authoring.md#1-最小雛形を-ui-で成立させてから-clone-する)、[命名規則](references/naming-conventions.md)）。
- **接続**: Power Automate UI で接続を事前作成し、Connected 状態の接続を検索してソリューション内の接続参照に紐づける。Flow API / PowerApps API / Graph API / Dataverse API のスコープを混用しない（[認証と接続](references/code-first-flow-authoring.md#認証環境解決と接続参照)）。
- **起動と応答**: Webhook 型は有効化後に Flow API `/start` を実施する。Power Apps V2 や Teams 投稿、Dataverse File 列、AI Builder、GrantAccess / RevokeAccess は UI 由来の形に従う（[トリガー・アクション](references/trigger-action-patterns.md)）。Microsoft 365 Copilot Chat へのリンク応答は[表示と出力契約](references/code-first-flow-authoring.md#microsoft-365-copilot-chat-のリンク応答)を参照。
- **既存フロー**: 削除・再作成はべき等更新ではない。`--execute` / `--replace-workflow-id` は退避・参照先・ID 依存・承認を確認した場合だけ指定する（[デプロイ前チェック](references/pre-deploy-checks.md#破壊的なサンプルデプロイ)、[Modern Flow 復旧条件](references/code-first-flow-authoring.md#アクション組み立て復旧時の注意)）。

## 構築手順（5ステップ — 接続参照を確認し、有効化と実行を検証）

### Step 1: 環境 ID 解決 + 接続検索

Flow API で `DATAVERSE_URL` から環境 ID を解決し、PowerApps API で対象環境の Connected 接続を探す。接続が無ければ UI で作成・再認証してから進む。解決方法と 504 / Timeout 時の再試行は[実装ガイド](references/code-first-flow-authoring.md#認証環境解決と接続参照)。

### Step 2: 接続参照の作成（★ 有効化成功の核心）

同じソリューションで必要な接続参照を作成または紐づけ更新し、全 `connectionid`・`connectorid` とフロー定義の参照キーを検査する。論理名のみの未解決状態で有効化しない（[接続参照の形式と条件](references/code-first-flow-authoring.md#認証環境解決と接続参照)）。

### Step 3: フロー定義の構築

UI 保存済み定義をもとに `definition` と `connectionReferences` を組み立てる。各 `host.connectionName` と参照キーを合わせ、対象トリガー・アクションの形は[パターン集](references/trigger-action-patterns.md)、定義の配置と f-string の式表記は[実装ガイド](references/code-first-flow-authoring.md#定義作成有効化の詳細)を参照。送信する最終 JSON に[デプロイ前チェック](references/pre-deploy-checks.md#対象と実行)を行う。

### Step 4: workflow テーブルに Draft 作成

Dataverse `workflows` に `MSCRM.SolutionUniqueName` を付け、対象ソリューションの Draft を作成する。既存フローの置換は先に破壊的操作の承認を確認する（[Draft のフィールドと条件](references/code-first-flow-authoring.md#定義作成有効化の詳細)、[置換時の安全確認](references/pre-deploy-checks.md#破壊的なサンプルデプロイ)）。

### Step 5: 有効化 + Webhook 登録

接続参照を確認して有効化する。Dataverse Webhook 型のみ Flow API `/start` で登録し、その他のトリガーには不要な起動呼び出しをしない。デザイナー保存・公開/有効化・実行 run と出力を別ゲートで検証する（[トリガーごとの条件](references/code-first-flow-authoring.md#定義作成有効化の詳細)、[次の確認ゲート](references/pre-deploy-checks.md#次の確認ゲート)）。

## 通知デザイン（デフォルト適用 — ユーザー指定不要）

メール・Teams 通知にはユーザーから別指定がない限り[通知デザインテンプレート](references/notification-templates.md)を適用する。メールのカード型テーブル・インラインスタイルと Teams の専用テンプレート、目的別 variant の判断は参照先を正本とする。

## 代表的パターン

SharePoint、Dataverse、Teams、Power Apps V2、AI Builder、OneDrive PDF 変換等は[トリガー・アクションパターン](references/trigger-action-patterns.md)。コードファーストの順序とゲートは[実装ガイド](references/code-first-flow-authoring.md)、アクション名は[命名規則](references/naming-conventions.md)。

## .env 必須項目

`DATAVERSE_URL`、`SOLUTION_NAME`、`PUBLISHER_PREFIX` を使用する。接続 ID をハードコードせず PowerApps API で検索する。共通認証と `.env` の取得元は[standard](../standard/SKILL.md#共通基盤-env-と認証)を参照。

## よくあるエラーと解決策

import / save / publish / 実行を分けて切り分ける。UI と docs の parameter shape がずれた場合は保存済み code view と clone 定義を正本とし、sync の内容が不自然な場合は fresh clone と比較する。接続認証、Webhook、operationId、コネクタ削除の整合や Modern Flow import 不具合は[実装ガイド](references/code-first-flow-authoring.md#アクション組み立て復旧時の注意)、[パターン集](references/trigger-action-patterns.md)、[デプロイ前チェック](references/pre-deploy-checks.md)で条件と対処を確認する。
