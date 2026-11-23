"use client";

import Link from "next/link";
import { useState } from "react";
import { FavoriteButton } from "@/components/phones/favorite-button";
import type { SmartphoneResult } from "@/lib/services/recommendations";
import { CRITERIA } from "@/lib/recommendation/criteria";
import type { Criterion } from "@/lib/recommendation/types";
import { formatPhp } from "@/lib/utils/format";
import styles from "./RecommendationWorkspace.module.css";

const label = (key: Criterion) => CRITERIA.find(c => c.key === key)!.label;
const signed = (number: number, digits: number) => (number > 0 ? "+" : "") + number.toFixed(digits);
function ScenarioComparison({ result }: { result: SmartphoneResult }) {
  const [index, select] = useState(1);
  const baseline = result.scenarios[0];
  const scenario = result.scenarios[index];
  const baselineRows = new Map(baseline.results.map(row => [row.id, row]));
  return <details className={styles.details}>
    <summary>Compare preference scenarios</summary>
    <p>The same phones and measurements are used in all three scenarios. Changes are relative to equal weights.</p>
    <div className="field"><label htmlFor="comparison-scenario">Scenario</label>
      <select id="comparison-scenario" className="select" value={index} onChange={event => select(Number(event.target.value))}>
        {result.scenarios.map((item, i) => <option key={item.id} value={i}>{item.label}</option>)}
      </select>
    </div>
    {scenario.weights ? <>
      <p>{result.criteria.map(key => label(key) + " " + (scenario.weights![key] * 100).toFixed(2) + "%").join(" · ")}</p>
      <p><strong>Equal-weight leaders</strong> {baseline.results.filter(row => row.rank === 1).map(row => row.label).join(", ")}</p>
      <p><strong>Scenario leaders</strong> {scenario.results.filter(row => row.rank === 1).map(row => row.label).join(", ")}</p>
      <div className={styles.scroll} role="region" aria-label="Scenario scores and positions" tabIndex={0}><table>
        <caption>Positive position change means the phone moved up.</caption>
        <thead><tr>{["Phone", "Score", "Score change", "Rank", "Positions gained"].map(h => <th key={h} scope="col">{h}</th>)}</tr></thead>
        <tbody>{scenario.results.map(row => {
          const previous = baselineRows.get(row.id)!;
          return <tr key={row.id}><th scope="row">{row.label}</th><td>{row.score.toFixed(2)}</td><td>{signed(row.score - previous.score, 2)}</td><td>{row.rank}</td><td>{signed(previous.rank - row.rank, 0)}</td></tr>;
        })}</tbody>
      </table></div>
    </> : <p role="status">Not assessable. {scenario.reason}</p>}
  </details>;
}

export function RecommendationResults({ result }: { result: SmartphoneResult }) {
  return <section className={styles.results} aria-label="Recommendation results">
    <h2>{result.eligibleCount ? "Your shortlist" : "No eligible phones"}</h2>
    {result.matches.length > 0 && <p>Showing {result.matches.length} of {result.eligibleCount} eligible examples. Scores range from 0 to 1.</p>}
    {result.constants.length > 0 && <p>Same value across all matches: {result.constants.map(label).join(", ")}. These fields carry no weight here.</p>}
    {result.unranked.length > 0 && <div className="glass-panel card"><p>These phones meet your requirements. No measure varies, so a relative score or scenario ranking cannot be calculated.</p>
      {result.unranked.map(p => <p key={p.id}><Link href={`/phones/${p.slug}`}>{p.name}</Link></p>)}</div>}
    {!result.eligibleCount && <p>Broaden a requirement or remove a filter. Phones need a recorded price and battery capacity to enter this comparison.</p>}
    {result.excluded.length > 0 && <details className={styles.details}><summary>Excluded phones ({result.excluded.length})</summary>
      <ul>{result.excluded.map((p, i) => <li key={i}>{p.name} — {p.reason}</li>)}</ul></details>}
    {result.scenarios.length > 0 && <ScenarioComparison result={result} />}
    {result.matches.map(({ phone, rank, score }) => <article className={`glass-panel ${styles.match}`} key={phone.id}>
      <div className={styles.matchTop}><div><span className="section-label">Rank {rank}</span><h3>{phone.name}</h3>
        <p>{formatPhp(phone.price)} · {phone.battery?.toLocaleString("en-PH")} mAh</p></div>
        <div className={styles.overall}><strong>{score.overall.toFixed(2)}</strong><span>Weighted score</span></div></div>
      <details className={styles.details}><summary>Calculation and sources</summary>
        <p>{[phone.ram && phone.ram + " GB RAM", phone.storage && phone.storage + " GB storage"].filter(Boolean).join(" · ") || "Memory configuration unrecorded"}</p>
        <div className={styles.scroll} role="region" aria-label={phone.name + " calculation"} tabIndex={0}><table>
          <thead><tr>{["Measure", "Value", "Eligible range", "Normalized", "Weight", "Contribution"].map(h => <th key={h} scope="col">{h}</th>)}</tr></thead>
          <tbody>{result.criteria.map(key => {
            const c = score.criteria[key]!;
            const range = result.ranges[key]!;
            return <tr key={key}><th scope="row">{c.label}</th><td>{key === "price" ? formatPhp(phone.price) : phone.battery + " mAh"}</td><td>{range.minimum}–{range.maximum}</td><td>{c.normalizedScore.toFixed(2)}</td><td>{(c.weight * 100).toFixed(2)}%</td><td>{c.weightedContribution.toFixed(2)}</td></tr>;
          })}</tbody></table></div>
        <p>Illustrative catalog values. The price and capacity lack individual source and retrieval records.</p>
        {phone.sourceUrl && <p><a href={phone.sourceUrl} rel="noreferrer" target="_blank">Model reference</a> · {phone.fetchedAt ? phone.fetchedAt.slice(0, 10) : "Retrieval date unrecorded"}</p>}
      </details>
      <div className="button-row"><Link href={`/compare?left=${phone.slug}`} className="button">Compare</Link>
        <Link href={`/phones/${phone.slug}`} className="button-secondary">Specifications</Link><FavoriteButton phoneId={phone.id} variant="full" /></div>
    </article>)}
  </section>;
}
