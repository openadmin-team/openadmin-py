// Tailwind CSS palette (500 shade) for each Color name in openadmin/spec/colors.py
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
  blue: '#3b82f6',
  indigo: '#6366f1',
  violet: '#8b5cf6',
  purple: '#a855f7',
  fuchsia: '#d946ef',
  pink: '#ec4899',
  rose: '#f43f5e',
  black: '#171717',
  white: '#ffffff',
}

const DEFAULT_COLOR = '#6366f1' // indigo, used when no color is set

export function colorToHex(name?: string | null): string {
  if (!name) return DEFAULT_COLOR
  return COLOR_HEX[name] ?? DEFAULT_COLOR
}

/** A palette of hex colors cycled through for multi-series charts, in COLORS order. */
export const CHART_PALETTE = [
  '#3b82f6',
  '#f97316',
  '#22c55e',
  '#a855f7',
  '#ef4444',
  '#06b6d4',
  '#eab308',
  '#ec4899',
  '#14b8a6',
  '#6366f1',
  '#84cc16',
  '#f43f5e',
]

export function paletteColor(index: number): string {
  return CHART_PALETTE[index % CHART_PALETTE.length]
}
