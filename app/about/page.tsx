import Link from "next/link";

export default function AboutPage() {
  return <section className="page-shell section stack"><h1 className="section-title">Method and sources</h1><p className="section-copy">DeviceIQ shows matching records after category-specific filters. Results follow the selected sort order; no device receives a composite rating.</p>
    <article className="glass-panel card stack"><h2>Coverage</h2><p>The planned study window is 1 January 2021 through 30 November 2026. The current catalog has 10 sourced configurations in each category. It is a starting set, not a census. Older illustrative smartphone examples remain outside this catalog pending source review.</p><p>Official Philippine product and store pages are linked from each record. A page observation date establishes when a listing was checked, not the original launch date.</p></article>
    <article className="glass-panel card stack"><h2>How filtering works</h2><p>Every active field must match. Multiple choices within one field include any selected choice. Minimum capacity filters include larger values. Missing values do not pass an active filter. Results are displayed ten per page after sorting.</p></article>
    <article className="glass-panel card stack"><h2>Prices</h2><p>Displayed Philippine prices include a source, condition and observation date. Missing prices remain unverified. A discontinued record would require a separately verified used price; no current record has a confirmed discontinued status.</p></article>
    <Link className="button-secondary" href="/browse">Choose a category</Link>
  </section>;
}
