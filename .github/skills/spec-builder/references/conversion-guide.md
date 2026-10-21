# 仕様書 markdown 変換ガイド（anthropics/skills + agent-ocr）

## 1. 何を作るか

このスキルの出力は `spec/` 配下の構成。

```
spec/
├── input/                     # 変換元ドキュメントを置く
├── output/
│   ├── staging/               # ファイル単位 markdown
│   └── docs/                  # 業務要件 / 機能要件 / 設計要件 / テスト要件 + インデックス
│       ├── index.md
│       ├── business-requirements.md
│       ├── functional-requirements.md
│       ├── design-requirements.md
│       └── test-requirements.md
└── .cache/                    # システム内部用
    ├── conversion-checklist.json
    ├── pending_ocr.json
    └── pending_skills.json
```

## 2. 推奨コマンド

まずリポジトリルートで preflight/bootstrap を実行する。

```bash
npm install
# または再実行時
npm run setup
```

### macOS / Linux

```bash
cd .github/skills/spec-builder/scripts
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python convert_documents.py
```

### Windows (PowerShell)

```powershell
cd .github\skills\spec-builder\scripts
powershell -ExecutionPolicy Bypass -File run_windows.ps1
```

## 3. 既定パス

- 入力: `<repo-root>/spec/input/`
- staging: `<repo-root>/spec/output/staging/`
- docs: `<repo-root>/spec/output/docs/`
- checklist: `<repo-root>/spec/.cache/conversion-checklist.json`
- pending JSON: checklist と同じ `spec/.cache/` に自動配置

`spec/input/` に変換対象がない場合、`convert_documents.py` はワークスペース・フォルダ全体をスキャンし、変換候補になりうるファイル（対応拡張子）がないか確認する。見つかった場合は候補一覧を提示するので、元の場所を `--input` で指定するか、必要に応じて `spec/input/` へコピーする。
元資料は移動・削除しない。コピーする場合も元ファイルは保持し、重複する候補は入力パスを指定して区別する。
オプション（checklist のパスを変えると pending JSON も同じディレクトリに移動する）:

```bash
python convert_documents.py \
  --input /absolute/path/to/input \
  --staging /absolute/path/to/staging \
  --docs /absolute/path/to/docs \
  --checklist /absolute/path/to/.cache/conversion-checklist.json
```

## 4. 出力ファイル命名

`staging` の各ファイルは次の命名に統一する。

- `元のファイル名.元の拡張子.MD`
- 例: `要件定義.docx.MD`, `画面設計.xlsx.MD`, `menu.png.MD`

同名衝突時は相対ディレクトリ由来のサフィックスを自動付与する。

## 5. pending manifest

### pending_ocr.json

画像ファイルを agent-ocr で処理するための manifest。

- `source_path`
- `relative_path`
- `staging_markdown_path`
- `sha256`
- `processor` (`agent-ocr`)
- `ocr_prompt_hint`（抽出時の最小指示）

### pending_skills.json

画像以外を anthropics/skills で処理するための manifest。

- `source_path`
- `relative_path`
- `staging_markdown_path`
- `sha256`
- `processor` (`anthropics/skills`)
- `context_hint`（抽出時の観点ヒント — どの要件観点で読み取るかを明示）

## 6. docs の構成

### index.md

- ドキュメント一覧（各 docs へのリンク・役割・主な利用者）
- 処理状況テーブル
- 開発利用フロー（番号付き手順）

### business-requirements.md

- 概要（対象業務・プロジェクト背景・開発段階・目的・検証仮説・スコープと対象外・成功条件）
- ステークホルダー / ロール（表）
- ユーザーストーリー（As a…I want…so that…形式）
- 業務フロー
- 未確定事項 / 要確認事項（表）
- 要件変更履歴（理由を併記）

### functional-requirements.md

- 機能一覧（MoSCoW 優先度・受け入れ条件の表 — 受け入れ条件の正はここ。今回の対象範囲と対象外は business-requirements の判断を反映）
- Dataverse テーブル候補（表）
- UI 要件 / 自動化要件 / AI 連携要件（コンポーネント選定は `.github/skills/architecture/SKILL.md` の判断フローを優先。画面 UI が本当に必要なら Canvas App を基本案とし、Canvas App では要件実現が難しい場合は Code Apps / Model-Driven Apps も代替候補として提案。実現性・ライセンス・費用を確認し、外部ユーザー向けの構成も案件要件と実現可能性で判断）
- 非機能要件（パフォーマンス・セキュリティ・可用性・スケーラビリティ・ユーザビリティの表 — test の非機能テストと区分を一致させる）
- 要件変更履歴（理由を併記）

### design-requirements.md

> ★ 全体構成・コンポーネント選定・構築フェーズは `.github/skills/architecture/SKILL.md` を正とし、
> architecture スキルの判断フロー・設計アウトプットテンプレート（`references/design-patterns.md` §8）で確定した結果を転記する。

- Power Platform 全体構成案（architecture スキルのテンプレート準拠、Mermaid 構成図）
- Phase 0 実現可能性判定（重要経路ごとの判定表または参照先、未確認・不適合への対応、承認者と承認結果）
- 採用した構成・実装範囲と、PoC / MVPで対象外にした本番向け作り込みや後続判断事項
- コンポーネント設計（表 — architecture スキルの「コンポーネント構成」表と整合させる）
- セキュリティ / 権限 / 監査（表）
- 設計上のリスク（影響度・発生確率・対応方針の表）
- Phase 1 確認事項
- 実装タスク分解（タスク・依存・優先度・見積の表 — フェーズ順序は architecture スキルの「構築フェーズ」に沿う）
- 要件変更履歴（理由を併記）

### test-requirements.md

- テスト戦略（今回確認する目的・未検証の範囲を含める。PoC / MVPの結果を本番品質の保証として扱わない）
- テストシナリオ（前提条件・操作手順・期待結果・優先度の表）
- 受け入れ条件（functional の機能 # を参照し確認方法を定義 — 条件本文の正は functional 側、二重管理しない）
- 非機能テスト（合格基準の表 — 区分は functional の非機能要件と一致させる）
- 要件変更履歴（理由を併記）

## 7. conversion-checklist の運用

- 新規ファイルが `spec/input/` に増えたらチェックリストへ追加
- `is_completed=false` のファイルは再処理対象
- 既存ファイルでも `source_sha256` が変わったら再処理対象
- 全件完了時は `spec/output/docs/` を参照して開発を進める

## 8. 処理ルール

- 画像は必ず agent-ocr
- 画像以外は anthropics/skills（`context_hint` を参照して抽出観点を確認）
- 推測で埋めず、情報不足は `要確認`
- OCR 抽出では表を markdown table 化し、判読不能箇所は `[判読不可]` とする

設計案・作成時の説明・現在の入力資料が食い違う場合は、各記述の出所と確定状況を分けて記録する。現行資料の内容を抽出した事実と、採用する仕様が確定したことは同義ではない。判断が変わる矛盾は `要確認` に残し、旧記述を現行の定義として転記しない。差分検索では変更履歴中の言及と現在有効な記述を区別する。

補足: anthropics/skills（Claude）も画像読解は可能だが、この運用では OCR を agent-ocr に固定する。

## 9. staging → docs 統合後の開発フロー

staging が全件完了したら、以下の流れで開発に入る。

1. **要件合意**: `business-requirements.md` の未確定事項を PO / BA と確認し、`要確認` を解消する
2. **優先度合意**: `functional-requirements.md` の MoSCoW 優先度を PO と合意する
3. **設計確定**: `.github/skills/architecture/SKILL.md` の判断フローで全体構成・コンポーネント選定を確定し、結果を `design-requirements.md` に転記して実装タスク分解を確定させる
4. **テスト設計**: `test-requirements.md` の受け入れ条件を `functional-requirements.md` の機能 # と紐付ける
5. **開発着手**: `design-requirements.md` の実装タスク表を元にタスクを割り当てる
6. **変更管理**: 仕様変更時は各 docs の「要件変更履歴」に変更内容と理由を記録する

## 10. 備考

`convert_documents.py` は `spec/output/staging/`・`spec/output/docs/` の土台作成と  
`spec/.cache/` への pending manifest 生成を担当する。  
manifest の解消（agent-ocr / anthropics/skills 実行）後、`spec/output/docs/` を確定版に更新する。
