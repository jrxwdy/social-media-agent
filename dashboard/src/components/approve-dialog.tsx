"use client";

import { useState } from "react";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
  DialogFooter,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { PlatformBadge } from "@/components/platform-icon";
import { Badge } from "@/components/ui/badge";
import type { Post } from "@/lib/mock-data";

interface ApproveDialogProps {
  post: Post | null;
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onApprove?: (id: string) => void;
  onReject?: (id: string) => void;
}

function toDatetimeLocal(iso: string): string {
  const d = new Date(iso);
  const offset = d.getTimezoneOffset() * 60000;
  return new Date(d.getTime() - offset).toISOString().slice(0, 16);
}

export function ApproveDialog({
  post,
  open,
  onOpenChange,
  onApprove,
  onReject,
}: ApproveDialogProps) {
  const [editedContent, setEditedContent] = useState("");
  const [editedTime, setEditedTime] = useState("");

  // Sync state when dialog opens with a new post
  const handleOpenChange = (next: boolean) => {
    if (next && post) {
      setEditedContent(post.content);
      setEditedTime(toDatetimeLocal(post.scheduledAt));
    }
    onOpenChange(next);
  };

  if (!post) return null;

  return (
    <Dialog open={open} onOpenChange={handleOpenChange}>
      <DialogContent className="sm:max-w-lg">
        <DialogHeader>
          <DialogTitle>Review Post</DialogTitle>
          <DialogDescription>
            Review and approve, edit, or reject this queued post.
          </DialogDescription>
        </DialogHeader>

        <div className="space-y-4">
          <div className="flex items-center gap-2">
            <PlatformBadge platform={post.platform} />
            <Badge variant="secondary" className="capitalize">
              {post.format}
            </Badge>
          </div>

          <div className="space-y-1.5">
            <Label htmlFor="post-content">Content</Label>
            <Textarea
              id="post-content"
              value={editedContent}
              onChange={(e) => setEditedContent(e.target.value)}
              rows={5}
              className="resize-none"
            />
          </div>

          <div className="space-y-1.5">
            <Label htmlFor="post-time">Scheduled Time</Label>
            <Input
              id="post-time"
              type="datetime-local"
              value={editedTime}
              onChange={(e) => setEditedTime(e.target.value)}
            />
          </div>
        </div>

        <DialogFooter>
          <Button
            variant="destructive"
            onClick={() => {
              onReject?.(post.id);
              onOpenChange(false);
            }}
          >
            Reject
          </Button>
          <Button
            className="bg-emerald-600 text-white hover:bg-emerald-700"
            onClick={() => {
              onApprove?.(post.id);
              onOpenChange(false);
            }}
          >
            Approve
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
