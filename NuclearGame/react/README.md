# The Grid — React integration

Drop-in React version of **Page 1** for the HackAtom Armenia app. Matches `../index.html` behavior (math, themes, demos, hydro slider, read-only fossil slider). **Logic lives in `gridEngine.js` only** — `index.html` imports it via ES module.

## Files

| File | Purpose |
|------|---------|
| `GridSimulator.jsx` | Main UI component |
| `GridSimulator.css` | Scoped styles (`.grid-simulator` root) |
| `gridEngine.js` | Pure math & story logic (no React) |
| `index.js` | Barrel exports |

## Quick integrate (Vite / CRA / Next)

1. Copy the entire `react/` folder into the team repo (e.g. `src/components/grid/`).

2. Import the component and CSS:

```jsx
import GridSimulator from "./components/grid/GridSimulator.jsx";
// CSS is imported inside GridSimulator.jsx — no extra import needed
```

3. Render on Page 1:

```jsx
export default function GridPage() {
  return <GridSimulator />;
}
```

### Minimal embed (no header/footer)

```jsx
<GridSimulator
  showHeader={false}
  showFooter={false}
  showDemos={true}
  showThemeToggle={true}
/>
```

### Props

| Prop | Default | Description |
|------|---------|-------------|
| `className` | `""` | Extra class on root `.grid-simulator` |
| `showHeader` | `true` | Title + subtitle |
| `showFooter` | `true` | HackAtom footer line |
| `showDemos` | `true` | Demo scenario buttons |
| `showThemeToggle` | `true` | Dark/light toggle |
| `initialNuclear` | `40` | Starting nuclear % |
| `initialSolar` | `25` | Starting solar % |
| `initialHydro` | `10` | Starting hydro % |
| `defaultTheme` | from `localStorage` | `"dark"` or `"light"` |

## Use engine only (no UI)

```jsx
import {
  calculateGridMetrics,
  getGridStoryMessage,
  DEMO_SCENARIOS,
} from "./components/grid/gridEngine.js";

const m = calculateGridMetrics(55, 30, 10);
// { nuclear, solar, hydro, fossil, stability, co2, cost }
```

## Path alias example (Vite)

```js
// vite.config.js
resolve: {
  alias: {
    "@grid": path.resolve(__dirname, "./src/components/grid"),
  },
},
```

```jsx
import GridSimulator from "@grid/GridSimulator.jsx";
```

## Vanilla HTML alternative

If you are not using React on this page, keep using `../index.html` or embed:

```html
<iframe src="../index.html" title="The Grid" width="100%" height="800" style="border:0;" />
```

## Requirements

- React 18+
- No other dependencies

## Handoff (from mission brief)

```jsx
import GridSimulator from "./react/GridSimulator.jsx";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/grid" element={<GridSimulator />} />
    </Routes>
  );
}
```

When updating formulas, edit **`gridEngine.js` only** — both HTML and React use that file.
