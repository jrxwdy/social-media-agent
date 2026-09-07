"use client";

import { CreatePostForm } from "@/components/create-post-form";
import type { Platform, PostFormat } from "@/lib/mock-data";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";

interface CreateViewProps {
  onCreate?: (post: {
    content: string;
    platforms: Platform[];
    format: PostFormat;
    scheduledAt: string;
  }) => void;
}

export function CreateView({ onCreate }: CreateViewProps) {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-xl font-semibold tracking-tight">Create Post</h2>
        <p className="text-sm text-muted-foreground">
          Compose a new post and add it to the approval queue.
        </p>
      </div>

      <div className="mx-auto w-full max-w-2xl">
        <Card>
          <CardHeader>
            <CardTitle className="text-base">New Post</CardTitle>
            <CardDescription>
              Write your content, pick platforms, and schedule. Use AI to generate ideas.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <CreatePostForm onCreate={onCreate} />
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
