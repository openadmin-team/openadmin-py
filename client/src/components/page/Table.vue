<script setup lang="ts">
import { useTable } from "@/composables/openadmin-table"
import DataTable from "./DataTable.vue";

const props = defineProps<{
	sectionId: string
	pageId: string
	tableId: string
}>()

const { columns, rows } = useTable({
	sectionId: props.sectionId,
	pageId: props.pageId,
	tableId: props.tableId,
})
</script>

<template>
     <div class="container py-10 mx-auto">
    <DataTable :columns="columns" :data="rows" />
  </div>
</template>
