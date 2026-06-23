import { Link } from "react-router-dom";
import { ArrowRight } from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

type StarterAction = {
  label: string;
  to: string;
};

type StarterPageProps = {
  eyebrow: string;
  title: string;
  description: string;
  checklist: string[];
  actions?: StarterAction[];
};

export function StarterPage({
  eyebrow,
  title,
  description,
  checklist,
  actions = [],
}: StarterPageProps) {
  return (
    <div className="space-y-6">
      <section className="space-y-3">
        <p className="text-sm font-medium uppercase tracking-[0.18em] text-primary">
          {eyebrow}
        </p>
        <div className="space-y-2">
          <h2 className="text-3xl font-semibold tracking-tight">{title}</h2>
          <p className="max-w-3xl text-muted-foreground">{description}</p>
        </div>
      </section>

      <div className="grid gap-6 lg:grid-cols-[minmax(0,1.6fr)_minmax(280px,1fr)]">
        <Card>
          <CardHeader>
            <CardTitle>最初に進めること</CardTitle>
            <CardDescription>
              このスターターは Dataverse 未接続でも build できる状態を保ちます。
            </CardDescription>
          </CardHeader>
          <CardContent>
            <ol className="space-y-3 text-sm text-muted-foreground">
              {checklist.map((item, index) => (
                <li key={item} className="flex gap-3">
                  <span className="mt-0.5 inline-flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-primary/10 text-xs font-semibold text-primary">
                    {index + 1}
                  </span>
                  <span>{item}</span>
                </li>
              ))}
            </ol>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>関連ページ</CardTitle>
            <CardDescription>
              画面遷移とレイアウトの確認用に、そのまま開けるページを残しています。
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-3">
            {actions.map((action) => (
              <Button
                key={action.to}
                asChild
                variant="outline"
                className="w-full justify-between"
              >
                <Link to={action.to}>
                  <span>{action.label}</span>
                  <ArrowRight className="h-4 w-4" />
                </Link>
              </Button>
            ))}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
