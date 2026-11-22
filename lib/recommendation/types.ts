export const CRITERION_KEYS = ["price", "performance", "battery", "camera"] as const;

export type Criterion = (typeof CRITERION_KEYS)[number];

export type CriterionWeight = Record<Criterion, number>;
export type NormalizedCriterionScore = Partial<Record<Criterion, number>>;

export interface CriterionContribution {
  label: string;
  normalizedScore: number;
  weight: number;
  weightedContribution: number;
}

export type RecommendationScore = {
  overall: number;
  overallPercentage: number;
  criteria: Partial<Record<Criterion, CriterionContribution>>;
};

export interface PhoneRanking<TPhone = unknown> {
  rank: number;
  phone: TPhone;
  finalScore: number;
  personalizedScore: number;
  score: RecommendationScore;
}

export interface UserPreference {
  weights: CriterionWeight;
  source: "user" | "preset" | "default";
  preset: string | null;
}

export interface DecisionConstraints {
  minPrice?: number;
  maxPrice?: number;
  brands: string[];
  os: "any" | "android" | "ios";
  minBattery?: number;
  minRam?: number;
}

export interface RecommendationResult<TPhone = unknown> {
  criteria: readonly Criterion[];
  preferences: UserPreference;
  weights: CriterionWeight;
  constraints: DecisionConstraints;
  eligibleCount: number;
  excludedMissingCount: number;
  matches: PhoneRanking<TPhone>[];
}
