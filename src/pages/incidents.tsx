import { StarterPage } from "@/components/starter-page";

export default function IncidentListPage() {
  return (
    <StarterPage
      eyebrow="Incidents"
      title="インシデント一覧の雛形"
      description="実データ接続前のプレースホルダーです。要件確定後に一覧取得 hook、検索条件、詳細導線へ差し替える前提で残しています。"
      checklist={[
        "一覧で見せる列と検索条件を整理する",
        "Dataverse モデル生成後に query hook を実装する",
        "一覧行から詳細ルートへ遷移できるように置き換える",
      ]}
      actions={[
        { label: "ダッシュボードへ戻る", to: "/dashboard" },
        { label: "サンプル詳細ページを開く", to: "/incidents/sample" },
      ]}
    />
  );
}
