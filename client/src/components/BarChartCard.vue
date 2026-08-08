<script setup lang="ts">
import { Chart } from 'chart.js/auto'
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { callComponent } from '../api/client'
import type { BarChartComponent } from '../types/spec'
import { colorToHex, paletteColor } from '../utils/colors'
import { resolveIcon } from '../utils/icons'
import { humanize } from '../utils/text'
import CardShell from './CardShell.vue'

const props = defineProps<{
  sectionId: string
  pageId: string
  component: BarChartComponent
}>()

const loading = ref(true)
const error = ref<string | null>(null)
const rows = ref<Record<string, unknown>[]>([])
const canvasEl = ref<HTMLCanvasElement | null>(null)
let chart: Chart | null = null

const categoryKey = computed(() => props.component.data_key || 'label')
const seriesKeys = computed(() => (props.component.config ? Object.keys(props.component.config) : ['value']))
const CaptionIcon = computed(() => resolveIcon(props.component.caption_icon))

async function load() {
  loading.value = true
  error.value = null
  try {
    const response = await callComponent(props.sectionId, props.pageId, props.component)
    if (response && typeof response === 'object' && !Array.isArray(response) && 'data' in (response as Record<string, unknown>)) {
      rows.value = ((response as Record<string, unknown>).data as Record<string, unknown>[]) ?? []
    } else if (Array.isArray(response)) {
      rows.value = response as Record<string, unknown>[]
    } else {
      rows.value = []
    }
  } catch (err) {
    error.value = err instanceof Error ? err.message : String(err)
  } finally {
    loading.value = false
  }
}

function render() {
  if (!canvasEl.value) return
  const labels = rows.value.map((r) => String(r[categoryKey.value]))
  const datasets = seriesKeys.value.map((key, idx) => {
    const cfg = props.component.config?.[key]
    return {
      label: cfg?.name || humanize(key),
      data: rows.value.map((r) => Number(r[key])),
      backgroundColor: cfg?.color ? colorToHex(cfg.color) : paletteColor(idx),
    }
  })

  chart?.destroy()
  chart = new Chart(canvasEl.value, {
    type: 'bar',
    data: { labels, datasets },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: datasets.length > 1, labels: { boxWidth: 12, font: { size: 11 } } } },
      scales: { y: { beginAtZero: true } },
    },
  })
}

onMounted(async () => {
  await load()
  await nextTick()
  render()
})

watch(rows, async () => {
  await nextTick()
  render()
})

onBeforeUnmount(() => chart?.destroy())
</script>

<template>
  <CardShell :icon="component.icon" :color="component.color" :title="component.name" :description="component.description">
    <p v-if="loading" class="chart-status">Loading…</p>
    <p v-else-if="error" class="chart-status chart-status--error">{{ error }}</p>
    <p v-else-if="rows.length === 0" class="chart-status">No data.</p>
    <div v-show="!loading && !error && rows.length" class="chart-canvas-wrap">
      <canvas ref="canvasEl"></canvas>
    </div>
    <div v-if="component.caption" class="chart-caption">
      <component :is="CaptionIcon" v-if="CaptionIcon" :size="14" />
      <div>
        <div class="chart-caption__title">{{ component.caption }}</div>
        <div v-if="component.caption_description" class="chart-caption__desc">{{ component.caption_description }}</div>
      </div>
    </div>
  </CardShell>
</template>

<style scoped>
.chart-status {
  color: var(--text-muted);
  font-size: 0.85rem;
}

.chart-status--error {
  color: #dc2626;
}

.chart-canvas-wrap {
  position: relative;
  height: 14rem;
}

.chart-caption {
  display: flex;
  align-items: flex-start;
  gap: 0.5rem;
  margin-top: 0.75rem;
  padding-top: 0.6rem;
  border-top: 1px solid var(--border);
  font-size: 0.78rem;
  color: var(--text-muted);
}

.chart-caption__title {
  font-weight: 600;
  color: var(--text);
}
</style>
