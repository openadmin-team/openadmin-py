import { reactive } from 'vue'
import { fetchSpec } from '../api/client'
import type { Component, Page, Section, Spec } from '../types/spec'

interface SpecState {
  spec: Spec | null
  loading: boolean
  error: string | null
}

const state = reactive<SpecState>({ spec: null, loading: false, error: null })
let loadPromise: Promise<void> | null = null

function load(): Promise<void> {
  if (loadPromise) return loadPromise
  state.loading = true
  state.error = null
  loadPromise = fetchSpec()
    .then((spec) => {
      state.spec = spec
    })
    .catch((err) => {
      state.error = err instanceof Error ? err.message : String(err)
    })
    .finally(() => {
      state.loading = false
    })
  return loadPromise
}

export function useSpec() {
  return { state, load }
}

export function findSection(spec: Spec | null, sectionId: string): Section | undefined {
  return spec?.sections.find((s) => s.id === sectionId)
}

export function findPage(section: Section | undefined, pageId: string): Page | undefined {
  return section?.pages.find((p) => p.id === pageId)
}

export interface LocatedComponent {
  section: Section
  page: Page
  component: Component
}

/** Search the whole spec tree for a component by id (component ids are unique spec-wide). */
export function findComponentById(
  spec: Spec | null,
  componentId: string,
  type?: Component['type'],
): LocatedComponent | undefined {
  if (!spec) return undefined
  for (const section of spec.sections) {
    for (const page of section.pages) {
      for (const component of page.components) {
        if (component.id === componentId && (!type || component.type === type)) {
          return { section, page, component }
        }
      }
    }
  }
  return undefined
}
