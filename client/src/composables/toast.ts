import { reactive } from 'vue'

export type ToastKind = 'success' | 'error' | 'info'

export interface ToastItem {
  id: number
  kind: ToastKind
  message: string
}

let nextId = 1
const toasts = reactive<ToastItem[]>([])

function push(message: string, kind: ToastKind = 'info', durationMs = 4000) {
  const id = nextId++
  toasts.push({ id, kind, message })
  setTimeout(() => dismiss(id), durationMs)
}

function dismiss(id: number) {
  const idx = toasts.findIndex((t) => t.id === id)
  if (idx !== -1) toasts.splice(idx, 1)
}

export function useToast() {
  return {
    toasts,
    success: (message: string) => push(message, 'success'),
    error: (message: string) => push(message, 'error'),
    info: (message: string) => push(message, 'info'),
    dismiss,
  }
}
