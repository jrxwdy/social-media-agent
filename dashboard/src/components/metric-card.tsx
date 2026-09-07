import { cn } from "@/lib/utils";
import { ArrowUpRight, ArrowDownRight, Minus } from "lucide-react";
import type { Metric } from "@/lib/mock-data";

interface MetricCardProps {
  metric: Metric;
  className?: string;
}

export function MetricCard({ metric, className }: MetricCardProps) {
  const TrendIcon =
    metric.trend === "up" ? ArrowUpRight : metric.trend === "down" ? ArrowDownRight : Minus;
  const trendColor =
    metric.trend === "up"
      ? "text-emerald-600"
      : metric.trend === "down"
        ? "text-rose-600"
        : "text-muted-foreground";

  return (
    <div
      className={cn(
        "rounded-2xl border border-border bg-card p-5 transition-all hover:shadow-sm",
        className
      )}
    >
      <p className="text-sm font-medium text-muted-foreground">{metric.label}</p>
      <div className="mt-2 flex items-baseline gap-2">
        <span className="text-3xl font-semibold tracking-tight text-foreground">
          {metric.value}
        </span>
      </div>
      <div className="mt-2 flex items-center gap-1 text-xs">
        <TrendIcon className={cn("size-3.5", trendColor)} />
        <span className={trendColor}>
          {metric.change > 0 ? "+" : ""}
          {metric.change}%
        </span>
        <span className="text-muted-foreground">vs last month</span>
      </div>
    </div>
  );
}
