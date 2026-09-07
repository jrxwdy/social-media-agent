"use client";

import { useEffect, useState } from "react";
import { PostCard } from "@/components/post-card";
import { ApproveDialog } from "@/components/approve-dialog";
import { getQueuedPosts, approvePost, rejectPost } from "@/lib/api";
import type { Post } from "@/lib/mock-data";
import { CheckCircle2 } from "lucide-react";

interface QueueViewProps {
  onEdit?: (id: string) => void;
  onQueueChange?: (count: number) => void;
}

export function QueueView({ onEdit, onQueueChange }: QueueViewProps) {
  const [posts, setPosts] = useState<Post[]>([]);
  const [loading, setLoading] = useState(true);
  const [dialogPost, setDialogPost] = useState<Post | null>(null);
  const [dialogOpen, setDialogOpen] = useState(false);

  useEffect(() => {
    getQueuedPosts().then((p) => {
      setPosts(p);
      onQueueChange?.(p.length);
      setLoading(false);
    });
  }, [onQueueChange]);

  const handleApprove = async (id: string) => {
    await approvePost(id);
    setPosts((prev) => {
      const next = prev.filter((p) => p.id !== id);
      onQueueChange?.(next.length);
      return next;
    });
  };

  const handleReject = async (id: string) => {
    await rejectPost(id);
    setPosts((prev) => {
      const next = prev.filter((p) => p.id !== id);
      onQueueChange?.(next.length);
      return next;
    });
  };

  const handleEdit = (id: string) => {
    const post = posts.find((p) => p.id === id);
    if (post) {
      setDialogPost(post);
      setDialogOpen(true);
      onEdit?.(id);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-xl font-semibold tracking-tight">Queue</h2>
        <p className="text-sm text-muted-foreground">
          {posts.length > 0
            ? `${posts.length} post${posts.length === 1 ? "" : "s"} awaiting approval`
            : "No posts waiting for approval"}
        </p>
      </div>

      {loading ? (
        <div className="flex h-40 items-center justify-center">
          <p className="text-sm text-muted-foreground">Loading queue...</p>
        </div>
      ) : posts.length === 0 ? (
        <div className="flex flex-col items-center justify-center rounded-2xl border border-dashed border-border py-16">
          <div className="flex h-12 w-12 items-center justify-center rounded-full bg-emerald-50">
            <CheckCircle2 className="size-6 text-emerald-600" />
          </div>
          <p className="mt-4 text-sm font-medium">All caught up!</p>
          <p className="mt-1 text-xs text-muted-foreground">
            No posts waiting for approval right now.
          </p>
        </div>
      ) : (
        <div className="grid gap-3 sm:grid-cols-2 xl:grid-cols-3">
          {posts.map((post) => (
            <PostCard
              key={post.id}
              id={post.id}
              content={post.content}
              platform={post.platform}
              scheduledAt={post.scheduledAt}
              format={post.format}
              variant="queue"
              onApprove={handleApprove}
              onEdit={handleEdit}
              onReject={handleReject}
            />
          ))}
        </div>
      )}

      <ApproveDialog
        post={dialogPost}
        open={dialogOpen}
        onOpenChange={setDialogOpen}
        onApprove={handleApprove}
        onReject={handleReject}
      />
    </div>
  );
}
