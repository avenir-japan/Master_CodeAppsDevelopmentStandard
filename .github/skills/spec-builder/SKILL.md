---
name: spec-builder
description: "M365 Copilot・Copilot Cowork・VS Code GitHub Copilot から対話で要件を整理し、案件に必要な SPEC.md と開発入力ファイルを作成する。Office・画像資料がある場合は任意の変換工程も扱う。"
category: ai
argument-hint: "[省略可: 変換する資料のパス — 変換時の既定は spec/input/]"
user-invocable: true
triggers:
  - "要件ディスカバリー"
  - "要件整理"
  - "SPEC.md 作成"
  - "anthropics/skills"
  - "仕様書作成"
  - "仕様書変換"
  - "仕様書を markdown にしたい"
  - "PDF を markdown"
  - "PowerPoint を markdown"
  - "Excel を markdown"
  - "requirements markdown"
  - "spec/input"
  - "画像をOCR"
---

# 仕様書作成スキル

## 共通の入口

依頼の主目的で入口を選ぶ。資料変換と要件確定の両方が必要なら、変換結果を入力として対話で確認する。

| 主目的 | 使用するスキル・方法 | 出力と位置づけ |
|---|---|---|
| 対話で案件の要件・未決事項を整理する | `spec-builder`（必要時のみ anthropics/skills・agent-ocr で資料変換） | 確認状態を明示した `SPEC.md` と必要な開発入力。変換時の 5 文書は下書き |
| 資料を先に Markdown 化して横断整理する | [spec-to-markdown](../spec-to-markdown/SKILL.md)（MarkItDown、精度不足時は OCR 等を併用） | `factsheets/*.md` と `document.md`。確定した開発入力ではない |

1. M365 Copilot・Copilot Cowork・VS Code GitHub Copilot のいずれから始めても、**質問する前に**[要件ディスカバリー](references/requirements-discovery.md) に従い、対象資料と会話を読み、目的・制約・承認状態と未決事項を整理する。必要なら Office・画像資料を変換するが、変換結果は確定要件としない。
2. **SPEC 初稿の前に**、案件に関係する [architecture](../architecture/SKILL.md)・[standard](../standard/SKILL.md)・採用候補の個別スキルを必要な範囲で参照する。代表入力・期待出力・制約から技術的な論点を先回りして抽出し、[初稿前・提示前の点検](references/requirements-discovery.md#step-4-開発入力を作成する)で入出力、構成、受入、権限、引き渡しを照合する。人にしか決められない事項は未決として担当・影響・確認時期を残し、回答待ちで初稿を止めない。
3. 案件固有の `SPEC.md` を中心に作成し、詳細文書は必要な場合だけ分割する。処理ロジック・起動／制御経路・製品機能の比較と判断状態は、**初稿から** [architecture の設計判断](../architecture/SKILL.md#設計提案の進め方)を適用し、採用未確定の方式と理由・次の確認を残す。本文は[要件ディスカバリーの記述方針](references/requirements-discovery.md#step-4-開発入力を作成する)に沿って見出し・箇条書き・表で整理する。単一文書の案件に索引や固定の文書セットを要求しない。
   エージェント案件は、仕様書の完成前にオリジナルアイコンを作成する。
   選定・保存・`SPEC.md` への記録は[要件ディスカバリー](references/requirements-discovery.md#step-3-作成するファイルを決める)に従う。クラウド登録は構築時に行う。
4. M365 Copilot・Copilot Cowork で作成した確認状態付き Markdown は人が案件リポジトリへ配置する。VS Code GitHub Copilot は案件リポジトリへ直接作成できる。

Office・画像などの元資料を変換する必要がある場合に限り、以下の変換フローを利用する。MarkItDown による factsheet・全体文書が主目的なら [spec-to-markdown](../spec-to-markdown/SKILL.md) を選ぶ。変換中の staging と `spec/output/docs/` は確定した案件の開発入力とは区別し、出典・確認状態を確かめて必要なファイルへ統合する。

## 任意: 資料変換フロー

Office ドキュメント（PDF / PowerPoint / Excel / Word など）は **anthropics/skills** で読み取り、
画像ファイル（PNG/JPG 等）は **agent-ocr** で OCR する。このフローが作る 5 文書は変換用の出力であり、全案件に要求する開発入力ファイルの構成ではない。


## 変換ルートの基本フロー

1. `scripts/convert_documents.py` で `spec/input/`（引数なしの既定）または `--input` の資料を走査し、`spec/output/staging/` にファイル単位の下書きを作る。入力が空なら候補を確認し、元資料は移動・削除しない。
2. 画像は `pending_ocr.json` を使って agent-ocr、画像以外は `pending_skills.json` を使って anthropics/skills で本文を抽出する。**manifest と仮の staging だけでは抽出未完了**として報告する。
3. `conversion-checklist.json` で未完了・更新分を確認し、staging を補完して `spec/output/docs/` の 5 文書に統合する。情報不足は `要確認` とする。
4. 変換成果物から確認済みの内容だけを、[要件ディスカバリー](references/requirements-discovery.md) で作成する `SPEC.md` 等の案件の開発入力へ反映する。変換先を確定要件の正本にしない。

入出力パス、オプション、manifest、再処理条件は[変換ガイド](references/conversion-guide.md)を参照する。

## 実行例

```bash
cd .github/skills/spec-builder/scripts
python convert_documents.py
```

```powershell
cd .github\skills\spec-builder\scripts
powershell -ExecutionPolicy Bypass -File run_windows.ps1
```

## 参照

- [変換ガイド](references/conversion-guide.md)
- [architecture スキル](../architecture/SKILL.md) — 全体構成・コンポーネント選定の正（design-requirements / UI・AI 連携要件はこちらを優先して参照）
