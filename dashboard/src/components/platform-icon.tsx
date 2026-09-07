import type { Platform } from "@/lib/mock-data";
import { PLATFORM_META } from "@/lib/mock-data";
import { cn } from "@/lib/utils";

interface PlatformIconProps {
  platform: Platform;
  className?: string;
}

// Custom brand SVGs — lucide-react removed brand icons in recent versions.
export function PlatformIcon({ platform, className }: PlatformIconProps) {
  const meta = PLATFORM_META[platform];
  const cls = cn("size-4", meta.color, className);

  switch (platform) {
    case "instagram":
      return (
        <svg viewBox="0 0 24 24" fill="currentColor" className={cls} aria-hidden="true">
          <path d="M12 2c2.7 0 3.05.01 4.12.06 1.07.05 1.8.22 2.43.47.66.25 1.22.6 1.77 1.15.55.55.9 1.11 1.15 1.77.25.63.42 1.36.47 2.43.05 1.07.06 1.42.06 4.12s-.01 3.05-.06 4.12c-.05 1.07-.22 1.8-.47 2.43-.25.66-.6 1.22-1.15 1.77-.55.55-1.11.9-1.77 1.15-.63.25-1.36.42-2.43.47-1.07.05-1.42.06-4.12.06s-3.05-.01-4.12-.06c-1.07-.05-1.8-.22-2.43-.47a4.9 4.9 0 01-1.77-1.15 4.9 4.9 0 01-1.15-1.77c-.25-.63-.42-1.36-.47-2.43C2.01 15.05 2 14.7 2 12s.01-3.05.06-4.12c.05-1.07.22-1.8.47-2.43.25-.66.6-1.22 1.15-1.77.55-.55 1.11-.9 1.77-1.15.63-.25 1.36-.42 2.43-.47C8.95 2.01 9.3 2 12 2zm0 1.8c-2.65 0-2.97.01-4.02.06-.96.04-1.48.2-1.83.34-.46.18-.79.39-1.13.74-.35.34-.56.67-.74 1.13-.14.35-.3.87-.34 1.83-.05 1.05-.06 1.37-.06 4.02s.01 2.97.06 4.02c.04.96.2 1.48.34 1.83.18.46.39.79.74 1.13.34.35.67.56 1.13.74.35.14.87.3 1.83.34 1.05.05 1.37.06 4.02.06s2.97-.01 4.02-.06c.96-.04 1.48-.2 1.83-.34.46-.18.79-.39 1.13-.74.35-.34.56-.67.74-1.13.14-.35.3-.87.34-1.83.05-1.05.06-1.37.06-4.02s-.01-2.97-.06-4.02c-.04-.96-.2-1.48-.34-1.83a3.02 3.02 0 00-.74-1.13 3.02 3.02 0 00-1.13-.74c-.35-.14-.87-.3-1.83-.34-1.05-.05-1.37-.06-4.02-.06zm0 3.06a5.14 5.14 0 110 10.28 5.14 5.14 0 010-10.28zm0 1.8a3.34 3.34 0 100 6.68 3.34 3.34 0 000-6.68zm5.34-3.2a1.2 1.2 0 110 2.4 1.2 1.2 0 010-2.4z" />
        </svg>
      );
    case "facebook":
      return (
        <svg viewBox="0 0 24 24" fill="currentColor" className={cls} aria-hidden="true">
          <path d="M24 12.07C24 5.4 18.63 0 12 0S0 5.4 0 12.07c0 6.02 4.39 11.01 10.13 11.93v-8.44H7.08v-3.49h3.05V9.41c0-3.02 1.79-4.69 4.53-4.69 1.31 0 2.69.24 2.69.24v2.97h-1.52c-1.49 0-1.96.93-1.96 1.89v2.25h3.33l-.53 3.49h-2.8v8.44C19.61 23.08 24 18.09 24 12.07z" />
        </svg>
      );
    case "tiktok":
      return (
        <svg viewBox="0 0 24 24" fill="currentColor" className={cls} aria-hidden="true">
          <path d="M19.59 6.69a4.83 4.83 0 01-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 01-5.2 1.73 2.89 2.89 0 012.31-4.67c.3 0 .59.04.87.13V9.4a6.33 6.33 0 00-.87-.06A6.34 6.34 0 105.6 18.34a6.34 6.34 0 006.77 0v.01a6.34 6.34 0 003.2-5.52V8.3a8.16 8.16 0 004.76 1.52V6.36a4.82 4.82 0 01-.74.33z" />
        </svg>
      );
    case "x":
      return (
        <svg viewBox="0 0 24 24" fill="currentColor" className={cls} aria-hidden="true">
          <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.242h-6.66l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.03l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z" />
        </svg>
      );
    default:
      return null;
  }
}

export function PlatformBadge({
  platform,
  className,
}: {
  platform: Platform;
  className?: string;
}) {
  const meta = PLATFORM_META[platform];
  return (
    <span
      className={cn(
        "inline-flex h-6 items-center gap-1.5 rounded-full px-2.5 text-xs font-medium",
        meta.bgColor,
        meta.color,
        className
      )}
    >
      <PlatformIcon platform={platform} className="size-3" />
      {meta.label}
    </span>
  );
}
