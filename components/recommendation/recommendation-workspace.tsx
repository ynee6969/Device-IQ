"use client";

import Link from "next/link";
import { LoaderCircle, SlidersHorizontal } from "lucide-react";
import { useState } from "react";

import { FavoriteButton } from "@/components/phones/favorite-button";
import {
  ACTIVE_RECOMMENDATION_CRITERIA,
  CRITERIA,
  DEFAULT_WEIGHTS
} from "@/lib/recommendation/criteria";
import type { Criterion, CriterionWeight, RecommendationResult } from "@/lib/recommendation/types";
import { formatPhp } from "@/lib/utils/format";
import { getPhoneDisplayName } from "@/lib/utils/phone-presentation";
import styles from "./RecommendationWorkspace.module.css";

type Result = RecommendationResult<{
  id: string;
  slug: string;
  brand: string;
  model: string;
  price: number;
  ram: number | null;
  storage: number | null;
  battery: number | null;
  sources?: Array<{ sourceUrl: string; fetchedAt: string | null }>;
}>;

const initialWeights = Object.fromEntries(
  Object.entries(DEFAULT_WEIGHTS).map(([key, value]) => [key, String(value * 100)])
) as Record<Criterion, string>;

export function RecommendationWorkspace({ brands }: { brands: string[] }) {
  const [budget, setBudget] = useState("");
  const [minBudget, setMinBudget] = useState("");
  const [brand, setBrand] = useState("");
  const [osPreference, setOsPreference] = useState<"any" | "android" | "ios">("any");
  const [minRam, setMinRam] = useState("");
  const [minBattery, setMinBattery] = useState("");
  const [weightInputs, setWeightInputs] = useState(initialWeights);
  const [sensitivity, setSensitivity] = useState(true);
  const [result, setResult] = useState<Result | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const numericWeights = Object.fromEntries(
    CRITERIA.map(({ key }) => [key, weightInputs[key].trim() === "" ? 0 : Number(weightInputs[key])])
  ) as CriterionWeight;
  const totalPoints = Object.values(numericWeights).reduce((total, value) => total + value, 0);
  const totalValid = Object.values(numericWeights).every((value) => Number.isFinite(value) && value >= 0) && totalPoints > 0;

  function setEqualWeights() {
    setWeightInputs(
      Object.fromEntries(
        CRITERIA.map(({ key }) => [
          key,
          String(ACTIVE_RECOMMENDATION_CRITERIA.includes(key) ? 100 / ACTIVE_RECOMMENDATION_CRITERIA.length : 0)
        ])
      ) as Record<Criterion, string>
    );
  }

  async function submit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(null);
    if (!totalValid) {
      setError("Enter finite, non-negative relative weights and assign a positive total to available criteria.");
      return;
    }

    const numberOrUndefined = (value: string) => (value.trim() ? Number(value) : undefined);
    const min = numberOrUndefined(minBudget);
    const max = numberOrUndefined(budget);
    const minimumRam = numberOrUndefined(minRam);
    const minimumBattery = numberOrUndefined(minBattery);
    if (
      [min, max, minimumRam, minimumBattery].some(
        (value) => value !== undefined && (!Number.isFinite(value) || value <= 0)
      ) ||
      (min !== undefined && max !== undefined && min > max)
    ) {
      setError("Enter valid positive requirements. Minimum budget cannot exceed maximum budget.");
      return;
    }

    setLoading(true);
    try {
      const response = await fetch("/api/recommend", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          budget: max,
          minBudget: min,
          brands: brand ? [brand] : [],
          osPreference,
          minRam: minimumRam,
          minBattery: minimumBattery,
          weights: numericWeights,
          limit: 10,
          includeSensitivity: sensitivity
        })
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.error ?? "Could not create recommendations.");
      setResult(data as Result);
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Could not create recommendations.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className={styles.scope}>
      <header className="stack">
        <span className="section-label">Smartphone recommendation</span>
        <h1 className="section-title">Choose a smartphone using your requirements and priorities.</h1>
        <p className="section-copy">
          Mandatory filters determine eligibility first. Price and listed battery capacity are then normalized
          across the eligible records and combined with your effective weights.
        </p>
      </header>

      <form className="glass-panel" onSubmit={submit}>
        <div className={styles.formHeader}>
          <div>
            <h2>1. Set requirements</h2>
            <p className="muted">These filters are applied before score ranges are calculated.</p>
          </div>
          <span className="chip">Eligibility filters</span>
        </div>
        <div className={styles.fields}>
          <label className="field">
            Maximum budget (PHP)
            <input className="input" type="number" min="1" value={budget} onChange={(event) => setBudget(event.target.value)} />
          </label>
          <label className="field">
            Minimum budget (PHP)
            <input className="input" type="number" min="1" value={minBudget} onChange={(event) => setMinBudget(event.target.value)} />
          </label>
          <label className="field">
            Brand
            <select className="select" value={brand} onChange={(event) => setBrand(event.target.value)}>
              <option value="">Any brand</option>
              {brands.map((item) => <option key={item}>{item}</option>)}
            </select>
          </label>
          <label className="field">
            Operating system
            <select className="select" value={osPreference} onChange={(event) => setOsPreference(event.target.value as typeof osPreference)}>
              <option value="any">Any OS</option>
              <option value="android">Android</option>
              <option value="ios">iOS</option>
            </select>
          </label>
          <label className="field">
            Minimum RAM (GB)
            <input className="input" type="number" min="1" value={minRam} onChange={(event) => setMinRam(event.target.value)} />
          </label>
          <label className="field">
            Minimum battery capacity (mAh)
            <input className="input" type="number" min="1" value={minBattery} onChange={(event) => setMinBattery(event.target.value)} />
          </label>
        </div>

        <div className={styles.formHeader}>
          <div>
            <h2>2. Set relative weights</h2>
            <p className="muted">
              Enter non-negative points. The system divides each active value by the active total; it displays the
              effective weights with the results.
            </p>
          </div>
          <span className={`chip ${totalValid ? styles.valid : styles.invalid}`}>
            Entered total: {Number.isFinite(totalPoints) ? totalPoints.toFixed(1) : "Invalid"} points
          </span>
        </div>
        <div className={styles.presetRow}>
          <button type="button" className="button-secondary" onClick={setEqualWeights}>Use equal weights</button>
        </div>
        <div className={styles.weights}>
          {CRITERIA.map((criterion) => {
            const active = ACTIVE_RECOMMENDATION_CRITERIA.includes(criterion.key);
            return (
              <label className="field" key={criterion.key}>
                {criterion.label} ({criterion.unit})
                <div className={styles.weightInput}>
                  <input
                    className="input"
                    type="number"
                    min="0"
                    step="any"
                    value={weightInputs[criterion.key]}
                    disabled={!active}
                    aria-describedby={!active ? `${criterion.key}-unavailable` : undefined}
                    onChange={(event) => setWeightInputs((current) => ({ ...current, [criterion.key]: event.target.value }))}
                  />
                  <span>{active ? "points" : "unavailable"}</span>
                </div>
                {!active ? <small className={styles.unavailable} id={`${criterion.key}-unavailable`}>{criterion.description}</small> : null}
              </label>
            );
          })}
        </div>
        <label className={styles.check}>
          <input type="checkbox" checked={sensitivity} onChange={(event) => setSensitivity(event.target.checked)} />
          Include the three proposal preference scenarios
          <span className="muted"> Equal-weight, affordability-focused, and performance-focused.</span>
        </label>
        {error ? <p className={styles.error} role="alert">{error}</p> : null}
        <button className="button magnetic-button" disabled={loading || !totalValid}>
          {loading ? <><LoaderCircle className="spin" size={16} /> Ranking smartphones…</> : <><SlidersHorizontal size={16} /> Get recommendations</>}
        </button>
      </form>

      {result ? (
        <p className="sr-only" role="status" aria-live="polite">
          {result.eligibleCount} smartphone results are ready. {result.excludedMissingCount} records were excluded for missing active values.
        </p>
      ) : null}
      {result ? (
        <section className={styles.results} role="region" aria-label="Smartphone recommendation results">
          <div className={styles.resultHeader}>
            <div>
              <span className="section-label">Eligible smartphone results</span>
              <h2>{result.eligibleCount} smartphone{result.eligibleCount === 1 ? " has" : "s have"} complete values for the active criteria.</h2>
              <p className="muted">{result.formula}. A higher score means a stronger match under these inputs and weights.</p>
            </div>
            <span className="chip">{result.preferences.source === "user" ? "Entered weights normalized" : "Equal-weight default"}</span>
          </div>
          <div className={styles.notice} role="note">
            This is a calculation demonstration using seeded catalog records. Product prices and specifications do not
            yet have complete field-level sources and retrieval dates, so these scores are not verified market
            recommendations or completed research results.
          </div>
          <p className={styles.dataCounts}>
            {result.filterEligibleCount} smartphone{result.filterEligibleCount === 1 ? " passes" : "s pass"} the filters;
            {` ${result.excludedMissingCount} excluded for missing active values.`}
            {result.criteria.length ? ` Active criteria: ${result.criteria.map((key) => CRITERIA.find((item) => item.key === key)?.label).join(", ")}.` : " No criterion currently distinguishes the eligible set."}
          </p>
          <div className={styles.effectiveWeights}>
            Effective weights: {result.criteria.map((key) => {
              const label = CRITERIA.find((item) => item.key === key)?.label ?? key;
              return `${label} ${(result.weights[key] * 100).toFixed(2)}%`;
            }).join(" · ")}
            {result.constantCriteriaRemoved.length
              ? ` · Constant criteria removed: ${result.constantCriteriaRemoved.map((key) => CRITERIA.find((item) => item.key === key)?.label ?? key).join(", ")}`
              : ""}
          </div>
          <div className={styles.constraints}>
            Applied filters: {result.constraints.maxPrice !== undefined ? `up to ${formatPhp(result.constraints.maxPrice)}` : "any budget"}
            {result.constraints.minPrice !== undefined ? ` · from ${formatPhp(result.constraints.minPrice)}` : ""}
            {result.constraints.brands.length ? ` · ${result.constraints.brands.join(", ")}` : ""}
            {result.constraints.os !== "any" ? ` · ${result.constraints.os}` : ""}
            {result.constraints.minRam !== undefined ? ` · ${result.constraints.minRam}GB RAM+` : ""}
            {result.constraints.minBattery !== undefined ? ` · ${result.constraints.minBattery}mAh+` : ""}
          </div>
          {result.unavailableCriteria.length ? (
            <div className={styles.unavailableNotice}>
              {result.unavailableCriteria.map(({ criterion, reason }) => (
                <p key={criterion}><strong>{CRITERIA.find((item) => item.key === criterion)?.label}:</strong> {reason}</p>
              ))}
            </div>
          ) : null}
          {result.matches.length ? (
            result.matches.map((match) => (
              <article className={`glass-panel ${styles.match}`} key={match.phone.id}>
                <div className={styles.matchTop}>
                  <div>
                    <span className="chip">Rank #{match.rank}</span>
                    <h3>{getPhoneDisplayName(match.phone.brand, match.phone.model)}</h3>
                    <p className="muted">
                      {formatPhp(match.phone.price)} · {match.phone.battery ? `${match.phone.battery} mAh battery capacity` : "Battery capacity not recorded"}
                      {match.phone.ram || match.phone.storage
                        ? ` · ${match.phone.ram ? `${match.phone.ram} GB RAM` : "RAM not recorded"} / ${match.phone.storage ? `${match.phone.storage} GB storage` : "storage not recorded"}`
                        : " · Configuration not recorded"}
                    </p>
                  </div>
                  <div className={styles.overall}>
                    <span>Weighted match score</span>
                    <strong>{match.score.overall.toFixed(2)}</strong>
                    <small>0 to 1</small>
                  </div>
                </div>
                <p className="muted">Higher scores indicate a stronger match under the selected criteria, catalog values, and effective weights.</p>
                <div className={styles.breakdown}>
                  {result.criteria.map((key) => {
                    const criterion = match.score.criteria[key];
                    if (!criterion) return null;
                    return (
                      <div key={key}>
                        <strong>{criterion.label}</strong>
                        <span>Normalized: {criterion.normalizedScore.toFixed(2)}</span>
                        <span>Weight: {(criterion.weight * 100).toFixed(2)}%</span>
                        <span>Contribution: {criterion.weightedContribution.toFixed(2)}</span>
                      </div>
                    );
                  })}
                </div>
                {match.phone.sources?.[0]?.sourceUrl ? (
                  <small className={styles.provenance}>
                    Phone reference: <a href={match.phone.sources[0].sourceUrl} target="_blank" rel="noreferrer">open source</a>
                    {match.phone.sources[0].fetchedAt
                      ? ` · retrieved ${new Intl.DateTimeFormat("en-PH", { dateStyle: "medium" }).format(new Date(match.phone.sources[0].fetchedAt))}`
                      : " · retrieval date not recorded"}
                    . This phone-level reference does not verify each scored field.
                  </small>
                ) : (
                  <small className={styles.provenance}>No phone reference source or retrieval date is recorded for this entry.</small>
                )}
                <div className="button-row">
                  <Link className="button-secondary" href={`/phones/${match.phone.slug}`}>View details</Link>
                  <Link className="button" href={`/compare?left=${match.phone.slug}`}>Compare</Link>
                  <FavoriteButton phoneId={match.phone.id} variant="full" />
                </div>
              </article>
            ))
          ) : (
            <div className="glass-panel empty-state">
              {result.filterEligibleCount === 0
                ? "No smartphones meet all selected requirements. Try relaxing one of the filters."
                : "No smartphones have complete price and battery-capacity values for scoring. Missing values were not replaced with zero or an estimate."}
            </div>
          )}
          {result.sensitivity ? (
            <article className={`glass-panel ${styles.sensitivity}`}>
              <h3>Predefined preference scenarios</h3>
              <p className="muted">The smartphone set and criteria stay fixed. Each table shows both its calculated score and rank position.</p>
              {result.sensitivity.scenarios.map((scenario) => (
                <section className={styles.scenario} key={scenario.id}>
                  <h4>{scenario.label}</h4>
                  {scenario.status === "not_assessable" ? (
                    <p className={styles.unavailable}>{scenario.reason}</p>
                  ) : (
                    <>
                      <p className="muted">Weights: {result.criteria.map((key) => `${CRITERIA.find((item) => item.key === key)?.label} ${((scenario.weights?.[key] ?? 0) * 100).toFixed(2)}%`).join(" · ")}</p>
                      <ol className={styles.scenarioResults}>
                        {scenario.results.map((row) => (
                          <li key={row.id}>
                            <span>Rank {row.rank}</span>
                            <span>{row.label}</span>
                            <strong>Score {row.score.toFixed(2)}</strong>
                          </li>
                        ))}
                      </ol>
                      <small>Scores within 0.000001 share a rank; tied phones are displayed alphabetically.</small>
                    </>
                  )}
                </section>
              ))}
            </article>
          ) : null}
        </section>
      ) : null}
    </div>
  );
}
