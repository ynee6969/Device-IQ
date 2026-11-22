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
    label: "Performance",
    unit: "DeviceIQ rating",
    direction: "benefit",
    description: "DeviceIQ rating out of 100."
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
    label: "Camera",
    unit: "DeviceIQ rating",
    direction: "benefit",
    description: "DeviceIQ rating out of 100."
  }
] as const;

export const ACTIVE_RECOMMENDATION_CRITERIA: readonly Criterion[] = CRITERION_KEYS;

export const DEFAULT_WEIGHTS: CriterionWeight = {
  price: 0.25,
  performance: 0.25,
  battery: 0.25,
  camera: 0.25
};

export function sumWeights(weights: CriterionWeight) {
  return CRITERION_KEYS.reduce((total, criterion) => total + weights[criterion], 0);
}

export function roundScore(value: number, decimals = 6) {
  const factor = 10 ** decimals;
  return Math.round(value * factor) / factor;
}
