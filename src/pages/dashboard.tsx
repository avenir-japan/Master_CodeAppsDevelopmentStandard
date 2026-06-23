import { StarterPage } from "@/components/starter-page";

export default function DashboardPage() {
  return (
    <StarterPage
      eyebrow="Dashboard"
      title="Code Apps スターターダッシュボード"
      description="このテンプレートは Dataverse 未接続でも build が通る最小構成です。実案件ではこの画面を起点に、要件に応じた KPI、一覧、検索、導線へ置き換えます。"
      checklist={[
        "architecture スキルで UI 方式を確定する",
        "Dataverse テーブルと接続方式を決めてから data source を追加する",
        "このダッシュボードを案件固有の集計や導線に差し替える",
      ]}
      actions={[
        { label: "インシデント一覧の雛形を見る", to: "/incidents" },
        { label: "カンバン画面の雛形を見る", to: "/kanban" },
        { label: "資産管理画面の雛形を見る", to: "/assets" },
      ]}
    />
  );
}
