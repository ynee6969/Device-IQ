import Link from "next/link";

export default function AboutPage() {
  return <section className="page-shell section stack"><h1 className="section-title">Method and sources</h1><p className="section-copy">DeviceIQ shows matching records after category-specific filters. Results follow the selected sort order; no device receives a composite rating.</p>
    <article className="glass-panel card stack"><h2>Coverage</h2><p>The planned study window is 1 January 2021 through 30 November 2026. The current public snapshot covers 1 January 2021 through 24 November 2026 and contains 28 source-linked models: 14 smartphones, 9 tablets and 5 laptops. It is a reviewed slice of a provisional inventory, not a census.</p><p>Pending claims, unresolved local dates and held-out products stay in the research files. Product details link to official Philippine evidence and recorded specifications. A source observation date is not a model launch date.</p></article>
    <article className="glass-panel card stack"><h2>How filtering works</h2><p>Every active field must match. Multiple choices within one field include any selected choice. Minimum capacity filters include larger values. Missing values do not pass an active filter. Results are displayed ten per page after sorting.</p></article>
    <article className="glass-panel card stack"><h2>Prices</h2><p>Displayed Philippine prices include a source, condition and observation date. Missing prices are shown as not recorded. A discontinued record would require a separately verified second-hand price; no current record has a confirmed discontinued status.</p></article>
    <Link className="button-secondary" href="/browse">Choose a category</Link>
  </section>;
}
