<script setup lang="ts">
import type { Component } from '../types/spec'
import ActionCard from './ActionCard.vue'
import BarChartCard from './BarChartCard.vue'
import FormCard from './FormCard.vue'
import MarkdownCard from './MarkdownCard.vue'
import PieChartCard from './PieChartCard.vue'
import StatCard from './StatCard.vue'
import TableView from './TableView.vue'
import UnsupportedCard from './UnsupportedCard.vue'

defineProps<{
  sectionId: string
  pageId: string
  component: Component
}>()
</script>

<template>
  <StatCard v-if="component.type === 'stat'" :section-id="sectionId" :page-id="pageId" :component="component" />
  <TableView
    v-else-if="component.type === 'table'"
    :section-id="sectionId"
    :page-id="pageId"
    :component="component"
  />
  <FormCard v-else-if="component.type === 'form'" :section-id="sectionId" :page-id="pageId" :component="component" />
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
