import {
  MOCK_POSTS,
  MOCK_METRICS,
  MOCK_PLATFORM_ENGAGEMENT,
  MOCK_TOP_POSTS,
  type Post,
  type Metric,
  type PlatformEngagement,
  type TopPost,
  type Platform,
  type PostFormat,
  type PostStatus,
} from "./mock-data";

// Placeholder API functions — these call /api routes that we'll wire to a
// real backend later. For now they return mock data after a simulated delay.

async function delay(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

export async function getPosts(status?: PostStatus): Promise<Post[]> {
  await delay(200);
  const posts = status ? MOCK_POSTS.filter((p) => p.status === status) : MOCK_POSTS;
  // Return a fresh copy so callers can mutate safely
  return posts.map((p) => ({ ...p }));
}

export async function getScheduledPosts(): Promise<Post[]> {
  return getPosts("scheduled");
}

export async function getQueuedPosts(): Promise<Post[]> {
  return getPosts("queued");
}

export async function getMetrics(): Promise<Metric[]> {
  await delay(150);
  return [...MOCK_METRICS];
}

export async function getPlatformEngagement(): Promise<PlatformEngagement[]> {
  await delay(150);
  return [...MOCK_PLATFORM_ENGAGEMENT];
}

export async function getTopPosts(): Promise<TopPost[]> {
  await delay(150);
  return [...MOCK_TOP_POSTS];
}

export interface CreatePostInput {
  content: string;
  platforms: Platform[];
  format: PostFormat;
  scheduledAt: string;
}

export async function createPost(input: CreatePostInput): Promise<Post> {
  await delay(300);
  // In the future this will POST to /api/posts
  return {
    id: `post_${Date.now()}`,
    content: input.content,
    platform: input.platforms[0] ?? "linkedin",
    format: input.format,
    status: "queued",
    scheduledAt: input.scheduledAt,
    createdAt: new Date().toISOString(),
  };
}

export async function approvePost(id: string): Promise<{ id: string; status: PostStatus }> {
  await delay(200);
  return { id, status: "approved" };
}

export async function rejectPost(id: string): Promise<{ id: string; status: PostStatus }> {
  await delay(200);
  return { id, status: "rejected" };
}

export async function generateIdeas(prompt: string): Promise<string[]> {
  await delay(600);
  // Placeholder — calls /api/generate-ideas later
  return [
    `5 lessons from ${prompt} that your audience won't see coming`,
    `The hidden cost of ignoring ${prompt} in 2026`,
    `Why ${prompt} is harder than everyone says (and how to fix it)`,
    `I spent 30 days studying ${prompt}. Here's what changed my mind.`,
    `${prompt}: the underrated strategy your competitors are missing`,
  ];
}
