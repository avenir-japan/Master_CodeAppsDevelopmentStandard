# 仕様書 markdown 変換ガイド

## 1. 何を作るか

このスキルの最初のゴールは次の 2 つ。

1. **各入力ファイルの factsheet**
2. **全体統合 document.md**

Power Platform 向け要件整理に使えるよう、出力は raw markdown の貼り付けではなく **要件の分類軸** を固定する。

## 2. 推奨コマンド

依頼例: `@PowerCode input フォルダの仕様書を requirements markdown に変換して`、`@PowerCode spec-to-markdown input`。入力を指定する場合は `@PowerCode <input パス> の PDF と Excel を factsheet 化して` と伝える。

まずリポジトリルートで preflight/bootstrap を実行する。

```bash
npm install
# または再実行時
npm run setup
```

その後、必要に応じて個別に実行する。

```bash
cd .github/skills/spec-to-markdown/scripts
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python convert_documents.py
```

既定では次を使う。

- 入力: `<repo-root>/work/spec-to-markdown/input/`
- 出力: `<repo-root>/work/spec-to-markdown/output/<input-set>-<timestamp>/`

入力や出力を明示したい場合だけ override する。

```bash
python convert_documents.py \
  --input /absolute/path/to/input \
  --output /absolute/path/to/output
```

### 入力セット運用の例

```text
work/spec-to-markdown/input/
  customer-a/
    要件定義書.pdf
    画面一覧.xlsx
  project-x/
    業務フロー.pptx
```

- `python convert_documents.py` の既定入力は `input/` 全体
- `python convert_documents.py --input <repo-root>/work/spec-to-markdown/input/customer-a` とすると `customer-a-<timestamp>/` 配下へ出力される
- `input/` 直下のファイルは `batch-<timestamp>/`、入力セットを指定すると `<input-set>-<timestamp>/`（例: `customer-a-<timestamp>/`）へ出力する
- `--output` を省略すると、毎回タイムスタンプ付きの別フォルダになるため上書き事故を避けやすい。固定したい場合だけ `--output <出力先の絶対パス>` を使う
- 入力ファイルは読み取り専用として扱い、元資料を移動・削除しない。変換結果は出力フォルダに作成する

## 3. 対応対象

- PDF
- PowerPoint (`.ppt`, `.pptx`)
- Excel (`.xls`, `.xlsx`)
- Word (`.doc`, `.docx`)
- markdown / text / html

> Word / markdown / html まで含めるのは、添付仕様や補足メモが混在しやすいため。

## 4. factsheet テンプレート

各 factsheet は対象業務・目的、利用者・ロール、Dataverse テーブル・主要列・マスタ・リレーション候補、UI・チャネル要件、Power Automate の自動化要件、Copilot Studio / AI Builder の利用余地、外部連携、セキュリティ・権限・監査、未確定事項を整理する。UI は Teams / Microsoft 365 Copilot を初期候補とし、画面が必要なら Canvas App を基本案にする。Canvas App で難しい場合に Code Apps / Model-Driven Apps を代替案とし、実現性・ライセンス・費用を確認する。選定は [architecture](../../architecture/SKILL.md) に引き継ぐ。

各 factsheet は最低限次の構造にする。

```markdown
# {タイトル} factsheet

## 1. Source

- File:
- Relative path:
- Converted at:

## 2. Power Platform requirement summary

### Source facts and source locations

### Open questions and proposal hypotheses (not confirmed facts)

### Business objective

### Users / roles

### Dataverse tables

### Main columns / master data

### UI / app requirements

### Automations

### Agent / AI opportunities

### External integrations

### Security / compliance

### Open questions

## 3. Extracted markdown
```

## 5. document.md テンプレート

対象文書一覧と文書間の重複・差分・矛盾、共通業務フロー、Power Platform 全体構成の初期案、Phase 0 でユーザー確認が必要な論点を含める。

```markdown
# Power Platform requirements document

## 1. Conversion summary

## 2. Source documents

## 3. Cross-document requirements summary

### Source facts, open questions, and proposal hypotheses

### Business scope

### Users / roles

### Dataverse design candidates

### App design candidates

### Automation candidates

### Agent / AI candidates

### Integration candidates

### Risks / open questions

## 4. Factsheet index
```

## 6. 要件整理ルール

- **推測で補完しない**
- 文書間で表現が違う場合は `差分あり` と記録する
- Power Platform 用語に正規化する
  - 業務データ → Dataverse テーブル候補
  - 入力 / 一覧 / ダッシュボード → App/UI 要件
  - 通知 / 承認 / 定期処理 → Power Automate
  - 対話 / 検索 / 要約 → Copilot Studio / AI Builder
- 画面名・帳票名・マスタ名・外部システム名はそのまま残す

## 7. MarkItDown を使う理由

- PDF / Office 系ファイルを markdown に寄せて扱える
- 見出し・箇条書き・表の構造を比較的保ちやすい
- 後段の LLM 要約や requirements 整理に渡しやすい

## 8. 限界と補完方針

- スキャン PDF や画像中心の資料は抽出精度が落ちる
- 複雑な表は崩れることがある
- 図そのものの意味は取りきれないため、図番号やキャプションを優先して残す
- 必要に応じて Power Automate + OneDrive PDF 変換、または AI Builder の document input を組み合わせる
