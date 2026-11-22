# DeviceIQ thesis alignment

## Source and status

Implementation reference: `DeviceIQ_Revised_Thesis_Aligned_Revision.docx`, supplied in Downloads and dated 20 November 2026 in Word metadata. It is the newest aligned proposal file reviewed in this task. The file does not identify an approval date, so this document does not claim that the proposal has adviser or panel approval. The companion `DeviceIQ_Comprehensive_Thesis_Defense_Question_Bank_and_Critical_Research_Audit.docx` is a review document; its recommendations informed gap checks, but it is not the source of the research questions.

The aligned proposal states three research questions:

1. What device information and system requirements are needed for DeviceIQ to provide personalized smartphone and tablet recommendations?
2. To what extent does DeviceIQ meet its functional requirements and produce filtering, scoring, and ranking results that agree with independent calculations?
3. What changes occur in recommendation scores and rankings when user preferences are varied under predefined scenarios?

## SOP traceability

| Research question | Website feature and current evidence | Verification procedure |
| --- | --- | --- |
| SOP 1: required information and requirements | `app/recommend/page.tsx` and `components/recommendation/recommendation-workspace.tsx` expose phone filters, relative weights, active criteria, and score explanations. `lib/recommendation/criteria.ts` defines price in PHP and listed battery capacity in mAh. Benchmark performance and camera scoring are marked unavailable until their approved operational measures and traceable sources exist. The catalog notice identifies seeded records and incomplete field-level source dates. | Review each data field and unit; confirm unavailable measures are not scored; verify the notice and configuration labels; confirm source and retrieval-date gaps are visible. |
| SOP 2: requirements and independent calculations | `lib/recommendation/eligibility.ts` filters before scoring. `lib/recommendation/normalization.ts` applies cost min–max for price, benefit min–max for battery capacity, removes constant criteria, and excludes missing active values. `lib/recommendation/scoring.ts` normalizes entered relative points and calculates the weighted sum. | `scripts/test-recommendation.ts` checks boundary filters, normalization directions and ranges, missing values, weights, contributions, constant criteria, ranking ties, and scenario calculations against hand-prepared expected values. These are implementation checks, not completed research evaluation records. |
| SOP 3: predefined preference scenarios | `lib/recommendation/sensitivity.ts` implements the equal-weight baseline and the 0.60 affordability scenario. The performance-focused scenario is retained as not assessable because the catalog lacks an approved, source-traceable benchmark measure. `components/recommendation/recommendation-workspace.tsx` reports scenario scores and rank positions separately. | Run all three scenarios on the same eligible set; verify the exact scenario weights and displayed scores/ranks. The current performance scenario must remain not assessable until the data dictionary and benchmark records are approved and populated. |

## Proposal-to-implementation conflicts and data limits

- The supplied implementation brief limits this task to smartphone functionality. The proposal's title, scope, and SOP 1 include tablets. This release intentionally remains phone-only; the researchers must align the approved study scope and research question before claiming that the site answers the entire tablet-inclusive SOP.
- The proposal gives a study period ending 30 November 2026 and a data cut-off on that date. That date is still in the future as of 22 November 2026. The site and documentation therefore do not claim complete data collection or completed evaluation.
- The current seeded catalog does not provide a complete field-level source and retrieval-date audit, and its model configurations are often unspecified. It is labelled illustrative and is not presented as verified market data.
- The proposal's performance candidate requires one benchmark, its name and version, configuration, and source. Camera scoring requires a common documented score or reproducible composite. Those measures are unavailable in the current catalog and are excluded from recommendation scoring. Battery is treated as capacity in mAh, not endurance.
- The currently active price and battery values are used only to demonstrate the model. Their scores are not research results until the records, exact configurations, sources, and retrieval dates are checked and retained.
- The proposal's missing-value rule excludes phones missing an active criterion. Its constant-value rule removes a non-discriminating criterion and proportionally rescales the remaining weights. Scores are calculated at full precision; values within 0.000001 share a rank, with tied phones displayed alphabetically.

## Verification record

Checks run on 22 November 2026:

- `npm run test:recommendation` passed. Independently prepared expected values covered eligibility boundaries, missing active values, benefit and cost normalization, weight normalization, weighted contributions, constant criteria, ties, and all three scenario definitions.
- `npm run lint` passed. It reported the existing `<img>` optimization warnings in `app/compare/page.tsx`, `app/phones/[slug]/page.tsx`, and `components/phones/device-card.tsx`; it reported no new warnings in the changed recommendation files.
- `npm run build` passed, including Next.js lint and TypeScript checks.
- Local integration check: `GET /recommend` returned 200 with the page title and research-status notice. `POST /api/recommend` returned 200 with active criteria `price` and `battery`, correctly normalized 60:40 weights, and the three expected scenario statuses. The local fallback catalog returned 78 filter-eligible and scored records; this count is only a development check, not a verified study-dataset count. An all-zero weight request returned 400.
- Headless browser checks at 390 × 844 and 1440 × 900 found no horizontal overflow. The price control had an accessible label, unsupported performance and camera controls were disabled, all three scenario headings rendered, keyboard focus reached the budget input, and the page reported no JavaScript errors.
- `git diff --check` passed. Git reported only its line-ending notices for Windows working copies.

No production deployment was made. The supplied Vercel project `dialed` showed “No Production Deployment.” The local Vercel link metadata identifies `device-iq`, whose dashboard also showed “No Production Deployment.” The local Vercel CLI has no saved credentials, and the supplied production hostname resolves to a protected Vercel login page. Therefore the linked project and current production alias could not be verified as the same target; no project, domain, or environment setting was changed.

These software checks do not replace the proposal's planned field-level data review, independent research workbook, validator review, or retained evaluation records. Do not describe them as completed research evaluation results.
