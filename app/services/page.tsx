import Link from "next/link";

export default function ServicesPage() {
  return <section className="section"><div className="page-shell stack"><h1 className="section-title">Phone tools</h1>
    <article className="glass-panel card stack"><h2>Browse specifications</h2><p>Filter catalog records by brand, price and specifications.</p><Link href="/dashboard">Open catalog →</Link></article>
    <article className="glass-panel card stack"><h2>Rank a shortlist</h2><p>Set requirements and inspect each phone’s weighted score.</p><Link href="/recommend">Set priorities →</Link></article>
    <article className="glass-panel card stack"><h2>Compare two phones</h2><p>Read specifications for both models side by side.</p><Link href="/compare">Choose phones →</Link></article>
  </div></section>;
}
