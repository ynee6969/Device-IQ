# DeviceIQ Smartphone Recommendation System

DeviceIQ is a smartphone decision-support website built with Next.js App Router, Prisma, and PostgreSQL. Its catalog includes seeded illustrative values and does not yet have a complete field-level source and retrieval-date audit. Recommendation scores demonstrate the calculation and are not verified market findings or completed research results.

## Stack

- Next.js App Router with React 19 and TypeScript
- Prisma + PostgreSQL
- Firecrawl-ready content cleaning layer
- Pluggable LLM extraction providers (OpenAI, Anthropic, Ollama)
- Modular recommendation and comparison services
- Responsive SaaS UI with Framer Motion

## Quick Start

1. Copy `.env.example` to `.env` and fill in your database and provider keys.
2. Install dependencies with `npm install`.
3. Generate Prisma client with `npm run prisma:generate`.
4. Run migrations with `npm run prisma:migrate:dev`.
5. Seed the catalog with `npm run prisma:seed`.
6. Start the app with `npm run dev`.

## Environment Notes

- If `BOOTSTRAP_ON_STARTUP=true`, the app will ensure seed data exists and queue stale phones for enrichment on first load.
- If no AI provider keys are set, the system still operates using seed data and cached database values.
- `POST /api/enrich` can be called manually or by a scheduler/worker to process queued enrichment jobs.

## Main Modules

- `prisma/schema.prisma`: normalized database schema
- `lib/data/seed-phones.ts`: base smartphone dataset
- `lib/pipeline/`: source discovery, Firecrawl fetch, extraction orchestration, fallbacks
- `lib/services/`: bootstrap, recommendation, comparison, phone querying
- `app/api/`: production-style route handlers
- `app/dashboard`: interactive recommendation and compare UI

## Recommendation method and research status

- The recommendation flow applies mandatory filters before calculating min–max ranges.
- Price is a cost criterion in Philippine pesos. Battery is manufacturer-listed capacity in mAh, not endurance.
- The current demo scores only price and battery capacity. Performance benchmark and camera criteria remain unavailable until their operational definitions and source records are approved and present.
- Weights are non-negative relative points; active weights are divided by their total. Missing active values exclude a phone from scoring, and constant criteria are removed before the remaining weights are rescaled.
- Preference analysis uses the proposal's equal-weight, affordability-focused, and performance-focused scenarios. An unavailable scenario is reported as not assessable.
- See [`docs/THESIS_ALIGNMENT.md`](docs/THESIS_ALIGNMENT.md) for the SOP traceability map, scope conflicts, data limits, and verification procedure.

## Folder Guide

- Website pages: `app/`
- Reusable frontend UI: `components/`
- Main stylesheet: `app/globals.css`
- Backend services and data logic: `lib/services/`
- Enrichment pipeline: `lib/pipeline/`
- AI integrations: `lib/ai/`
- Database schema and seed setup: `prisma/`
- Dev scripts: `scripts/`
- Thesis alignment: `docs/THESIS_ALIGNMENT.md`

## Generated And Runtime Files

- `.next/` is generated build output.
- `node_modules/` contains installed packages.
- `prisma/dev.db` is the local SQLite dev database.
- `.next-dev.out.log` and `.next-dev.err.log` are local runtime logs.
