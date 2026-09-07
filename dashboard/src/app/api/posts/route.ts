import { NextResponse } from "next/server";
import { MOCK_POSTS } from "@/lib/mock-data";

export async function GET() {
  return NextResponse.json({ posts: MOCK_POSTS });
}

export async function POST(request: Request) {
  const body = await request.json().catch(() => ({}));
  // Placeholder — wire to real backend later
  return NextResponse.json({
    id: `post_${Date.now()}`,
    ...body,
    status: "queued",
  });
}
