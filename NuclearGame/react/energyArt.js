/**
 * SVG facility illustrations — idle (unbuilt) vs acquired (operating).
 */

const art = {
  nuclear: {
    idle: `<svg viewBox="0 0 160 100" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
      <rect width="160" height="100" fill="#1a2030" rx="8"/>
      <ellipse cx="80" cy="88" rx="55" ry="6" fill="#0d1118" opacity="0.6"/>
      <path d="M52 88V52c0-8 12-14 28-14s28 6 28 14v36" fill="#2a3548" stroke="#3d4d66" stroke-width="1.5"/>
      <path d="M58 88V58c0-5 8-9 22-9s22 4 22 9v30" fill="#232d3d"/>
      <circle cx="80" cy="42" r="14" fill="#2a3548" stroke="#4a5f7a" stroke-width="1.5" stroke-dasharray="4 3"/>
      <path d="M80 28v6M80 50v6M66 42h-6M94 42h6" stroke="#4a5f7a" stroke-width="1.5" opacity="0.5"/>
      <text x="80" y="72" text-anchor="middle" fill="#5a6d85" font-size="7" font-family="system-ui,sans-serif">UNBUILT</text>
    </svg>`,
    acquired: `<svg viewBox="0 0 160 100" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
      <defs>
        <linearGradient id="nucGlow" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#00e5ff"/><stop offset="100%" stop-color="#0077b6"/>
        </linearGradient>
        <filter id="nucBlur"><feGaussianBlur stdDeviation="2"/></filter>
      </defs>
      <rect width="160" height="100" fill="#0d1828" rx="8"/>
      <ellipse cx="80" cy="88" rx="55" ry="6" fill="#00b4d8" opacity="0.15"/>
      <path d="M52 88V52c0-8 12-14 28-14s28 6 28 14v36" fill="#1a3a5c" stroke="#00b4d8" stroke-width="2"/>
      <path d="M58 88V58c0-5 8-9 22-9s22 4 22 9v30" fill="#143050"/>
      <circle cx="80" cy="42" r="14" fill="url(#nucGlow)" filter="url(#nucBlur)"/>
      <circle cx="80" cy="42" r="10" fill="#00e5ff" opacity="0.9"/>
      <path d="M80 30v4M80 50v4M68 42h-4M92 42h4" stroke="#7df9ff" stroke-width="2" stroke-linecap="round"/>
      <circle cx="80" cy="42" r="18" fill="none" stroke="#00b4d8" stroke-width="1" opacity="0.4">
        <animate attributeName="r" values="14;20;14" dur="2.5s" repeatCount="indefinite"/>
        <animate attributeName="opacity" values="0.5;0;0.5" dur="2.5s" repeatCount="indefinite"/>
      </circle>
      <rect x="70" y="78" width="20" height="4" rx="1" fill="#3fb950" opacity="0.8"/>
    </svg>`,
  },
  solar: {
    idle: `<svg viewBox="0 0 160 100" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
      <rect width="160" height="100" fill="#1a1c18" rx="8"/>
      <circle cx="120" cy="28" r="16" fill="#2a2820" stroke="#4a4535" stroke-width="1.5" stroke-dasharray="3 2"/>
      <g opacity="0.35">
        <path d="M120 10v6M120 42v6M104 28h-6M136 28h6" stroke="#5a5540" stroke-width="1.5"/>
      </g>
      <g transform="translate(24,48)">
        <rect width="72" height="36" rx="3" fill="#2a2e28" stroke="#3d4238" stroke-width="1.5"/>
        <line x1="24" y1="0" x2="24" y2="36" stroke="#3d4238"/>
        <line x1="48" y1="0" x2="48" y2="36" stroke="#3d4238"/>
        <line x1="0" y1="18" x2="72" y2="18" stroke="#3d4238"/>
      </g>
      <line x1="60" y1="84" x2="60" y2="92" stroke="#3d4238" stroke-width="2"/>
      <text x="80" y="72" text-anchor="middle" fill="#5a5d50" font-size="7" font-family="system-ui,sans-serif">UNBUILT</text>
    </svg>`,
    acquired: `<svg viewBox="0 0 160 100" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
      <defs>
        <linearGradient id="sunGrad" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#fff3b0"/><stop offset="100%" stop-color="#ffd166"/>
        </linearGradient>
      </defs>
      <rect width="160" height="100" fill="#1a1810" rx="8"/>
      <circle cx="120" cy="28" r="18" fill="url(#sunGrad)"/>
      <g stroke="#ffe566" stroke-width="2" stroke-linecap="round">
        <path d="M120 6v8M120 42v8M104 28h-8M136 28h8M109 17l6 6M125 33l6 6M131 17l-6 6M115 33l-6 6"/>
      </g>
      <g transform="translate(24,48)">
        <rect width="72" height="36" rx="3" fill="#1e3a5f" stroke="#4a9eff" stroke-width="1.5"/>
        <rect width="72" height="36" rx="3" fill="#2563eb" opacity="0.35"/>
        <line x1="24" y1="0" x2="24" y2="36" stroke="#7eb8ff" opacity="0.6"/>
        <line x1="48" y1="0" x2="48" y2="36" stroke="#7eb8ff" opacity="0.6"/>
        <line x1="0" y1="18" x2="72" y2="18" stroke="#7eb8ff" opacity="0.6"/>
      </g>
      <path d="M18 55 L42 75 L66 55" fill="none" stroke="#ffd166" stroke-width="1" opacity="0.3">
        <animate attributeName="opacity" values="0.2;0.5;0.2" dur="2s" repeatCount="indefinite"/>
      </path>
      <line x1="60" y1="84" x2="60" y2="92" stroke="#8a7a50" stroke-width="2"/>
    </svg>`,
  },
  hydro: {
    idle: `<svg viewBox="0 0 160 100" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
      <rect width="160" height="100" fill="#141a1e" rx="8"/>
      <path d="M0 72 Q40 68 80 72 T160 72 L160 100 L0 100Z" fill="#1a2830"/>
      <rect x="48" y="38" width="64" height="34" rx="2" fill="#2a3840" stroke="#3d5560" stroke-width="1.5"/>
      <rect x="70" y="48" width="20" height="24" fill="#1a2830" stroke="#3d5560" stroke-width="1"/>
      <path d="M52 72h56" stroke="#3d5560" stroke-width="2"/>
      <path d="M80 38 L80 28 L95 38Z" fill="#2a3840" stroke="#3d5560"/>
      <text x="80" y="62" text-anchor="middle" fill="#4a6570" font-size="7" font-family="system-ui,sans-serif">UNBUILT</text>
    </svg>`,
    acquired: `<svg viewBox="0 0 160 100" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
      <defs>
        <linearGradient id="waterGrad" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%" stop-color="#5eb8d4"/><stop offset="100%" stop-color="#2a8fa8"/>
        </linearGradient>
      </defs>
      <rect width="160" height="100" fill="#0d1a22" rx="8"/>
      <path d="M0 70 Q40 62 80 70 T160 70 L160 100 L0 100Z" fill="url(#waterGrad)" opacity="0.85"/>
      <path d="M0 78 Q50 72 100 78 T160 78" fill="none" stroke="#7df9ff" stroke-width="1" opacity="0.5">
        <animate attributeName="d" values="M0 78 Q50 72 100 78 T160 78;M0 78 Q50 76 100 72 T160 78;M0 78 Q50 72 100 78 T160 78" dur="3s" repeatCount="indefinite"/>
      </path>
      <rect x="48" y="38" width="64" height="34" rx="2" fill="#3a5560" stroke="#5eb8d4" stroke-width="2"/>
      <rect x="70" y="48" width="20" height="24" fill="#1a4050"/>
      <ellipse cx="80" cy="60" rx="6" ry="8" fill="#7df9ff" opacity="0.6">
        <animate attributeName="opacity" values="0.4;0.8;0.4" dur="1.5s" repeatCount="indefinite"/>
      </ellipse>
      <path d="M80 38 L80 26 L98 38Z" fill="#4a7080" stroke="#5eb8d4"/>
      <path d="M108 72c-4 6-8 6-12 0" fill="#5eb8d4" opacity="0.7">
        <animate attributeName="d" values="M108 72c-4 6-8 6-12 0;M108 74c-4 4-8 8-12 2;M108 72c-4 6-8 6-12 0" dur="2s" repeatCount="indefinite"/>
      </path>
    </svg>`,
  },
  fossil: {
    idle: `<svg viewBox="0 0 160 100" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
      <rect width="160" height="100" fill="#1a1816" rx="8"/>
      <rect x="44" y="42" width="72" height="46" rx="3" fill="#2a2620" stroke="#4a4035" stroke-width="1.5"/>
      <rect x="58" y="52" width="18" height="28" fill="#1a1816" stroke="#4a4035"/>
      <rect x="84" y="52" width="18" height="28" fill="#1a1816" stroke="#4a4035"/>
      <rect x="72" y="28" width="16" height="14" rx="2" fill="#2a2620" stroke="#4a4035"/>
      <rect x="76" y="8" width="8" height="22" fill="#2a2620" stroke="#4a4035"/>
      <text x="80" y="68" text-anchor="middle" fill="#5a5045" font-size="7" font-family="system-ui,sans-serif">UNBUILT</text>
    </svg>`,
    acquired: `<svg viewBox="0 0 160 100" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
      <defs>
        <linearGradient id="smokeGrad" x1="0%" y1="100%" x2="0%" y2="0%">
          <stop offset="0%" stop-color="#6a5a4a" stop-opacity="0"/><stop offset="100%" stop-color="#9a8a7a" stop-opacity="0.6"/>
        </linearGradient>
      </defs>
      <rect width="160" height="100" fill="#1a1410" rx="8"/>
      <rect x="44" y="42" width="72" height="46" rx="3" fill="#4a3828" stroke="#a08060" stroke-width="2"/>
      <rect x="58" y="52" width="18" height="28" fill="#2a2018"/>
      <rect x="84" y="52" width="18" height="28" fill="#2a2018"/>
      <rect x="58" y="58" width="18" height="8" fill="#e85d04" opacity="0.7">
        <animate attributeName="opacity" values="0.5;0.9;0.5" dur="1.2s" repeatCount="indefinite"/>
      </rect>
      <rect x="72" y="28" width="16" height="14" rx="2" fill="#5a4535" stroke="#c49a6c"/>
      <rect x="76" y="8" width="8" height="22" fill="#5a4535" stroke="#c49a6c"/>
      <ellipse cx="80" cy="6" rx="12" ry="8" fill="url(#smokeGrad)">
        <animate attributeName="cy" values="6;0;6" dur="3s" repeatCount="indefinite"/>
        <animate attributeName="rx" values="10;16;10" dur="3s" repeatCount="indefinite"/>
      </ellipse>
      <ellipse cx="72" cy="10" rx="8" ry="6" fill="#7a6a5a" opacity="0.4">
        <animate attributeName="cy" values="10;2;10" dur="2.5s" repeatCount="indefinite"/>
      </ellipse>
      <circle cx="130" cy="78" r="3" fill="#e05252" opacity="0.5"/>
    </svg>`,
  },
};

/** Small icon for card header (compact). */
const icons = {
  nuclear: {
    idle: `<svg viewBox="0 0 40 40"><circle cx="20" cy="20" r="8" fill="none" stroke="currentColor" stroke-width="1.5" stroke-dasharray="3 2" opacity="0.5"/><path d="M20 8v4M20 28v4M8 20h4M28 20h4" stroke="currentColor" stroke-width="1.5" opacity="0.4"/></svg>`,
    acquired: `<svg viewBox="0 0 40 40"><circle cx="20" cy="20" r="7" fill="currentColor" opacity="0.9"/><path d="M20 6v5M20 29v5M7 20h5M28 20h5" stroke="currentColor" stroke-width="2"/></svg>`,
  },
  solar: {
    idle: `<svg viewBox="0 0 40 40"><circle cx="28" cy="12" r="6" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.4"/><rect x="6" y="22" width="28" height="14" rx="2" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.5"/></svg>`,
    acquired: `<svg viewBox="0 0 40 40"><circle cx="28" cy="12" r="7" fill="currentColor"/><rect x="6" y="22" width="28" height="14" rx="2" fill="currentColor" opacity="0.5" stroke="currentColor" stroke-width="1.5"/></svg>`,
  },
  hydro: { idle: `<svg viewBox="0 0 40 40"><path d="M8 32h24v-14H8z" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.5"/><path d="M20 18v-8l8 8" fill="none" stroke="currentColor" opacity="0.4"/></svg>`,
    acquired: `<svg viewBox="0 0 40 40"><path d="M6 32 Q20 28 34 32 L34 36 L6 36Z" fill="currentColor" opacity="0.4"/><rect x="10" y="16" width="20" height="16" rx="1" fill="currentColor" opacity="0.7"/></svg>`,
  },
  fossil: { idle: `<svg viewBox="0 0 40 40"><rect x="10" y="18" width="20" height="16" rx="2" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.5"/><rect x="17" y="8" width="6" height="12" fill="none" stroke="currentColor" opacity="0.4"/></svg>`,
    acquired: `<svg viewBox="0 0 40 40"><rect x="10" y="18" width="20" height="16" rx="2" fill="currentColor" opacity="0.6"/><rect x="17" y="6" width="6" height="14" fill="currentColor"/><ellipse cx="20" cy="4" rx="5" ry="3" fill="currentColor" opacity="0.35"/></svg>`,
  },
};

export function getFacilityArt(sourceId, acquired = false) {
  const set = art[sourceId];
  if (!set) return "";
  return acquired ? set.acquired : set.idle;
}

export function getSourceIcon(sourceId, acquired = false) {
  const set = icons[sourceId];
  if (!set) return "";
  return acquired ? set.acquired : set.idle;
}

export function renderFacilityPanel(sourceId, acquired, label, color = "") {
  const state = acquired ? "acquired" : "idle";
  const style = color ? ` style="--facility-color:${color}"` : "";
  return `
    <div class="facility-panel ${state}" data-source="${sourceId}"${style}>
      <div class="facility-art">${getFacilityArt(sourceId, acquired)}</div>
      <span class="facility-label">${label}</span>
      <span class="facility-status">${acquired ? "Online" : "Not built"}</span>
    </div>
  `;
}
