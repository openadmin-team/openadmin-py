<script setup lang="ts">
import { computed } from "vue"
import { isTableRow, useTable } from "@/composables/openadmin-table"
import DataTable from "./DataTable.vue"

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

const data = computed(() => (rows.value ?? []).filter(isTableRow))
</script>

<template>
	<div class="container py-10 mx-auto">
		<DataTable :columns="columns" :data="data" />
	</div>
</template>
