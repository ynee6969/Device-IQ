import { CRITERION_KEYS } from "@/lib/recommendation/criteria";
import type { Criterion, NormalizedCriterionScore } from "@/lib/recommendation/types";

export interface RecommendationPhoneData {
  id: string;
  price: number | null;
  benchmarkScore?: number | null;
  cameraScore?: number | null;
  battery?: number | null;
}

export interface NormalizationResult<TPhone extends RecommendationPhoneData> {
  comparisonPhones: TPhone[];
  normalizedScores: ReadonlyMap<string, NormalizedCriterionScore>;
  activeCriteria: Criterion[];
  constantCriteria: Criterion[];
  missingValueCount: number;
}

function rawValue(phone: RecommendationPhoneData, criterion: Criterion) {
  switch (criterion) {
    case "price":
      return phone.price;
    case "performance":
      return phone.benchmarkScore;
    case "battery":
      return phone.battery;
    case "camera":
      return phone.cameraScore;
  }
}

function isUsableValue(value: number | null | undefined, criterion: Criterion) {
  return (
    typeof value === "number" &&
    Number.isFinite(value) &&
    value >= 0 &&
    ((criterion !== "price" && criterion !== "battery") || value > 0)
  );
}

export function normalizeBenefit(value: number, minimum: number, maximum: number) {
  return (value - minimum) / (maximum - minimum);
}

export function normalizeCost(value: number, minimum: number, maximum: number) {
  return (maximum - value) / (maximum - minimum);
}

/**
 * Applies missing-value exclusion before deriving min–max ranges. Constant
 * criteria are omitted from the returned score set so their weights can be
 * redistributed proportionally by the scoring layer.
 */
export function normalizePhoneCriteria<TPhone extends RecommendationPhoneData>(
  phones: readonly TPhone[],
  criteria: readonly Criterion[]
): NormalizationResult<TPhone> {
  const comparisonPhones = phones.filter((phone) =>
    criteria.every((criterion) => isUsableValue(rawValue(phone, criterion), criterion))
  );
  const missingValueCount = phones.length - comparisonPhones.length;
  const constants: Criterion[] = [];
  const ranges = new Map<Criterion, { minimum: number; maximum: number }>();

  for (const criterion of criteria) {
    const values = comparisonPhones.map((phone) => rawValue(phone, criterion) as number);
    if (!values.length) {
      continue;
    }

    const minimum = Math.min(...values);
    const maximum = Math.max(...values);
    if (minimum === maximum) {
      constants.push(criterion);
    } else {
      ranges.set(criterion, { minimum, maximum });
    }
  }

  const activeCriteria = comparisonPhones.length
    ? criteria.filter((criterion) => ranges.has(criterion))
    : [...criteria];

  const normalizedScores = new Map<string, NormalizedCriterionScore>();
  for (const phone of comparisonPhones) {
    const normalized: NormalizedCriterionScore = {};
    for (const criterion of activeCriteria) {
      const range = ranges.get(criterion);
      const value = rawValue(phone, criterion);
      if (!range || typeof value !== "number") {
        continue;
      }

      const score =
        criterion === "price"
          ? normalizeCost(value, range.minimum, range.maximum)
          : normalizeBenefit(value, range.minimum, range.maximum);
      normalized[criterion] = score;
    }
    normalizedScores.set(phone.id, normalized);
  }

  return {
    comparisonPhones,
    normalizedScores,
    activeCriteria,
    constantCriteria: constants,
    missingValueCount
  };
}

export function isNormalizedCriterionScore(value: unknown): value is NormalizedCriterionScore {
  if (typeof value !== "object" || value === null) {
    return false;
  }

  const entries = Object.entries(value as Record<string, unknown>);
  return (
    entries.length > 0 &&
    entries.every(
      ([criterion, score]) =>
        CRITERION_KEYS.includes(criterion as Criterion) &&
        typeof score === "number" &&
        Number.isFinite(score) &&
        score >= 0 &&
        score <= 1
    )
  );
}
