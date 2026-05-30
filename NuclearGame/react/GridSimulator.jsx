import { useCallback, useMemo, useState } from "react";
import {
  calculateGridMetrics,
  DEMO_SCENARIOS,
  getGridStoryMessage,
  getMetricState,
  getStabilityDisplayState,
  loadSavedTheme,
  saveTheme,
  stabilityStatusIcon,
} from "./gridEngine.js";
import "./GridSimulator.css";

function metricCardClass(state) {
  if (state === "good") return "grid-metric-card grid-metric-card--good";
  if (state === "warning") return "grid-metric-card grid-metric-card--warning";
  if (state === "danger") return "grid-metric-card grid-metric-card--danger";
  return "grid-metric-card";
}

/**
 * Page 1: The Grid — Armenia energy mix simulator (HackAtom 2026 National Stage).
 */
export default function GridSimulator({
  className = "",
  showHeader = true,
  showFooter = true,
  showDemos = true,
  showThemeToggle = true,
  initialNuclear = 40,
  initialSolar = 25,
  initialHydro = 10,
  defaultTheme,
}) {
  const [nuclear, setNuclear] = useState(initialNuclear);
  const [solar, setSolar] = useState(initialSolar);
  const [hydro, setHydro] = useState(initialHydro);
  const [theme, setTheme] = useState(() => defaultTheme ?? loadSavedTheme());

  const metrics = useMemo(
    () => calculateGridMetrics(nuclear, solar, hydro),
    [nuclear, solar, hydro]
  );

  const story = useMemo(
    () =>
      getGridStoryMessage(
        metrics.stability,
        metrics.co2,
        metrics.cost,
        metrics.nuclear,
        metrics.solar,
        metrics.hydro,
        metrics.fossil
      ),
    [metrics]
  );

  const stabState = getStabilityDisplayState(
    metrics.stability,
    metrics.nuclear,
    metrics.solar
  );
  const co2State = getMetricState("co2", metrics.co2);
  const costState = getMetricState("cost", metrics.cost);

  const handleNuclearChange = useCallback(
    (value) => {
      const maxNuclear = 100 - solar - hydro;
      setNuclear(Math.min(Math.max(0, value), maxNuclear));
    },
    [solar, hydro]
  );

  const handleSolarChange = useCallback(
    (value) => {
      const maxSolar = 100 - nuclear - hydro;
      setSolar(Math.min(Math.max(0, value), maxSolar));
    },
    [nuclear, hydro]
  );

  const handleHydroChange = useCallback(
    (value) => {
      const maxHydro = 100 - nuclear - solar;
      setHydro(Math.min(Math.max(0, value), maxHydro));
    },
    [nuclear, solar]
  );

  const applyDemo = useCallback((demoNuclear, demoSolar, demoHydro) => {
    let n = demoNuclear;
    let s = demoSolar;
    let h = demoHydro;
    if (n + s + h > 100) {
      h = Math.max(0, 100 - n - s);
    }
    setNuclear(n);
    setSolar(s);
    setHydro(h);
  }, []);

  const toggleTheme = useCallback(() => {
    setTheme((t) => {
      const next = t === "dark" ? "light" : "dark";
      saveTheme(next);
      return next;
    });
  }, []);

  const rootClass = ["grid-simulator", className].filter(Boolean).join(" ");

  return (
    <div className={rootClass} data-theme={theme}>
      <div className="grid-page">
        {showHeader && (
          <header className="grid-header">
            {showThemeToggle && (
              <div className="grid-header-top">
                <button
                  type="button"
                  className="grid-theme-toggle"
                  onClick={toggleTheme}
                  aria-label="Toggle theme"
                >
                  <span>{theme === "dark" ? "🌙" : "☀️"}</span>
                  <span>{theme === "dark" ? "Dark" : "Light"}</span>
                </button>
              </div>
            )}
            <h1 className="grid-title">⚡ THE GRID — Armenia&apos;s Energy Mix Simulator</h1>
            <p className="grid-subtitle">Can Armenia survive without nuclear?</p>
          </header>
        )}

        <div className="grid-dashboard">
          <section className="grid-panel">
            <div className="grid-panel-title">Energy mix controls</div>

            <div className="grid-slider-group">
              <div className="grid-slider-label">
                <span>☢️ Nuclear</span>
                <span className="grid-slider-value grid-slider-value--nuclear">
                  {metrics.nuclear}%
                </span>
              </div>
              <input
                type="range"
                className="grid-range grid-range--nuclear"
                min={0}
                max={100}
                value={metrics.nuclear}
                onChange={(e) => handleNuclearChange(Number(e.target.value))}
              />
            </div>

            <div className="grid-slider-group">
              <div className="grid-slider-label">
                <span>☀️ Solar &amp; Wind</span>
                <span className="grid-slider-value grid-slider-value--solar">
                  {metrics.solar}%
                </span>
              </div>
              <input
                type="range"
                className="grid-range grid-range--solar"
                min={0}
                max={100}
                value={metrics.solar}
                onChange={(e) => handleSolarChange(Number(e.target.value))}
              />
            </div>

            <div className="grid-slider-group">
              <div className="grid-slider-label">
                <span>💧 Hydro</span>
                <span className="grid-slider-value grid-slider-value--hydro">
                  {metrics.hydro}%
                </span>
              </div>
              <input
                type="range"
                className="grid-range grid-range--hydro"
                min={0}
                max={100}
                value={metrics.hydro}
                onChange={(e) => handleHydroChange(Number(e.target.value))}
              />
            </div>

            <div className="grid-slider-group">
              <div className="grid-slider-label">
                <span>🛢️ Fossil fuel</span>
                <span className="grid-slider-value grid-slider-value--fossil">
                  {metrics.fossil}%
                </span>
              </div>
              <input
                type="range"
                className="grid-range grid-range--fossil grid-range--readonly"
                min={0}
                max={100}
                value={metrics.fossil}
                readOnly
                tabIndex={-1}
                aria-readonly="true"
                aria-label="Fossil fuel share (auto-calculated)"
              />
              <p className="grid-mix-hint">
                Read-only. Auto-calculated:{" "}
                <strong>100% − nuclear − solar − hydro</strong>
              </p>
            </div>

            <div className="grid-mix-bar" aria-hidden="true">
              <div
                className="grid-mix-segment grid-mix-segment--nuclear"
                style={{ width: `${metrics.nuclear}%` }}
              />
              <div
                className="grid-mix-segment grid-mix-segment--solar"
                style={{ width: `${metrics.solar}%` }}
              />
              <div
                className="grid-mix-segment grid-mix-segment--hydro"
                style={{ width: `${metrics.hydro}%` }}
              />
              <div
                className="grid-mix-segment grid-mix-segment--fossil"
                style={{ width: `${metrics.fossil}%` }}
              />
            </div>
            <div className="grid-mix-legend">
              <span className="grid-legend-nuclear">Nuclear</span>
              <span className="grid-legend-solar">Solar &amp; wind</span>
              <span className="grid-legend-hydro">Hydro</span>
              <span className="grid-legend-fossil">Fossil</span>
            </div>
          </section>

          <section>
            <div className="grid-metrics">
              <div className={metricCardClass(stabState)}>
                <div className="grid-metric-label">Grid stability</div>
                <div>
                  <span className="grid-metric-number">{metrics.stability}</span>
                  <span className="grid-metric-unit">%</span>
                  <span className="grid-metric-icon">
                    {stabilityStatusIcon(stabState)}
                  </span>
                </div>
              </div>
              <div className={metricCardClass(co2State)}>
                <div className="grid-metric-label">CO₂ emissions</div>
                <div>
                  <span className="grid-metric-number">{metrics.co2}</span>
                  <span className="grid-metric-unit">tons/hr</span>
                </div>
              </div>
              <div className={`${metricCardClass(costState)} grid-metric-card--wide`}>
                <div className="grid-metric-label">Energy cost</div>
                <div>
                  <span className="grid-metric-number">{metrics.cost}</span>
                  <span className="grid-metric-unit">AMD/kWh</span>
                </div>
              </div>
            </div>

            <div className={`grid-story grid-story--${story.type}`}>
              <span className="grid-story-icon">{story.icon}</span>
              <p className="grid-story-text">{story.message}</p>
            </div>
          </section>
        </div>

        {showDemos && (
          <div className="grid-demos">
            <div className="grid-demos-title">Quick demo scenarios</div>
            <div className="grid-demo-buttons">
              {DEMO_SCENARIOS.map((demo) => (
                <button
                  key={demo.id}
                  type="button"
                  className="grid-demo-btn"
                  onClick={() =>
                    applyDemo(demo.nuclear, demo.solar, demo.hydro)
                  }
                >
                  {demo.label}
                </button>
              ))}
            </div>
            <p className="grid-demos-source">
              <strong>Armenia today (2025):</strong> Statistical Committee — gas/TPP
              33.6%, Metsamor nuclear 29.1%, hydro 21%, solar 16.3%, wind 0.02%
              (ARKA, Feb 2026).
            </p>
          </div>
        )}

        {showFooter && (
          <footer className="grid-footer">
            HackAtom 2026 National Stage · Metsamor ~29% of generation (2025) · IAEA
            lifecycle data
          </footer>
        )}
      </div>
    </div>
  );
}
