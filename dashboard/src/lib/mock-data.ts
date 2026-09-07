export type Platform =
  | "instagram"
  | "facebook"
  | "tiktok"
  | "x";

export type PostFormat =
  | "text"
  | "carousel"
  | "reel"
  | "video"
  | "thread";

export type PostStatus = "scheduled" | "queued" | "approved" | "rejected" | "draft";

export interface Post {
  id: string;
  content: string;
  platform: Platform;
  format: PostFormat;
  status: PostStatus;
  scheduledAt: string; // ISO string
  createdAt: string;
  hashtags?: string[];
  engagement?: {
    likes: number;
    comments: number;
    shares: number;
    impressions: number;
  };
}

export interface Metric {
  label: string;
  value: string;
  change: number; // percent
  trend: "up" | "down" | "flat";
}

export interface PlatformEngagement {
  platform: Platform;
  engagement: number; // 0-100 scale for bar chart
  value: string;
}

export interface TopPost {
  id: string;
  content: string;
  platform: Platform;
  engagement: number;
  impressions: number;
}

export const PLATFORM_META: Record<
  Platform,
  { label: string; color: string; bgColor: string }
> = {
  instagram: { label: "Instagram", color: "text-[#e1306c]", bgColor: "bg-[#e1306c]/10" },
  facebook: { label: "Facebook", color: "text-[#1877f2]", bgColor: "bg-[#1877f2]/10" },
  tiktok: { label: "TikTok", color: "text-[#111827]", bgColor: "bg-[#111827]/10" },
  x: { label: "X", color: "text-[#111827]", bgColor: "bg-[#111827]/10" },
};

export const FORMAT_META: Record<PostFormat, { label: string }> = {
  text: { label: "Text" },
  carousel: { label: "Carousel" },
  reel: { label: "Reel" },
  video: { label: "Video" },
  thread: { label: "Thread" },
};

// Helper to create ISO strings relative to now
function daysFromNow(days: number, hour = 9, minute = 0): string {
  const d = new Date();
  d.setDate(d.getDate() + days);
  d.setHours(hour, minute, 0, 0);
  return d.toISOString();
}

export const MOCK_POSTS: Post[] = [
  {
    id: "p1",
    content:
      "Just shipped a new feature that reduces inference latency by 40%. Here's what we learned about batching requests efficiently 🧵",
    platform: "x",
    format: "thread",
    status: "scheduled",
    scheduledAt: daysFromNow(0, 14, 0),
    createdAt: daysFromNow(-2, 10, 0),
    hashtags: ["#AI", "#engineering"],
    engagement: { likes: 342, comments: 56, shares: 89, impressions: 12400 },
  },
  {
    id: "p2",
    content:
      "Behind the scenes of our latest product shoot 📸 Sometimes the best ideas come from the simplest setups.",
    platform: "instagram",
    format: "carousel",
    status: "scheduled",
    scheduledAt: daysFromNow(0, 17, 30),
    createdAt: daysFromNow(-3, 9, 0),
    hashtags: ["#bts", "#product"],
    engagement: { likes: 1200, comments: 78, shares: 23, impressions: 18500 },
  },
  {
    id: "p3",
    content:
      "AI is not replacing creators — it's amplifying them. The best content in 2026 will be human ideas, AI-powered execution.",
    platform: "x",
    format: "text",
    status: "scheduled",
    scheduledAt: daysFromNow(1, 9, 0),
    createdAt: daysFromNow(-1, 15, 0),
    hashtags: ["#AI", "#creators"],
    engagement: { likes: 890, comments: 120, shares: 210, impressions: 42000 },
  },
  {
    id: "p4",
    content:
      "How we built a 10x faster pipeline for content generation — a deep dive into our architecture and the trade-offs we made.",
    platform: "instagram",
    format: "video",
    status: "scheduled",
    scheduledAt: daysFromNow(2, 11, 0),
    createdAt: daysFromNow(-1, 11, 0),
    hashtags: ["#engineering", "#content"],
    engagement: { likes: 521, comments: 43, shares: 67, impressions: 9800 },
  },
  {
    id: "p5",
    content:
      "POV: When the AI generates the perfect caption on the first try ✨",
    platform: "tiktok",
    format: "reel",
    status: "scheduled",
    scheduledAt: daysFromNow(3, 18, 0),
    createdAt: daysFromNow(-1, 16, 0),
    hashtags: ["#pov", "#ai", "#contentcreator"],
    engagement: { likes: 3200, comments: 180, shares: 440, impressions: 88000 },
  },
  {
    id: "p6",
    content:
      "Our community hit 50K this week 🎉 Thank you for being part of this journey. Here's what's coming next.",
    platform: "facebook",
    format: "text",
    status: "scheduled",
    scheduledAt: daysFromNow(4, 10, 0),
    createdAt: daysFromNow(-2, 12, 0),
    hashtags: ["#community", "#milestone"],
    engagement: { likes: 670, comments: 92, shares: 31, impressions: 15600 },
  },
  {
    id: "p7",
    content:
      "5 lessons from scaling our content operations to 200+ posts/month without burning out the team. Thread 🧵",
    platform: "x",
    format: "thread",
    status: "scheduled",
    scheduledAt: daysFromNow(5, 13, 0),
    createdAt: daysFromNow(-1, 14, 0),
    hashtags: ["#scaling", "#content"],
    engagement: { likes: 670, comments: 89, shares: 145, impressions: 31000 },
  },
  {
    id: "p8",
    content:
      "The future of content marketing is not more content — it's better content. Quality over quantity, every time.",
    platform: "instagram",
    format: "text",
    status: "scheduled",
    scheduledAt: daysFromNow(6, 15, 0),
    createdAt: daysFromNow(-1, 13, 0),
    hashtags: ["#content", "#marketing"],
    engagement: { likes: 423, comments: 67, shares: 78, impressions: 14200 },
  },
  // Queued — need approval
  {
    id: "q1",
    content:
      "Excited to announce our partnership with leading AI researchers to bring you smarter content tools. This is just the beginning 🚀",
    platform: "instagram",
    format: "text",
    status: "queued",
    scheduledAt: daysFromNow(2, 12, 0),
    createdAt: daysFromNow(-1, 9, 0),
    hashtags: ["#partnership", "#AI"],
  },
  {
    id: "q2",
    content:
      "Wait for it... 🤯 The new carousel feature just dropped and it's a game-changer for engagement.",
    platform: "instagram",
    format: "carousel",
    status: "queued",
    scheduledAt: daysFromNow(3, 16, 0),
    createdAt: daysFromNow(-1, 10, 0),
    hashtags: ["#newfeature", "#carousel"],
  },
  {
    id: "q3",
    content:
      "Breaking down the top 3 AI content trends for Q4 2026. Which one are you betting on? 📊",
    platform: "x",
    format: "thread",
    status: "queued",
    scheduledAt: daysFromNow(1, 14, 0),
    createdAt: daysFromNow(-1, 11, 0),
    hashtags: ["#AI", "#trends"],
  },
  {
    id: "q4",
    content:
      "Day in the life of a content creator using AI tools to 10x their output 🎬 #creatorlife",
    platform: "tiktok",
    format: "reel",
    status: "queued",
    scheduledAt: daysFromNow(4, 19, 0),
    createdAt: daysFromNow(-1, 17, 0),
    hashtags: ["#creatorlife", "#ai", "#dayinthelife"],
  },
  {
    id: "q5",
    content:
      "We're hiring! Looking for a creative content strategist to join our team. Remote-friendly, competitive comp, great people.",
    platform: "facebook",
    format: "text",
    status: "queued",
    scheduledAt: daysFromNow(5, 9, 0),
    createdAt: daysFromNow(-1, 8, 0),
    hashtags: ["#hiring", "#contentjobs"],
  },
];

export const MOCK_METRICS: Metric[] = [
  { label: "Total Followers", value: "248.5K", change: 12.4, trend: "up" },
  { label: "Engagement Rate", value: "8.2%", change: 3.1, trend: "up" },
  { label: "Posts This Month", value: "47", change: 18, trend: "up" },
  { label: "AI Citations", value: "1,204", change: -2.3, trend: "down" },
];

export const MOCK_PLATFORM_ENGAGEMENT: PlatformEngagement[] = [
  { platform: "instagram", engagement: 85, value: "85K" },
  { platform: "x", engagement: 64, value: "64K" },
  { platform: "tiktok", engagement: 91, value: "91K" },
  { platform: "facebook", engagement: 38, value: "38K" },
];

export const MOCK_TOP_POSTS: TopPost[] = [
  {
    id: "t1",
    content:
      "AI is not replacing creators — it's amplifying them. The best content in 2026 will be human ideas, AI-powered execution.",
    platform: "x",
    engagement: 1220,
    impressions: 42000,
  },
  {
    id: "t2",
    content:
      "POV: When the AI generates the perfect caption on the first try ✨",
    platform: "tiktok",
    engagement: 3820,
    impressions: 88000,
  },
  {
    id: "t3",
    content:
      "Behind the scenes of our latest product shoot 📸 Sometimes the best ideas come from the simplest setups.",
    platform: "instagram",
    engagement: 1301,
    impressions: 18500,
  },
  {
    id: "t4",
    content:
      "Just shipped a new feature that reduces inference latency by 40%. Here's what we learned about batching requests efficiently 🧵",
    platform: "instagram",
    engagement: 487,
    impressions: 12400,
  },
  {
    id: "t5",
    content:
      "Our community hit 50K this week 🎉 Thank you for being part of this journey.",
    platform: "facebook",
    engagement: 793,
    impressions: 15600,
  },
];
