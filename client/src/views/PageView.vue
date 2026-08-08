<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import ActionCard from '../components/ActionCard.vue'
import BarChartCard from '../components/BarChartCard.vue'
import FormCard from '../components/FormCard.vue'
import MarkdownCard from '../components/MarkdownCard.vue'
import PieChartCard from '../components/PieChartCard.vue'
import StatCard from '../components/StatCard.vue'
import TableView from '../components/TableView.vue'
import UnsupportedCard from '../components/UnsupportedCard.vue'
import { findPage, findSection, useSpec } from '../composables/spec'
import type { Component } from '../types/spec'

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
</script>

<template>
  <div v-if="!page" class="page-missing">Page not found.</div>
  <div v-else class="page">
    <header class="page__header">
      <h1>{{ page.name }}</h1>
      <p v-if="page.description">{{ page.description }}</p>
    </header>

    <div class="page__grid">
      <template v-for="component in visibleComponents" :key="component.id">
        <StatCard v-if="component.type === 'stat'" :section-id="sectionId" :page-id="pageId" :component="component" />
        <TableView
          v-else-if="component.type === 'table'"
          :section-id="sectionId"
          :page-id="pageId"
          :component="component"
        />
        <FormCard
          v-else-if="component.type === 'form'"
          :section-id="sectionId"
          :page-id="pageId"
          :component="component"
        />
        <ActionCard
          v-else-if="component.type === 'action'"
          :section-id="sectionId"
          :page-id="pageId"
          :component="component"
        />
        <MarkdownCard
          v-else-if="component.type === 'markdown'"
          :section-id="sectionId"
          :page-id="pageId"
          :component="component"
        />
        <BarChartCard
          v-else-if="component.type === 'bar-chart'"
          :section-id="sectionId"
          :page-id="pageId"
          :component="component"
        />
        <PieChartCard
          v-else-if="component.type === 'pie-chart'"
          :section-id="sectionId"
          :page-id="pageId"
          :component="component"
        />
        <UnsupportedCard v-else :component="component" />
      </template>
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
  font-size: 1.3rem;
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
