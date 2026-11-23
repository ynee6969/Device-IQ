import Link from "next/link";
import { ArrowRight } from "lucide-react";

export function HeroSection() {
  return <header>
    <h1 className="section-title">Compare smartphones</h1>
    <p className="section-copy">See how price and battery capacity change the order of phones within your budget.</p>
    <div className="button-row"><Link className="button" href="/recommend">Rank phones <ArrowRight size={16} /></Link>
      <Link className="button-secondary" href="/compare">Compare two models</Link></div>
  </header>;
}
