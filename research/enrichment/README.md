# Automated device enrichment

This job queues all **438 smartphones and tablets** in the 2026-11-24 research inventory. It reads the 42 models with linked source pages, discovers smartphone and tablet pages from Pinoy Techno Guide's published sitemaps, and can search for additional official pages with the Brave Search API. With that API key it also discovers exact-model GSMArena page links for human cross-checking. GSMArena pages are **not fetched or copied** into the database because its [terms](https://www.gsmarena.com/terms.php3) restrict reuse of its content and images without permission. Each run records fetch status, source URL and type, page title, observed specification excerpt, and dated PHP price. The separate SQLite file and JSON report are review material; neither is read by the website.

## Run locally

From the repository root:

```powershell
npm ci
node --test scripts/test-enrichment.mjs
node scripts/enrich_devices.mjs
python scripts/store_enrichment.py
```

The Pinoy Techno Guide sitemaps need no key. The job matches exact smartphone and tablet slugs, marks them as independent Philippine reference candidates, and fetches up to 60 rotating pages each week. To discover additional official pages and GSMArena review links, set `BRAVE_SEARCH_API_KEY` in your environment or as a GitHub Actions repository secret. The key is sent only to the Brave Search API; the weekly job searches up to 60 rotating unsourced models and 20 rotating GSMArena model links per run. Search results are **unreviewed candidates**, even when the domain is official. The job checks each fetched host's `robots.txt`, skips unavailable or blocked hosts, uses request timeouts and per-host spacing, and does not bypass access controls.

The page parser accepts an exact model heading and unambiguous structured specification fields. Official store prices require a PHP-denominated Product offer. Pinoy Techno Guide prices require an explicit variant and are labeled `independent_reported_official_price`, since they are the site's report rather than a manufacturer quote. Each price preserves variant RAM/storage, the article publication date when available, and the observation date. The configuration is exact only when the SKU or both RAM and storage match. Dated prices are observations, not current guarantees. The collector does not infer original release dates, local-market availability, or missing values. Existing conflicting specification values are listed in `conflicts` for review. Findings do not enter the public catalog until separately reviewed and promoted.

## Scheduled run

`.github/workflows/enrich-devices.yml` runs weekly and can be started manually. It retains snapshots on `codex/enrichment-data` and opens or updates a pull request with the refreshed research database and review report. Review that pull request before merging; the job never updates `lib/catalog/public-inventory.json` or production data. GitHub schedules run from the default branch, so the workflow must be present on `main` to activate.

## Public catalog images

`research/catalog-image-sources.json` contains curated manufacturer pages and image choices. `research/catalog-image-aliases.json` connects other exact-model images already present in the project to workbook IDs. Run `npm run assets:catalog-images` to cache curated choices as optimized WebP assets, then `py -3.12 scripts/build_public_catalog.py` to attach image IDs to the public catalog. `npm run test:images` checks every assigned local image. Records without a reviewed exact-model image show an "Image unavailable" placeholder. The image manifest records the source page, asset URL, and match scope. This image step does not use GSMArena assets.
