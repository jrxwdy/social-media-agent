import type { Post } from "@/lib/mock-data";
import { PostCard } from "@/components/post-card";
import { cn } from "@/lib/utils";

interface CalendarGridProps {
  posts: Post[];
  onEdit?: (id: string) => void;
  className?: string;
}

const DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];

function getWeekDates(weekOffset: number): Date[] {
  const today = new Date();
  const day = today.getDay(); // 0 = Sun
  const mondayOffset = day === 0 ? -6 : 1 - day;
  const monday = new Date(today);
  monday.setDate(today.getDate() + mondayOffset + weekOffset * 7);
  monday.setHours(0, 0, 0, 0);

  const dates: Date[] = [];
  for (let i = 0; i < 7; i++) {
    const d = new Date(monday);
    d.setDate(monday.getDate() + i);
    dates.push(d);
  }
  return dates;
}

function isSameDay(a: Date, b: Date): boolean {
  return (
    a.getFullYear() === b.getFullYear() &&
    a.getMonth() === b.getMonth() &&
    a.getDate() === b.getDate()
  );
}

export function CalendarGrid({ posts, onEdit, className }: CalendarGridProps) {
  const weekDates = getWeekDates(0);
  const today = new Date();

  return (
    <div className={cn("w-full", className)}>
      {/* Day headers */}
      <div className="grid grid-cols-7 gap-2 border-b border-border pb-2">
        {weekDates.map((date, i) => {
          const isToday = isSameDay(date, today);
          return (
            <div key={i} className="flex flex-col items-center gap-1">
              <span className="text-xs font-medium text-muted-foreground">
                {DAYS[i]}
              </span>
              <span
                className={cn(
                  "flex h-7 w-7 items-center justify-center rounded-full text-sm font-semibold",
                  isToday
                    ? "bg-foreground text-background"
                    : "text-foreground"
                )}
              >
                {date.getDate()}
              </span>
            </div>
          );
        })}
      </div>

      {/* Day cells */}
      <div className="mt-2 grid grid-cols-7 gap-2">
        {weekDates.map((date, i) => {
          const dayPosts = posts.filter((p) => {
            const postDate = new Date(p.scheduledAt);
            return isSameDay(postDate, date);
          });
          const isToday = isSameDay(date, today);

          return (
            <div
              key={i}
              className={cn(
                "min-h-[200px] rounded-xl border p-2",
                isToday
                  ? "border-foreground/20 bg-foreground/[0.03]"
                  : "border-border bg-card/50"
              )}
            >
              <div className="space-y-2">
                {dayPosts
                  .sort(
                    (a, b) =>
                      new Date(a.scheduledAt).getTime() -
                      new Date(b.scheduledAt).getTime()
                  )
                  .map((post) => (
                    <PostCard
                      key={post.id}
                      id={post.id}
                      content={post.content}
                      platform={post.platform}
                      scheduledAt={post.scheduledAt}
                      format={post.format}
                      variant="calendar"
                      onEdit={onEdit}
                    />
                  ))}
                {dayPosts.length === 0 && (
                  <div className="flex h-24 items-center justify-center">
                    <span className="text-[11px] text-muted-foreground/40">
                      No posts
                    </span>
                  </div>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
