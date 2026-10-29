# Power Platform Skills カタログ

Power Platform コードファースト開発で使用するスキル群。
GitHub Copilot の段階的読込と Progressive Disclosure を前提に構成。

## このカタログの既定スコープ

このマスターリポジトリでは、検証導入パッケージの**条件付き初期提案**を **ベースライセンス（Microsoft 365 + Copilot）の範囲内** に置く。採用前に案件要件、契約、利用者・実行主体の利用権を確認する。

- UI / チャネルの初期候補は **Teams / Microsoft 365 Copilot**。利用条件と要件適合を確認する
- **Canvas App（標準コネクタ）** は画面 UI が必要な場合の候補とし、既存資産、接続の利用条件と工数を確認する。PDF・添付を扱わないアプリに SharePoint staging を追加しない
- Code Apps、Dataverse カスタムテーブル、AI Builder、プレミアム / カスタムコネクタ、Credits 消費が見込まれる Copilot Studio パターンは、消費量の大小によらず既定提案から外し、案件ごとにライセンスと Credits を評価する
- クラウドフローからエージェントを呼ぶ自律型構成は既定提案に含めない。必要時は例外案として、フロー側とエージェント側の費用・実行条件を別々に判定する。エージェント側トリガーやエージェントフローにクラウドフロー起点の Credits 条件を流用しない
- 個別スキルの技術手順は残し、採用可否や優先順位は [standard](standard/SKILL.md) / [architecture](architecture/SKILL.md) / [ライセンス確認ルール](standard/references/license-requirements.md) を正本とする

## スキル構成規約

### フォルダ構成（Progressive Disclosure モデル）

各スキルは以下の 3 層構造に従う:

```
skill-name/
  SKILL.md              # Level 1-2: フロントマター（常時読込）+ 本体（トリガー時読込）
  scripts/              # Level 3: デプロイ・ユーティリティスクリプト（オンデマンド読込）
    deploy_xxx.py
    check_xxx.py
  references/           # Level 3: 補足ドキュメント（オンデマンド読込）
    build-reference.md
    troubleshooting.md
```

### 統合方針

関連するスキルは **製品単位** で 1 つのスキルに統合する。
統合前に独立スキルだった内容は `references/` に配置し、メインの `SKILL.md` からリンクする。

```
例: code-apps/
  SKILL.md                          # 開発・デプロイの本体（旧 code-apps-dev）
  references/
    design-system.md                # UI 設計パターン（旧 code-apps-design）
    csp.md                          # CSP 構成（旧 code-apps-csp）
    mail-pdf.md                     # PDF メール送信（旧 code-apps-mail）
    component-catalog.md            # コンポーネントカタログ
    japan-map-pattern.md            # 日本地図パターン
    build-reference.md              # ビルドリファレンス
  scripts/
    add_app_to_solution.py
```

### YAML フロントマター規約

```yaml
---
name: skill-name # kebab-case 識別子（必須）
description: "短い説明文" # スキルの目的を簡潔に（必須）。トリガーキーワードは含めない
category: カテゴリ名 # 分類タグ（必須）: architecture / data / ui / automation / ai
argument-hint: "引数の説明" # ユーザー入力を受け付ける場合のみ（任意）
user-invocable: true # ユーザーが直接呼び出せる場合のみ（任意）
triggers: # スキル発動条件キーワード（必須）
  - "キーワード1"
  - "キーワード2"
---
```

### 命名規則

| 対象                     | 規則                               | 例                                               |
| ------------------------ | ---------------------------------- | ------------------------------------------------ |
| スキルディレクトリ名     | kebab-case                         | `copilot-studio`                                 |
| YAML `name` フィールド   | kebab-case（ディレクトリ名と一致） | `copilot-studio`                                 |
| Python スクリプト        | snake_case                         | `deploy_agent.py`                                |
| リファレンスドキュメント | kebab-case                         | `build-reference.md`                             |
| カテゴリ名               | 英小文字                           | `architecture`, `data`, `ui`, `automation`, `ai` |

---

## スキル一覧（14 スキル）

### architecture — アーキテクチャ・基盤

| スキル                                  | 説明                                                                           |
| --------------------------------------- | ------------------------------------------------------------------------------ |
| [architecture](architecture/SKILL.md)   | Power Platform 全体の構成方針を設計し、最適なコンポーネント構成を決定する。    |
| [standard](standard/SKILL.md)           | 共通認証・環境変数・ソリューション運用など、全スキル共通の開発基盤を提供する。 |
| [update-skills](update-skills/SKILL.md) | スキル更新の標準化、検証、PR 作成・更新運用を一貫して実施する。                |

### data — データ層

| スキル                          | 説明                                                                                                           |
| ------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| [dataverse](dataverse/SKILL.md) | Dataverse のテーブル設計・構築・デモデータ投入・権限設定を一括で実施する。会話ログ分析の入口もここから辿れる。 |

### ui — UI / フロントエンド

| スキル                                        | 説明                                                                                                                                                      |
| --------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [code-apps](code-apps/SKILL.md)               | Code Apps を TypeScript/React ベースで開発し、UI 設計からデプロイまで対応する。                                                                           |
| [canvas-app](canvas-app/SKILL.md)             | Canvas App の AI 主導編集、Git によるソース管理、single app / package による限定移送を整理し、添付・PDF 要件では SharePoint staging + Flow 中継まで扱う。 |
| [generative-page](generative-page/SKILL.md)   | Generative Pages（genux）を開発・デバッグし、モデル駆動型アプリへデプロイする。                                                                           |
| [model-driven-app](model-driven-app/SKILL.md) | モデル駆動型アプリを作成・構成し、公開まで実行する。                                                                                                      |

### automation — 自動化

| スキル                                          | 説明                                                                                                         |
| ----------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| [copilot-studio](copilot-studio/SKILL.md)       | 既存アーキテクチャ（v1）のエージェントを構築・運用する。生成オーケストレーションは利用権を確認して適用する。 |
| [copilot-studio-v2](copilot-studio-v2/SKILL.md) | Copilot Studio の新アーキテクチャ（cliagent）の制約・構造・手動運用手順を整理する。単独利用時の判断基準。    |
| [power-automate](power-automate/SKILL.md)       | Power Automate クラウドフローをソリューション対応で作成・デプロイする。                                      |

### ai — AI / プロンプト

| スキル                                        | 説明                                                                                                           |
| --------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| [ai-builder](ai-builder/SKILL.md)             | AI Builder の AI プロンプトを作成し、エージェントのツールとして組み込む。                                      |
| [spec-to-markdown](spec-to-markdown/SKILL.md) | PDF・PowerPoint・Excel 等の仕様書を markdown 化し、Power Platform 開発向けの factsheet / document を整理する。 |
| [spec-builder](spec-builder/SKILL.md)         | 3 つの入口で要件を対話整理し、案件の開発入力を作成する。必要な場合は資料変換も扱う。                           |

---

## 目的別の入口

| やりたいこと                                  | 最初に読むスキル                                                                                                                                                                                                                                                    |
| --------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 何から始めるか決めたい                        | [architecture](architecture/SKILL.md)                                                                                                                                                                                                                               |
| 既存仕様書を整理して要件化したい              | [spec-to-markdown](spec-to-markdown/SKILL.md)                                                                                                                                                                                                                       |
| 対話で要件を整理し開発入力を作りたい          | [spec-builder](spec-builder/SKILL.md)                                                                                                                                                                                                                               |
| SDK や upstream skills の更新追従を確認したい | [standard](standard/SKILL.md)                                                                                                                                                                                                                                       |
| Dataverse のテーブル・列・権限から固めたい    | [dataverse](dataverse/SKILL.md) / [Conversation Transcript 分析](dataverse/references/conversation-transcript-analysis.md)                                                                                                                                          |
| 画面 UI が本当に必要                          | [architecture](architecture/SKILL.md) で要否・利用条件を確認し、[canvas-app](canvas-app/SKILL.md) を基本案に検討。難しい場合のみ [code-apps](code-apps/SKILL.md) / [model-driven-app](model-driven-app/SKILL.md) を実現性・ライセンス・費用と承認を確認して代替検討 |
| 自動化・通知・外部トリガーを作りたい          | [power-automate](power-automate/SKILL.md) でフロー種別を確認。エージェント連携時は [architecture](architecture/SKILL.md) で方式・例外条件を判断する                                                                                                                 |
| エージェントや AI ツールを作りたい            | [architecture](architecture/SKILL.md) で連携利用か単独利用かを判断し、[copilot-studio](copilot-studio/SKILL.md)（v1）または [copilot-studio-v2](copilot-studio-v2/SKILL.md)（v2）を選ぶ。AI Builder は要件・ライセンス確認後の候補                                  |

---

## 推奨開発フロー

```
0. spec-to-markdown   → 既存仕様書を factsheet / document に正規化（必要時）
1. architecture       → 全体設計・コンポーネント選定（Teams / M365 Copilot 優先。画面 UI が必要なら Canvas App を基本案とし、要件実現が難しい場合は Code Apps / Model-Driven Apps も代替候補として提案。実現性・ライセンス・費用と承認を確認）
2. standard           → 共通基盤の確認（.env・認証）
3. dataverse          → カスタムテーブルが必要な場合、設計承認後にテーブル構築・セキュリティロール設定（依存するアプリ・フローより先）
4. copilot-studio     → エージェントが必要な場合のみ。連携利用や既存トリガー資産を使う構成
  OR copilot-studio-v2 → エージェントが必要な場合のみ。Teams / M365 Copilot 単独利用向けの新アーキ構成
5. canvas-app         → 画面 UI が必要な場合のみ Canvas App（MCP + coauthoring / Git Integration / single app・package の使い分けと、添付・staging・Flow 中継）を検討
  OR code-apps        → Canvas App では難しい場合、実現性・ライセンス・費用を確認し明示承認後に代替採用
  OR model-driven-app → Canvas App では難しい場合、実現性・ライセンス・費用を確認し明示承認後に代替採用
6. power-automate     → フローが必要な場合のみ。フロー種別・実行主体・接続条件を確認して作成
7. ai-builder         → AI プロンプト追加（必要時。最新ライセンス条件を確認）
8. update-skills      → スキル更新・PR 連携・検証の標準化（標準運用へ反映する場合）
```
