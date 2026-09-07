"use client";

import { cn } from "@/lib/utils";
import {
  CalendarDays,
  ListChecks,
  PenSquare,
  BarChart3,
  Sparkles,
  Menu,
  X,
} from "lucide-react";
import { useState } from "react";

export type ViewId = "calendar" | "queue" | "create" | "analytics";

interface NavItem {
  id: ViewId;
  label: string;
  icon: typeof CalendarDays;
}

const NAV_ITEMS: NavItem[] = [
  { id: "calendar", label: "Calendar", icon: CalendarDays },
  { id: "queue", label: "Queue", icon: ListChecks },
  { id: "create", label: "Create", icon: PenSquare },
  { id: "analytics", label: "Analytics", icon: BarChart3 },
];

interface SidebarProps {
  active: ViewId;
  onNavigate: (view: ViewId) => void;
  queueCount?: number;
}

export function Sidebar({ active, onNavigate, queueCount = 0 }: SidebarProps) {
  const [mobileOpen, setMobileOpen] = useState(false);

  const NavContent = () => (
    <>
      {/* Logo */}
      <div className="flex items-center gap-2.5 px-4 py-5">
        <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-foreground text-background">
          <Sparkles className="size-5" />
        </div>
        <div>
          <p className="text-sm font-semibold tracking-tight">Barry</p>
          <p className="text-[11px] text-muted-foreground">Content Agent</p>
        </div>
      </div>

      {/* Nav */}
      <nav className="flex-1 space-y-1 px-2 py-2">
        <p className="px-3 pb-2 text-[11px] font-medium uppercase tracking-wider text-muted-foreground/60">
          Dashboard
        </p>
        {NAV_ITEMS.map((item) => {
          const Icon = item.icon;
          const isActive = active === item.id;
          return (
            <button
              key={item.id}
              onClick={() => {
                onNavigate(item.id);
                setMobileOpen(false);
              }}
              className={cn(
                "group flex w-full items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-all",
                isActive
                  ? "bg-foreground text-background"
                  : "text-muted-foreground hover:bg-muted hover:text-foreground"
              )}
            >
              <Icon className="size-4 shrink-0" />
              <span className="flex-1 text-left">{item.label}</span>
              {item.id === "queue" && queueCount > 0 && (
                <span
                  className={cn(
                    "inline-flex h-5 min-w-5 items-center justify-center rounded-full px-1.5 text-xs font-semibold",
                    isActive
                      ? "bg-background/20 text-background"
                      : "bg-primary text-primary-foreground"
                  )}
                >
                  {queueCount}
                </span>
              )}
            </button>
          );
        })}
      </nav>

      {/* Footer */}
      <div className="border-t border-border p-3">
        <div className="flex items-center gap-2.5 rounded-lg px-2 py-2">
          <div className="flex h-8 w-8 items-center justify-center rounded-full bg-gradient-to-br from-violet-500 to-pink-500 text-xs font-semibold text-white">
            B
          </div>
          <div className="min-w-0 flex-1">
            <p className="truncate text-sm font-medium">Barry Team</p>
            <p className="truncate text-[11px] text-muted-foreground">Pro Plan</p>
          </div>
        </div>
      </div>
    </>
  );

  return (
    <>
      {/* Mobile toggle */}
      <button
        onClick={() => setMobileOpen(true)}
        className="fixed left-4 top-4 z-30 inline-flex h-9 w-9 items-center justify-center rounded-lg border border-border bg-card text-foreground lg:hidden"
        aria-label="Open menu"
      >
        <Menu className="size-5" />
      </button>

      {/* Mobile overlay */}
      {mobileOpen && (
        <div
          className="fixed inset-0 z-40 bg-black/20 lg:hidden"
          onClick={() => setMobileOpen(false)}
        />
      )}

      {/* Mobile drawer */}
      {mobileOpen && (
        <aside className="fixed left-0 top-0 z-50 flex h-full w-64 flex-col border-r border-border bg-sidebar lg:hidden">
          <button
            onClick={() => setMobileOpen(false)}
            className="absolute right-3 top-4 inline-flex h-8 w-8 items-center justify-center rounded-lg text-muted-foreground hover:bg-muted"
          >
            <X className="size-5" />
          </button>
          <NavContent />
        </aside>
      )}

      {/* Desktop */}
      <aside className="sticky top-0 hidden h-screen w-64 shrink-0 flex-col border-r border-border bg-sidebar lg:flex">
        <NavContent />
      </aside>
    </>
  );
}
