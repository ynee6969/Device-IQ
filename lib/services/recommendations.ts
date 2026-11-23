import { z } from "zod";

import { ACTIVE_RECOMMENDATION_CRITERIA as measures, DEFAULT_WEIGHTS } from "@/lib/recommendation/criteria";
import { exclusionReason } from "@/lib/recommendation/eligibility";
import { normalizePhoneCriteria } from "@/lib/recommendation/normalization";
import { calculateWeightedScore, normalizeWeights, PreferenceError } from "@/lib/recommendation/scoring";
import { rankUnderWeights } from "@/lib/recommendation/ranking";
import { analyzePreferenceScenarios } from "@/lib/recommendation/sensitivity";
import { listPhones } from "@/lib/services/phones";
import { getPhoneDisplayName } from "@/lib/utils/phone-presentation";

const positive = z.number().finite().positive();
const points = z.number().finite().nonnegative();
export const recommendationInput = z.object({
  minBudget: positive.optional(),
  budget: positive.optional(),
  minBattery: positive.optional(),
  minRam: positive.optional(),
  brands: z.array(z.string().min(1)).default([]),
  osPreference: z.enum(["any", "android", "ios"]).default("any"),
  weights: z.object({ price: points, performance: points, battery: points, camera: points }).optional(),
  limit: z.number().int().min(1).max(10).default(5)
}).refine(({ minBudget, budget }) => minBudget === undefined || budget === undefined || minBudget <= budget,
  "Minimum price must be at or below maximum price.");

type Input = z.infer<typeof recommendationInput>;
type RecordData = {
  id: string; slug: string; brand: string; model: string; price: number;
  ram: number | null; battery: number | null; storage: number | null; os: string | null;
  sources?: Array<{ sourceUrl: string; fetchedAt: Date | null }>;
};

export function evaluatePhones(catalog: RecordData[], input: Input) {
  const constraints = {
    minPrice: input.minBudget, maxPrice: input.budget, minBattery: input.minBattery,
    minRam: input.minRam, brands: input.brands, os: input.osPreference
  };
  const entered = input.weights ?? DEFAULT_WEIGHTS;
  const requested = normalizeWeights(entered, measures);
  const excluded: Array<{ name: string; reason: string }> = [];
  const eligible = catalog.filter(phone => {
    const reason = exclusionReason(phone, constraints);
    if (reason) excluded.push({ name: getPhoneDisplayName(phone.brand, phone.model), reason });
    return !reason;
  });
  const normalized = normalizePhoneCriteria(eligible, measures);
  for (const phone of eligible) {
    if (!normalized.normalizedScores.has(phone.id)) excluded.push({
      name: getPhoneDisplayName(phone.brand, phone.model), reason: "Missing or invalid price or battery capacity"
    });
  }
  const phones = normalized.comparisonPhones.map(phone => {
    const reference = phone.sources?.find(source => /^https?:\/\//i.test(source.sourceUrl) && !source.sourceUrl.includes("results.php3"));
    return { id: phone.id, slug: phone.slug, brand: phone.brand, model: phone.model, name: getPhoneDisplayName(phone.brand, phone.model),
      price: phone.price, battery: phone.battery, ram: phone.ram, storage: phone.storage,
      sourceUrl: reference?.sourceUrl ?? null, fetchedAt: reference?.fetchedAt?.toISOString() ?? null };
  });
  const active = normalized.activeCriteria;
  const canRank = phones.length > 0 && active.length > 0;
  if (canRank && active.every(key => entered[key] === 0)) {
    throw new PreferenceError("Your selected priority has the same value for every match. Give a varying priority a positive weight.");
  }
  const weights = canRank ? normalizeWeights(entered, active, normalized.constantCriteria) : requested;
  const items = phones.map(phone => ({
    id: phone.id, label: phone.name, normalizedScores: normalized.normalizedScores.get(phone.id)!
  }));
  const phoneById = new Map(phones.map(phone => [phone.id, phone]));
  const order = canRank ? rankUnderWeights(items, weights, active) : [];
  const matches = order.slice(0, input.limit).map(row => {
    const score = calculateWeightedScore(normalized.normalizedScores.get(row.id)!, weights, active);
    return { rank: row.rank, phone: phoneById.get(row.id)!, score,
      finalScore: score.overallPercentage, personalizedScore: score.overallPercentage };
  });
  return { dataStatus: "illustrative" as const, eligibleCount: phones.length, matches, excluded, weights,
    excludedMissingCount: normalized.missingValueCount,
    preferences: { weights, preset: null, source: input.weights ? "user" : "default" },
    requested, constraints, criteria: active, constants: normalized.constantCriteria, ranges: normalized.ranges,
    unranked: canRank ? [] : phones,
    scenarios: canRank ? analyzePreferenceScenarios(items, active).scenarios : [] };
}

export async function recommendPhones(rawInput: unknown) {
  const parsed = recommendationInput.safeParse(rawInput);
  if (!parsed.success) {
    const issue = parsed.error.issues[0];
    if (issue.code === "custom") throw new PreferenceError(issue.message);
    throw new PreferenceError(issue.path[0] === "weights"
      ? "Enter a finite, nonnegative weight for each priority."
      : `Check the value for ${issue.path[0] ?? "your filters"}.`);
  }
  const catalog = await listPhones({ take: "all" });
  return evaluatePhones(catalog.phones, parsed.data);
}

export type SmartphoneResult = ReturnType<typeof evaluatePhones>;
