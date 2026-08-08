export interface ExtractedResult {
  message?: string
  table?: unknown
  icon?: string
  color?: string
}

/** Normalize an Action/Form response, which per spec.py may be a bare string, null, or a response object. */
export function extractResult(response: unknown): ExtractedResult {
  if (response === null || response === undefined) return {}
  if (typeof response === 'string') return { message: response }
  if (typeof response === 'object') {
    const record = response as Record<string, unknown>
    return {
      message:
        (typeof record.toast === 'string' && record.toast) ||
        (typeof record.message === 'string' && record.message) ||
        undefined,
      table: record.table,
      icon: typeof record.icon === 'string' ? record.icon : undefined,
      color: typeof record.color === 'string' ? record.color : undefined,
    }
  }
  return {}
}
