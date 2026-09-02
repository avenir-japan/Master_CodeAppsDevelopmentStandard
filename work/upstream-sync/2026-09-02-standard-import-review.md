# Upstream 差分反映メモ 2026-09-02

対象 upstream:

- geekfujiwara/CodeAppsDevelopmentStandard
- 比較基準: upstream main 最新 vs 現在の Master_CodeAppsDevelopmentStandard

## 今回の方針

- Master_CodeAppsDevelopmentStandard の開発方針を正本とする
- Code Apps / Dataverse 直接関連は今回の採用候補から除外する
- 品質・検証プロセスと開発速度に効く差分を優先して取り込む
- upstream を丸ごと移植せず、必要なスキル・参照・スクリプトだけを追加する

## 採用して反映した内容

### 1. update-skills

追加:

- .github/skills/update-skills/SKILL.md
- .github/skills/update-skills/references/.env.example
- .github/skills/update-skills/references/pr-strategy.md
- .github/skills/update-skills/references/sample-packaging.md
- .github/skills/update-skills/references/troubleshooting.md
- .github/skills/update-skills/scripts/manage_skill_pr.py
- .github/skills/update-skills/scripts/publish_skill.py
- .github/skills/update-skills/scripts/validate_skill.py

目的:

- スキル更新の標準化
- 構成検証と秘匿情報スキャンの自動化
- PR 更新優先の運用ルール整備

### 2. spec-builder

追加:

- .github/skills/spec-builder/SKILL.md
- .github/skills/spec-builder/references/conversion-guide.md
- .github/skills/spec-builder/scripts/convert_documents.py
- .github/skills/spec-builder/scripts/requirements.txt
- .github/skills/spec-builder/scripts/run_windows.ps1

追加対応:

- convert_documents.py のリポジトリルート検出に .git 非存在時フォールバックを追加
- run_windows.ps1 を ASCII 化し、-Help スイッチを追加

目的:

- Office/PDF/画像の一次情報を staging 化し、要件定義書へ統合

### 3. SDK 更新検知

追加:

- .github/scripts/check-sdk-updates.mjs
- .github/scripts/check-sdk-updates.test.mjs
- .github/scripts/check-sdk-updates.env.example

追加対応:

- check-sdk-updates.mjs に --help を追加

目的:

- npm SDK と upstream skills 更新の自動検知
- dry-run と Issue 作成モードの両対応

### 4. standard への横断方針追加

追加:

- .github/skills/standard/references/browser-automation.md
- .github/skills/standard/references/.env.example
- .github/skills/standard/references/gitignore-template
- .github/skills/standard/references/interactive-setup.md
- .github/skills/standard/references/sdk-update-check.md
- .github/skills/standard/scripts/check_mcp_client.py
- .github/skills/standard/scripts/setup_environment.py

更新:

- .github/skills/standard/SKILL.md

追加対応:

- check_mcp_client.py に --help を追加
- DATAVERSE_URL 未設定時にトレースバックではなく案内文を返すよう改善
- interactive-setup.md の upstream 直取得手順を Master 正本前提へ修正
- setup_environment.py / .env.example / gitignore-template を追加して対話型セットアップ導線を実体化
- standard から SDK 更新検知の正本リファレンスへ導線追加

目的:

- ブラウザ自動化方針の標準化
- AskUserQuestion 前提の対話セットアップ導線
- MCP クライアントの事前検証

### 5. Copilot Studio v2 の検証導線強化

追加:

- .github/skills/copilot-studio-v2/scripts/verify_agent.py
- .github/skills/copilot-studio-v2/scripts/verify_config.py
- .github/skills/copilot-studio-v2/references/verify-run-template.md

更新:

- .github/skills/copilot-studio-v2/SKILL.md

追加対応:

- verify_agent.py に --help / --bot-id を追加
- verify_config.py を実行可能な CLI に拡張し、--help / --bot-id を追加
- auth_helper の動的ロード化で Pylance 診断を解消
- MCP サーバー追加前に check_mcp_client.py で事前確認する導線を追加

目的:

- v2 cliagent の設定検証を実行可能な形で残す
- UI 手動変更後の検証導線を明確化する

### 6. Copilot Studio の障害対応導線強化

追加:

- .github/skills/copilot-studio/references/troubleshooting.md
- .github/skills/copilot-studio/references/trigger.md
- .github/skills/copilot-studio/references/trigger-patterns.md

更新:

- .github/skills/copilot-studio/SKILL.md

目的:

- trigger 以外を含む切り分け導線を追加

### 7. カタログ更新

更新:

- .github/skills/README.md
- .github/agents/PowerCode.agent.md

内容:

- update-skills / spec-builder をカタログへ追加
- PowerCode からの参照導線を追加
- SDK 更新検知を standard 経由で辿れるようにした

## 実施した検証

成功:

- py -3 .github/skills/update-skills/scripts/validate_skill.py .github/skills/update-skills
- py -3 .github/skills/update-skills/scripts/validate_skill.py .github/skills/spec-builder
- py -3 .github/skills/update-skills/scripts/validate_skill.py .github/skills/generative-page
- py -3 .github/skills/update-skills/scripts/validate_skill.py .github/skills/copilot-studio
- py -3 .github/skills/update-skills/scripts/manage_skill_pr.py --help
- py -3 .github/skills/update-skills/scripts/publish_skill.py --help
- py -3 .github/skills/standard/scripts/setup_environment.py --help
- py -3 .github/skills/copilot-studio-v2/scripts/verify_agent.py --help
- py -3 .github/skills/copilot-studio-v2/scripts/verify_config.py --help
- py -3 .github/skills/standard/scripts/check_mcp_client.py --help
- py -3 .github/skills/standard/scripts/check_mcp_client.py
- node .github/scripts/check-sdk-updates.mjs --help
- node .github/scripts/check-sdk-updates.test.mjs
- ISSUE_REPOSITORY=owner/repo, DRY_RUN=true で check-sdk-updates.mjs 実行
- powershell -NoProfile -ExecutionPolicy Bypass -File .github/skills/spec-builder/scripts/run_windows.ps1 -Help
- py -3 .github/skills/update-skills/scripts/validate_skill.py --all

確認結果:

- 新規導入スキルの最小 CLI 動作は確認済み
- standard の MCP 事前検証スクリプトは help 表示と設定不足時の案内を確認済み
- 対話型セットアップ導線は setup_environment.py の help と参照ファイル整合まで確認済み
- validate_skill.py --all は error 0、残りは scripts/ 未配置の warning のみ
- v2 verify の実環境検証には .env と Bot ID が必要
- SDK 更新検知の Issue 作成モードには GH_TOKEN または GITHUB_TOKEN が必要

## 全体検証で見えた既存課題

`py -3 .github/skills/update-skills/scripts/validate_skill.py --all` の error は解消済み。
現時点で残るのは warning のみ。

- architecture の scripts/ 欠如 warning
- canvas-app の scripts/ 欠如 warning
- generative-page の scripts/ 欠如 warning

今回の方針では warning 解消のための広範囲な構成変更までは行っていない。
必要なら別タスクで scripts/ 整備を実施する。

## 次回の優先順

1. v2 実検証

- .env と AGENT_BOTID を用意して verify_config.py / verify_agent.py を実行

2. SDK 更新検知の本番化

- GH_TOKEN を設定して Issue 自動作成モードを確認

3. validation warning の是正

- architecture / canvas-app / generative-page の scripts/ 整備方針を決める

## 今回の結論

標準導入として決めた範囲は、実ファイル反映、導線補完、repo-wide validation error 解消まで完了。
残る未実施は、実環境値が必要な確認と、warning 解消のための追加整備のみ。
