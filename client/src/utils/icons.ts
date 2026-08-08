import * as icons from 'lucide-vue-next'
import type { Component } from 'vue'

const cache = new Map<string, Component | null>()

function toPascalCase(kebab: string): string {
  return kebab
    .split(/[-_]/)
    .filter(Boolean)
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join('')
}

/** Resolve a lucide icon by its kebab-case spec name (e.g. "users-round" -> UsersRound). */
export function resolveIcon(name?: string | null): Component | null {
  if (!name) return null
  if (cache.has(name)) return cache.get(name) ?? null

  const pascal = toPascalCase(name)
  const found = (icons as unknown as Record<string, Component>)[pascal] ?? null
  cache.set(name, found)
  return found
}
