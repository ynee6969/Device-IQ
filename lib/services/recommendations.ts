import { z } from "zod";

import {
  ACTIVE_RECOMMENDATION_CRITERIA,
  DEFAULT_WEIGHTS
} from "@/lib/recommendation/criteria";
import { normalizePhoneCriteria } from "@/lib/recommendation/normalization";
import { calculateWeightedScore, normalizeWeights } from "@/lib/recommendation/scoring";
import { rankUnderWeights } from "@/lib/recommendation/ranking";
import { filterEligibleSmartphones } from "@/lib/recommendation/eligibility";
import type {
  DecisionConstraints,
  RecommendationResult,
  UserPreference
} from "@/lib/recommendation/types";
import { listPhones } from "@/lib/services/phones";

const weightSchema = z.object({
  price: z.number().finite().min(0).max(100),
  performance: z.number().finite().min(0).max(100),
  battery: z.number().finite().min(0).max(100),
  camera: z.number().finite().min(0).max(100)
});

const recommendationSchema = z
  .object({
    budget: z.number().finite().positive().optional(),
    minBudget: z.number().finite().positive().optional(),
    brands: z.array(z.string().min(1)).default([]),
    osPreference: z.enum(["any", "android", "ios"]).default("any"),
    minBattery: z.number().finite().positive().optional(),
    minRam: z.number().finite().positive().optional(),
    weights: weightSchema.optional(),
    limit: z.number().int().min(1).max(10).default(5)
  })
  .superRefine((input, context) => {
    if (input.minBudget !== undefined && input.budget !== undefined && input.minBudget > input.budget) {
      context.addIssue({
        code: z.ZodIssueCode.custom,
        path: ["minBudget"],
        message: "Minimum budget cannot exceed maximum budget."
      });
    }
  });

export type RecommendationInput = z.infer<typeof recommendationSchema>;

function resolvePreference(input: RecommendationInput): UserPreference {
  const enteredWeights = input.weights ?? DEFAULT_WEIGHTS;
  const weights = normalizeWeights(enteredWeights, ACTIVE_RECOMMENDATION_CRITERIA);
  return {
    weights,
    source: input.weights ? "user" : "default",
    preset: null
  };
}

export async function recommendPhones(rawInput: unknown) {
  const input = recommendationSchema.parse(rawInput);
  const preference = resolvePreference(input);
  const constraints: DecisionConstraints = {
    minPrice: input.minBudget,
    maxPrice: input.budget,
    brands: input.brands,
    os: input.osPreference,
    minBattery: input.minBattery,
    minRam: input.minRam
  };

  // Mandatory filters are applied before the comparison set and its ranges are built.
  const catalog = await listPhones({
    minPrice: input.minBudget,
    maxPrice: input.budget,
    minBattery: input.minBattery,
    minRam: input.minRam,
    take: 1000
  });
  const filterEligiblePhones = filterEligibleSmartphones(catalog.phones, constraints);
  const normalization = normalizePhoneCriteria(
    filterEligiblePhones,
    ACTIVE_RECOMMENDATION_CRITERIA
  );

  const weights = normalizeWeights(input.weights ?? DEFAULT_WEIGHTS, normalization.activeCriteria);
  const normalizedScores = normalization.normalizedScores;
  const scoredPhones = normalization.comparisonPhones;
  const scoreById = new Map(
    scoredPhones.map((phone) => {
      const normalized = normalizedScores.get(phone.id);
      if (!normalized) {
        throw new Error(`Missing normalized values for smartphone ${phone.id}.`);
      }
      return [phone.id, calculateWeightedScore(normalized, weights, normalization.activeCriteria)];
    })
  );
  const labels = new Map(
    scoredPhones.map((phone) => [phone.id, `${phone.brand} ${phone.model}`])
  );
  const rankedRows = rankUnderWeights(
    scoredPhones.flatMap((phone) => {
      const normalized = normalizedScores.get(phone.id);
      return normalized
        ? [{ id: phone.id, label: labels.get(phone.id)!, normalizedScores: normalized }]
        : [];
    }),
    weights,
    normalization.activeCriteria
  );
  const phoneById = new Map(scoredPhones.map((phone) => [phone.id, phone]));
  const ranked = rankedRows
    .map(({ id, rank }) => {
      const phone = phoneById.get(id);
      const score = scoreById.get(id);
      if (!phone || !score) {
        throw new Error(`Could not map ranked smartphone ${id} to its score and record.`);
      }

      return {
        rank,
        phone,
        finalScore: score.overallPercentage,
        personalizedScore: score.overallPercentage,
        score
      };
    })
    .slice(0, input.limit);

  const result: RecommendationResult<typeof ranked[number]["phone"]> = {
    criteria: normalization.activeCriteria,
    preferences: { ...preference, weights },
    weights,
    constraints,
    eligibleCount: scoredPhones.length,
    excludedMissingCount: normalization.missingValueCount,
    matches: ranked
  };

  return result;
}
