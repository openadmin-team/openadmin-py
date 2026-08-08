<script setup lang="ts">
import { ref } from 'vue'
import type { TableComponent } from '../types/spec'
import { resolveIcon } from '../utils/icons'
import TableView from './TableView.vue'

const props = defineProps<{
  sectionId: string
  pageId: string
  tables: TableComponent[]
}>()

const activeId = ref(props.tables[0]?.id)
</script>

<template>
  <div class="table-tabs">
    <div class="table-tabs__bar">
      <button
        v-for="table in tables"
        :key="table.id"
        type="button"
        class="table-tabs__tab"
        :class="{ 'table-tabs__tab--active': table.id === activeId }"
        @click="activeId = table.id"
      >
        <component :is="resolveIcon(table.icon)" v-if="resolveIcon(table.icon)" :size="14" />
        {{ table.name }}
      </button>
    </div>
    <div v-for="table in tables" v-show="table.id === activeId" :key="table.id">
      <TableView :section-id="sectionId" :page-id="pageId" :component="table" />
    </div>
  </div>
</template>

<style scoped>
.table-tabs {
  grid-column: 1 / -1;
}

.table-tabs__bar {
  display: flex;
  flex-wrap: wrap;
  gap: 0.35rem;
  margin-bottom: 0.6rem;
}

.table-tabs__tab {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  border: 1px solid var(--border);
  background: var(--surface);
  color: var(--text-muted);
  padding: 0.4rem 0.75rem;
  border-radius: 0.5rem;
  font-size: 0.8rem;
  font-weight: 500;
}

.table-tabs__tab:hover {
  color: var(--text);
}

.table-tabs__tab--active {
  background: var(--accent-soft);
  color: var(--accent-strong);
  border-color: var(--accent-soft);
  font-weight: 600;
}
</style>
