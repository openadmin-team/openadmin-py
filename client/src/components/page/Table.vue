<!--
SPDX-FileCopyrightText: 2026 OpenAdmin

SPDX-License-Identifier: AGPL-3.0-or-later
-->

<script setup lang="ts">
import { computed } from "vue"
import { Button } from "@/components/ui/button"
import {
	Pagination,
	PaginationContent,
	PaginationEllipsis,
	PaginationFirst,
	PaginationItem,
	PaginationLast,
	PaginationNext,
	PaginationPrevious,
} from "@/components/ui/pagination"
import { isTableRow, useTable } from "@/composables/openadmin-table"
import DataTable from "./DataTable.vue"

const props = defineProps<{
	sectionId: string
	pageId: string
	tableId: string
}>()

const {
	columns,
	rows,
	hasPagination,
	pageIndex,
	perPage,
	total,
	hasPreviousPage,
	hasNextPage,
} = useTable({
	sectionId: props.sectionId,
	pageId: props.pageId,
	tableId: props.tableId,
})

const data = computed(() => (rows.value ?? []).filter(isTableRow))
</script>

<template>
	<div class="container py-10 mx-auto space-y-4">
		<DataTable :columns="columns" :data="data" :manual-pagination="hasPagination" />

		<Pagination
			v-if="hasPagination && total !== null"
			v-model:page="pageIndex"
			:total="total"
			:items-per-page="perPage"
			:sibling-count="1"
			show-edges
		>
			<PaginationContent v-slot="{ items }">
				<PaginationFirst />
				<PaginationPrevious />

				<template v-for="(item, index) in items">
					<PaginationItem
						v-if="item.type === 'page'"
						:key="index"
						:value="item.value"
						:is-active="item.value === pageIndex"
					>
						{{ item.value }}
					</PaginationItem>
					<PaginationEllipsis v-else :key="item.type" :index="index" />
				</template>

				<PaginationNext />
				<PaginationLast />
			</PaginationContent>
		</Pagination>

		<div v-else-if="hasPagination" class="flex items-center justify-end gap-2">
			<Button variant="outline" size="sm" :disabled="!hasPreviousPage" @click="pageIndex--">
				Previous
			</Button>
			<Button variant="outline" size="sm" :disabled="!hasNextPage" @click="pageIndex++">
				Next
			</Button>
		</div>
	</div>
</template>
