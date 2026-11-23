"use client";

import Link from "next/link";
import { useEffect, useRef, useState, type FormEvent } from "react";
import type { SmartphoneResult } from "@/lib/services/recommendations";
import { RecommendationResults } from "./recommendation-results";
import styles from "./RecommendationWorkspace.module.css";

export function RecommendationWorkspace({ brands }: { brands: string[] }) {
  const [price, setPrice] = useState(50);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState<SmartphoneResult | null>(null);
  const resultsRef = useRef<HTMLDivElement>(null);
  useEffect(() => { if (result) resultsRef.current?.focus(); }, [result]);

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const fields = new FormData(event.currentTarget);
    const optionalNumber = (name: string) => fields.get(name) ? Number(fields.get(name)) : undefined;
    const minBudget = optionalNumber("minBudget");
    const budget = optionalNumber("budget");
    setResult(null);
    if (minBudget !== undefined && budget !== undefined && minBudget > budget) {
      setError("Minimum price must be at or below maximum price.");
      return;
    }
    setError("");
    setBusy(true);
    try {
      const brand = fields.get("brand");
      const response = await fetch("/api/recommend", { method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ minBudget, budget, brands: brand ? [brand] : [], osPreference: fields.get("os"),
          minRam: optionalNumber("minRam"), minBattery: optionalNumber("minBattery"),
          weights: { price, battery: 100 - price, performance: 0, camera: 0 }, limit: 10 }) });
      if (response.status >= 500) throw new Error("Could not load the catalog. Please try again.");
      const data = await response.json();
      if (!response.ok) throw new Error(data.error);
      setResult(data);
    } catch (cause) {
      setError(cause instanceof TypeError ? "Connection interrupted. Please try again." : cause instanceof Error ? cause.message : "Could not load matches.");
    } finally {
      setBusy(false);
    }
  }

  return <div className={styles.scope}>
    <header className={styles.intro}><h1 className="section-title">Rank smartphones</h1>
      <p className="section-copy">Set your requirements, then choose how much price and battery capacity matter. This catalog uses illustrative records.</p></header>
    <form className={`glass-panel ${styles.form}`} onSubmit={submit} onChange={() => { setError(""); setResult(null); }}>
      <fieldset className={styles.group} disabled={busy}><legend>Requirements</legend>
        <div className={styles.fields}>
          <label className="field">Minimum price (₱)<input type="number" name="minBudget" className="input" min="0.01" step="0.01" placeholder="No minimum" /></label>
          <label className="field">Maximum price (₱)<input type="number" name="budget" className="input" min="0.01" step="0.01" placeholder="No maximum" /></label>
          <div className="field"><label htmlFor="brand">Brand</label><select id="brand" name="brand" className="select"><option value="">All brands</option>{brands.map(b => <option key={b}>{b}</option>)}</select></div>
          <div className="field"><label htmlFor="os">Operating system</label><select id="os" name="os" className="select"><option value="any">Any system</option><option value="android">Android</option><option value="ios">iOS</option></select></div>
          <label className="field">Minimum RAM (GB)<input type="number" min="1" name="minRam" className="input" placeholder="Any" /></label>
          <label className="field">Minimum battery (mAh)<input type="number" min="1" name="minBattery" className="input" placeholder="Any" /></label>
        </div></fieldset>
      <fieldset className={styles.group} disabled={busy}><legend>Your priorities</legend>
        <div className={styles.weightCard}>
          <label htmlFor="price-weight">Share assigned to lower price</label>
          <input id="price-weight" type="range" min="0" max="100" value={price} aria-valuetext={price + "% price, " + (100-price) + "% battery capacity"} onChange={e => setPrice(Number(e.target.value))} />
          <div className={styles.weightHeading}><span>Price <strong>{price}%</strong></span><span>Battery capacity <strong>{100 - price}%</strong></span></div>
        </div></fieldset>
      <details className={styles.details}><summary>How the score works</summary>
        <p>Budget and specification limits are inclusive. A phone must have the requested specifications and both scored values. The remaining phones set the minimum and maximum for each measure.</p>
        <p>Price uses (maximum − price) / (maximum − minimum). Capacity uses (capacity − minimum) / (maximum − minimum). Each normalized value is multiplied by its weight, then the contributions are added.</p>
        <p>A constant measure is omitted and the remaining weights are rescaled. Totals within 0.000001 share a rank. Calculations use full precision and scores are displayed to two decimals.</p>
        <Link href="/about">Criteria and sources</Link></details>
      {error && <p role="alert" className={styles.error}>{error}</p>}
      <button disabled={busy} className={`button ${styles.submit}`}>{busy ? "Calculating…" : "Show matches"}</button>
    </form>
    {result && <div ref={resultsRef} tabIndex={-1}><RecommendationResults result={result} /></div>}
  </div>;
}
