# DeviceIQ

DeviceIQ is a category-based catalog for smartphones, tablets and laptops in the Philippine market. Choose a category, filter recorded configurations, sort the matches and inspect source-linked product details. The public catalog is generated from the provisional research inventory. Its 28 models have official Philippine evidence within the website's January 2021 to November 2026 study period; the larger research inventory is not a verified device census.

## Run locally

```bash
npm install
npm run dev
```

Open `/browse` to select a category. `npm run build` checks the production build and `npm run test:catalog` runs independent expected-ID filter cases. Sign-in uses the existing NextAuth setup; configure the documented environment values for account features. Catalog saved items are currently stored in the browser.

## Structure

- `lib/catalog/data.ts` and `public-inventory.json`: source-linked, eligible public snapshot. Rebuild with `python scripts/build_public_catalog.py` after a reviewed inventory update.
- `lib/catalog/pilot.ts`: preserved 30-record pilot used to reproduce the research seed and earlier filter checks.
- `lib/catalog/filtering.ts`: deterministic category filter, sort and pagination logic.
- `components/catalog/`: browse, compare and saved-item interfaces.
- `app/browse/` and `app/devices/`: category choice, results and model detail routes.
- `docs/CATALOG_COVERAGE.md`: current source coverage and missing evidence.
- `docs/THESIS_ALIGNMENT.md`: provisional requirements-to-feature-to-test traceability and the manuscript mismatch.

The study window begins 1 January 2021; the current research snapshot ends 24 November 2026, before the planned 30 November cutoff. Pending, held-out, and unresolved-date research records stay out of public results. Missing values are not filled with estimates, and source observation dates are not treated as model launch dates. The website reads a checked-in public snapshot; no production database import is required.
