"use client";

import { useState, useCallback } from "react";
import { Sidebar, type ViewId } from "@/components/sidebar";
import { CalendarView } from "@/components/views/calendar-view";
import { QueueView } from "@/components/views/queue-view";
import { CreateView } from "@/components/views/create-view";
import { AnalyticsView } from "@/components/views/analytics-view";
import type { Platform, PostFormat } from "@/lib/mock-data";
import { createPost } from "@/lib/api";

export default function Home() {
  const [view, setView] = useState<ViewId>("calendar");
  const [queueCount, setQueueCount] = useState(0);

  const handleNavigate = useCallback((v: ViewId) => setView(v), []);

  const handleEditFromCalendar = useCallback((id: string) => {
    // Switch to queue view to review the post there
    setView("queue");
  }, []);

  const handleCreate = useCallback(
    async (post: {
      content: string;
      platforms: Platform[];
      format: PostFormat;
      scheduledAt: string;
    }) => {
      await createPost(post);
      setQueueCount((c) => c + 1);
      setView("queue");
    },
    []
  );

  return (
    <div className="flex min-h-screen w-full bg-background">
      <Sidebar
        active={view}
        onNavigate={handleNavigate}
        queueCount={queueCount}
      />

      <main className="flex-1 min-w-0">
        <div className="mx-auto max-w-6xl px-4 py-6 sm:px-6 lg:px-8 lg:py-8">
          {view === "calendar" && <CalendarView onEdit={handleEditFromCalendar} />}
          {view === "queue" && (
            <QueueView onQueueChange={setQueueCount} />
          )}
          {view === "create" && <CreateView onCreate={handleCreate} />}
          {view === "analytics" && <AnalyticsView />}
        </div>
      </main>
    </div>
  );
}
