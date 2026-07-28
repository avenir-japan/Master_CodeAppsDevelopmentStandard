# Canvas App 案件運用テンプレート

このフォルダは、**案件固有の Canvas App 実装運用メモ** を置く場所です。

> [!IMPORTANT]
> ここに置く文書は、M365 Copilot などで先に作成した **設計書の代替ではありません**。
> 要件、画面仕様、データ定義、受入条件の正本は、案件側の設計書を参照してください。

## このフォルダの役割

このフォルダには、設計書と重複しにくい次の情報だけを置きます。

- Canvas App の実装モード
  - MCP + coauthoring
  - Git Integration
  - single app / package
- 実装で参照する実値
  - Designer URL
  - Environment ID
  - App ID
  - Flow 名
  - SharePoint リスト名
  - Data source の参照名
- 実装担当と運用担当
  - 誰が Studio を開くか
  - 誰が connection を追加するか
  - 誰が Save / Publish するか
- 実装再開時に必要な手順
- 設計書からの差分メモ

## 置かないもの

次の内容は、原則として案件の設計書を正本にします。

- 要件全文
- 業務フロー全文
- 画面仕様全文
- データ定義全文
- 受入条件全文

## 最小構成

最小運用では、次の 2 つだけあれば十分です。

1. この README
2. [project-ops.md](project-ops.md)

> [!NOTE]
> このリポジトリ自体を案件ごとに複製する運用を前提に、
> Canvas App の案件運用メモは **`project-ops.md` をそのまま編集して使う**。
> 追加でテンプレートを案件名付きファイルへ複製する運用は既定にしない。

必要であれば、画面別の補足メモや一時的な検証メモだけを、この配下へ追加する。

- 例: `work/canvas-app/screen-layout-notes.md`
- 例: `work/canvas-app/import-fallback-notes.md`

## 使い方

1. M365 Copilot などで作成した設計書のパスを確定する
2. [project-ops.md](project-ops.md) を開く
3. 実装モードと担当者、実値だけ埋める
4. 実装中に判明した差分だけ追記する
5. 再開時は、この README と [project-ops.md](project-ops.md) を先に確認する

## この構成にしている理由

- この repo は案件ごとに複製して使うため、`work/canvas-app/` 配下もその案件専用になる
- そのため、案件運用メモをさらに複製すると二重化しやすい
- `project-ops.md` を固定の正本にすると、再開時の参照先がぶれにくい
- 詳細要件は設計書、実装運用差分は `project-ops.md` と役割分担しやすい

## 参照先

- 共通方針: [../../.github/copilot-instructions.md](../../.github/copilot-instructions.md)
- Canvas App スキル: [../../.github/skills/canvas-app/SKILL.md](../../.github/skills/canvas-app/SKILL.md)
- AI 編集フロー: [../../.github/skills/canvas-app/references/ai-codegen-workflow.md](../../.github/skills/canvas-app/references/ai-codegen-workflow.md)
- Source control 指針: [../../.github/skills/canvas-app/references/source-code-and-git-integration.md](../../.github/skills/canvas-app/references/source-code-and-git-integration.md)
- ALM / 移送指針: [../../.github/skills/canvas-app/references/alm-and-import-options.md](../../.github/skills/canvas-app/references/alm-and-import-options.md)
