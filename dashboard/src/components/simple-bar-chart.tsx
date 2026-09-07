import type { PlatformEngagement } from "@/lib/mock-data";
import { PLATFORM_META } from "@/lib/mock-data";
import { PlatformIcon } from "@/components/platform-icon";
import { cn } from "@/lib/utils";

interface SimpleBarChartProps {
  data: PlatformEngagement[];
  className?: string;
}

export function SimpleBarChart({ data, className }: SimpleBarChartProps) {
  const maxVal = Math.max(...data.map((d) => d.engagement), 100);

  return (
    <div className={cn("w-full", className)}>
      <div className="flex h-64 items-end justify-between gap-4 px-2">
        {data.map((item) => {
          const heightPct = (item.engagement / maxVal) * 100;
          const meta = PLATFORM_META[item.platform];
          return (
            <div
              key={item.platform}
              className="flex h-full flex-1 flex-col items-center justify-end gap-2"
            >
              <span className="text-xs font-medium text-muted-foreground">
                {item.value}
              </span>
              <div className="relative flex w-full max-w-[48px] flex-1 items-end justify-center">
                <div
                  className={cn(
                    "w-full rounded-t-lg transition-all duration-700 ease-out",
                    meta.bgColor
                  )}
                  style={{
                    height: `${heightPct}%`,
                    minHeight: "8px",
                    backgroundColor: meta.color.replace("text-", "").replace("[", "").replace("]", ""),
                  }}
                >
                  <div
                    className="h-full w-full rounded-t-lg opacity-90"
                    style={{ backgroundColor: "currentColor" }}
                  />
                </div>
              </div>
            </div>
          );
        })}
      </div>
      <div className="mt-3 flex justify-between gap-4 px-2">
        {data.map((item) => (
          <div
            key={item.platform}
            className="flex flex-1 flex-col items-center gap-1"
          >
            <PlatformIcon platform={item.platform} className="size-4" />
            <span className="text-[11px] font-medium text-muted-foreground">
              {PLATFORM_META[item.platform].label}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
