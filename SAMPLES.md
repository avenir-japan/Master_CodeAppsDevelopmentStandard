# サンプル実装ガイド

本リポジトリには **開発標準・スキル（汎用テンプレート）** と **インシデント管理サンプル（リファレンス実装）** の 2 種類のコードが含まれています。

> [!TIP]
> このリポジトリから案件を始める場合は、まず **`@PowerCode` + GPT-5.4** で要件を伝える運用を推奨します。
> サンプルの置き換え判断や、どのスキルから入るかの整理をエージェント側に寄せられます。

## 構成の区分

### そのまま再利用できるもの（開発標準・テンプレート）

| パス                                             | 内容                                                           |
| ------------------------------------------------ | -------------------------------------------------------------- |
| `.github/agents/`                                | GitHub Copilot カスタムエージェント定義                        |
| `.github/skills/`                                | 各フェーズの開発スキル（検証済み教訓・パターン集）             |
| `.github/skills/**/references/`                  | 開発標準ドキュメント                                           |
| `src/components/`                                | shadcn/ui + カスタム UI コンポーネント                         |
| `src/providers/`                                 | React Context Providers                                        |
| `src/lib/utils.ts`                               | ユーティリティ                                                 |
| `.github/skills/standard/scripts/auth_helper.py` | MSAL 認証ヘルパー                                              |
| `plugins/`                                       | Power Apps 用 Vite プラグイン（Copilot Agent Plugin ではない） |
| `styles/`                                        | Tailwind CSS テーマ                                            |
| `patch-nameutils.cjs`                            | 日本語 DisplayName パッチ                                      |
| `.env.example`                                   | 環境変数テンプレート                                           |
| `package.json`                                   | 依存関係（shadcn/ui, TanStack Query 等）                       |
| `vite.config.ts`, `tsconfig*.json`               | ビルド設定                                                     |

### サンプル実装（プロジェクトに合わせて置き換え）

> インシデント管理（IT Service Management）を題材とした End-to-End のリファレンス実装です。
> テーブル名・エージェント名・フロー名等をあなたのプロジェクトに書き換えてください。
> `incident` 系の画面・型・ルート名もサンプル実装のため、案件では画面設計に合わせてまとめて置き換えてください。

| パス                                                     | 内容                            | 置き換え対象                           |
| -------------------------------------------------------- | ------------------------------- | -------------------------------------- |
| `.github/skills/dataverse/scripts/setup_dataverse.py`    | Dataverse テーブル構築          | テーブル定義・列・Lookup・デモデータ   |
| `.github/skills/copilot-studio/scripts/deploy_agent.py`  | Copilot Studio エージェント設定 | BOT_NAME・Instructions・推奨プロンプト |
| `.github/skills/power-automate/scripts/deploy_flow.py`   | ステータス変更通知フロー        | テーブル名・通知メール本文             |
| `.github/skills/power-automate/scripts/deploy_flow_*.py` | 各種 Power Automate フロー      | フロー定義全体                         |
| `.github/skills/ai-builder/scripts/deploy_ai_prompt.py`  | AI Builder プロンプト           | プロンプト内容・入出力定義             |
| `.github/skills/standard/scripts/add_to_solution.py`     | ソリューション包含検証          | テーブル名リスト                       |
| `src/router.tsx`                                         | 画面ルーティング定義            | ルート構成・画面遷移                   |
| `src/pages/assets.tsx`                                   | 資産一覧ページ                  | ページ全体                             |
| `src/pages/dashboard.tsx`                                | ダッシュボード                  | 集計ロジック・KPI                      |
| `src/pages/incidents.tsx`                                | インシデント一覧ページ          | ページ全体                             |
| `src/pages/incident-detail.tsx`                          | インシデント詳細ページ          | ページ全体                             |
| `src/pages/kanban.tsx`                                   | カンバンボード                  | データソース                           |
| `src/pages/_layout.tsx`                                  | レイアウト定義                  | ナビゲーション・共通レイアウト         |
| `src/types/incident.ts`                                  | 型定義                          | エンティティ型                         |

### SDK 自動生成（環境ごとに再生成）

| パス                | 内容                                                           |
| ------------------- | -------------------------------------------------------------- |
| `src/generated/`    | `npx power-apps add-data-source` で自動生成（.gitignore 対象） |
| `.power/`           | Power Apps SDK 内部ファイル（.gitignore 対象）                 |
| `power.config.json` | `npx power-apps init` で自動生成（.gitignore 対象）            |

## 新しいプロジェクトの始め方

### 方法 1: テンプレートとしてクローン

> [!IMPORTANT]
> このリポジトリを複数案件向けのマスターとして使う場合、`.env` はマスター側に保持しません。案件ごとに `.env.example` を複製して `.env` を作成し、その案件の接続先・ソリューション名・認証プロファイル名を設定してください。

```powershell
git clone https://github.com/geekfujiwara/CodeAppsDevelopmentStandard my-project
cd my-project

# 1. .env を設定
Copy-Item .env.example .env
# DATAVERSE_URL, TENANT_ID, SOLUTION_NAME, PUBLISHER_PREFIX を編集

# 2. GitHub Copilot に指示（PowerCode エージェント）
# @PowerCode {あなたのアプリ}を作成してください
# 推奨モデル: GPT-5.4
# → エージェントが setup_dataverse.py 等を自動生成
```

### 方法 2: standard スキルだけ導入（既存プロジェクトに追加）

```powershell
$base = "https://raw.githubusercontent.com/geekfujiwara/CodeAppsDevelopmentStandard/main"
@(".github/skills/standard", ".github/skills/standard/references") | ForEach-Object {
  New-Item -ItemType Directory -Path $_ -Force
}
@(
  @{Src="$base/.github/skills/standard/SKILL.md"; Dst=".github/skills/standard/SKILL.md"},
  @{Src="$base/.github/skills/standard/references/power-platform-development-standard.md"; Dst=".github/skills/standard/references/power-platform-development-standard.md"}
) | ForEach-Object { Invoke-WebRequest -Uri $_.Src -OutFile $_.Dst }
```

> [!NOTE]
> この方法で取り込まれるのは、`standard` スキルと全体ガイドだけです。
> VS Code 拡張機能、Power Platform Tools、Canvas Apps Plugin、Copilot Studio plugin などの外部追加物は含まれません。
> それらは開発者端末へ別途インストールし、必要に応じて前提条件を満たしてください。

> [!IMPORTANT]
> `PowerCode.agent.md` は `dataverse`、`code-apps`、`copilot-studio` など複数の製品別スキルを参照します。
> そのため、既存プロジェクトへ最小セットだけを入れるこの方法には含めません。
> `@PowerCode` をそのまま使いたい場合は、`.github/agents/PowerCode.agent.md` に加えて、参照先となる `.github/skills/` 一式、または必要な製品別スキルを合わせて取り込んでください。

## サンプルの置き換え手順

1. **PowerCode エージェントに要件を伝える**
   - エージェントが Phase 0（設計）から自動でガイド
   - テーブル設計・UI 設計・エージェント設計をそれぞれ提案 → 承認後に実装

2. **エージェントが以下を自動で行う**
   - `setup_dataverse.py` を要件に合わせて新規生成
   - `deploy_agent.py` のエージェント名・Instructions を更新
   - `deploy_flow.py` のフロー定義を更新
   - `src/pages/` をプロジェクトの画面設計に合わせて実装

3. **手動で行うこと**
   - `.env` の設定
   - VS Code 拡張機能や外部 Agent Plugin が必要な場合は、開発者端末へ別途インストール
   - Copilot Studio UI でのエージェント作成
   - Power Automate 接続の事前作成
   - ナレッジ・MCP Server の UI での追加

> [!NOTE]
> ナレッジ・MCP Server の追加は、repo に含まれる `.github/skills/` の設定だけでは完了しません。
> 外部 plugin や MCP を使う場合は、それぞれの README にある前提条件とインストール手順を先に満たしてください。
