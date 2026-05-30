/**
 * Grid Commander — budget & scoring (framework-agnostic).
 * Works with gridEngine mix metrics.
 */

export const BUDGET_TOTAL = 1_000_000;

export const ENERGY_SOURCES = [
  {
    id: "nuclear",
    name: "Nuclear",
    tagline: "Baseload backbone",
    unitCost: 275_000,
    capacityMW: 48,
    color: "#00b4d8",
    accent: "#0077b6",
  },
  {
    id: "solar",
    name: "Solar & Wind",
    tagline: "Clean but variable",
    unitCost: 92_000,
    capacityMW: 22,
    color: "#ffd166",
    accent: "#f4a261",
  },
  {
    id: "hydro",
    name: "Hydro",
    tagline: "Flexible & clean",
    unitCost: 105_000,
    capacityMW: 38,
    color: "#5eb8d4",
    accent: "#2a8fa8",
  },
  {
    id: "fossil",
    name: "Fossil",
    tagline: "Peaking · high CO₂",
    unitCost: 52_000,
    capacityMW: 32,
    color: "#a08060",
    accent: "#6b5344",
  },
];

export function getSourceById(id) {
  return ENERGY_SOURCES.find((s) => s.id === id);
}

export function calculateSpend(allocations) {
  return ENERGY_SOURCES.reduce(
    (sum, s) => sum + (allocations[s.id] || 0) * s.unitCost,
    0
  );
}

export function getRemainingBudget(allocations) {
  return BUDGET_TOTAL - calculateSpend(allocations);
}

/** True if buying one more unit of this source stays within budget. */
export function canIncrementAllocation(allocations, sourceId) {
  const source = getSourceById(sourceId);
  if (!source) return false;
  return calculateSpend(allocations) + source.unitCost <= BUDGET_TOTAL;
}

export function getMaxUnitsForSource(sourceId, allocations) {
  const source = getSourceById(sourceId);
  const remaining = getRemainingBudget(allocations) + (allocations[sourceId] || 0) * source.unitCost;
  return Math.max(0, Math.floor(remaining / source.unitCost));
}

/** Try to add one unit; returns false if it would exceed budget. */
export function tryIncrementAllocation(allocations, sourceId) {
  if (!canIncrementAllocation(allocations, sourceId)) return false;
  allocations[sourceId] = (allocations[sourceId] || 0) + 1;
  return true;
}

/** Strip units (cheapest first) until spend ≤ budget — used for presets and safety clamp. */
export function normalizeAllocationsToBudget(allocations) {
  const out = { nuclear: 0, solar: 0, hydro: 0, fossil: 0, ...allocations };
  const trimOrder = ["fossil", "solar", "hydro", "nuclear"];
  while (calculateSpend(out) > BUDGET_TOTAL) {
    let trimmed = false;
    for (const id of trimOrder) {
      if (out[id] > 0) {
        out[id]--;
        trimmed = true;
        break;
      }
    }
    if (!trimmed) break;
  }
  return out;
}

export function applyAllocations(target, next) {
  const normalized = normalizeAllocationsToBudget(next);
  for (const s of ENERGY_SOURCES) {
    target[s.id] = normalized[s.id] || 0;
  }
  return normalized;
}

export function calculateCapacity(allocations) {
  const perSource = {};
  let totalMW = 0;
  for (const s of ENERGY_SOURCES) {
    const mw = (allocations[s.id] || 0) * s.capacityMW;
    perSource[s.id] = mw;
    totalMW += mw;
  }
  return { perSource, totalMW };
}

/** Mix percentages from installed MW (0 if no capacity). */
export function capacityToMix(perSource, totalMW) {
  if (totalMW <= 0) {
    return { nuclear: 0, solar: 0, hydro: 0, fossil: 0 };
  }
  return {
    nuclear: Math.round((perSource.nuclear / totalMW) * 100),
    solar: Math.round((perSource.solar / totalMW) * 100),
    hydro: Math.round((perSource.hydro / totalMW) * 100),
    fossil: Math.round((perSource.fossil / totalMW) * 100),
  };
}

/** Annual output proxy: MW × capacity factor × hours. */
export function calculateAnnualOutputGWh(totalMW, stability) {
  if (totalMW <= 0) return 0;
  const baseFactor = 0.52;
  const stabilityFactor = 0.7 + (stability / 100) * 0.3;
  return Math.round(totalMW * baseFactor * stabilityFactor * 8760 * 0.001);
}

/**
 * Diversification: reward multiple source types and avoid one fuel dominating the mix.
 * Returns 0–25.
 */
export function calculateDiversificationPts(allocations, mix, totalMW) {
  if (totalMW <= 0) return 0;

  const activeTypes = ENERGY_SOURCES.filter((s) => (allocations[s.id] || 0) > 0).length;
  const shares = [mix.nuclear, mix.solar, mix.hydro, mix.fossil];
  const maxShare = Math.max(...shares);
  const represented = shares.filter((p) => p >= 8).length;

  let pts = 0;

  if (activeTypes >= 4) pts += 10;
  else if (activeTypes === 3) pts += 7;
  else if (activeTypes === 2) pts += 3;

  if (represented >= 4) pts += 8;
  else if (represented === 3) pts += 5;
  else if (represented === 2) pts += 2;

  if (maxShare <= 50) pts += 7;
  else if (maxShare <= 60) pts += 5;
  else if (maxShare <= 70) pts += 2;

  if (maxShare >= 85) pts = Math.max(0, pts - 8);
  if (activeTypes === 1) pts = Math.max(0, pts - 10);

  return Math.min(25, Math.max(0, pts));
}

export function calculateGameScore(metrics, totalMW, annualGWh, allocations, mix) {
  const empty = {
    score: 0,
    grade: "—",
    outputPts: 0,
    emissionPts: 0,
    stabilityPts: 0,
    diversificationPts: 0,
    activeTypes: 0,
    maxShare: 0,
  };

  if (totalMW <= 0) return empty;

  const outputPts = Math.min(25, Math.round((annualGWh / 1000) * 25));
  const emissionPts = Math.max(0, Math.min(25, Math.round(25 - metrics.co2 / 14)));
  const stabilityPts = Math.max(0, Math.min(25, Math.round((metrics.stability / 100) * 25)));
  const diversificationPts = calculateDiversificationPts(allocations, mix, totalMW);
  const activeTypes = ENERGY_SOURCES.filter((s) => (allocations[s.id] || 0) > 0).length;
  const maxShare = Math.max(mix.nuclear, mix.solar, mix.hydro, mix.fossil);

  let score = outputPts + emissionPts + stabilityPts + diversificationPts;

  if (metrics.stability < 50) score = Math.max(0, score - 12);
  if (metrics.co2 > 500) score = Math.max(0, score - 8);

  score = Math.min(100, Math.max(0, score));

  let grade = "F";
  if (score >= 90) grade = "S";
  else if (score >= 80) grade = "A";
  else if (score >= 65) grade = "B";
  else if (score >= 50) grade = "C";
  else if (score >= 35) grade = "D";

  return {
    score,
    grade,
    outputPts,
    emissionPts,
    stabilityPts,
    diversificationPts,
    activeTypes,
    maxShare,
  };
}

export function getCharacterState(metrics, score, totalMW) {
  if (totalMW === 0) return { mood: "idle", message: "Allocate your $1M budget to build the grid." };

  if (metrics.stability < 40) {
    return {
      mood: "alert",
      message: "Blackout risk! Add nuclear baseload or reduce volatile solar share.",
    };
  }

  if (metrics.stability < 60) {
    return {
      mood: "worried",
      message: "Grid is shaky. Nuclear and hydro stabilize weather-dependent solar.",
    };
  }

  if (score.diversificationPts >= 20 && score.score >= 85 && metrics.co2 < 180) {
    return {
      mood: "celebrate",
      message: "Outstanding! Diversified, high output, and low emissions — a resilient grid.",
    };
  }

  if (score.activeTypes === 1) {
    return {
      mood: "worried",
      message: "All eggs in one basket. Real grids diversify across nuclear, hydro, solar, and peaking plants.",
    };
  }

  if (score.maxShare >= 75) {
    return {
      mood: "thinking",
      message: `One source dominates at ${score.maxShare}% of capacity. Spread investment for a stronger score.`,
    };
  }

  if (score.diversificationPts < 10 && score.activeTypes >= 2) {
    return {
      mood: "thinking",
      message: "You use multiple fuels, but the mix is still lopsided. Aim for ~10%+ from at least three sources.",
    };
  }

  if (metrics.co2 > 400) {
    return {
      mood: "worried",
      message: "Emissions are crushing climate goals. Shift budget from fossil to clean sources.",
    };
  }

  if (score.grade === "A" || score.grade === "S") {
    return {
      mood: score.grade === "S" ? "celebrate" : "happy",
      message:
        score.grade === "S"
          ? "S-rank grid! Diversified, powerful, and clean — outstanding work."
          : "A-rank achieved. Strong diversified mix — keep pushing for S-rank perfection.",
    };
  }

  if (metrics.stability >= 80 && metrics.co2 < 220 && score.diversificationPts >= 15) {
    return {
      mood: "happy",
      message: "Solid balance — diversified mix, stable grid, and manageable emissions.",
    };
  }

  return {
    mood: "thinking",
    message: "Maximize output and stability, cut CO₂, and diversify — no single source should dominate.",
  };
}

/** Face expression: A/S grades smile unless the grid is in crisis. */
export function resolveFaceMood(advisorMood, grade, stability) {
  if (stability < 40) return advisorMood;
  if (grade === "S") return "celebrate";
  if (grade === "A") return "happy";
  return advisorMood;
}

export const PRESET_STRATEGIES = [
  {
    id: "blank",
    label: "Fresh start",
    allocations: { nuclear: 0, solar: 0, hydro: 0, fossil: 0 },
  },
  {
    id: "balanced",
    label: "Balanced future",
    allocations: { nuclear: 2, solar: 2, hydro: 1, fossil: 1 },
  },
  {
    id: "green",
    label: "Renewables push",
    allocations: { nuclear: 1, solar: 4, hydro: 2, fossil: 0 },
  },
  {
    id: "mistake",
    label: "Anti-nuclear trap",
    allocations: { nuclear: 0, solar: 5, hydro: 1, fossil: 3 },
  },
  {
    id: "armenia",
    label: "Armenia-scale mix",
    allocations: { nuclear: 1, solar: 2, hydro: 2, fossil: 2 },
  },
];
