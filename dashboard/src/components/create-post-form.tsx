"use client";

import { useState } from "react";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { PlatformIcon } from "@/components/platform-icon";
import { Sparkles, Send, Loader2 } from "lucide-react";
import {
  PLATFORM_META,
  FORMAT_META,
  type Platform,
  type PostFormat,
} from "@/lib/mock-data";
import { generateIdeas } from "@/lib/api";

const ALL_PLATFORMS: Platform[] = [
  "linkedin",
  "instagram",
  "facebook",
  "tiktok",
  "x",
];
const ALL_FORMATS: PostFormat[] = ["text", "carousel", "reel", "video", "thread"];

interface CreatePostFormProps {
  onCreate?: (post: {
    content: string;
    platforms: Platform[];
    format: PostFormat;
    scheduledAt: string;
  }) => void;
  className?: string;
}

export function CreatePostForm({ onCreate, className }: CreatePostFormProps) {
  const [content, setContent] = useState("");
  const [selectedPlatforms, setSelectedPlatforms] = useState<Platform[]>([
    "linkedin",
  ]);
  const [format, setFormat] = useState<PostFormat>("text");
  const [scheduledAt, setScheduledAt] = useState<string>("");
  const [ideas, setIdeas] = useState<string[]>([]);
  const [generating, setGenerating] = useState(false);
  const [submitting, setSubmitting] = useState(false);

  const togglePlatform = (p: Platform) => {
    setSelectedPlatforms((prev) =>
      prev.includes(p) ? prev.filter((x) => x !== p) : [...prev, p]
    );
  };

  const handleGenerate = async () => {
    setGenerating(true);
    try {
      const prompt = content.trim() || "content marketing";
      const result = await generateIdeas(prompt);
      setIdeas(result);
    } finally {
      setGenerating(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!content.trim() || selectedPlatforms.length === 0) return;
    setSubmitting(true);
    try {
      const iso = scheduledAt
        ? new Date(scheduledAt).toISOString()
        : new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString();
      onCreate?.({
        content,
        platforms: selectedPlatforms,
        format,
        scheduledAt: iso,
      });
      // Reset
      setContent("");
      setSelectedPlatforms(["linkedin"]);
      setFormat("text");
      setScheduledAt("");
      setIdeas([]);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className={cn("w-full", className)}>
      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Content */}
        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <Label htmlFor="content" className="text-sm font-medium">
              Post Content
            </Label>
            <span className="text-xs text-muted-foreground">
              {content.length} chars
            </span>
          </div>
          <Textarea
            id="content"
            value={content}
            onChange={(e) => setContent(e.target.value)}
            placeholder="Write your post or generate ideas with AI..."
            rows={5}
            className="resize-none"
          />
        </div>

        {/* Generate Ideas */}
        <div className="space-y-2">
          <Button
            type="button"
            variant="outline"
            onClick={handleGenerate}
            disabled={generating}
            className="w-full"
          >
            {generating ? (
              <Loader2 className="size-4 animate-spin" />
            ) : (
              <Sparkles className="size-4" />
            )}
            {generating ? "Generating ideas..." : "Generate Ideas with AI"}
          </Button>
          {ideas.length > 0 && (
            <div className="space-y-1.5 rounded-xl border border-border bg-muted/30 p-3">
              <p className="text-xs font-medium text-muted-foreground">
                AI Suggestions — click to use:
              </p>
              {ideas.map((idea, i) => (
                <button
                  key={i}
                  type="button"
                  onClick={() => {
                    setContent(idea);
                    setIdeas([]);
                  }}
                  className="block w-full rounded-lg px-3 py-2 text-left text-sm text-foreground transition-colors hover:bg-muted"
                >
                  {idea}
                </button>
              ))}
            </div>
          )}
        </div>

        <div className="grid gap-6 sm:grid-cols-2">
          {/* Platforms */}
          <div className="space-y-2">
            <Label className="text-sm font-medium">Platforms</Label>
            <div className="flex flex-wrap gap-2">
              {ALL_PLATFORMS.map((p) => {
                const meta = PLATFORM_META[p];
                const active = selectedPlatforms.includes(p);
                return (
                  <button
                    key={p}
                    type="button"
                    onClick={() => togglePlatform(p)}
                    className={cn(
                      "inline-flex h-9 items-center gap-1.5 rounded-full border px-3 text-sm font-medium transition-all",
                      active
                        ? cn("border-transparent", meta.bgColor, meta.color)
                        : "border-border text-muted-foreground hover:border-foreground/20"
                    )}
                  >
                    <PlatformIcon platform={p} className="size-3.5" />
                    {meta.label}
                  </button>
                );
              })}
            </div>
          </div>

          {/* Format */}
          <div className="space-y-2">
            <Label className="text-sm font-medium">Format</Label>
            <Select
              value={format}
              onValueChange={(v) => v && setFormat(v as PostFormat)}
            >
              <SelectTrigger className="w-full">
                <SelectValue>
                  {(v: string) => FORMAT_META[v as PostFormat]?.label ?? "Select format"}
                </SelectValue>
              </SelectTrigger>
              <SelectContent>
                {ALL_FORMATS.map((f) => (
                  <SelectItem key={f} value={f}>
                    {FORMAT_META[f].label}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
        </div>

        {/* Schedule */}
        <div className="space-y-2">
          <Label htmlFor="schedule" className="text-sm font-medium">
            Schedule Date & Time
          </Label>
          <Input
            id="schedule"
            type="datetime-local"
            value={scheduledAt}
            onChange={(e) => setScheduledAt(e.target.value)}
          />
        </div>

        {/* Submit */}
        <div className="flex items-center justify-end gap-3">
          <Button type="button" variant="ghost" onClick={() => setIdeas([])}>
            Clear
          </Button>
          <Button
            type="submit"
            disabled={!content.trim() || selectedPlatforms.length === 0 || submitting}
          >
            {submitting ? (
              <Loader2 className="size-4 animate-spin" />
            ) : (
              <Send className="size-4" />
            )}
            Add to Queue
          </Button>
        </div>
      </form>
    </div>
  );
}
