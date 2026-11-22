import assert from "node:assert/strict";

import { ACTIVE_RECOMMENDATION_CRITERIA, DEFAULT_WEIGHTS } from "@/lib/recommendation/criteria";
import { filterEligibleSmartphones } from "@/lib/recommendation/eligibility";
import { normalizePhoneCriteria, normalizeCost } from "@/lib/recommendation/normalization";
import { analyzePreferenceScenarios, rankUnderWeights } from "@/lib/recommendation/sensitivity";
import { calculateWeightedScore, normalizeWeights } from "@/lib/recommendation/scoring";
import type { CriterionWeight, DecisionConstraints } from "@/lib/recommendation/types";

const phones = [
  { id: "a", label: "Aster One", brand: "Aster", model: "One", os: "Android", price: 10_000, battery: 4_000, ram: 8 },
  { id: "b", label: "Beryl Two", brand: "Beryl", model: "Two", os: "Android", price: 20_000, battery: 5_000, ram: 12 },
  { id: "c", label: "Cedar Three", brand: "Cedar", model: "Three", os: "iOS", price: 30_000, battery: 5_000, ram: 8 },
  { id: "missing", label: "Dune Four", brand: "Dune", model: "Four", os: "Android", price: 15_000, battery: null, ram: 8 }
];

const constraints: DecisionConstraints = {
  minPrice: 10_000,
  maxPrice: 20_000,
  brands: [],
  os: "any"
};
const eligible = filterEligibleSmartphones(phones, constraints);
assert.deepEqual(eligible.map((phone) => phone.id), ["a", "b", "missing"]);

const normalized = normalizePhoneCriteria(eligible, ACTIVE_RECOMMENDATION_CRITERIA);
assert.deepEqual(normalized.comparisonPhones.map((phone) => phone.id), ["a", "b"]);
assert.equal(normalized.missingValueCount, 1);
assert.deepEqual(normalized.activeCriteria, ["price", "battery"]);
assert.equal(normalized.normalizedScores.get("a")?.price, 1);
assert.equal(normalized.normalizedScores.get("a")?.battery, 0);
assert.equal(normalized.normalizedScores.get("b")?.price, 0);
assert.equal(normalized.normalizedScores.get("b")?.battery, 1);

// Independent hand calculation: (10,000 is the minimum; 20,000 is the maximum).
assert.equal(normalizeCost(10_000, 10_000, 20_000), 1);
assert.equal(normalizeCost(20_000, 10_000, 20_000), 0);
assert.equal((4_000 - 4_000) / (5_000 - 4_000), 0);
assert.equal((5_000 - 4_000) / (5_000 - 4_000), 1);

const enteredWeights: CriterionWeight = { price: 60, performance: 0, battery: 40, camera: 0 };
const effectiveWeights = normalizeWeights(enteredWeights, ["price", "battery"]);
assert.equal(effectiveWeights.price, 0.6);
assert.equal(effectiveWeights.battery, 0.4);
assert.equal(effectiveWeights.performance, 0);
assert.equal(effectiveWeights.camera, 0);

const scoreA = calculateWeightedScore(normalized.normalizedScores.get("a")!, effectiveWeights, ["price", "battery"]);
const scoreB = calculateWeightedScore(normalized.normalizedScores.get("b")!, effectiveWeights, ["price", "battery"]);
assert.equal(scoreA.overall, 0.6);
assert.equal(scoreA.criteria.price?.weightedContribution, 0.6);
assert.equal(scoreA.criteria.battery?.weightedContribution, 0);
assert.equal(scoreB.overall, 0.4);

// A criterion with no range is removed, and the remaining user weight is rescaled.
const constantData = normalizePhoneCriteria(
  [
    { id: "east", price: 12_000, battery: 4_000 },
    { id: "west", price: 12_000, battery: 5_000 }
  ],
  ["price", "battery"]
);
assert.deepEqual(constantData.constantCriteria, ["price"]);
assert.deepEqual(constantData.activeCriteria, ["battery"]);
const reweighted = normalizeWeights(enteredWeights, ["battery"], ["price"]);
assert.equal(reweighted.battery, 1);
assert.equal(reweighted.price, 0);
assert.equal(
  calculateWeightedScore(constantData.normalizedScores.get("west")!, reweighted, ["battery"]).overall,
  1
);

assert.throws(
  () => normalizeWeights({ price: 0, performance: 0, battery: 0, camera: 0 }, ["price", "battery"]),
  /positive weight/
);
assert.throws(
  () => normalizeWeights({ price: -1, performance: 0, battery: 2, camera: 0 }, ["price", "battery"]),
  /non-negative/
);
assert.throws(
  () => normalizeWeights({ price: 50, performance: 1, battery: 50, camera: 0 }, ["price", "battery"]),
  /unavailable/
);
assert.equal(DEFAULT_WEIGHTS.price, 0.5);

const scenarioPhones = [
  { id: "a", label: "Aster One", price: 10_000, battery: 4_000 },
  { id: "b", label: "Beryl Two", price: 20_000, battery: 5_000 },
  { id: "c", label: "Cedar Three", price: 30_000, battery: 5_000 }
];
const scenarioNormalization = normalizePhoneCriteria(scenarioPhones, ["price", "battery"]);
const scenarioItems = scenarioNormalization.comparisonPhones.map((phone) => ({
  id: phone.id,
  label: phone.label,
  normalizedScores: scenarioNormalization.normalizedScores.get(phone.id)!
}));
const scenarios = analyzePreferenceScenarios(scenarioItems, ["price", "battery"]).scenarios;
assert.deepEqual(scenarios.map((scenario) => scenario.id), ["equal", "affordability", "performance"]);
assert.deepEqual(scenarios.map((scenario) => scenario.status), ["available", "available", "not_assessable"]);
assert.equal(scenarios[0].weights?.price, 0.5);
assert.equal(scenarios[0].weights?.battery, 0.5);
assert.equal(scenarios[0].results.find((row) => row.id === "b")?.score, 0.75);
assert.equal(scenarios[1].weights?.price, 0.6);
assert.equal(scenarios[1].weights?.battery, 0.4);
assert.equal(scenarios[1].results.find((row) => row.id === "a")?.score, 0.6);
assert.equal(scenarios[1].results.find((row) => row.id === "b")?.score, 0.7);
assert.match(scenarios[2].reason ?? "", /performance is unavailable/);

const tied = rankUnderWeights(
  [
    { id: "z", label: "Zeta", normalizedScores: { price: 0.5 } },
    { id: "a", label: "Alpha", normalizedScores: { price: 0.5000005 } }
  ],
  { price: 1, performance: 0, battery: 0, camera: 0 },
  ["price"]
);
assert.deepEqual(tied.map((row) => row.label), ["Alpha", "Zeta"]);
assert.deepEqual(tied.map((row) => row.rank), [1, 1]);

assert.throws(
  () => normalizeWeights({ ...DEFAULT_WEIGHTS, price: Number.NaN }, ["price", "battery"]),
  /finite/
);

console.log("Smartphone recommendation checks passed: filters, missing values, normalization, weights, scores, ties, and preference scenarios.");
