import { CRITERIA, CRITERION_KEYS, sumWeights } from "@/lib/recommendation/criteria";
import type {
  Criterion,
  CriterionWeight,
  NormalizedCriterionScore,
  RecommendationScore
} from "@/lib/recommendation/types";

export class PreferenceError extends Error {}

const WEIGHT_TOLERANCE = 0.000001;

export function validateWeights(weights: CriterionWeight, activeCriteria: readonly Criterion[]) {
  const values = CRITERION_KEYS.map((criterion) => weights[criterion]);
  if (values.some((weight) => !Number.isFinite(weight) || weight < 0)) {
    throw new Error("Weights must be finite, non-negative numbers.");
  }

  if (CRITERION_KEYS.some((criterion) => !activeCriteria.includes(criterion) && weights[criterion] > 0)) {
    throw new Error("A weight was assigned to a criterion that is unavailable for this comparison.");
  }

  const activeTotal = activeCriteria.reduce((total, criterion) => total + weights[criterion], 0);
  if (Math.abs(activeTotal - 1) > WEIGHT_TOLERANCE) {
    throw new Error("Effective weights for active criteria must sum to 1 (100%).");
  }

  return weights;
}

/**
 * Converts entered relative points to effective weights. The proposal permits
 * proportional normalization and requires the active weights to total one.
 */
export function normalizeWeights(
  enteredWeights: CriterionWeight,
  activeCriteria: readonly Criterion[],
  removedConstantCriteria: readonly Criterion[] = []
) {
  if (CRITERION_KEYS.some((criterion) => !Number.isFinite(enteredWeights[criterion]) || enteredWeights[criterion] < 0)) {
    throw new PreferenceError("Weights must be finite, non-negative numbers.");
  }

  if (
    CRITERION_KEYS.some(
      (criterion) =>
        !activeCriteria.includes(criterion) &&
        !removedConstantCriteria.includes(criterion) &&
        enteredWeights[criterion] > 0
    )
  ) {
    throw new PreferenceError("A weight was assigned to a criterion that is unavailable for this comparison.");
  }

  const largest = Math.max(...activeCriteria.map(key => enteredWeights[key]));
  if (!(largest > 0)) {
    throw new PreferenceError("Enter a positive weight for at least one available criterion.");
  }
  // Divide by the largest input first so finite relative weights cannot overflow their sum.
  const activeTotal = activeCriteria.reduce((sum, key) => sum + enteredWeights[key] / largest, 0);

  const normalized = Object.fromEntries(
    CRITERION_KEYS.map((criterion) => [
      criterion,
      activeCriteria.includes(criterion) ? (enteredWeights[criterion] / largest) / activeTotal : 0
    ])
  ) as CriterionWeight;

  return normalized;
}

/** Implements S_j = Σ(w_i × r_ij) for one smartphone. */
export function calculateWeightedScore(
  normalizedScores: NormalizedCriterionScore,
  weights: CriterionWeight,
  activeCriteria: readonly Criterion[]
): RecommendationScore {
  validateWeights(weights, activeCriteria);

  const criteria: RecommendationScore["criteria"] = {};
  for (const definition of CRITERIA) {
    if (!activeCriteria.includes(definition.key)) {
      continue;
    }

    const normalizedScore = normalizedScores[definition.key];
    if (
      typeof normalizedScore !== "number" ||
      !Number.isFinite(normalizedScore) ||
      normalizedScore < 0 ||
      normalizedScore > 1
    ) {
      throw new Error(`Missing or invalid normalized value for ${definition.label}.`);
    }

    const weight = weights[definition.key];
    criteria[definition.key] = {
      label: definition.label,
      normalizedScore,
      weight,
      weightedContribution: normalizedScore * weight
    };
  }

  const overall = Object.values(criteria).reduce(
    (total, criterion) => total + (criterion?.weightedContribution ?? 0),
    0
  );

  return {
    overall,
    overallPercentage: overall * 100,
    criteria
  };
}

export function weightsTotal(weights: CriterionWeight) {
  return sumWeights(weights);
}
