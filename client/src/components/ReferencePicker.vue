<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { callComponent } from '../api/client'
import { findComponentById, useSpec } from '../composables/spec'
import { extractTableRows } from '../utils/table'
import { getObjectFields } from '../utils/jsonSchema'

const props = defineProps<{
  referenceId: string
  referenceField: string
  modelValue: unknown
  inputId?: string
  inputName?: string
}>()

const emit = defineEmits<{ 'update:modelValue': [value: unknown] }>()

const { state } = useSpec()
const rows = ref<Record<string, unknown>[]>([])
const loading = ref(false)
const loadError = ref<string | null>(null)

const located = computed(() => findComponentById(state.spec, props.referenceId, 'table'))

function labelFor(row: Record<string, unknown>): string {
  const candidateKeys = ['name', 'title', 'label']
  for (const key of candidateKeys) {
    if (key in row && row[key] !== null && row[key] !== undefined) return String(row[key])
  }
  return String(row[props.referenceField])
}

async function load() {
  const target = located.value
  if (!target || target.component.type !== 'table') return
  loading.value = true
  loadError.value = null
  try {
    const query = getObjectFields(target.component.query).some((f) => f.name === 'per_page')
      ? { per_page: 100 }
      : undefined
    const response = await callComponent(target.section.id, target.page.id, target.component, { query })
    rows.value = extractTableRows(response)
  } catch (err) {
    loadError.value = err instanceof Error ? err.message : String(err)
  } finally {
    loading.value = false
  }
}

onMounted(load)
watch(() => props.referenceId, load)

function onChange(event: Event) {
  const raw = (event.target as HTMLSelectElement).value
  if (raw === '') {
    emit('update:modelValue', undefined)
    return
  }
  const match = rows.value.find((r) => String(r[props.referenceField]) === raw)
  emit('update:modelValue', match ? match[props.referenceField] : raw)
}
</script>

<template>
  <div class="reference-picker">
    <select
      :id="inputId"
      :name="inputName"
      :value="modelValue === undefined || modelValue === null ? '' : String(modelValue)"
      @change="onChange"
    >
      <option value="">— select —</option>
      <option v-for="row in rows" :key="String(row[referenceField])" :value="String(row[referenceField])">
        {{ labelFor(row) }}
      </option>
    </select>
    <span v-if="loading" class="hint">loading…</span>
    <span v-else-if="loadError" class="hint hint--error">{{ loadError }}</span>
    <span v-else-if="!located" class="hint hint--error">unknown reference "{{ referenceId }}"</span>
  </div>
</template>

<style scoped>
.reference-picker {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

select {
  flex: 1;
}

.hint {
  font-size: 0.75rem;
  color: var(--text-muted);
}

.hint--error {
  color: #dc2626;
}
</style>
