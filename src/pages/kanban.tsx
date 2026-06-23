import { StarterPage } from "@/components/starter-page";

export default function KanbanPage() {
  return (
    <StarterPage
      eyebrow="Kanban"
      title="カンバン画面の雛形"
      description="ドラッグ操作を伴う業務ボードは、テーブル設計と状態遷移が固まってから実装するのが安全です。このページはその置き換え先として残しています。"
      checklist={[
        "列に対応する choice または status 定義を決める",
        "一覧取得 hook と更新 API の責務を分ける",
        "必要ならこのルートに dnd-kit ベースの UI を実装する",
      ]}
      actions={[
        { label: "ダッシュボードへ戻る", to: "/dashboard" },
        { label: "インシデント一覧の雛形を見る", to: "/incidents" },
      ]}
    />
  );
}
