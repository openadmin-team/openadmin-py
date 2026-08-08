// Tailwind CSS palette (500 shade) for each Color name in openadmin/spec/colors.py.
// "blue" is pulled to the brand's structural primary (DESIGN.md) for cohesion
// when a spec explicitly requests it; the rest stay close to Tailwind so
// arbitrary backend-declared names (violet, amber, emerald, ...) stay
// recognizable by name.
const COLOR_HEX: Record<string, string> = {
  slate: '#64748b',
  gray: '#6b7280',
  zinc: '#71717a',
  neutral: '#737373',
  stone: '#78716c',
  red: '#ef4444',
  orange: '#f97316',
  amber: '#f59e0b',
  yellow: '#eab308',
  lime: '#84cc16',
  green: '#22c55e',
  emerald: '#10b981',
  teal: '#14b8a6',
  cyan: '#06b6d4',
  sky: '#0ea5e9',
  blue: '#0075de',
  indigo: '#6366f1',
  violet: '#8b5cf6',
  purple: '#a855f7',
  fuchsia: '#d946ef',
  pink: '#ec4899',
  rose: '#f43f5e',
  black: '#171717',
  white: '#ffffff',
}

const DEFAULT_COLOR = '#0075de' // DESIGN.md primary, used when no color is set

export function colorToHex(name?: string | null): string {
  if (!name) return DEFAULT_COLOR
  return COLOR_HEX[name] ?? DEFAULT_COLOR
}

/**
 * Decorative-only palette for multi-series charts (DESIGN.md's "sticker"
 * colors) — used only when a component doesn't declare its own series
 * colors, never for structural UI.
 */
export const CHART_PALETTE = [
  '#62aef0', // sticker-sky
  '#dd5b00', // sticker-orange
  '#1aae39', // sticker-green
  '#d6b6f6', // sticker-purple
  '#ff64c8', // sticker-pink
  '#2a9d99', // sticker-teal
  '#523410', // sticker-brown
  '#391c57', // sticker-purple-deep
]

export function paletteColor(index: number): string {
  return CHART_PALETTE[index % CHART_PALETTE.length]
}
