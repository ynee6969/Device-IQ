# Automated device enrichment

This job queues all **456 device models** in the research inventory: smartphones, tablets, and laptops. Pinoy Techno Guide sitemap discovery and collection are limited to the 438 smartphone and tablet records; laptops use linked or discovered manufacturer pages. It reads models with linked source pages and can search for additional official pages with the Brave Search API. With that API key it also discovers exact-model GSMArena page links for human cross-checking. GSMArena pages are **not fetched or copied** into the database because its [terms](https://www.gsmarena.com/terms.php3) restrict reuse of its content and images without permission. Each run records fetch status, source URL and type, page title, observed specification excerpt, and dated PHP price. These observations are unreviewed research material, not updates to public catalog values.

## Run locally

From the repository root:

```powershell
npm ci
node --test scripts/test-enrichment.mjs
node scripts/enrich_devices.mjs
python scripts/store_enrichment.py
```

For a focused rerun after reviewing one inventory model, pass its stable device ID. This is useful for correcting a reviewed name alias without recollecting the whole queue:

```powershell
node scripts/enrich_devices.mjs --device-id <device_id> --source-url <reviewed_source_url> --discover-limit 0 --gsmarena-limit 0 --ptg-limit 1 --output research/enrichment/<review-snapshot>.json
```

Model identity matching treats a final `+` and the word `Plus` as equivalent product-name notation, while keeping a base model such as `S23` distinct from `S23+`.
An explicit source URL is still checked against robots rules, approved HTTPS host rules, category, redirects, and the exact-model heading gate before its fields are collected.

The Pinoy Techno Guide sitemaps need no key. The job matches exact smartphone and tablet slugs, marks them as independent Philippine reference candidates, and fetches up to 60 rotating pages each week. To discover additional official pages and GSMArena review links, set `BRAVE_SEARCH_API_KEY` in your environment or as a GitHub Actions repository secret. The key is sent only to the Brave Search API; the weekly job searches up to 60 rotating unsourced models across all three categories and 20 rotating GSMArena model links per run. Search results are **unreviewed candidates**, even when the domain is official. The job checks each fetched host's `robots.txt`, skips unavailable or blocked hosts, uses request timeouts and per-host spacing, and does not bypass access controls.

The page parser accepts an exact model heading and unambiguous structured specification fields. It collects candidate values only; these require field-level review against the exact model and configuration before promotion. Official store prices require a PHP-denominated Product offer. Pinoy Techno Guide prices require an explicit variant and are labeled `independent_reported_official_price`, since they are the site's report rather than a manufacturer quote. Each price preserves variant RAM/storage, the article publication date when available, and the observation date. The configuration is exact only when the SKU or both RAM and storage match. Dated prices are observations, not current guarantees. The collector does not infer original release dates, local-market availability, or missing values. Existing conflicting specification values are listed in `conflicts` for review. Findings do not enter the public catalog until separately reviewed and promoted.

## Additional research references

`reference-sources.json` records source roles and automated-use rules. [NanoReview](https://nanoreview.net/) is included as a manual lookup reference only: its published `robots.txt` disallows GPTBot and ChatGPT-User, so the automated collector must not fetch its pages. [Kimovil](https://www.kimovil.com/en/) is also link-only in this project. Its terms restrict copying, distribution, and transformation of site content without express written authorization; no automated extraction or image reuse is configured. Any candidate found through either reference must be corroborated against sources allowed for recorded evidence.

## Specification audit

Run `py -3.12 scripts/build_public_catalog.py --workbook <inventory.xlsx>` first to import the supplied workbook and apply only explicit source-backed reviews in `manual-field-reviews.json`, then run `py -3.12 scripts/build_specification_audit.py --workbook <inventory.xlsx>`. The audit command produces `DEVICEIQ_SPECIFICATION_COMPLETENESS_REPORT.md`, `DEVICEIQ_RESEARCH_PROGRESS.md`, and the full configuration-level evidence matrix. It also writes a copy of the supplied workbook with `SPEC FIELD AUDIT`, `AUDIT SUMMARY`, `REFERENCE LOOKUPS`, `PRICE CANDIDATES`, and `IMAGE AUDIT` sheets under `outputs/`; the original workbook is only read. GitHub Actions uses `--skip-workbook` because the source workbook is not in the repository. Exact-model page observations can be promoted as model-level specifications only when the source and field match; variant-specific data, Philippine release/availability, current prices, ambiguous values, and conflicts stay pending. The detail page shows each field's value, review status, source link, and remaining candidates.

For a new full-inventory source run, write to a dated file under `research/enrichment/`, merge it with retained candidate history using `python scripts/merge_enrichment_snapshots.py --incoming <dated-snapshot.json>`, and run `python scripts/review_exact_model_observations.py`. That reviewer only promotes exact-page, model-wide technical fields; it does not promote RAM/storage variants, Philippine release or availability, current prices, or ambiguous values. Use an additional manual review script for source facts that need human interpretation, then rebuild the public catalog and audit.

## Scheduled run

`.github/workflows/enrich-devices.yml` runs weekly and can be started manually. It retains snapshots on `codex/enrichment-data` and opens or updates a pull request with the refreshed research database and review report. Review that pull request before merging; the job never updates `lib/catalog/public-inventory.json` or production data. GitHub schedules run from the default branch, so the workflow must be present on `main` to activate.

## Public catalog images

`research/catalog-image-sources.json` contains image candidates; a candidate is not permission to republish it. `scripts/cache_catalog_images.mjs` now requires a recorded reusable license or written permission before fetching or caching an image. `scripts/reconcile_catalog_image_rights.py` checks Commons license metadata, removes unlicensed local assets from the public manifest, and records each blocked or unmatched image in `research/catalog-image-unavailable.json`. Only images with source, attribution, license, and rights-check date remain public. Records without a rights-cleared exact-model match show the neutral "Image unavailable" placeholder, and the workbook's `IMAGE AUDIT` sheet gives the reason. This image step does not use GSMArena, NanoReview, or Kimovil assets.
