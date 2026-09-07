import type { TopPost } from "@/lib/mock-data";
import { PlatformIcon } from "@/components/platform-icon";
import { PLATFORM_META } from "@/lib/mock-data";
import { cn } from "@/lib/utils";

interface TopPostsListProps {
  posts: TopPost[];
  className?: string;
}

export function TopPostsList({ posts, className }: TopPostsListProps) {
  const maxEngagement = Math.max(...posts.map((p) => p.engagement), 1);

  return (
    <div className={cn("space-y-1", className)}>
      {posts.map((post, i) => {
        const meta = PLATFORM_META[post.platform];
        const widthPct = (post.engagement / maxEngagement) * 100;
        return (
          <div
            key={post.id}
            className="group flex items-start gap-3 rounded-lg p-2 transition-colors hover:bg-muted/50"
          >
            <span className="mt-0.5 w-5 text-sm font-semibold text-muted-foreground/60">
              {i + 1}
            </span>
            <span
              className={cn(
                "mt-0.5 inline-flex h-7 w-7 shrink-0 items-center justify-center rounded-lg",
                meta.bgColor
              )}
            >
              <PlatformIcon platform={post.platform} className="size-3.5" />
            </span>
            <div className="min-w-0 flex-1">
              <p className="line-clamp-1 text-sm text-foreground">{post.content}</p>
              <div className="mt-1 flex items-center gap-3 text-xs text-muted-foreground">
                <span>{post.impressions.toLocaleString()} impressions</span>
                <span className="flex items-center gap-1">
                  <span className="font-medium text-foreground">
                    {post.engagement.toLocaleString()}
                  </span>
                  engagement
                </span>
              </div>
              <div className="mt-1.5 h-1 w-full overflow-hidden rounded-full bg-muted">
                <div
                  className={cn("h-full rounded-full", meta.bgColor)}
                  style={{ width: `${widthPct}%`, backgroundColor: meta.color.replace("text-[", "").replace("]", "") }}
                />
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
}
