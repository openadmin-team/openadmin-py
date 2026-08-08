<script setup lang="ts">
import { computed, reactive, ref } from 'vue'
import { callComponent } from '../api/client'
import { findComponentById, useSpec } from '../composables/spec'
import { getObjectFields } from '../utils/jsonSchema'
import { collectColumns, extractTableRows, formatCellValue } from '../utils/table'
import { humanize } from '../utils/text'
import Modal from './Modal.vue'

const props = defineProps<{
  referenceId: string
  referenceField: string
  modelValue: unknown[] | undefined
  inputId?: string
  inputName?: string
}>()

const emit = defineEmits<{ 'update:modelValue': [value: unknown[]] }>()

const { state } = useSpec()
const located = computed(() => findComponentById(state.spec, props.referenceId, 'table'))

const isOpen = ref(false)
const selectedLabels = reactive<Record<string, string>>({})

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

const selected = computed(() => props.modelValue ?? [])

let searchDebounce: ReturnType<typeof setTimeout> | undefined

function labelFor(row: Record<string, unknown>): string {
  for (const key of ['name', 'title', 'label']) {
    if (key in row && row[key] !== null && row[key] !== undefined) return String(row[key])
  }
  return String(row[props.referenceField])
}

function labelForValue(value: unknown): string {
  return selectedLabels[String(value)] ?? `#${value}`
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
    for (const row of rows.value) {
      selectedLabels[String(row[props.referenceField])] = labelFor(row)
    }
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

function isSelected(row: Record<string, unknown>): boolean {
  return selected.value.includes(row[props.referenceField])
}

function toggle(row: Record<string, unknown>) {
  const value = row[props.referenceField]
  if (isSelected(row)) {
    emit(
      'update:modelValue',
      selected.value.filter((v) => v !== value),
    )
  } else {
    selectedLabels[String(value)] = labelFor(row)
    emit('update:modelValue', [...selected.value, value])
  }
}

function remove(value: unknown) {
  emit(
    'update:modelValue',
    selected.value.filter((v) => v !== value),
  )
}

const modalTitle = computed(() => `Select ${located.value ? located.value.component.name : props.referenceId}`)
</script>

<template>
  <div class="multi-reference-picker">
    <input type="hidden" :id="inputId" :name="inputName" :value="JSON.stringify(selected)" />
    <div class="multi-reference-picker__chips">
      <span v-for="value in selected" :key="String(value)" class="chip">
        {{ labelForValue(value) }}
        <button type="button" aria-label="Remove" @click="remove(value)">✕</button>
      </span>
      <button type="button" class="reference-picker__trigger reference-picker__trigger--add" @click="open">
        + Add
      </button>
    </div>

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
              <tr v-for="(row, idx) in rows" :key="idx" class="picker-row" @click="toggle(row)">
                <td v-for="col in columns" :key="col">{{ formatCellValue(row[col]) }}</td>
                <td>
                  <button type="button" class="icon-button" @click.stop="toggle(row)">
                    {{ isSelected(row) ? 'Added' : 'Add' }}
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div v-if="hasPagination" class="table-pager">
          <button class="icon-button" :disabled="page <= 1" @click="prevPage">← Prev</button>
          <span>Page {{ page }}</span>
          <button class="icon-button" :disabled="!canGoNext" @click="nextPage">Next →</button>
        </div>

        <button type="button" class="primary-button picker-done" @click="isOpen = false">Done</button>
      </template>
    </Modal>
  </div>
</template>

<style scoped>
.multi-reference-picker__chips {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 0.4rem;
}

.chip {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  background: var(--accent-soft);
  color: var(--accent-strong);
  border-radius: 999px;
  padding: 0.25rem 0.5rem 0.25rem 0.7rem;
  font-size: 0.78rem;
  font-weight: 600;
}

.chip button {
  border: none;
  background: transparent;
  color: inherit;
  cursor: pointer;
  font-size: 0.75rem;
  line-height: 1;
  padding: 0;
}

.reference-picker__trigger {
  border: 1px dashed var(--border);
  background: var(--surface);
  border-radius: 999px;
  padding: 0.3rem 0.7rem;
  font-size: 0.78rem;
  color: var(--text-muted);
}

.reference-picker__trigger:hover {
  background: var(--surface-muted);
  color: var(--text);
}

.picker-search {
  margin-bottom: 0.75rem;
}

.picker-done {
  margin-top: 0.9rem;
}
</style>
