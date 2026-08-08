export function extractTableRows(response: unknown): Record<string, unknown>[] {
  if (Array.isArray(response)) return response as Record<string, unknown>[]
  if (response && typeof response === 'object' && 'data' in (response as Record<string, unknown>)) {
    const data = (response as { data: unknown }).data
    if (Array.isArray(data)) return data as Record<string, unknown>[]
  }
  return []
}

export interface TableMeta {
  icon?: string
  color?: string
}

export function extractTableMeta(response: unknown): TableMeta {
  if (response && typeof response === 'object' && !Array.isArray(response)) {
    const record = response as Record<string, unknown>
    return {
      icon: typeof record.icon === 'string' ? record.icon : undefined,
      color: typeof record.color === 'string' ? record.color : undefined,
    }
  }
  return {}
}

/** Column names across all rows, preserving first-seen order. */
export function collectColumns(rows: Record<string, unknown>[]): string[] {
  const columns: string[] = []
  const seen = new Set<string>()
  for (const row of rows) {
    for (const key of Object.keys(row)) {
      if (key === '__view__' || key === '__veiw__') continue
      if (!seen.has(key)) {
        seen.add(key)
        columns.push(key)
      }
    }
  }
  return columns
}

export function formatCellValue(value: unknown): string {
  if (value === null || value === undefined) return ''
  if (typeof value === 'boolean') return value ? 'true' : 'false'
  if (typeof value === 'object') return JSON.stringify(value)
  return String(value)
}
