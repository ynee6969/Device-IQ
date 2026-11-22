import assert from "node:assert/strict";

import { ACTIVE_RECOMMENDATION_CRITERIA, DEFAULT_WEIGHTS } from "@/lib/recommendation/criteria";
import { filterEligibleSmartphones } from "@/lib/recommendation/eligibility";
import { normalizePhoneCriteria, normalizeCost } from "@/lib/recommendation/normalization";
import { rankUnderWeights } from "@/lib/recommendation/ranking";
import { calculateWeightedScore, normalizeWeights } from "@/lib/recommendation/scoring";
import type { CriterionWeight, DecisionConstraints } from "@/lib/recommendation/types";

const phones = [
  { id: "a", label: "Aster One", brand: "Aster", model: "One", os: "Android", price: 10_000, performanceScore: 80, cameraScore: 60, battery: 4_000, ram: 8 },
  { id: "b", label: "Beryl Two", brand: "Beryl", model: "Two", os: "Android", price: 20_000, performanceScore: 70, cameraScore: 90, battery: 5_000, ram: 12 },
  { id: "c", label: "Cedar Three", brand: "Cedar", model: "Three", os: "iOS", price: 30_000, performanceScore: 90, cameraScore: 80, battery: 5_000, ram: 8 },
  { id: "missing", label: "Dune Four", brand: "Dune", model: "Four", os: "Android", price: 15_000, performanceScore: 75, cameraScore: 80, battery: null, ram: 8 }
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
assert.deepEqual(normalized.activeCriteria, ["price", "performance", "battery", "camera"]);
assert.equal(normalized.normalizedScores.get("a")?.price, 1);
assert.equal(normalized.normalizedScores.get("a")?.performance, 1);
assert.equal(normalized.normalizedScores.get("a")?.battery, 0);
assert.equal(normalized.normalizedScores.get("a")?.camera, 0);
assert.equal(normalized.normalizedScores.get("b")?.price, 0);
assert.equal(normalized.normalizedScores.get("b")?.performance, 0);
assert.equal(normalized.normalizedScores.get("b")?.battery, 1);
assert.equal(normalized.normalizedScores.get("b")?.camera, 1);

assert.equal(normalizeCost(10_000, 10_000, 20_000), 1);
assert.equal(normalizeCost(20_000, 10_000, 20_000), 0);

const enteredWeights: CriterionWeight = { price: 40, performance: 30, battery: 20, camera: 10 };
const effectiveWeights = normalizeWeights(enteredWeights, ACTIVE_RECOMMENDATION_CRITERIA);
assert.equal(effectiveWeights.price, 0.4);
assert.equal(effectiveWeights.performance, 0.3);
assert.equal(effectiveWeights.battery, 0.2);
assert.equal(effectiveWeights.camera, 0.1);

const scoreA = calculateWeightedScore(normalized.normalizedScores.get("a")!, effectiveWeights, ACTIVE_RECOMMENDATION_CRITERIA);
const scoreB = calculateWeightedScore(normalized.normalizedScores.get("b")!, effectiveWeights, ACTIVE_RECOMMENDATION_CRITERIA);
assert.equal(scoreA.overall, 0.7);
assert.equal(scoreA.criteria.price?.weightedContribution, 0.4);
assert.equal(scoreA.criteria.performance?.weightedContribution, 0.3);
assert.equal(scoreA.criteria.battery?.weightedContribution, 0);
assert.equal(scoreB.overall, 0.3);

// Equal values receive the same score and do not change a phone's relative rank.
const constantData = normalizePhoneCriteria(
  [
    { id: "east", price: 12_000, battery: 4_000 },
    { id: "west", price: 12_000, battery: 5_000 }
  ],
  ["price", "battery"]
);
assert.deepEqual(constantData.constantCriteria, ["price"]);
assert.deepEqual(constantData.activeCriteria, ["price", "battery"]);
assert.equal(constantData.normalizedScores.get("east")?.price, 1);
assert.equal(constantData.normalizedScores.get("west")?.price, 1);
const batteryOnlyWeights = normalizeWeights({ price: 0, performance: 0, battery: 100, camera: 0 }, ["battery"]);
assert.equal(batteryOnlyWeights.battery, 1);
assert.equal(
  calculateWeightedScore(constantData.normalizedScores.get("west")!, batteryOnlyWeights, ["battery"]).overall,
  1
);

assert.throws(
  () => normalizeWeights({ price: 0, performance: 0, battery: 0, camera: 0 }, ACTIVE_RECOMMENDATION_CRITERIA),
  /positive weight/
);
assert.throws(
  () => normalizeWeights({ price: -1, performance: 0, battery: 2, camera: 0 }, ACTIVE_RECOMMENDATION_CRITERIA),
  /non-negative/
);
assert.throws(
  () => normalizeWeights({ price: 50, performance: 1, battery: 50, camera: 0 }, ["price", "battery"]),
  /unavailable/
);
assert.equal(DEFAULT_WEIGHTS.price, 0.25);
assert.equal(DEFAULT_WEIGHTS.performance, 0.25);
assert.equal(DEFAULT_WEIGHTS.battery, 0.25);
assert.equal(DEFAULT_WEIGHTS.camera, 0.25);

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
  () => normalizeWeights({ ...DEFAULT_WEIGHTS, price: Number.NaN }, ACTIVE_RECOMMENDATION_CRITERIA),
  /finite/
);

console.log("Smartphone recommendation checks passed: filters, catalog ratings, normalization, weights, scores, and ties.");
