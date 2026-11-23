import { CRITERION_KEYS, type Criterion, type CriterionWeight } from "@/lib/recommendation/types";

export { CRITERION_KEYS } from "@/lib/recommendation/types";

export interface CriterionDefinition {
  key: Criterion;
  label: string;
  unit: string;
  direction: "benefit" | "cost";
  description: string;
}

export const CRITERIA: readonly CriterionDefinition[] = [
  {
    key: "price",
    label: "Price",
    unit: "PHP",
    direction: "cost",
    description: "Price for the exact smartphone configuration; lower is preferred."
  },
  {
    key: "performance",
    label: "Performance benchmark",
    unit: "documented benchmark score",
    direction: "benefit",
    description: "One benchmark name, version, configuration, and traceable source; higher is preferred."
  },
  {
    key: "battery",
    label: "Battery capacity",
    unit: "mAh",
    direction: "benefit",
    description: "Manufacturer-listed capacity; this is not a battery-endurance measure."
  },
  {
    key: "camera",
    label: "Camera capability",
    unit: "documented camera score",
    direction: "benefit",
    description: "A common documented camera score or reproducible composite; megapixels alone are insufficient."
  }
] as const;

/**
 * The current catalog has no approved, field-level evidence for benchmark or
 * camera measures. Price and listed battery capacity are used only to
 * demonstrate the calculation; the ranking form identifies catalog records
 * as illustrative until their sources and retrieval dates are verified.
 */
export const ACTIVE_RECOMMENDATION_CRITERIA: readonly Criterion[] = ["price", "battery"];

export const DEFAULT_WEIGHTS: CriterionWeight = {
  price: 0.5,
  performance: 0,
  battery: 0.5,
  camera: 0
};

export function sumWeights(weights: CriterionWeight) {
  return CRITERION_KEYS.reduce((total, criterion) => total + weights[criterion], 0);
}

export function roundScore(value: number, decimals = 6) {
  const factor = 10 ** decimals;
  return Math.round(value * factor) / factor;
}
