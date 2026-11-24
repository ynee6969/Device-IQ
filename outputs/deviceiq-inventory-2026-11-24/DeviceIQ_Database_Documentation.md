# DeviceIQ Philippine device research inventory

Snapshot: **2026-11-24**. This is an evidence-tracked working inventory, **not** a complete census of Philippine releases. It does not change the live DeviceIQ catalog.

## Rebuild

From the repository root, with the existing Node dependencies installed:

```powershell
python scripts/build_research_inventory.py
python scripts/build_postgres_research_schema.py
npx.cmd tsx scripts/seed_research_postgres.ts
```

The first command rebuilds the standalone SQLite database, JSON, CSV, and reports under `outputs/deviceiq-inventory-2026-11-24/`. It deliberately replaces only that generated SQLite file. The second command regenerates the additive PostgreSQL SQL. The third is a **dry run** that lists import row counts and does not connect to a database.

The workbook is built with the bundled `@oai/artifact-tool` spreadsheet runtime:

```powershell
node research/build_workbook.mjs
```

The build environment must make `@oai/artifact-tool` resolvable from `research/` (for example via a local `node_modules` junction to the bundled runtime). The `node_modules` junction is ignored by Git.

## Research rules

| Item | Rule |
| --- | --- |
| Historical capture | 2021-01-01 through 2026-11-24 |
| Provisional rolling window | 2021-11-24 through 2026-11-24 |
| Prior approved website panel | 2021-01-01 through planned 2026-11-30; separate from this snapshot |
| Market | Philippines |
| Model grain | One base marketed device per brand and category; configurations are separate rows |
| Verified launch | A dated official local launch is documented; this does not imply a first retail sale date |
| Verified availability | An official Philippine product/store page or local announcement establishes local presence; the original release date can remain unknown |
| Pending | A supplied brand/example claim lacks direct model-level Philippine evidence |
| Excluded | Evidence places the model outside the selected window or another stated inclusion rule |

The annual and 2026 notes are copied verbatim into `source_notes/` and their nonblank lines are stored in `raw_research_claims`. Their cited publication labels did not include direct URLs. The model examples derived from them are **leads**. A series label stays in `research_queue` until exact models are identified. The 33 repeated 2026 claims remain in staging and do not create duplicate base models. The 30 existing catalog items, 22 Samsung models, and 8 ASUS laptops have linked official Philippine sources. ASUS's announced Zenbook A16 and a later UX3480 color remain outside the verified configuration list because their local retail availability was described as coming soon. Manufacturer relationships are recorded only when supported; blanks mean research remains open.

The release table distinguishes an exact Philippine launch date, a release year, and the date by which local availability was observed. Do not fill missing original dates with global dates, current store listing dates, or a guessed January 1. The workbook's selected scope formulas conservatively leave uncertain boundary-year records pending.

## Relational design

The SQLite schema is `schema.sql`. Its 14 tables are:

| Table | Grain and main relationship |
| --- | --- |
| `manufacturers` | Corporate maker or verified owner, with optional parent manufacturer |
| `brands` | Consumer-facing brand, optionally linked to a manufacturer |
| `device_categories` | Smartphone, tablet, laptop lookup |
| `device_models` | One canonical base model linked to brand, category, and optional manufacturer |
| `device_configurations` | One specific storage/hardware version linked to a model |
| `device_specifications` | Source-backed model or configuration specification key/value |
| `philippines_market_releases` | One local-market release/availability assessment per model |
| `data_sources` | One source URL and its publication/access metadata |
| `device_source_evidence` | A source-to-model claim with evidence type and reviewer result |
| `raw_research_claims` | Original source line, claim text, parsing state, duplicate pointer |
| `research_queue` | Actionable unresolved model, series, date, or laptop discovery task |
| `excluded_records` | Original record and reason for exclusion |
| `audit_log` | Verification status transitions with reason and date |
| `scope_settings` | Research snapshot and earlier panel cutoff settings |

IDs are deterministic hashes of stable identity fields. Foreign keys, uniqueness checks, inclusion flags, and source links are checked on each build. The CSV directory exports all 14 tables in import order independent files; the requested core ten are included. `deviceiq_inventory.json` contains the same relations by ID. `DeviceIQ_Validation_Report.md`, `DeviceIQ_Data_Quality_Report.md`, and `DeviceIQ_Duplicate_Review.md` explain each build's status.

## Application compatibility

The existing app uses Prisma with PostgreSQL for its `Phone` and user tables, plus a static cross-category catalog. Importing preliminary research claims into the website would present unverified devices as released. The app is therefore unchanged.

`postgres_compatibility.sql` is an **additive** 14-table schema using `research_` prefixes and deferred foreign keys. `scripts/seed_research_postgres.ts` reads the generated JSON and upserts by stable primary key. It defaults to a dry run. After reviewing the SQL and supplying the intended `DATABASE_URL`, an operator can apply the SQL, then run the importer with `--apply`. Neither action has been run against the live application database. The research tables can later support a review interface and promotion of verified, window-eligible models to the catalog. This is a prepared import path, not completed website integration.

## Remaining research

1. Verify the 396 pending model candidates against exact Philippine model-level sources; resolve apparent aliases and series claims.
2. Locate the 29 missing original Philippine release dates among verified local-presence models.
3. Complete laptop discovery by brand and year; the supplied annual notes focus on smartphones and tablets.
4. Record more source-backed configurations and technical specifications, particularly for the 405 models with no current specification field.
5. Verify manufacturer and parent-company relationships for brands currently unmapped.
6. Review rolling-window boundary cases and reconcile the approved website panel end date with the research snapshot before changing website eligibility rules.
