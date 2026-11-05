---
name: spec-to-markdown
description: "PDF・PowerPoint・Excel などの仕様書を MarkItDown ベースで markdown 化し、Power Platform 開発向け factsheet と document を整理する。"
category: ai
argument-hint: "[任意: input フォルダのパス or ファイルパス]"
user-invocable: true
triggers:
  - "MarkItDown"
  - "仕様書変換"
  - "仕様書を markdown にしたい"
  - "PDF を markdown"
  - "PowerPoint を markdown"
  - "Excel を markdown"
  - "factsheet"
  - "document.md"
  - "requirements markdown"
  - "inputフォルダ"
---

# 仕様書→要件 markdown 変換スキル

PDF・PowerPoint・Excel・Word などの資料を MarkItDown ベースで変換し、Power Platform 開発向けの `factsheets/*.md` と `document.md` に整理する。

- **入口の判断**: 依頼の主目的と成果物の位置づけは [spec-builder の共通の入口](../spec-builder/SKILL.md#共通の入口)を正本とする。
- **変換精度が不足する場合**: OCR 等を併用する。
- **要件確定も必要な場合**: 出典と未決事項を確認して [spec-builder の要件ディスカバリー](../spec-builder/references/requirements-discovery.md) に引き継ぐ。変換成果物を確定した開発入力としない。

## 最初の依頼を簡単にする

このスキルは **引数なしでも開始できる** ようにする。

- 既定入力: `work/spec-to-markdown/input/`
- 既定出力: `work/spec-to-markdown/output/<input-set>-<timestamp>/`
- `--input` / `--output` を指定した場合はそのパスを優先する
- 入力の元資料は読み取り専用として扱い、移動・削除しない

利用例と入力セットの扱いは[変換ガイド](references/conversion-guide.md#2-推奨コマンド)を参照する。

## 目的

出力は **Power Platform 前提の開発要件整理** に寄せる。
単なる全文変換で終わらせず、Dataverse / Code Apps / Power Automate / Copilot Studio / AI Builder の観点で整理する。

## 基本フロー

1. `scripts/convert_documents.py` で既定 input フォルダ、または指定された input パス内の仕様書を markdown 化する
2. 各ファイルごとに `factsheets/*.md` を作る
3. 横断要件を `document.md` にまとめる
4. 不明点・矛盾点・未記載事項は推測で埋めず `要確認` として残す
5. 資料から確認できた事実は出典を示し、未確認事項や改善案は事実と区別した仮説・提案として記録する

## 出力フォルダ構成

```text
{output}/
  raw/                 # MarkItDown の変換結果
  factsheets/          # ファイル単位の factsheet
  document.md          # 全体統合ドキュメント
```

入力セット別の出力命名と固定出力パスの指定は[変換ガイド](references/conversion-guide.md#2-推奨コマンド)を参照する。

## factsheet と document.md の整理

各資料の業務・データ・UI・自動化・AI・権限の候補と未確定事項を factsheet に記録し、文書間の重複・矛盾、共通業務フロー、全体構成の初期案、Phase 0 の確認事項を `document.md` に統合する。項目・テンプレートと UI の選択条件は[変換ガイド](references/conversion-guide.md#4-factsheet-テンプレート)を参照する。

## MarkItDown 方針

- 変換の第一候補は **Microsoft MarkItDown**
- スキャン PDF や画像中心資料で精度不足の場合は、OCR や Power Automate / AI Builder を併用する
- 表や箇条書きは markdown として残し、情報欠落時は factsheet に注記する

## 変換後の次アクション

- 全体構成の判断 → `architecture`
- Dataverse テーブル設計 → `dataverse`
- UI 実装 → `code-apps` または `model-driven-app`
- 自動化 → `power-automate`
- エージェント化 → `copilot-studio`
- AI プロンプト化 → `ai-builder`

## 参照

- [変換ガイド](references/conversion-guide.md)

## 関連スキル

| スキル                                           | 次に読む場面                               |
| ------------------------------------------------ | ------------------------------------------ |
| [architecture](../architecture/SKILL.md)         | factsheet から全体構成と UI 方式を決める   |
| [dataverse](../dataverse/SKILL.md)               | テーブル・列・リレーション候補を具体化する |
| [code-apps](../code-apps/SKILL.md)               | Code Apps で UI 実装に進む                 |
| [model-driven-app](../model-driven-app/SKILL.md) | 標準 CRUD 中心なら MDA に進む              |
| [power-automate](../power-automate/SKILL.md)     | 自動化要件をクラウドフローに落とす         |
| [copilot-studio](../copilot-studio/SKILL.md)     | エージェント化・対話導線に進む             |
| [ai-builder](../ai-builder/SKILL.md)             | 再利用 AI 処理をプロンプト化する           |
