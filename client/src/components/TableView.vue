<script setup lang="ts">
import { computed, onMounted, reactive, ref, watch } from 'vue'
import { callComponent } from '../api/client'
import type { TableComponent } from '../types/spec'
import { getObjectFields } from '../utils/jsonSchema'
import { collectColumns, extractTableMeta, extractTableRows, formatCellValue } from '../utils/table'
import { humanize } from '../utils/text'
import CardShell from './CardShell.vue'

const props = defineProps<{
  sectionId: string
  pageId: string
  component: TableComponent
}>()

const queryFields = computed(() => getObjectFields(props.component.query))
const hasSearch = computed(() => queryFields.value.some((f) => f.name === 'search'))
const hasPagination = computed(() => queryFields.value.some((f) => f.name === 'page'))
const perPageField = computed(() => queryFields.value.find((f) => f.name === 'per_page'))
const otherFields = computed(() =>
  queryFields.value.filter((f) => !['search', 'page', 'per_page'].includes(f.name)),
)

const search = ref('')
const page = ref(1)
const perPage = ref((perPageField.value?.default as number | undefined) ?? 10)
const extraQuery = reactive<Record<string, unknown>>({})

const loading = ref(true)
const error = ref<string | null>(null)
const rows = ref<Record<string, unknown>[]>([])
const icon = ref<string | null | undefined>(props.component.icon)
const color = ref<string | null | undefined>(props.component.color)
const expandedRow = ref<number | null>(null)

const columns = computed(() => collectColumns(rows.value))
const hasViewColumn = computed(() => rows.value.some((r) => '__view__' in r))

let searchDebounce: ReturnType<typeof setTimeout> | undefined

async function load() {
  loading.value = true
  error.value = null
  try {
    const query: Record<string, unknown> = { ...extraQuery }
    if (hasSearch.value && search.value) query.search = search.value
    if (hasPagination.value) query.page = page.value
    if (perPageField.value) query.per_page = perPage.value

    const response = await callComponent(props.sectionId, props.pageId, props.component, { query })
    rows.value = extractTableRows(response)
    const meta = extractTableMeta(response)
    if (meta.icon) icon.value = meta.icon
    if (meta.color) color.value = meta.color
  } catch (err) {
    error.value = err instanceof Error ? err.message : String(err)
    rows.value = []
  } finally {
    loading.value = false
  }
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

const canGoNext = computed(() => rows.value.length > 0 && rows.value.length >= perPage.value)

watch(perPage, () => {
  page.value = 1
  load()
})

onMounted(load)
</script>

<template>
  <CardShell :icon="icon" :color="color" :title="component.name" :description="component.description" wide>
    <template #actions>
      <button class="icon-button" title="Refresh" @click="load">↻</button>
    </template>

    <div class="table-filters" v-if="hasSearch || otherFields.length">
      <input
        v-if="hasSearch"
        type="search"
        class="search-input"
        placeholder="Search…"
        :value="search"
        @input="onSearchInput(($event.target as HTMLInputElement).value)"
      />
      <label v-for="field in otherFields" :key="field.name" class="filter-field">
        <span>{{ humanize(field.name) }}</span>
        <input
          type="text"
          :value="extraQuery[field.name] ?? ''"
          @change="(e) => { extraQuery[field.name] = (e.target as HTMLInputElement).value; page = 1; load() }"
        />
      </label>
    </div>

    <p v-if="loading" class="table-status">Loading…</p>
    <p v-else-if="error" class="table-status table-status--error">{{ error }}</p>
    <p v-else-if="rows.length === 0" class="table-status">No rows.</p>

    <div v-else class="table-scroll">
      <table>
        <thead>
          <tr>
            <th v-for="col in columns" :key="col">{{ humanize(col) }}</th>
            <th v-if="hasViewColumn"></th>
          </tr>
        </thead>
        <tbody>
          <template v-for="(row, idx) in rows" :key="idx">
            <tr>
              <td v-for="col in columns" :key="col">{{ formatCellValue(row[col]) }}</td>
              <td v-if="hasViewColumn">
                <button
                  v-if="'__view__' in row"
                  class="icon-button"
                  @click="expandedRow = expandedRow === idx ? null : idx"
                >
                  {{ expandedRow === idx ? 'Hide' : 'View' }}
                </button>
              </td>
            </tr>
            <tr v-if="expandedRow === idx" class="row-detail">
              <td :colspan="columns.length + 1">{{ formatCellValue(row.__view__) }}</td>
            </tr>
          </template>
        </tbody>
      </table>
    </div>

    <div class="table-pager" v-if="hasPagination">
      <button class="icon-button" :disabled="page <= 1" @click="prevPage">← Prev</button>
      <span>Page {{ page }}</span>
      <button class="icon-button" :disabled="!canGoNext" @click="nextPage">Next →</button>
      <select v-if="perPageField" v-model.number="perPage">
        <option v-for="n in [10, 25, 50, 100]" :key="n" :value="n">{{ n }} / page</option>
      </select>
    </div>
  </CardShell>
</template>

<style scoped>
.table-filters {
  display: flex;
  flex-wrap: wrap;
  gap: 0.6rem;
  margin-bottom: 0.75rem;
}

.table-filters .search-input {
  flex: 1;
  min-width: 10rem;
}

.filter-field {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  font-size: 0.78rem;
  color: var(--text-muted);
}
</style>
