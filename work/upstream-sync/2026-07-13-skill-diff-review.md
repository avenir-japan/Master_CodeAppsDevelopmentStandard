# Upstream 差分レビュー 2026-07-13

対象 upstream:

- geekfujiwara/CodeAppsDevelopmentStandard
- 確認起点: activity ページと関連 skill ファイル

## 今回の前提

- このマスターで今すぐ反映対象にするのは、**Copilot Studio v2 周辺の更新**を中心とする
- **Azure / Power Pages / Cowork / Code Apps 実務差分**は、今回の基本運用スコープでは扱わない
- upstream の設計思想を丸ごと移植するのではなく、**このマスターの方針を維持したまま必要差分だけ拾う**

## 採用済み

### Copilot Studio v2 の追加

以下をこのマスターへ追加・更新済み:

- `.github/skills/copilot-studio-v2/SKILL.md`
- `.github/skills/copilot-studio-v2/references/new-architecture.md`
- `.github/skills/copilot-studio-v2/references/mcp-servers.md`
- `.github/skills/copilot-studio-v2/references/troubleshooting.md`
- `.github/skills/copilot-studio-v2/references/manual-creation-checklist.md`
- `.github/skills/copilot-studio-v2/references/icon-and-publish.md`
- `.github/skills/copilot-studio-v2/references/publish-description-template.md`

### 既存スキルへの反映

- `.github/skills/architecture/SKILL.md`
  - Copilot Studio v1 / v2 の選び分けを追加
- `.github/skills/README.md`
  - `copilot-studio-v2` を追加

## 保留

### Code Apps 実務差分

upstream の最近の更新には、以下のような Code Apps 実務差分がある:

- `check_code_apps_environment.py`
- `toggle_table_lang.py`
- `japanese-sanitize.md`
- `data-source-patterns.md`
- `lookup-resolution.md`
- `user-identity.md`
- `new-theme-checklist.md`
- `design-templates.md`
- `crud-ui-pattern.md`
- 各種 UI パターン reference

判断:

- **価値はあるが今回は保留**
- Code Apps を案件で本格採用すると決まったタイミングで、`code-apps` スキル単位で別タスクとして取り込む
- `code-apps/SKILL.md` の全文差し替えは行わず、scripts / references の選択追加を基本方針とする

### standard の共通差分

upstream には次の横断 reference がある:

- `browser-automation.md`
- `interactive-setup.md`
- `dataverse-mcp-setup.md`
- `design-language.md`

判断:

- **今すぐ必須ではないため保留**
- ただし `browser-automation.md` は Copilot Studio v2 の手動運用と相性がよく、次回の候補として優先度は高い

## 今回の運用スコープ外

### Azure スキル

- 外部公開サイト
- Azure 上の Web
- Foundry エージェント

判断:

- このマスターの現行スコープでは **基本フォーカス外**
- 将来 Azure 案件を扱うときに別テーマとして追加判断する

### Power Pages スキル

判断:

- 外部向けポータル案件が無い限り **不要**
- 今回は内部業務中心のため見送り

### Cowork スキル

判断:

- upstream では中心的な設計思想だが、このマスターでは **方針変更を伴う**
- 単なる差分反映ではなく、別テーマで評価すべきため今回は見送る

### update-skills / package-sample / business sample 群

判断:

- 開発標準の運用高度化や公開サンプル整備の話であり、今回の主題ではない
- 今回は見送る

## 次回再開時の判断順

1. Copilot Studio v2 で不足が出ていないか確認
2. 必要なら `standard/references/browser-automation.md` を先に取り込む
3. Code Apps を案件で使うことが確定したら `code-apps` 差分を別タスクで反映
4. Azure / Power Pages / Cowork は案件要件が出た時点で別判断
