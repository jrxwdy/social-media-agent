import { cn } from "@/lib/utils";
import { PLATFORM_META, type Platform } from "@/lib/mock-data";
import { PlatformIcon } from "@/components/platform-icon";
import { Check, Clock, Edit3, X, Trash2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";

export interface PostCardProps {
  id: string;
  content: string;
  platform: Platform;
  scheduledAt: string;
  format: string;
  variant?: "calendar" | "queue";
  onApprove?: (id: string) => void;
  onEdit?: (id: string) => void;
  onReject?: (id: string) => void;
}

function formatTime(iso: string): string {
  return new Date(iso).toLocaleTimeString("en-US", {
    hour: "numeric",
    minute: "2-digit",
    hour12: true,
  });
}

export function PostCard({
  id,
  content,
  platform,
  scheduledAt,
  format,
  variant = "calendar",
  onApprove,
  onEdit,
  onReject,
}: PostCardProps) {
  if (variant === "queue") {
    return (
      <div className="group rounded-xl border border-border bg-card p-4 transition-all hover:shadow-sm">
        <div className="flex items-start justify-between gap-3">
          <div className="flex items-center gap-2">
            <span
              className={cn(
                "inline-flex h-8 w-8 items-center justify-center rounded-lg",
                PLATFORM_META[platform].bgColor
              )}
            >
              <PlatformIcon platform={platform} />
            </span>
            <div>
              <p className="text-xs font-medium text-muted-foreground">
                {formatTime(scheduledAt)}
              </p>
              <p className="text-[11px] text-muted-foreground/70">
                {new Date(scheduledAt).toLocaleDateString("en-US", {
                  month: "short",
                  day: "numeric",
                })}
              </p>
            </div>
          </div>
          <Badge variant="secondary" className="capitalize">
            {format}
          </Badge>
        </div>

        <p className="mt-3 line-clamp-3 text-sm leading-relaxed text-foreground">
          {content}
        </p>

        <div className="mt-4 flex items-center gap-2">
          <Button
            size="sm"
            className="bg-emerald-600 text-white hover:bg-emerald-700"
            onClick={() => onApprove?.(id)}
          >
            <Check className="size-3.5" />
            Approve
          </Button>
          <Button
            size="sm"
            variant="outline"
            onClick={() => onEdit?.(id)}
          >
            <Edit3 className="size-3.5" />
            Edit
          </Button>
          <Button
            size="sm"
            variant="destructive"
            onClick={() => onReject?.(id)}
          >
            <X className="size-3.5" />
            Reject
          </Button>
        </div>
      </div>
    );
  }

  // Calendar variant — compact
  return (
    <button
      onClick={() => onEdit?.(id)}
      className="group w-full rounded-xl border border-border bg-card p-3 text-left transition-all hover:shadow-sm hover:border-foreground/20"
    >
      <div className="flex items-center gap-2">
        <span
          className={cn(
            "inline-flex h-6 w-6 shrink-0 items-center justify-center rounded-md",
            PLATFORM_META[platform].bgColor
          )}
        >
          <PlatformIcon platform={platform} className="size-3" />
        </span>
        <span className="flex items-center gap-1 text-xs font-medium text-muted-foreground">
          <Clock className="size-3" />
          {formatTime(scheduledAt)}
        </span>
        <Badge variant="outline" className="ml-auto text-[10px] capitalize">
          {format}
        </Badge>
      </div>
      <p className="mt-2 line-clamp-2 text-xs leading-relaxed text-foreground/80">
        {content}
      </p>
    </button>
  );
}
