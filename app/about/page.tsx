import Link from "next/link";

export default function AboutPage() {
  return <section className="section"><div className="page-shell stack">
    <h1 className="section-title">Method and sources</h1>
    <p className="section-copy">DeviceIQ ranks eligible smartphones against the priorities you enter for a single comparison.</p>
    <article className="glass-panel card stack"><h2>What goes into the score?</h2>
      <p><strong>Price (PHP).</strong> A lower price earns a higher normalized score. The study calls for a dated Philippine price for the exact configuration.</p>
      <p><strong>Battery capacity (mAh).</strong> Larger listed capacity earns a higher score. Endurance also depends on how a phone is used.</p>
      <p><strong>Performance and camera.</strong> The catalog lacks a consistent, sourced benchmark version and comparable camera measure. These two priorities are omitted from ranking.</p>
    </article>
    <article className="glass-panel card stack"><h2>Where the numbers come from</h2>
      <p>The smartphone catalog includes example records. Where available, a model’s specifications page links to its reference and retrieval date. Price and capacity still need field-level source checks.</p>
      <p>Study inclusion requires a distinct configuration, a release from 1 November 2021 through 30 November 2026, and evidence of Philippine availability by the cut-off. The example catalog has not passed that audit.</p>
    </article>
    <div className="button-row"><Link className="button" href="/recommend">Rank phones</Link><Link className="button-secondary" href="/dashboard">Browse records</Link></div>
  </div></section>;
}
