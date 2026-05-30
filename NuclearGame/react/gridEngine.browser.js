/**
 * AUTO-GENERATED from gridEngine.js — run: node scripts/build-browser-engine.mjs
 * Classic script for index.html (file:// and portable opens).
 */
(function (g) {
function calculateStability(nuclear, solar, hydro, fossil) {
  let stability = 30 + nuclear * 0.65 + fossil * 0.3 + hydro * 0.35;

  if (solar > 40) {
    stability -= (solar - 40) * 1.8;
  }

  if (nuclear >= 30 && solar > 40) {
    stability += nuclear * 0.25;
  }

  if (
    nuclear >= 50 &&
    solar >= 20 &&
    solar <= 45 &&
    hydro >= 5 &&
    fossil > 0 &&
    fossil <= 15
  ) {
    stability += 15;
  }

  return Math.round(Math.max(0, Math.min(100, stability)));
}

function calculateCO2(nuclear, solar, hydro, fossil) {
  const fossilCO2 = fossil * 0.01 * 650;
  const solarCO2 = solar * 0.01 * 48;
  const hydroCO2 = hydro * 0.01 * 24;
  const nuclearCO2 = nuclear * 0.01 * 12;
  const totalGCO2perKwh = fossilCO2 + solarCO2 + hydroCO2 + nuclearCO2;
  return Math.round((totalGCO2perKwh * 970 * 1000) / 1_000_000);
}

function calculateCost(nuclear, solar, hydro, fossil, stability) {
  let cost =
    75 - solar * 0.15 - hydro * 0.12 + fossil * 0.3 + nuclear * 0.05;

  if (stability < 80) {
    cost += (80 - stability) * 2.5;
  }

  if (stability < 50) {
    cost *= 1.6;
  }

  return Math.round(Math.max(40, cost));
}

function calculateGridMetrics(nuclear, solar, hydro = 0) {
  const fossil = Math.max(0, 100 - nuclear - solar - hydro);
  const stability = calculateStability(nuclear, solar, hydro, fossil);
  const co2 = calculateCO2(nuclear, solar, hydro, fossil);
  const cost = calculateCost(nuclear, solar, hydro, fossil, stability);
  return { nuclear, solar, hydro, fossil, stability, co2, cost };
}

function isOptimalMix(nuclear, solar, hydro, fossil, stability, co2, cost) {
  return (
    nuclear >= 50 &&
    solar >= 25 &&
    solar <= 45 &&
    hydro >= 5 &&
    fossil > 0 &&
    fossil <= 15 &&
    stability >= 80 &&
    co2 < 150 &&
    cost <= 105
  );
}

function getGridStoryMessage(
  stability,
  co2,
  cost,
  nuclear,
  solar,
  hydro,
  fossil
) {
  if (stability < 40) {
    return {
      icon: "🔴",
      type: "danger",
      message:
        "BLACKOUT IMMINENT. Grid instability has triggered emergency cost spikes. This is what happened to California in 2020.",
    };
  }

  if (stability < 60) {
    return {
      icon: "⚠️",
      type: "warning",
      message: `Dangerous instability. At ${solar}% solar/wind without enough nuclear backing, rolling blackouts become likely in winter when sun is low.`,
    };
  }

  if (nuclear === 0 && solar > 50) {
    return {
      icon: "⚠️",
      type: "warning",
      message:
        "Without nuclear baseload, this grid depends entirely on weather. Armenia's winters would cause frequent blackouts.",
    };
  }

  if (nuclear === 100) {
    return {
      icon: "⚠️",
      type: "warning",
      message:
        "100% nuclear is not realistic for Armenia. Real grids need diversification — peaking plants, renewables, and grid flexibility. Metsamor is vital baseload, not a solo solution overnight.",
    };
  }

  if (fossil === 0 && nuclear < 100) {
    return {
      icon: "⚠️",
      type: "warning",
      message:
        "0% oil/gas is not realistic. Every operating grid keeps gas or fuel-oil peaking plants for maintenance gaps, drought years, and winter spikes — even with nuclear and hydro.",
    };
  }

  if (stability >= 80 && nuclear >= 40 && solar < 20) {
    return {
      icon: "⚠️",
      type: "warning",
      message: `Stability looks fine (${stability}%) with ${nuclear}% nuclear, but only ${solar}% solar/wind is not a credible plan. Nuclear enables renewables — it does not replace them. Add meaningful solar/wind for a balanced grid.`,
    };
  }

  if (isOptimalMix(nuclear, solar, hydro, fossil, stability, co2, cost)) {
    return {
      icon: "✅",
      type: "success",
      message: `Optimal grid mix. ${nuclear}% nuclear + ${solar}% solar/wind + ${hydro}% hydro + ${fossil}% fossil peaking = ${stability}% stability, ${co2} tons CO₂/hr, ${cost} AMD/kWh. This is the balanced future Armenia should aim for.`,
    };
  }

  if (nuclear >= 40 && stability >= 80 && solar >= 20 && fossil > 0) {
    return {
      icon: "✅",
      type: "success",
      message: `Stable grid. ${nuclear}% nuclear, ${solar}% solar/wind, ${hydro}% hydro, and ${fossil}% fossil peaking work together — reliable, lower carbon, and economically viable.`,
    };
  }

  if (co2 > 400) {
    return {
      icon: "🌫️",
      type: "warning",
      message: `High emissions: ${co2} tons of CO₂/hour. At this rate, Armenia cannot meet its climate commitments.`,
    };
  }

  return {
    icon: "📊",
    type: "neutral",
    message: `Current mix produces ${co2} tons CO₂/hr at ${cost} AMD/kWh. Adjust sliders to see Armenia's energy trade-offs.`,
  };
}

function getStabilityDisplayState(stability, nuclear, solar) {
  if (stability >= 80 && nuclear >= 40 && solar < 20) return "warning";
  if (stability > 80) return "good";
  if (stability >= 60) return "warning";
  return "danger";
}

function getMetricState(metric, value) {
  if (metric === "stability") {
    if (value > 80) return "good";
    if (value >= 60) return "warning";
    return "danger";
  }
  if (metric === "co2") {
    if (value < 200) return "good";
    if (value <= 400) return "warning";
    return "danger";
  }
  if (metric === "cost") {
    if (value < 100) return "good";
    if (value <= 150) return "warning";
    return "danger";
  }
  return "neutral";
}

function stabilityStatusIcon(state) {
  if (state === "good") return "✅";
  if (state === "warning") return "⚠️";
  return "🔴";
}

/**
 * Armenia 2025 electricity generation (Statistical Committee, via ARKA Feb 2026):
 * TPP/gas 33.6%, nuclear 29.1%, hydro 21%, solar 16.3%, wind 0.02%.
 * Simulator: solar+wind ≈ 16%, fossil = gas/TPP ≈ 34%.
 */
const ARMENIA_2025_MIX = {
  nuclear: 29,
  solar: 16,
  hydro: 21,
  fossil: 34,
};

const DEMO_SCENARIOS = [
  {
    id: "armenia",
    label: "Armenia today (2025)",
    nuclear: ARMENIA_2025_MIX.nuclear,
    solar: ARMENIA_2025_MIX.solar,
    hydro: ARMENIA_2025_MIX.hydro,
  },
  { id: "anti-nuclear", label: "Anti-nuclear mistake", nuclear: 0, solar: 70, hydro: 10 },
  { id: "optimal", label: "Optimal future", nuclear: 55, solar: 30, hydro: 10 },
  { id: "pure-nuclear", label: "100% nuclear (unrealistic)", nuclear: 100, solar: 0, hydro: 0 },
];

const THEME_KEY = "grid-theme";

function loadSavedTheme() {
  try {
    const saved = localStorage.getItem(THEME_KEY);
    if (saved === "dark" || saved === "light") return saved;
  } catch {
    /* ignore */
  }
  return "dark";
}

function saveTheme(theme) {
  try {
    localStorage.setItem(THEME_KEY, theme);
  } catch {
    /* ignore */
  }
}

  g.GridEngine = {
    calculateStability,
    calculateCO2,
    calculateCost,
    calculateGridMetrics,
    isOptimalMix,
    getGridStoryMessage,
    getStabilityDisplayState,
    getMetricState,
    stabilityStatusIcon,
    ARMENIA_2025_MIX,
    DEMO_SCENARIOS,
    loadSavedTheme,
    saveTheme,
  };
})(typeof window !== "undefined" ? window : globalThis);
