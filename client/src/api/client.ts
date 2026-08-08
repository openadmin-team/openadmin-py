import type { Component, Spec } from '../types/spec'

// The example app mounts the AdminPanel sub-app at this prefix
// (see examples/main.py: app.mount("/admin", admin_panel.app)).
// The vite dev server proxies this same prefix to the FastAPI backend.
export const API_BASE = '/admin'

export class ApiError extends Error {
  status: number
  detail: unknown

  constructor(message: string, status: number, detail?: unknown) {
    super(message)
    this.name = 'ApiError'
    this.status = status
    this.detail = detail
  }
}

async function parseErrorResponse(response: Response): Promise<ApiError> {
  let payload: unknown = null
  try {
    payload = await response.json()
  } catch {
    // body wasn't JSON, fall through
  }

  if (payload && typeof payload === 'object') {
    if ('message' in payload && typeof (payload as { message: unknown }).message === 'string') {
      return new ApiError((payload as { message: string }).message, response.status, payload)
    }
    if ('detail' in payload) {
      const detail = (payload as { detail: unknown }).detail
      if (Array.isArray(detail)) {
        const message = detail
          .map((d) => {
            if (d && typeof d === 'object' && 'msg' in d) {
              const loc = Array.isArray((d as Record<string, unknown>).loc)
                ? ((d as Record<string, unknown>).loc as unknown[]).join('.')
                : ''
              return loc ? `${loc}: ${(d as Record<string, unknown>).msg}` : String((d as Record<string, unknown>).msg)
            }
            return String(d)
          })
          .join('; ')
        return new ApiError(message || 'Validation error', response.status, payload)
      }
      if (typeof detail === 'string') {
        return new ApiError(detail, response.status, payload)
      }
    }
  }

  return new ApiError(`${response.status} ${response.statusText}`, response.status, payload)
}

export async function fetchSpec(): Promise<Spec> {
  const response = await fetch(`${API_BASE}/spec.json`)
  if (!response.ok) throw await parseErrorResponse(response)
  return response.json()
}

export function componentUrl(sectionId: string, pageId: string, component: Component): string {
  return `${API_BASE}/${sectionId}/${pageId}/${component.type}/${component.id}`
}

export interface CallOptions {
  query?: Record<string, unknown>
  jsonBody?: unknown
  formData?: FormData
}

function appendQuery(url: string, query?: Record<string, unknown>): string {
  if (!query) return url
  const params = new URLSearchParams()
  for (const [key, value] of Object.entries(query)) {
    if (value === undefined || value === null || value === '') continue
    params.set(key, String(value))
  }
  const qs = params.toString()
  return qs ? `${url}?${qs}` : url
}

export async function callComponent(
  sectionId: string,
  pageId: string,
  component: Component,
  options: CallOptions = {},
): Promise<unknown> {
  const url = appendQuery(componentUrl(sectionId, pageId, component), options.query)
  const method = component.method.toUpperCase()

  const init: RequestInit = { method }

  if (options.formData) {
    init.body = options.formData
  } else if (options.jsonBody !== undefined && method !== 'GET' && method !== 'HEAD') {
    init.headers = { 'Content-Type': 'application/json' }
    init.body = JSON.stringify(options.jsonBody)
  }

  const response = await fetch(url, init)
  if (!response.ok) throw await parseErrorResponse(response)

  if (response.status === 204) return null
  const text = await response.text()
  if (!text) return null
  try {
    return JSON.parse(text)
  } catch {
    return text
  }
}
