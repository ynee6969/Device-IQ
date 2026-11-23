import { NextRequest, NextResponse } from "next/server";

import { RateLimitError, enforceRateLimit } from "@/lib/services/rate-limit";
import { PreferenceError } from "@/lib/recommendation/scoring";
import { recommendPhones } from "@/lib/services/recommendations";

export async function POST(request: NextRequest) {
  try {
    enforceRateLimit(
      `recommend:${request.headers.get("x-forwarded-for") ?? "local"}`,
      30,
      60_000
    );

    const body = await request.json();
    const result = await recommendPhones(body);

    return NextResponse.json(result);
  } catch (error) {
    if (error instanceof RateLimitError) {
      return NextResponse.json({ error: error.message }, { status: 429 });
    }

    if (error instanceof PreferenceError || error instanceof SyntaxError) {
      return NextResponse.json({ error: error instanceof SyntaxError ? "Send a valid JSON object." : error.message }, { status: 400 });
    }
    console.error("[recommend]", error);
    return NextResponse.json({ error: "Could not load the catalog. Please try again." }, { status: 503 });
  }
}
