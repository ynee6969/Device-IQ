import { CRITERION_KEYS } from "@/lib/recommendation/criteria";
import type {
  Criterion,
  CriterionWeight,
  SensitivityAnalysis,
  SensitivityScenario
} from "@/lib/recommendation/types";

import { rankUnderWeights, type RankingInput } from "@/lib/recommendation/ranking";

function createScenario(
  id: SensitivityScenario["id"],
  label: string,
  focusCriterion: Criterion | null,
  items: readonly RankingInput[],
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
  items: readonly RankingInput[],
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
