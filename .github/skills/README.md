# Power Platform Skills カタログ

Power Platform コードファースト開発で使用するスキル群。
GitHub Copilot の段階的読込と Progressive Disclosure を前提に構成。

## このカタログの既定スコープ

このマスターリポジトリでは、検証導入パッケージの既定提案を **ベースライセンス（Microsoft 365 + Copilot）の範囲内** に置く。

- 既定の UI / チャネル優先順位は **Teams / Microsoft 365 Copilot** を先頭に置く
- **Canvas App（標準コネクタ）** は既定スコープに含むが、工数を踏まえて **必要時のみ** 提案する
- Code Apps、Dataverse カスタムテーブル、AI Builder、プレミアム / カスタムコネクタ、クレジット消費が大きい Copilot Studio パターンは、**案件ごとの追加ライセンス評価項目** として扱う
- 個別スキルの技術手順は残し、採用可否や優先順位は上位の `standard` / `architecture` / ライセンス確認ルールを正本とする

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

## スキル一覧（12 スキル）

### architecture — アーキテクチャ・基盤

| スキル                                | 説明                                                                           |
| ------------------------------------- | ------------------------------------------------------------------------------ |
| [architecture](architecture/SKILL.md) | Power Platform 全体の構成方針を設計し、最適なコンポーネント構成を決定する。    |
| [standard](standard/SKILL.md)         | 共通認証・環境変数・ソリューション運用など、全スキル共通の開発基盤を提供する。 |

### data — データ層

| スキル                          | 説明                                                                       |
| ------------------------------- | -------------------------------------------------------------------------- |
| [dataverse](dataverse/SKILL.md) | Dataverse のテーブル設計・構築・デモデータ投入・権限設定を一括で実施する。 |

### ui — UI / フロントエンド

| スキル                                        | 説明                                                                                                                                                      |
| --------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [code-apps](code-apps/SKILL.md)               | Code Apps を TypeScript/React ベースで開発し、UI 設計からデプロイまで対応する。                                                                           |
| [canvas-app](canvas-app/SKILL.md)             | Canvas App の AI 主導編集、Git によるソース管理、single app / package による限定移送を整理し、添付・PDF 要件では SharePoint staging + Flow 中継まで扱う。 |
| [generative-page](generative-page/SKILL.md)   | Generative Pages（genux）を開発・デバッグし、モデル駆動型アプリへデプロイする。                                                                           |
| [model-driven-app](model-driven-app/SKILL.md) | モデル駆動型アプリを作成・構成し、公開まで実行する。                                                                                                      |

### automation — 自動化

| スキル                                          | 説明                                                                                                      |
| ----------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| [copilot-studio](copilot-studio/SKILL.md)       | Copilot Studio エージェントを生成オーケストレーション前提で構築・運用する。                               |
| [copilot-studio-v2](copilot-studio-v2/SKILL.md) | Copilot Studio の新アーキテクチャ（cliagent）の制約・構造・手動運用手順を整理する。単独利用時の判断基準。 |
| [power-automate](power-automate/SKILL.md)       | Power Automate クラウドフローをソリューション対応で作成・デプロイする。                                   |

### ai — AI / プロンプト

| スキル                                        | 説明                                                                                                           |
| --------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| [ai-builder](ai-builder/SKILL.md)             | AI Builder の AI プロンプトを作成し、エージェントのツールとして組み込む。                                      |
| [spec-to-markdown](spec-to-markdown/SKILL.md) | PDF・PowerPoint・Excel 等の仕様書を markdown 化し、Power Platform 開発向けの factsheet / document を整理する。 |

---

## 目的別の入口

| やりたいこと                               | 最初に読むスキル                                                                                                                                                  |
| ------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 何から始めるか決めたい                     | [architecture](architecture/SKILL.md)                                                                                                                             |
| 既存仕様書を整理して要件化したい           | [spec-to-markdown](spec-to-markdown/SKILL.md)                                                                                                                     |
| Dataverse のテーブル・列・権限から固めたい | [dataverse](dataverse/SKILL.md)                                                                                                                                   |
| UI 実装にすぐ入りたい                      | [code-apps](code-apps/SKILL.md) / [canvas-app](canvas-app/SKILL.md) / [model-driven-app](model-driven-app/SKILL.md) / [generative-page](generative-page/SKILL.md) |
| 自動化・通知・外部トリガーを作りたい       | [power-automate](power-automate/SKILL.md)                                                                                                                         |
| エージェントや AI ツールを作りたい         | [copilot-studio](copilot-studio/SKILL.md) / [copilot-studio-v2](copilot-studio-v2/SKILL.md) / [ai-builder](ai-builder/SKILL.md)                                   |

---

## 推奨開発フロー

```
0. spec-to-markdown   → 既存仕様書を factsheet / document に正規化（必要時）
1. architecture       → 全体設計・コンポーネント選定（UI / チャネルは Teams / M365 Copilot を既定提案。画面 UI が必要なら Canvas Apps / Model-Driven Apps / Code Apps を比較して必ずユーザー確認）
2. standard           → 共通基盤の確認（.env・認証）
3. copilot-studio     → 連携利用や既存トリガー資産を使う Copilot Studio 構成
  OR copilot-studio-v2 → Teams / M365 Copilot 単独利用向けの新アーキ構成
4. canvas-app         → 画面 UI が必要な場合のみ Canvas App（MCP + coauthoring / Git Integration / single app・package の使い分けと、添付・staging・Flow 中継）を検討
  OR model-driven-app → モデル駆動型アプリ構築
  OR code-apps        → Code Apps UI 設計・開発・デプロイ
  OR generative-page  → Generative Pages 開発
5. power-automate     → フロー作成
6. dataverse          → テーブル設計・構築・セキュリティロール設定（必要時）
7. ai-builder         → AI プロンプト追加（必要時。最新ライセンス条件を確認）
```
