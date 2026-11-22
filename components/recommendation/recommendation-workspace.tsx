"use client";

import Link from "next/link";
import { LoaderCircle, SlidersHorizontal } from "lucide-react";
import { useState } from "react";

import { FavoriteButton } from "@/components/phones/favorite-button";
import { CRITERIA, DEFAULT_WEIGHTS } from "@/lib/recommendation/criteria";
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
}>;

const presets: Array<{ label: string; weights: CriterionWeight }> = [
  { label: "Balanced", weights: { price: 25, performance: 25, battery: 25, camera: 25 } },
  { label: "Best value", weights: { price: 55, performance: 15, battery: 15, camera: 15 } },
  { label: "Gaming", weights: { price: 10, performance: 60, battery: 20, camera: 10 } },
  { label: "Photography", weights: { price: 10, performance: 15, battery: 15, camera: 60 } },
  { label: "Long battery", weights: { price: 10, performance: 15, battery: 60, camera: 15 } }
];

const initialWeights = Object.fromEntries(
  Object.entries(DEFAULT_WEIGHTS).map(([key, value]) => [key, value * 100])
) as CriterionWeight;

export function RecommendationWorkspace({ brands }: { brands: string[] }) {
  const [budget, setBudget] = useState("");
  const [minBudget, setMinBudget] = useState("");
  const [brand, setBrand] = useState("");
  const [osPreference, setOsPreference] = useState<"any" | "android" | "ios">("any");
  const [minRam, setMinRam] = useState("");
  const [minBattery, setMinBattery] = useState("");
  const [weightInputs, setWeightInputs] = useState(initialWeights);
  const [result, setResult] = useState<Result | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  function clearResults() {
    setResult(null);
    setError(null);
  }

  function setWeight(key: Criterion, value: number) {
    const nextValue = Math.max(0, Math.min(100, Math.round(value)));
    const otherCriteria = CRITERIA.map(({ key: criterion }) => criterion).filter((criterion) => criterion !== key);
    const previousTotal = otherCriteria.reduce((total, criterion) => total + weightInputs[criterion], 0);
    const remaining = 100 - nextValue;
    let assigned = 0;
    const nextWeights = { ...weightInputs, [key]: nextValue };

    otherCriteria.forEach((criterion, index) => {
      const isLast = index === otherCriteria.length - 1;
      const share = isLast
        ? remaining - assigned
        : previousTotal > 0
          ? Math.round((weightInputs[criterion] / previousTotal) * remaining)
          : Math.floor(remaining / otherCriteria.length);
      nextWeights[criterion] = Math.max(0, share);
      assigned += nextWeights[criterion];
    });

    setWeightInputs(nextWeights);
    clearResults();
  }

  function applyPreset(weights: CriterionWeight) {
    setWeightInputs({ ...weights });
    clearResults();
  }

  async function submit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(null);

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
      setError("Check your filters. The minimum price must be lower than the maximum price.");
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
          weights: weightInputs,
          limit: 10
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
      <header className={styles.intro}>
        <span className="section-label">Find your next phone</span>
        <h1 className="section-title">A shortlist built around what matters to you.</h1>
        <p className="section-copy">Set a few requirements, choose your priorities, and compare the closest matches.</p>
      </header>

      <form className={`glass-panel ${styles.form}`} onSubmit={submit}>
        <fieldset className={styles.group}>
          <legend>Find your fit</legend>
          <p className="muted">Narrow the catalog by price, brand, and key specifications.</p>
          <div className={styles.fields}>
            <label className="field">
              <span className={styles.fieldTitle}>Minimum price <span className={styles.unit}>PHP</span></span>
              <input className="input" type="number" min="1" step="100" inputMode="numeric" placeholder="No minimum" value={minBudget} onChange={(event) => { setMinBudget(event.target.value); clearResults(); }} />
            </label>
            <label className="field">
              <span className={styles.fieldTitle}>Maximum price <span className={styles.unit}>PHP</span></span>
              <input className="input" type="number" min="1" step="100" inputMode="numeric" placeholder="No maximum" value={budget} onChange={(event) => { setBudget(event.target.value); clearResults(); }} />
            </label>
            <label className="field">
              Brand
              <select className="select" value={brand} onChange={(event) => { setBrand(event.target.value); clearResults(); }}>
                <option value="">Any brand</option>
                {brands.map((item) => <option key={item}>{item}</option>)}
              </select>
            </label>
            <label className="field">
              Operating system
              <select className="select" value={osPreference} onChange={(event) => { setOsPreference(event.target.value as typeof osPreference); clearResults(); }}>
                <option value="any">Any system</option>
                <option value="android">Android</option>
                <option value="ios">iOS</option>
              </select>
            </label>
            <label className="field">
              <span className={styles.fieldTitle}>Minimum RAM <span className={styles.unit}>GB</span></span>
              <input className="input" type="number" min="1" step="1" inputMode="numeric" placeholder="Any amount" value={minRam} onChange={(event) => { setMinRam(event.target.value); clearResults(); }} />
            </label>
            <label className="field">
              <span className={styles.fieldTitle}>Minimum battery <span className={styles.unit}>mAh</span></span>
              <input className="input" type="number" min="1" step="100" inputMode="numeric" placeholder="Any capacity" value={minBattery} onChange={(event) => { setMinBattery(event.target.value); clearResults(); }} />
            </label>
          </div>
        </fieldset>

        <fieldset className={styles.group}>
          <legend>Set your priorities</legend>
          <div className={styles.priorityIntro}>
            <p className="muted">Move a slider. The other priorities adjust to keep the total at 100%.</p>
            <span className={styles.total}><strong>100%</strong><span>Total</span></span>
          </div>
          <div className={styles.presets} aria-label="Priority presets">
            {presets.map((preset) => {
              const selected = CRITERIA.every(({ key }) => weightInputs[key] === preset.weights[key]);
              return (
                <button
                  key={preset.label}
                  type="button"
                  className={selected ? styles.presetActive : styles.preset}
                  aria-pressed={selected}
                  onClick={() => applyPreset(preset.weights)}
                >
                  {preset.label}
                </button>
              );
            })}
          </div>
          <div className={styles.weights}>
            {CRITERIA.map((criterion) => (
              <div className={styles.weightCard} key={criterion.key}>
                <div className={styles.weightHeading}>
                  <label htmlFor={`priority-${criterion.key}`}>{criterion.label}</label>
                  <output htmlFor={`priority-${criterion.key}`}>{weightInputs[criterion.key]}%</output>
                </div>
                <input
                  id={`priority-${criterion.key}`}
                  type="range"
                  min="0"
                  max="100"
                  step="1"
                  value={weightInputs[criterion.key]}
                  aria-label={`${criterion.label} priority`}
                  onChange={(event) => setWeight(criterion.key, Number(event.target.value))}
                />
                <small>{criterion.key === "price" ? "Lower is better · PHP" : criterion.key === "battery" ? "Capacity · mAh" : "DeviceIQ catalog rating · 0–100"}</small>
              </div>
            ))}
          </div>
        </fieldset>

        {error ? <p className={styles.error} role="alert">{error}</p> : null}
        <button className={`button magnetic-button ${styles.submit}`} disabled={loading}>
          {loading ? <><LoaderCircle className="spin" size={16} /> Finding matches…</> : <><SlidersHorizontal size={16} /> Show my matches</>}
        </button>
      </form>

      {result ? (
        <p className="sr-only" role="status" aria-live="polite">
          {result.eligibleCount} phone matches are ready.
        </p>
      ) : null}
      {result ? (
        <section className={styles.results} role="region" aria-label="Phone matches">
          <div className={styles.resultHeader}>
            <div>
              <span className="section-label">Your shortlist</span>
              <h2>{result.eligibleCount ? `${result.eligibleCount} ${result.eligibleCount === 1 ? "match" : "matches"}` : "No matches yet"}</h2>
              <p className="muted">Match scores compare phones in this shortlist using your priorities.</p>
            </div>
            <span className={styles.total}><strong>{result.eligibleCount}</strong><span>phones</span></span>
          </div>
          {result.excludedMissingCount > 0 ? (
            <p className={styles.dataNote}>
              {result.excludedMissingCount} {result.excludedMissingCount === 1 ? "phone was" : "phones were"} left out because one or more ratings are missing.
            </p>
          ) : null}

          {result.matches.length ? (
            result.matches.map((match) => (
              <article className={`glass-panel ${styles.match}`} key={match.phone.id}>
                <div className={styles.matchTop}>
                  <div>
                    <span className="chip">Match #{match.rank}</span>
                    <h3>{getPhoneDisplayName(match.phone.brand, match.phone.model)}</h3>
                    <p className="muted">
                      {formatPhp(match.phone.price)}
                      {match.phone.battery ? ` · ${match.phone.battery.toLocaleString()} mAh` : ""}
                      {match.phone.ram ? ` · ${match.phone.ram} GB RAM` : ""}
                      {match.phone.storage ? ` · ${match.phone.storage} GB storage` : ""}
                    </p>
                  </div>
                  <div className={styles.overall}>
                    <strong>{Math.round(match.score.overallPercentage)}%</strong>
                    <span>Match</span>
                  </div>
                </div>
                <div className={styles.breakdown}>
                  {result.criteria.map((key) => {
                    const criterion = match.score.criteria[key];
                    if (!criterion) return null;
                    const value = Math.round(criterion.normalizedScore * 100);
                    return (
                      <div className={styles.breakdownItem} key={key}>
                        <div className={styles.breakdownHeading}>
                          <strong>{criterion.label}</strong>
                          <span>{value}%</span>
                        </div>
                        <div className={styles.bar} aria-hidden="true"><span style={{ width: `${value}%` }} /></div>
                        <small>{Math.round(criterion.weight * 100)}% of your priorities</small>
                      </div>
                    );
                  })}
                </div>
                <div className="button-row">
                  <Link className="button-secondary" href={`/phones/${match.phone.slug}`}>View details</Link>
                  <Link className="button" href={`/compare?left=${match.phone.slug}`}>Compare</Link>
                  <FavoriteButton phoneId={match.phone.id} variant="full" />
                </div>
              </article>
            ))
          ) : (
            <div className={`glass-panel empty-state ${styles.empty}`}>
              {result.excludedMissingCount > 0
                ? "Some phones meet these filters but are missing one or more ratings. Try changing a filter to see more options."
                : "No phones match these filters. Try raising the maximum price or removing a requirement."}
            </div>
          )}
        </section>
      ) : null}
    </div>
  );
}
