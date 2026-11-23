# DeviceIQ

DeviceIQ is a category-based catalog for smartphones, tablets and laptops in the Philippine market. Choose a category, filter exact configurations, sort the matches and inspect source-linked product details. The current pilot has 10 sourced configurations in each category. Older illustrative phone examples from the former app remain excluded pending source review.

## Run locally

```bash
npm install
npm run dev
```

Open `/browse` to select a category. `npm run build` checks the production build and `npm run test:catalog` runs independent expected-ID filter cases. Sign-in uses the existing NextAuth setup; configure the documented environment values for account features. Catalog saved items are currently stored in the browser.

## Structure

- `lib/catalog/data.ts`: initial product records, exact variants, source URLs, observation dates and price provenance.
- `lib/catalog/filtering.ts`: deterministic category filter, sort and pagination logic.
- `components/catalog/`: browse, compare and saved-item interfaces.
- `app/browse/` and `app/devices/`: category choice, results and model detail routes.
- `docs/CATALOG_COVERAGE.md`: current source coverage and missing evidence.
- `docs/THESIS_ALIGNMENT.md`: provisional requirements-to-feature-to-test traceability and the manuscript mismatch.

The study window is 1 January 2021 through the planned 30 November 2026 cutoff. The pilot is not a census. Missing values are not filled with estimates, and source observation dates are not treated as model launch dates.
