# DeviceIQ smartphone implementation

The reference for this phase is `DeviceIQ_Revised_Thesis.docx`, Word modification time 20 November 2026 at 22:49 UTC. The earlier `DeviceIQ_Revised_Thesis_Aligned_Revision.docx` is dated 16:59 UTC that day. Chapter 2 and Tables 2–4 in the newer manuscript specify the evaluation rules below. The member reviewer and critical research audit were used to cross-check interpretation. Adviser sign-off and instrument validation are additional research records.

## Questions and evidence

| Research question from the proposal | Smartphone implementation | How to inspect it |
| --- | --- | --- |
| What device information and system requirements are needed for DeviceIQ to provide personalized smartphone and tablet recommendations? | Browse and compare smartphones. Record units, model/configuration and gaps. Only PHP price and capacity in mAh are used in the illustrative ranking. | Open a phone’s specifications and expand Record and sources. On the rank page, check the exclusion list after applying requirements. |
| To what extent does DeviceIQ meet its functional requirements and produce filtering, scoring, and ranking results that agree with independent calculations? | Inclusive requirements precede normalization. Missing values exclude records. Constant measures are omitted. Result details expose the raw value, eligible range, normalized value, effective weight and contribution. | Run `npm run test:recommendation`. Inspect the fixed inputs and manual expectations in `scripts/test-recommendation.ts`. |
| What changes occur in recommendation scores and rankings when user preferences are varied under predefined scenarios? | The same eligible set and normalized values are used for equal weights, affordability focus and performance focus. Focus receives 0.60 and other active criteria share 0.40. | Expand Compare preference scenarios. Read score change, positions gained, and leaders against the equal baseline. The performance scenario identifies the missing benchmark. |

## Data limits and implementation decisions

- This phase implements smartphones. The proposal also includes tablets in separate comparisons.
- The example catalog has not been admitted to the study dataset. Study inclusion requires a distinct configuration, a release from 1 November 2021 through 30 November 2026, traceable Philippine availability by 30 November 2026, and dated evidence for scored fields. Neither local seed timestamps nor a generic model reference establish those facts. Source links and actual retrieval dates are shown when recorded.
- Performance requires one published benchmark and version for comparable configurations. Camera requires one documented score or reproducible composite. Legacy catalog ratings meet neither definition. Battery means listed capacity, not endurance. RAM, brand and recorded OS can restrict eligibility without adding score terms.
- A singleton or all-constant set is presented as eligible but unranked. There is no denominator or remaining weight available for a relative comparison. A positive weight assigned only to a constant criterion prompts the user to change their priorities. When no score can be calculated there is no scenario comparison.
- Software checks use fixed fixtures and the manuscript’s tolerance of 0.000001. Field-level source review, the independent study workbook, validator review and formal evaluation logs remain research work.

## Local verification

The smartphone workflow revision on `codex/smartphone-thesis-workflow` was checked locally on 23 November 2026 (Manila). The checked-in fixtures hold the inputs and expected values for reproduction at this Git revision.

| Check | Expected | Observed |
| --- | --- | --- |
| Fixed three-phone example, price and capacity weights 3:2 | B first at 0.70, A second at 0.60, C third at 0.20 | Passed within 0.000001. |
| Appendix example, two configurations with price and hypothetical benchmark | Equal weights tie. The 60% price and 60% performance scenarios have opposite leaders. | Passed, including shared ranks and the two focused scores of 0.60 and 0.40. |
| Recommendation API | Reject invalid JSON, negative budget, all-zero weights and unsupported priorities. Valid constraints must hold for every returned phone. | Passed on the local production server. |
| Browser at 390 and 1440 pixels | Browse, rank, inspect calculations, compare, open a source panel, and operate the controls by keyboard. Show loading, empty and error states and allow retry. | Passed in Chromium. The recovery case used a simulated 503 followed by an actual successful request. |
| Lint and production build | Complete with no errors. | Passed. Lint reported three existing image optimization warnings. |
