<script setup lang="ts">
import { computed, ref } from 'vue'
import { callComponent } from '../api/client'
import { findComponentById, useSpec } from '../composables/spec'
import { getObjectFields } from '../utils/jsonSchema'
import { collectColumns, extractTableRows, formatCellValue } from '../utils/table'
import { humanize } from '../utils/text'
import Modal from './Modal.vue'

const props = defineProps<{
  referenceId: string
  referenceField: string
  modelValue: unknown
  inputId?: string
  inputName?: string
}>()

const emit = defineEmits<{ 'update:modelValue': [value: unknown] }>()

const { state } = useSpec()
const located = computed(() => findComponentById(state.spec, props.referenceId, 'table'))

const isOpen = ref(false)
const selectedLabel = ref<string | null>(null)

const rows = ref<Record<string, unknown>[]>([])
const loading = ref(false)
const loadError = ref<string | null>(null)
const search = ref('')
const page = ref(1)
const perPage = ref(10)

const queryFields = computed(() => (located.value ? getObjectFields(located.value.component.query) : []))
const hasSearch = computed(() => queryFields.value.some((f) => f.name === 'search'))
const hasPagination = computed(() => queryFields.value.some((f) => f.name === 'page'))
const hasPerPage = computed(() => queryFields.value.some((f) => f.name === 'per_page'))
const columns = computed(() => collectColumns(rows.value))
const canGoNext = computed(() => rows.value.length > 0 && rows.value.length >= perPage.value)

let searchDebounce: ReturnType<typeof setTimeout> | undefined

function labelFor(row: Record<string, unknown>): string {
  for (const key of ['name', 'title', 'label']) {
    if (key in row && row[key] !== null && row[key] !== undefined) return String(row[key])
  }
  return String(row[props.referenceField])
}

async function load() {
  const target = located.value
  if (!target) return
  loading.value = true
  loadError.value = null
  try {
    const query: Record<string, unknown> = {}
    if (hasSearch.value && search.value) query.search = search.value
    if (hasPagination.value) query.page = page.value
    if (hasPerPage.value) query.per_page = perPage.value
    const response = await callComponent(target.section.id, target.page.id, target.component, { query })
    rows.value = extractTableRows(response)
  } catch (err) {
    loadError.value = err instanceof Error ? err.message : String(err)
    rows.value = []
  } finally {
    loading.value = false
  }
}

function open() {
  isOpen.value = true
  page.value = 1
  search.value = ''
  load()
}

function onSearchInput(value: string) {
  search.value = value
  page.value = 1
  clearTimeout(searchDebounce)
  searchDebounce = setTimeout(load, 350)
}

function prevPage() {
  if (page.value > 1) {
    page.value -= 1
    load()
  }
}

function nextPage() {
  page.value += 1
  load()
}

function select(row: Record<string, unknown>) {
  emit('update:modelValue', row[props.referenceField])
  selectedLabel.value = labelFor(row)
  isOpen.value = false
}

function clear() {
  emit('update:modelValue', undefined)
  selectedLabel.value = null
}

const displayLabel = computed(() => {
  if (selectedLabel.value) return selectedLabel.value
  if (props.modelValue !== undefined && props.modelValue !== null && props.modelValue !== '') {
    return `#${props.modelValue}`
  }
  return null
})

const modalTitle = computed(() => `Select ${located.value ? located.value.component.name : props.referenceId}`)
</script>

<template>
  <div class="reference-picker">
    <input type="hidden" :id="inputId" :name="inputName" :value="modelValue ?? ''" />
    <button type="button" class="reference-picker__trigger" @click="open">
      {{ displayLabel ?? 'Select…' }}
    </button>
    <button v-if="displayLabel" type="button" class="icon-button" title="Clear" @click="clear">✕</button>

    <Modal v-model="isOpen" :title="modalTitle">
      <p v-if="!located" class="table-status table-status--error">Unknown reference "{{ referenceId }}"</p>
      <template v-else>
        <input
          v-if="hasSearch"
          type="search"
          class="search-input picker-search"
          placeholder="Search…"
          :value="search"
          @input="onSearchInput(($event.target as HTMLInputElement).value)"
        />

        <p v-if="loading" class="table-status">Loading…</p>
        <p v-else-if="loadError" class="table-status table-status--error">{{ loadError }}</p>
        <p v-else-if="rows.length === 0" class="table-status">No rows.</p>

        <div v-else class="table-scroll">
          <table>
            <thead>
              <tr>
                <th v-for="col in columns" :key="col">{{ humanize(col) }}</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(row, idx) in rows" :key="idx" class="picker-row" @click="select(row)">
                <td v-for="col in columns" :key="col">{{ formatCellValue(row[col]) }}</td>
                <td><button type="button" class="icon-button" @click.stop="select(row)">Select</button></td>
              </tr>
            </tbody>
          </table>
        </div>

        <div v-if="hasPagination" class="table-pager">
          <button class="icon-button" :disabled="page <= 1" @click="prevPage">← Prev</button>
          <span>Page {{ page }}</span>
          <button class="icon-button" :disabled="!canGoNext" @click="nextPage">Next →</button>
        </div>
      </template>
    </Modal>
  </div>
</template>

<style scoped>
.reference-picker {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.reference-picker__trigger {
  flex: 1;
  text-align: left;
  border: 1px solid var(--input-border);
  background: var(--surface);
  border-radius: var(--radius-xs);
  padding: 0.4rem 0.55rem;
  font-size: 0.83rem;
  color: var(--text);
}

.reference-picker__trigger:hover {
  background: var(--surface-muted);
}

.picker-search {
  margin-bottom: 0.75rem;
}
</style>
