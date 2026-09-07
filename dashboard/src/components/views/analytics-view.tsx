"use client";

import { useEffect, useState } from "react";
import { MetricCard } from "@/components/metric-card";
import { SimpleBarChart } from "@/components/simple-bar-chart";
import { TopPostsList } from "@/components/top-posts-list";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { getMetrics, getPlatformEngagement, getTopPosts } from "@/lib/api";
import type { Metric, PlatformEngagement, TopPost } from "@/lib/mock-data";

export function AnalyticsView() {
  const [metrics, setMetrics] = useState<Metric[]>([]);
  const [engagement, setEngagement] = useState<PlatformEngagement[]>([]);
  const [topPosts, setTopPosts] = useState<TopPost[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([getMetrics(), getPlatformEngagement(), getTopPosts()]).then(
      ([m, e, t]) => {
        setMetrics(m);
        setEngagement(e);
        setTopPosts(t);
        setLoading(false);
      }
    );
  }, []);

  if (loading) {
    return (
      <div className="flex h-64 items-center justify-center">
        <p className="text-sm text-muted-foreground">Loading analytics...</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-xl font-semibold tracking-tight">Analytics</h2>
        <p className="text-sm text-muted-foreground">
          Performance overview for the last 30 days.
        </p>
      </div>

      {/* Metric cards */}
      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        {metrics.map((m) => (
          <MetricCard key={m.label} metric={m} />
        ))}
      </div>

      <div className="grid gap-4 lg:grid-cols-5">
        {/* Bar chart */}
        <Card className="lg:col-span-3">
          <CardHeader>
            <CardTitle className="text-base">Engagement by Platform</CardTitle>
            <CardDescription>
              Total engagement across all platforms this month.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <SimpleBarChart data={engagement} />
          </CardContent>
        </Card>

        {/* Top posts */}
        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle className="text-base">Top Posts</CardTitle>
            <CardDescription>
              Highest performing content this month.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <TopPostsList posts={topPosts} />
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
