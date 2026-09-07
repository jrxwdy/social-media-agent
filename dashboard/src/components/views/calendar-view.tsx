"use client";

import { useEffect, useState } from "react";
import { CalendarGrid } from "@/components/calendar-grid";
import { getScheduledPosts } from "@/lib/api";
import type { Post } from "@/lib/mock-data";
import { ChevronLeft, ChevronRight } from "lucide-react";
import { Button } from "@/components/ui/button";

interface CalendarViewProps {
  onEdit?: (id: string) => void;
}

export function CalendarView({ onEdit }: CalendarViewProps) {
  const [posts, setPosts] = useState<Post[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getScheduledPosts().then((p) => {
      setPosts(p);
      setLoading(false);
    });
  }, []);

  const today = new Date();
  const weekStart = new Date(today);
  const day = today.getDay();
  weekStart.setDate(today.getDate() - (day === 0 ? 6 : day - 1));
  const weekEnd = new Date(weekStart);
  weekEnd.setDate(weekStart.getDate() + 6);

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h2 className="text-xl font-semibold tracking-tight">Calendar</h2>
          <p className="text-sm text-muted-foreground">
            {weekStart.toLocaleDateString("en-US", { month: "short", day: "numeric" })}
            {" — "}
            {weekEnd.toLocaleDateString("en-US", { month: "short", day: "numeric" })}
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="outline" size="icon-sm" disabled>
            <ChevronLeft className="size-4" />
          </Button>
          <Button variant="outline" size="sm" className="min-w-20">
            This Week
          </Button>
          <Button variant="outline" size="icon-sm" disabled>
            <ChevronRight className="size-4" />
          </Button>
        </div>
      </div>

      {loading ? (
        <div className="flex h-64 items-center justify-center">
          <p className="text-sm text-muted-foreground">Loading calendar...</p>
        </div>
      ) : (
        <CalendarGrid posts={posts} onEdit={onEdit} />
      )}
    </div>
  );
}
