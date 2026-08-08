<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import ComponentRenderer from '../components/ComponentRenderer.vue'
import TableTabs from '../components/TableTabs.vue'
import TableView from '../components/TableView.vue'
import { findPage, findSection, useSpec } from '../composables/spec'
import type { Component, TableComponent } from '../types/spec'

const route = useRoute()
const { state } = useSpec()

const sectionId = computed(() => String(route.params.sectionId))
const pageId = computed(() => String(route.params.pageId))

const section = computed(() => findSection(state.spec, sectionId.value))
const page = computed(() => findPage(section.value, pageId.value))

function isHidden(component: Component): boolean {
  return 'is_hidden' in component && component.is_hidden
}

const visibleComponents = computed(() => (page.value?.components ?? []).filter((c) => !isHidden(c)))

// Group every table on the page into one tabbed block, positioned where the
// first table appeared; everything else keeps its original relative order.
const layout = computed(() => {
  const before: Component[] = []
  const tables: TableComponent[] = []
  const after: Component[] = []
  let seenTable = false
  for (const component of visibleComponents.value) {
    if (component.type === 'table') {
      tables.push(component)
      seenTable = true
    } else if (!seenTable) {
      before.push(component)
    } else {
      after.push(component)
    }
  }
  return { before, tables, after }
})
</script>

<template>
  <div v-if="!page" class="page-missing">Page not found.</div>
  <div v-else class="page">
    <header class="page__header">
      <h1>{{ page.name }}</h1>
      <p v-if="page.description">{{ page.description }}</p>
    </header>

    <div class="page__grid">
      <ComponentRenderer
        v-for="component in layout.before"
        :key="component.id"
        :section-id="sectionId"
        :page-id="pageId"
        :component="component"
      />

      <TableTabs v-if="layout.tables.length > 1" :section-id="sectionId" :page-id="pageId" :tables="layout.tables" />
      <TableView
        v-else-if="layout.tables.length === 1"
        :section-id="sectionId"
        :page-id="pageId"
        :component="layout.tables[0]"
      />

      <ComponentRenderer
        v-for="component in layout.after"
        :key="component.id"
        :section-id="sectionId"
        :page-id="pageId"
        :component="component"
      />
    </div>
  </div>
</template>

<style scoped>
.page-missing {
  padding: 2rem;
  color: var(--text-muted);
}

.page__header {
  margin-bottom: 1.25rem;
}

.page__header h1 {
  margin: 0;
  font-size: 1.45rem;
  color: var(--text);
}

.page__header p {
  margin: 0.25rem 0 0;
  color: var(--text-muted);
  font-size: 0.85rem;
}

.page__grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 1rem;
  align-items: start;
}
</style>
