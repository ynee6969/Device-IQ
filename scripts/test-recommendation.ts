import assert from "node:assert/strict";

import { evaluatePhones, recommendationInput } from "@/lib/services/recommendations";
import { normalizePhoneCriteria } from "@/lib/recommendation/normalization";
import { analyzePreferenceScenarios } from "@/lib/recommendation/sensitivity";
import { rankUnderWeights } from "@/lib/recommendation/ranking";
import { normalizeWeights } from "@/lib/recommendation/scoring";

const tolerance = 0.000001;
function near(actual: number | undefined, expected: number) {
  assert.ok(actual !== undefined && Math.abs(actual - expected) <= tolerance, `Expected ${expected}, received ${actual}`);
}
const common = { brand: "Example", os: "Android 14", ram: 8, storage: 128 };
const A = { ...common, id: "a", slug: "a", model: "A", price: 10000, battery: 4000 };
const B = { ...common, id: "b", slug: "b", model: "B", price: 20000, battery: 5000 };
const C = { ...common, id: "c", slug: "c", model: "C", price: 30000, battery: 4500 };
const missing = { ...A, id: "d", model: "D", battery: null };
const catalog = [A, B, C, missing];
const weights = { price: 3, battery: 2, camera: 0, performance: 0 };
const run = (input: object, devices = catalog) => evaluatePhones(devices, recommendationInput.parse(input));

// Price range 10k–30k gives A/B/C = 1, 1/2, 0. Capacity gives 0, 1, 1/2.
// At 3:2 the totals are .60, .70, .20. D is excluded before finding ranges.
const result = run({ weights });
assert.deepEqual(result.matches.map(r => [r.phone.id, r.rank]), [["b", 1], ["a", 2], ["c", 3]]);
assert.deepEqual(result.excluded.map(p => p.name), ["Example D"]);
const best = result.matches[0].score;
near(best.criteria.price?.normalizedScore, 0.5);
near(best.criteria.battery?.normalizedScore, 1);
near(best.criteria.price?.weightedContribution, 0.3);
near(best.criteria.battery?.weightedContribution, 0.4);
[result.matches[0], result.matches[1], result.matches[2]].forEach((row, i) => near(row.score.overall, [0.7, 0.6, 0.2][i]));

const boundary = run({ minBudget: 10000, budget: 20000, minRam: 8, minBattery: 4000, osPreference: "android", brands: ["Example"] });
assert.deepEqual(boundary.matches.map(row => [row.phone.id, row.rank]), [["a", 1], ["b", 1]]);
assert.equal(run({ budget: 9999 }).eligibleCount, 0);
const unknown = { ...A, os: null, ram: null };
assert.equal(evaluatePhones([unknown], recommendationInput.parse({ osPreference: "android" })).eligibleCount, 0);
assert.equal(evaluatePhones([unknown], recommendationInput.parse({ minRam: 1 })).eligibleCount, 0);
assert.equal(run({ brands: ["Other"] }).eligibleCount, 0);
const singleton = run({ budget: 10000 });
assert.deepEqual(singleton.unranked.map(p => p.id), ["a"]);
assert.equal(singleton.matches.length, 0);
const constant = run({ weights }, [A, { ...B, price: A.price }]);
assert.deepEqual(constant.constants, ["price"]);
near(constant.weights.battery, 1);
near(constant.matches[0].score.overall, 1);
assert.equal(constant.scenarios[1].status, "not_assessable");
assert.throws(() => run({ weights: { ...weights, battery: 0 } }, [A, { ...B, price: A.price }]), /same value/);
assert.throws(() => run({ weights: { ...weights, camera: 1 } }), /unavailable/);
assert.throws(() => run({ weights: { ...weights, price: 0, battery: 0 } }), /positive/);
for (const price of [-1, NaN, Infinity, undefined]) {
  assert.equal(recommendationInput.safeParse({ weights: { ...weights, price } }).success, false);
}
assert.equal(recommendationInput.safeParse({ budget: 1, minBudget: 2 }).success, false);
near(normalizeWeights({ ...weights, price: Number.MAX_VALUE, battery: Number.MAX_VALUE }, ["price", "battery"]).price, 0.5);

// Equal baseline B=.75, A=.50, C=.25. At 60% price the order is unchanged, but scores change.
assert.deepEqual(result.scenarios.map(s => s.status), ["available", "available", "not_assessable"]);
for (const [i, expected] of [[0, [.75, .5, .25]], [1, [.7, .6, .2]]] as const) {
  assert.deepEqual(result.scenarios[i].results.map(r => [r.id, r.rank]), [["b", 1], ["a", 2], ["c", 3]]);
  result.scenarios[i].results.forEach((r, j) => near(r.score, expected[j]));
}
// Manuscript appendix: hypothetical prices 20k/30k, benchmark 80/100.
const example = normalizePhoneCriteria([{ id: "a", price: 20000, benchmarkScore: 80 }, { id: "b", price: 30000, benchmarkScore: 100 }], ["price", "performance"]);
const rows = example.comparisonPhones.map(p => ({ id: p.id, label: p.id, normalizedScores: example.normalizedScores.get(p.id)! }));
const scenarios = analyzePreferenceScenarios(rows, example.activeCriteria).scenarios;
assert.deepEqual(scenarios[0].results.map(r => r.rank), [1, 1]);
assert.deepEqual(scenarios[1].results.map(r => [r.id, r.rank]), [["a", 1], ["b", 2]]);
assert.deepEqual(scenarios[2].results.map(r => [r.id, r.rank]), [["b", 1], ["a", 2]]);
near(scenarios[1].results[0].score, .6);
near(scenarios[2].results[1].score, .4);
const ties = rankUnderWeights([.2, .2000005, .19999].map((price, i) => ({ id: String(i), label: String(i), normalizedScores: { price } })), { ...weights, price: 1, battery: 0 }, ["price"]);
assert.deepEqual(ties.map(r => [r.id, r.rank]), [["0", 1], ["1", 1], ["2", 3]]);
console.log("Passed smartphone eligibility, validation, independent calculations, ties and scenario checks.");
