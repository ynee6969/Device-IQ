import { z } from "zod";

const REDACTED_ENV_VALUE_MARKERS = ["[SENSITIVE]", "[REDACTED]", "REDACTED", "SENSITIVE"];

function normalizeOptionalString(value: unknown) {
  if (typeof value !== "string") {
    return undefined;
  }

  const trimmed = value.trim();
  if (!trimmed) {
    return undefined;
  }

  if (REDACTED_ENV_VALUE_MARKERS.some((marker) => trimmed.includes(marker))) {
    return undefined;
  }

  return trimmed;
}

function normalizeStringWithFallback(value: unknown, fallback: string) {
  const normalized = normalizeOptionalString(value);
  return normalized ?? fallback;
}

function normalizePositiveInteger(value: unknown, fallback: number) {
  const normalized = normalizeOptionalString(value);

  if (normalized === undefined) {
    return fallback;
  }

  const numericValue = Number(normalized);
  return Number.isFinite(numericValue) ? numericValue : fallback;
}

function sanitizeProcessEnv(key: string, fallback?: string) {
  const value = process.env[key];
  const normalized = normalizeOptionalString(value);

  if (normalized === undefined) {
    if (fallback === undefined) {
      delete process.env[key];
      return;
    }

    process.env[key] = fallback;
    return;
  }

  process.env[key] = normalized;
}

const optionalNonEmptyString = z.preprocess(
  (value) => normalizeOptionalString(value),
  z.string().min(1).optional()
);

sanitizeProcessEnv("DATABASE_URL");
sanitizeProcessEnv("AUTH_SECRET");
sanitizeProcessEnv("NEXTAUTH_SECRET");
sanitizeProcessEnv("NEXTAUTH_URL", "http://localhost:3000");
sanitizeProcessEnv("SUPABASE_URL");
sanitizeProcessEnv("SUPABASE_ANON_KEY");
sanitizeProcessEnv("OPENAI_API_KEY");
sanitizeProcessEnv("OPENAI_MODEL", "gpt-4.1-mini");
sanitizeProcessEnv("ANTHROPIC_API_KEY");
sanitizeProcessEnv("ANTHROPIC_MODEL", "claude-3-7-sonnet-latest");
sanitizeProcessEnv("OLLAMA_BASE_URL", "http://localhost:11434");
sanitizeProcessEnv("OLLAMA_MODEL", "llama3.1");
sanitizeProcessEnv("FIRECRAWL_API_KEY");
sanitizeProcessEnv("FIRECRAWL_BASE_URL", "https://api.firecrawl.dev/v1");
sanitizeProcessEnv("APP_URL", "http://localhost:3000");
sanitizeProcessEnv("BOOTSTRAP_ON_STARTUP", "false");
sanitizeProcessEnv("ENRICHMENT_STALENESS_DAYS", "30");
sanitizeProcessEnv("MAX_ENRICHMENT_BATCH", "5");

const envSchema = z.object({
  // Vercel exposes an unset or redacted environment variable as an empty or
  // masked placeholder. Treat those as absent so optional integrations do not
  // fail the production build.
  DATABASE_URL: optionalNonEmptyString,
  AUTH_SECRET: optionalNonEmptyString,
  NEXTAUTH_SECRET: optionalNonEmptyString,
  NEXTAUTH_URL: optionalNonEmptyString,
  SUPABASE_URL: optionalNonEmptyString,
  SUPABASE_ANON_KEY: optionalNonEmptyString,
  OPENAI_API_KEY: optionalNonEmptyString,
  OPENAI_MODEL: z.preprocess(
    (value) => normalizeStringWithFallback(value, "gpt-4.1-mini"),
    z.string().default("gpt-4.1-mini")
  ),
  ANTHROPIC_API_KEY: optionalNonEmptyString,
  ANTHROPIC_MODEL: z.preprocess(
    (value) => normalizeStringWithFallback(value, "claude-3-7-sonnet-latest"),
    z.string().default("claude-3-7-sonnet-latest")
  ),
  OLLAMA_BASE_URL: z.preprocess(
    (value) => normalizeStringWithFallback(value, "http://localhost:11434"),
    z.string().default("http://localhost:11434")
  ),
  OLLAMA_MODEL: z.preprocess(
    (value) => normalizeStringWithFallback(value, "llama3.1"),
    z.string().default("llama3.1")
  ),
  FIRECRAWL_API_KEY: optionalNonEmptyString,
  FIRECRAWL_BASE_URL: z.preprocess(
    (value) => normalizeStringWithFallback(value, "https://api.firecrawl.dev/v1"),
    z.string().default("https://api.firecrawl.dev/v1")
  ),
  APP_URL: z.preprocess(
    (value) => normalizeStringWithFallback(value, "http://localhost:3000"),
    z.string().default("http://localhost:3000")
  ),
  BOOTSTRAP_ON_STARTUP: z.preprocess(
    (value) => normalizeStringWithFallback(value, "false"),
    z.string().default("false")
  ),
  ENRICHMENT_STALENESS_DAYS: z.preprocess(
    (value) => normalizePositiveInteger(value, 30),
    z.number().int().finite().default(30)
  ),
  MAX_ENRICHMENT_BATCH: z.preprocess(
    (value) => normalizePositiveInteger(value, 5),
    z.number().int().finite().default(5)
  )
});

export const env = envSchema.parse({
  DATABASE_URL: process.env.DATABASE_URL,
  AUTH_SECRET: process.env.AUTH_SECRET,
  NEXTAUTH_SECRET: process.env.NEXTAUTH_SECRET,
  NEXTAUTH_URL: process.env.NEXTAUTH_URL,
  SUPABASE_URL: process.env.SUPABASE_URL,
  SUPABASE_ANON_KEY: process.env.SUPABASE_ANON_KEY,
  OPENAI_API_KEY: process.env.OPENAI_API_KEY,
  OPENAI_MODEL: process.env.OPENAI_MODEL,
  ANTHROPIC_API_KEY: process.env.ANTHROPIC_API_KEY,
  ANTHROPIC_MODEL: process.env.ANTHROPIC_MODEL,
  OLLAMA_BASE_URL: process.env.OLLAMA_BASE_URL,
  OLLAMA_MODEL: process.env.OLLAMA_MODEL,
  FIRECRAWL_API_KEY: process.env.FIRECRAWL_API_KEY,
  FIRECRAWL_BASE_URL: process.env.FIRECRAWL_BASE_URL,
  APP_URL: process.env.APP_URL ?? process.env.NEXTAUTH_URL,
  BOOTSTRAP_ON_STARTUP:
    process.env.BOOTSTRAP_ON_STARTUP ?? (process.env.DATABASE_URL ? "true" : "false"),
  ENRICHMENT_STALENESS_DAYS: process.env.ENRICHMENT_STALENESS_DAYS,
  MAX_ENRICHMENT_BATCH: process.env.MAX_ENRICHMENT_BATCH
});
