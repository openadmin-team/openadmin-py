<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { callComponent } from '../api/client'
import type { StatComponent } from '../types/spec'
import CardShell from './CardShell.vue'

const props = defineProps<{
  sectionId: string
  pageId: string
  component: StatComponent
}>()

const loading = ref(true)
const error = ref<string | null>(null)
const value = ref<unknown>(null)
const icon = ref<string | null | undefined>(props.component.icon)
const color = ref<string | null | undefined>(props.component.color)

function extract(response: unknown) {
  if (response && typeof response === 'object' && 'value' in (response as Record<string, unknown>)) {
    const wrapped = response as { value: unknown; icon?: string; color?: string }
    value.value = wrapped.value
    if (wrapped.icon) icon.value = wrapped.icon
    if (wrapped.color) color.value = wrapped.color
  } else {
    value.value = response
  }
}

async function load() {
  loading.value = true
  error.value = null
  try {
    const response = await callComponent(props.sectionId, props.pageId, props.component)
    extract(response)
  } catch (err) {
    error.value = err instanceof Error ? err.message : String(err)
  } finally {
    loading.value = false
  }
}

const displayValue = computed(() => {
  if (value.value === null || value.value === undefined) return '—'
  if (typeof value.value === 'boolean') return value.value ? 'Yes' : 'No'
  return String(value.value)
})

onMounted(load)
</script>

<template>
  <CardShell :icon="icon" :color="color" :title="component.name" :description="component.description">
    <p v-if="loading" class="stat-loading">…</p>
    <p v-else-if="error" class="stat-error">{{ error }}</p>
    <p v-else class="stat-value">{{ displayValue }}</p>
  </CardShell>
</template>

<style scoped>
.stat-value {
  font-size: 1.9rem;
  font-weight: 700;
  color: var(--text);
  margin: 0;
}

.stat-loading {
  color: var(--text-muted);
  margin: 0;
}

.stat-error {
  color: #dc2626;
  font-size: 0.8rem;
  margin: 0;
}
</style>
