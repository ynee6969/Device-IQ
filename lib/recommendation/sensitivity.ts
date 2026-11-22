import { CRITERION_KEYS } from "@/lib/recommendation/criteria";
import { calculateWeightedScore } from "@/lib/recommendation/scoring";
import type {
  Criterion,
  CriterionWeight,
  NormalizedCriterionScore,
  SensitivityAnalysis,
  SensitivityScenario
} from "@/lib/recommendation/types";

export const RANK_TIE_TOLERANCE = 0.000001;

export interface SensitivityInput {
  id: string;
  label: string;
  normalizedScores: NormalizedCriterionScore;
}

export function rankUnderWeights(
  items: readonly SensitivityInput[],
  weights: CriterionWeight,
  activeCriteria: readonly Criterion[]
) {
  const scoreSorted = items
    .map((item) => ({
      id: item.id,
      label: item.label,
      score: calculateWeightedScore(item.normalizedScores, weights, activeCriteria).overall
    }))
    .sort((left, right) => right.score - left.score);

  const ranked: Array<(typeof scoreSorted)[number] & { rank: number }> = [];
  for (let start = 0; start < scoreSorted.length;) {
    let end = start + 1;
    while (
      end < scoreSorted.length &&
      Math.abs(scoreSorted[start].score - scoreSorted[end].score) <= RANK_TIE_TOLERANCE
    ) {
      end += 1;
    }

    const tieGroup = scoreSorted.slice(start, end).sort((left, right) => left.label.localeCompare(right.label));
    tieGroup.forEach((item) => ranked.push({ ...item, rank: start + 1 }));
    start = end;
  }

  return ranked;
}

function createScenario(
  id: SensitivityScenario["id"],
  label: string,
  focusCriterion: Criterion | null,
  items: readonly SensitivityInput[],
  activeCriteria: readonly Criterion[]
): SensitivityScenario {
  if (focusCriterion !== null && !activeCriteria.includes(focusCriterion)) {
    return {
      id,
      label,
      focusCriterion,
      status: "not_assessable",
      reason: `${label} cannot be assessed because ${focusCriterion} is unavailable in the active smartphone data.`,
      weights: null,
      results: []
    };
  }

  if (focusCriterion !== null && activeCriteria.length < 2) {
    return {
      id,
      label,
      focusCriterion,
      status: "not_assessable",
      reason: `${label} requires at least two active criteria.`,
      weights: null,
      results: []
    };
  }

  const weights = Object.fromEntries(CRITERION_KEYS.map((criterion) => [criterion, 0])) as CriterionWeight;
  if (focusCriterion === null) {
    for (const criterion of activeCriteria) {
      weights[criterion] = 1 / activeCriteria.length;
    }
  } else {
    weights[focusCriterion] = 0.6;
    const remainder = 0.4 / (activeCriteria.length - 1);
    for (const criterion of activeCriteria) {
      if (criterion !== focusCriterion) {
        weights[criterion] = remainder;
      }
    }
  }

  return {
    id,
    label,
    focusCriterion,
    status: "available",
    reason: null,
    weights,
    results: rankUnderWeights(items, weights, activeCriteria)
  };
}

/** Applies the three proposal-defined scenarios to the same scored dataset. */
export function analyzePreferenceScenarios(
  items: readonly SensitivityInput[],
  activeCriteria: readonly Criterion[]
): SensitivityAnalysis {
  if (activeCriteria.length === 0) {
    throw new Error("Preference scenarios require at least one active criterion.");
  }

  return {
    scenarios: [
      createScenario("equal", "Equal-weight baseline", null, items, activeCriteria),
      createScenario("affordability", "Affordability-focused", "price", items, activeCriteria),
      createScenario("performance", "Performance-focused", "performance", items, activeCriteria)
    ]
  };
}
