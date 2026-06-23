import { Link, useParams } from "react-router-dom";
import { ArrowLeft } from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

export default function IncidentDetailPage() {
  const { id } = useParams();

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between gap-4">
        <div className="space-y-2">
          <p className="text-sm font-medium uppercase tracking-[0.18em] text-primary">
            Incident Detail
          </p>
          <h2 className="text-3xl font-semibold tracking-tight">
            詳細ページの雛形
          </h2>
          <p className="max-w-3xl text-muted-foreground">
            ルート引数は取得できる状態です。Dataverse
            接続後に、ここへ取得処理と編集 UI を追加してください。
          </p>
        </div>
        <Button asChild variant="outline">
          <Link to="/incidents">
            <ArrowLeft className="h-4 w-4" />
            一覧へ戻る
          </Link>
        </Button>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>現在の route parameter</CardTitle>
          <CardDescription>
            画面遷移とルーティング確認のため、URL
            から受け取った値だけを表示しています。
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="rounded-lg border border-dashed p-4 text-sm text-muted-foreground">
            id:{" "}
            <span className="font-medium text-foreground">
              {id ?? "(none)"}
            </span>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
