import { StarterPage } from "@/components/starter-page";

export default function AssetsPage() {
  return (
    <StarterPage
      eyebrow="Assets"
      title="IT 資産管理の雛形"
      description="資産台帳は lookup、choice、所有者、棚卸し状態などの設計が先に必要です。このテンプレートでは、Dataverse モデル生成前でも安全に差し替えられる画面だけを残しています。"
      checklist={[
        "資産テーブル、カテゴリ、配置場所などのリレーションを定義する",
        "data source 生成後に一覧・編集 hook を追加する",
        "必要ならこのルートにテーブル、フォーム、棚卸し導線を実装する",
      ]}
      actions={[
        { label: "ダッシュボードへ戻る", to: "/dashboard" },
        { label: "カンバン画面の雛形を見る", to: "/kanban" },
      ]}
    />
  );
}
