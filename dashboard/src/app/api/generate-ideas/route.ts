import { NextResponse } from "next/server";

export async function POST(request: Request) {
  const body = await request.json().catch(() => ({}));
  const prompt = body.prompt ?? "content marketing";
  // Placeholder — wire to real AI backend later
  return NextResponse.json({
    ideas: [
      `5 lessons from ${prompt} that your audience won't see coming`,
      `The hidden cost of ignoring ${prompt} in 2026`,
      `Why ${prompt} is harder than everyone says (and how to fix it)`,
      `I spent 30 days studying ${prompt}. Here's what changed my mind.`,
      `${prompt}: the underrated strategy your competitors are missing`,
    ],
  });
}
