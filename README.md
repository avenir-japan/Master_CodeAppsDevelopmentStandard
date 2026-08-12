# Power Platform コードファースト開発標準

Power Platform の業務アプリやエージェントを **VS Code + GitHub Copilot** で開発するための、実践的な開発標準リポジトリです。
UI 実装方式として **Code Apps / Canvas Apps / Model-Driven Apps** を扱いますが、このリポジトリの実装標準は **TypeScript + React + Tailwind CSS + shadcn/ui による Code Apps** を基本とします。

> [!TIP]
> このリポジトリを GitHub Copilot と使う場合は、まず **`@PowerCode` + GPT-5.4** を入口として使う運用を推奨します。
> Power Platform 案件に必要なスキル選択、設計確認、実装フローをこの前提で揃えています。

> [!IMPORTANT]
> UI 方式は AI が独断で確定せず、要件・顧客要望・保守体制・既存資産を踏まえて **architecture スキルで比較し、ユーザー確認のうえ決定** します。

[![VS Code で開く](https://img.shields.io/badge/VS%20Code%E3%81%A7%E9%96%8B%E3%81%8F-007ACC?style=for-the-badge&logo=visual-studio-code&logoColor=white)](https://vscode.dev/github/geekfujiwara/Master_CodeAppsDevelopmentStandard)
[![GitHub Copilot](https://img.shields.io/badge/GitHub%20Copilot-対応-blueviolet?style=for-the-badge&logo=github)](https://github.com/features/copilot)

## 使い方動画

- [使い方を説明した動画（YouTube）](https://youtu.be/-BU7KnjvYoc?si=iO8MtVLq__gOfTqw)

---

## このリポジトリで提供するもの

- Power Platform 向けコードファースト開発標準（`.github/skills/*/references/`）
- GitHub Copilot 用のカスタムエージェント / スキル（`.github/`）
- UI 実装方式の選定ガイド（Code Apps / Canvas Apps / Model-Driven Apps）
- Code Apps のスターター UI コンポーネント（`src/components/`）
- Canvas App の AI 編集、Git 管理、限定的な受け渡しの 3 モード整理
- Power Automate / Copilot Studio 連携の実装パターン
- `.env.example` を含むプロジェクト初期化テンプレート

> [!TIP]
> サンプル実装はあくまでリファレンスです。業務要件に合わせて `src/pages/` やスキル内スクリプトを置き換えて利用してください。

---

## 目次

- [クイックスタート](#クイックスタート)
- [はじめての方向け](#はじめての方向け)
- [環境事前チェックとブートストラップ](#環境事前チェックとブートストラップ)
- [想定運用モデル](#想定運用モデル)
- [GitHub Copilot 利用方針](#github-copilot-利用方針)
- [案件開発の進め方（Copilot 運用）](#案件開発の進め方copilot-運用)
- [カスタムエージェント前提の利用方法](#カスタムエージェント前提の利用方法)
- [目的別の入口](#目的別の入口)
- [リポジトリ構成](#リポジトリ構成)
- [主要ドキュメント](#主要ドキュメント)
- [GitHub Copilot 活用](#github-copilot-活用)

---

## クイックスタート

```bash
git clone https://github.com/geekfujiwara/Master_CodeAppsDevelopmentStandard . && npm install
```

```powershell
Copy-Item .env.example .env
```

> [!NOTE]
> `.` へ clone するため、空ディレクトリで実行してください。既存ファイルがある場所で実行すると上書きリスクがあります。

> [!IMPORTANT]
> このリポジトリを複数案件向けのマスターとして使う場合、`.env` はリポジトリに保持しません。案件ごとに `.env.example` を複製して `.env` を作成し、接続先・ソリューション名・認証プロファイル名をその案件用の値に置き換えてください。

`npm install` では `postinstall` で **環境事前チェック (preflight)** を実行し、Node.js / npm / Python（`python` or `py -3`）/ pip / `npx power-apps` / `pac` を確認します。

Python と pip が利用可能な場合は、`spec-to-markdown` 用 `.venv` の作成と `requirements.txt` の導入まで自動で試行します。未導入ツールがある場合は、次に実行すべきコマンドを表示します。

セットアップ後は、GitHub Copilot のカスタムエージェントに「実現したいこと」をそのまま伝えて開発を進めます。

---

## はじめての方向け

このリポジトリでは、Power Platform 開発に関わるものを次の 3 層に分けて扱います。

| 区分                                  | 何が入るか                                                                        | このリポジトリに含まれるか | 補足                                                           |
| ------------------------------------- | --------------------------------------------------------------------------------- | -------------------------- | -------------------------------------------------------------- |
| VS Code 拡張機能・ランタイム          | VS Code、Node.js、GitHub Copilot、GitHub Copilot Chat、Power Platform Tools など  | ❌ 含まれない              | 開発者の端末へ別途インストールする                             |
| Copilot カスタムエージェント / スキル | `@PowerCode`、`.github/skills/` 配下の開発標準                                    | ✅ 含まれる                | このリポジトリを VS Code で開くと参照される                    |
| 外部 Agent Plugin / MCP               | Canvas Apps Plugin、Copilot Studio plugin、Dataverse 向けの外部 plugin / MCP など | ❌ 含まれない              | 必要な場合だけ別途追加し、各 plugin の README と前提条件に従う |

最初に押さえるべきポイント:

- VS Code 拡張機能の推奨一覧は [.vscode/extensions.json](./.vscode/extensions.json) を正本とする
- このリポジトリに含まれる Copilot 用の知識と作業ルールは [.github/agents/PowerCode.agent.md](./.github/agents/PowerCode.agent.md) と [.github/skills/README.md](./.github/skills/README.md) にある
- Power Platform Tools 拡張機能は VS Code 側へ別途インストールする。PAC CLI 連携の入口にはなるが、このリポジトリでは `pac` の利用可否を bootstrap で独立に確認する
- `plugins/plugin-power-apps.ts` は Power Apps 用の Vite プラグインであり、Copilot の Agent Plugin ではない
- Canvas Apps Plugin や Copilot Studio plugin、Dataverse 向けの外部 plugin / MCP は補助的な外部追加物であり、このリポジトリへ同梱して配布するものではない
- repo 同梱の skill と外部 plugin はテーマが重なることがあるが、前者は案件標準、後者は追加ツール群であり、同一物ではない

外部 plugin を使う場合の注意:

- Canvas Apps Plugin は preview 機能で、別途 `.NET 10 SDK` が必要。`canvas-authoring` MCP を登録し、YAML 検証・control/API/data source 参照・coauthoring sync を提供する
- Copilot Studio plugin は author / manage / test / advisor 系の外部 plugin で、VS Code では `@agentPlugins` から追加する。push/pull/clone では Copilot Studio Extension が別途必要になる
- Dataverse MCP Server は Power Platform 環境側で提供・有効化する機能であり、`dataverse` Agent Plugin は GitHub Copilot / Copilot CLI 側で使う外部補助機能です。どちらもこのリポジトリに同梱しません
- Dataverse でも外部 plugin や MCP を使う場合があるが、この repo の `.github/skills/dataverse/` とは別レイヤーの補助機能として扱う
- これらはあると便利だが、リポジトリ内の `.github/agents/` と `.github/skills/` を置き換えるものではない

### GitHub Copilot で Canvas Apps plugin を使い始める最短入口

このリポジトリは **GitHub Copilot での利用を第一候補** にしているため、
Canvas App の AI 編集もまず GitHub Copilot 前提で整理する。

- この repo だけでは Canvas Apps plugin / MCP は使える状態にならない
- まず外部 plugin と MCP サーバー設定を開発端末側へ追加する
- 追加後の運用ルールと実装方針は、この repo の `.github/skills/canvas-app/` を正本とする

Copilot CLI / Claude Code で導入する場合の代表コマンド:

```text
/plugin marketplace add microsoft/power-platform-skills
/plugin install canvas-apps@power-platform-skills
```

VS Code の GitHub Copilot で使う場合の見方:

- 拡張機能ビューの **エージェント プラグイン** に `canvas-apps` が見える
- **MCP サーバー** に `canvas-authoring` が見える
- ただし、表示されているだけでは対象 app に接続済みとは限らない

次の 3 点がそろって初めて、Canvas App の live editing を始められる。

1. Canvas Apps plugin がインストール済み
2. `canvas-authoring` MCP が対象 app の environment ID / app ID / cluster に向けて設定済み
3. Power Apps Studio 側で対象 app を開き、coauthoring が有効になっている

最短セットアップ手順と疎通確認は
[.github/skills/canvas-app/references/ai-codegen-workflow.md](./.github/skills/canvas-app/references/ai-codegen-workflow.md)
を参照する。

Canvas App の運用は、次の 3 モードで整理して使い分けます。

| モード               | 主目的                    | この repo での位置づけ |
| -------------------- | ------------------------- | ---------------------- |
| MCP + coauthoring    | AI 主導の作成・編集       | 第一選択               |
| Git Integration      | source control と軽微編集 | チーム標準             |
| single app / package | 限定的な受け渡し          | 例外運用               |

詳細は [.github/skills/canvas-app/SKILL.md](./.github/skills/canvas-app/SKILL.md) と、その配下の references を正本とします。

---

## 環境事前チェックとブートストラップ

```bash
# 事前チェックのみ（不足がある場合は exit 1）
npm run check:env

# 事前チェック + Python bootstrap を再実行
npm run setup
```

不足時の対応:

- Python 未検出: Python 3.10+ を導入して `python --version` または `py -3 --version` を通す
- pip 未検出: `python -m ensurepip --upgrade`（または `py -3 -m ensurepip --upgrade`）
- `pac` 未検出: `npm install -g @microsoft/power-apps-cli` 後、`pac auth create --environment {ENVIRONMENT_ID}`
- `npx power-apps` 未検出: `npm install` を再実行し `@microsoft/power-apps` 依存を確認

---

## 想定運用モデル

このリポジトリは、**弊社環境で Power Platform ソリューションを開発・検証するためのマスター**として使います。
案件ごとはこの標準を複製して進め、顧客要件に応じて `src/`、`scripts/`、`work/`、環境設定を追加します。

案件で得た汎用的に再利用できる知見は、案件リポジトリからこのマスターへスキル・ナレッジとして戻し、案件を重ねるごとにマスターを育てます。戻す対象・戻さない対象・戻し先の判断は [マスターリポジトリへの知見還元](./.github/skills/standard/references/master-repo-feedback-loop.md) を参照してください。

案件終了時の VS Code 上での具体手順と、GitHub Copilot へそのまま渡せる依頼テンプレートも同じ文書にまとめています。還元候補の洗い出し自体は Copilot が担い、利用者は案件フォルダ指定と最終判断に集中する前提です。運用に迷った場合は、まずこのリファレンスを起点にしてください。

納品時は、案件ごとに **マネージド** または **アンマネージド** のいずれかを選定し、ソリューションとして提供します。

- 開発環境は常にアンマネージドで作業する
- 納品形態は要件定義で確定し、選定理由を記録する
- 顧客環境ごとに変わる値は環境変数・接続参照に外出しする
- Teams 公開、認証設定、一部接続設定は納品先で再構成が必要になる

> [!IMPORTANT]
> 納品形態は固定でマネージドとはしません。顧客がどこまで編集するか、保守主体がどちらか、バージョンアップをどう運用するかを踏まえて、案件ごとに選びます。

> [!NOTE]
> ライセンス要件や Copilot Credits の消費は変更頻度が高いため、このリポジトリでは固定値の断定よりも **最新の Microsoft Learn / Licensing Guide を都度確認する運用** を優先します。

---

## GitHub Copilot 利用方針

README では全体像だけを示し、**Copilot の詳細ルールの正本は [standard スキル](./.github/skills/standard/SKILL.md)** に置きます。

- 作業の切り分けは `Copilot で自動整理`、`スクリプトで半自動`、`顧客管理者または案件責任者が実施` の 3 区分で扱う
- モデル運用は **既定を GPT-5.4** とし、軽作業は軽量モデル、コード中心の実装はコード特化モデルも候補にしつつ、高難度タスクではまず GPT 系の上位 reasoning model を候補にし、比較検討や別観点レビューが必要な場合は Opus 系も候補にする
- 納品案件では、環境変数だけでなくマネージドプロパティ、接続参照、顧客環境での初期設定作業までまとめて確認する

詳細は以下を参照:

- [standard スキル](./.github/skills/standard/SKILL.md)
- [Power Platform 開発標準](./.github/skills/standard/references/power-platform-development-standard.md)

---

## 案件開発の進め方（Copilot 運用）

- GitHub Copilot の参照方針：[.github/copilot-instructions.md](./.github/copilot-instructions.md)
- 要件ディスカバリーと生成物一式の作成（M365 Copilot／Copilot Cowork 用）：
  [.github/skills/standard/references/requirements-discovery.md](./.github/skills/standard/references/requirements-discovery.md)

### M365 Copilot／Copilot Cowork で要件整理を開始する

1. 本リポジトリを参照対象として指定する。
2. 「要件ディスカバリーと生成物一式の作成」の実際のファイルパス
   [.github/skills/standard/references/requirements-discovery.md](./.github/skills/standard/references/requirements-discovery.md)
   を指定し、その手順に従って要件整理を進めるよう依頼する。
3. 目的・現状・制約・構成を 1 問ずつ確認する。
4. 構成が確定した後、必要な開発入力ファイルの候補を提示させる。
5. 作成対象について合意した後に、開発入力ファイル一式を作成する。

---

## カスタムエージェント前提の利用方法

- この開発標準の実装・運用ルールは、GitHub Copilot カスタムエージェントのスキル（`.github/skills/`）に定義されています。
- 利用者は手順書を読み込んで操作するのではなく、カスタムエージェントに要件を伝えて進める前提です。
- このリポジトリで Power Platform 案件を進める場合は、通常の汎用 Agent よりも **`@PowerCode` を第一選択** とします。
- モデルは **既定で GPT-5.4 を推奨** し、高難度タスクで上位 reasoning model へ切り替える基準は [standard スキル](./.github/skills/standard/SKILL.md) の「Copilot 向け優先判断基準」を正本とします。
- チャット入力例 （バッククオート不要）: @PowerCode 在庫管理アプリを作りたい。Code Apps と Canvas Apps のどちらで進めるべきか設計して
- 既存仕様書がある場合の入力例: @PowerCode spec-to-markdown
- 既定以外の場所を使う場合の入力例: @PowerCode /home/.../input の仕様書を requirements markdown に変換して

> [!NOTE]
> Microsoft Learn の現行 Code Apps 概要に合わせ、このリポジトリでは **Code Apps は SPA をホストする機能** として扱います。
> 公式の推奨 CLI は `npx power-apps` 系に移行中で、`pac code` は将来廃止予定です。本リポジトリ内で `pac code push` を併記している箇所は、既知のテナント解決問題に対する暫定ワークアラウンドです。

---

## 目的別の入口

最初にどこを見ればよいか迷う場合は、次だけ見れば十分です。

| やりたいこと                          | 最初に読む場所                                                                                                                                                                                                                        |
| ------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 何から始めるか決めたい                | [architecture](./.github/skills/architecture/SKILL.md)                                                                                                                                                                                |
| 仕様書から要件を整理したい            | [spec-to-markdown](./.github/skills/spec-to-markdown/SKILL.md)                                                                                                                                                                        |
| Dataverse のテーブル設計から始めたい  | [dataverse](./.github/skills/dataverse/SKILL.md)                                                                                                                                                                                      |
| Copilot Studio の会話ログを分析したい | [Conversation Transcript 分析](./.github/skills/dataverse/references/conversation-transcript-analysis.md)                                                                                                                             |
| UI 実装に入りたい                     | [code-apps](./.github/skills/code-apps/SKILL.md) / [canvas-app](./.github/skills/canvas-app/SKILL.md) / [model-driven-app](./.github/skills/model-driven-app/SKILL.md) / [generative-page](./.github/skills/generative-page/SKILL.md) |
| 自動化や通知を作りたい                | [power-automate](./.github/skills/power-automate/SKILL.md)                                                                                                                                                                            |
| エージェントや AI を作りたい          | [copilot-studio](./.github/skills/copilot-studio/SKILL.md) / [ai-builder](./.github/skills/ai-builder/SKILL.md)                                                                                                                       |

詳細な構成規約や全スキルの一覧は [スキルカタログ](./.github/skills/README.md) を参照してください。

> [!IMPORTANT]
> Dataverse MCP Server の実環境 URL、接続設定、シークレットはリポジトリへ保存しません。必要な設定は VS Code の MCP 追加操作や、プレースホルダー付きの参照手順で扱ってください。

---

## リポジトリ構成

```text
.
├── .github/
│   ├── agents/                      # Copilot カスタムエージェント定義
│   └── skills/                      # 製品単位で統合された 12 スキル
│       ├── architecture/            # アーキテクチャ設計
│       ├── standard/                # 共通基盤（認証・アイコン・メールテンプレート）
│       ├── dataverse/               # テーブル設計・構築・セキュリティロール
│       ├── code-apps/               # Code Apps 開発（UI 設計・CSP・メール送信含む）
│       ├── canvas-app/              # Canvas App 開発（AI 編集・Git 管理・限定移送・添付パターン）
│       ├── generative-page/         # Generative Pages 開発
│       ├── model-driven-app/        # モデル駆動型アプリ構築
│       ├── copilot-studio/          # エージェント構築・トリガー・ニュース配信
│       ├── power-automate/          # クラウドフロー作成・デプロイ
│       ├── ai-builder/              # AI プロンプト作成
│       └── spec-to-markdown/        # 仕様書→要件 markdown 変換
├── src/
│   ├── components/                  # 再利用 UI コンポーネント
│   ├── pages/                       # サンプルページ実装
│   ├── providers/                   # Context / Provider 群
│   ├── hooks/                       # カスタムフック
│   ├── lib/                         # 共通ユーティリティ
│   └── types/                       # 型定義
├── scripts/                         # 環境チェック・ブートストラップ
├── plugins/                         # Power Apps Vite プラグイン
├── styles/                          # Tailwind スタイル
├── .env.example                     # 環境変数テンプレート
├── SAMPLES.md                       # サンプル実装の置き換えガイド
└── README.md
```

---

## 主要ドキュメント

- [.github/skills/standard/references/power-platform-development-standard.md](./.github/skills/standard/references/power-platform-development-standard.md)
- [.github/skills/standard/references/managed-solution-delivery.md](./.github/skills/standard/references/managed-solution-delivery.md)
- [.github/skills/standard/references/environment-variables.md](./.github/skills/standard/references/environment-variables.md)
- [.github/skills/standard/references/license-requirements.md](./.github/skills/standard/references/license-requirements.md)
- [.github/skills/copilot-studio/references/managed-solution-constraints.md](./.github/skills/copilot-studio/references/managed-solution-constraints.md)
- [.github/skills/dataverse/references/dataverse-guide.md](./.github/skills/dataverse/references/dataverse-guide.md)
- [.github/skills/code-apps/references/connector-reference.md](./.github/skills/code-apps/references/connector-reference.md)
- [.github/skills/canvas-app/references/ai-codegen-workflow.md](./.github/skills/canvas-app/references/ai-codegen-workflow.md)
- [.github/skills/canvas-app/references/source-code-and-git-integration.md](./.github/skills/canvas-app/references/source-code-and-git-integration.md)
- [.github/skills/canvas-app/references/alm-and-import-options.md](./.github/skills/canvas-app/references/alm-and-import-options.md)
- [.github/skills/canvas-app/references/design-patterns.md](./.github/skills/canvas-app/references/design-patterns.md)
- [.github/skills/canvas-app/references/coauthoring-checklist.md](./.github/skills/canvas-app/references/coauthoring-checklist.md)
- [.github/skills/canvas-app/references/coauthoring-limitations.md](./.github/skills/canvas-app/references/coauthoring-limitations.md)
- [.github/skills/canvas-app/references/data-source-and-connector-boundary.md](./.github/skills/canvas-app/references/data-source-and-connector-boundary.md)
- [.github/skills/code-apps/references/advanced-patterns.md](./.github/skills/code-apps/references/advanced-patterns.md)
- [SAMPLES.md](./SAMPLES.md)

---

## GitHub Copilot 活用

- VS Code で開くと `.github/agents/` と `.github/skills/` が認識されます
- `@PowerCode` に実現したい内容を伝えるだけで、必要なスキルが選択されて開発タスクを進められます
- このリポジトリの開発標準はスキルとして定義済みのため、マニュアル手順ベースではなくエージェント駆動で利用します

担当領域の選び方は [目的別の入口](#目的別の入口) を参照し、全スキルの一覧と構成規約は [スキルカタログ](./.github/skills/README.md) を正本とします。
