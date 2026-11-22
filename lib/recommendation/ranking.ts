import { calculateWeightedScore } from "@/lib/recommendation/scoring";
import type { Criterion, CriterionWeight, NormalizedCriterionScore } from "@/lib/recommendation/types";

export const RANK_TIE_TOLERANCE = 0.000001;

export interface RankingInput {
  id: string;
  label: string;
  normalizedScores: NormalizedCriterionScore;
}

export function rankUnderWeights(
  items: readonly RankingInput[],
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
