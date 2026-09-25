<!--
SPDX-FileCopyrightText: 2026 OpenAdmin

SPDX-License-Identifier: AGPL-3.0-or-later
-->

<script setup lang="ts">
import { ChevronLeftIcon, ChevronRightIcon } from "@lucide/vue"
import type { RowSelectionState } from "@tanstack/vue-table"
import { computed, ref, watch } from "vue"
import DataTable from "@/components/table/DataTable.vue"
import { Button } from "@/components/ui/button"
import {
	Drawer,
	DrawerClose,
	DrawerContent,
	DrawerFooter,
} from "@/components/ui/drawer"
import { Input } from "@/components/ui/input"
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
import type { TableRow as TableRowData } from "@/schemas/table"

const props = defineProps<{
	sectionId: string
	pageId: string
	tableId: string
	referenceField: string
	multiple: boolean
	title: string
	initialSelection: TableRowData[]
}>()

const emit = defineEmits<{
	confirm: [rows: TableRowData[]]
}>()

const open = defineModel<boolean>("open", { default: false })

function rowId(row: TableRowData) {
	return String(row[props.referenceField] ?? "")
}

const getRowId = (row: TableRowData) => rowId(row)

const {
	rows,
	columns: baseColumns,
	isLoading,
	isPlaceholderData,
	hasSearch,
	searchQuery,
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
	enabled: () => open.value,
})

const data = computed(() => (rows.value ?? []).filter(isTableRow))

const columns = computed(() =>
	baseColumns.value.filter((column) => {
		if (column.id === "__actions__") return false
		if (column.id === "__select__" && !props.multiple) return false
		return true
	}),
)

const emptyMessage = computed(() => (pageIndex.value > 1 ? "No rows left." : "No results."))

const rowSelection = ref<RowSelectionState>({})
const rowCache = ref(new Map<string, TableRowData>())

watch(open, (isOpen) => {
	if (!isOpen) return

	searchQuery.value = ""
	pageIndex.value = 1

	const seedSelection: RowSelectionState = {}
	const seedCache = new Map<string, TableRowData>()
	for (const row of props.initialSelection) {
		const id = rowId(row)
		seedSelection[id] = true
		seedCache.set(id, row)
	}
	rowSelection.value = seedSelection
	rowCache.value = seedCache
})

// Cache resolved rows as they're checked so a selection survives search/page
// changes even after the row that produced it scrolls out of the current page.
watch(rowSelection, (selection) => {
	for (const id of Object.keys(selection)) {
		if (rowCache.value.has(id)) continue
		const found = data.value.find((row) => rowId(row) === id)
		if (found) rowCache.value.set(id, found)
	}
})

const selectedCount = computed(() => Object.keys(rowSelection.value).length)

function selectRow(row: TableRowData) {
	emit("confirm", [row])
	open.value = false
}

function confirmSelection() {
	const selected = Object.keys(rowSelection.value)
		.map((id) => rowCache.value.get(id))
		.filter((row): row is TableRowData => !!row)
	emit("confirm", selected)
	open.value = false
}
</script>

<template>
	<Drawer v-model:open="open">
		<DrawerContent
			v-if="open"
			overlay-class="bg-transparent backdrop-blur-sm"
			class="data-[swipe-direction=down]:top-4 data-[swipe-direction=down]:mt-0 data-[swipe-direction=down]:max-h-none flex flex-col"
		>
			<div class="min-h-0 flex-1 overflow-auto px-4">
				<DataTable
					v-model:row-selection="rowSelection"
					:columns="columns"
					:data="data"
					:manual-pagination="hasPagination"
					:page-size="perPage"
					:is-loading="isLoading"
					:is-placeholder-data="isPlaceholderData"
					:empty-message="emptyMessage"
					:get-row-id="getRowId"
					:enable-row-selection="multiple"
					:enable-multi-row-selection="multiple"
					:row-clickable="!multiple"
					@row-click="selectRow"
				>
					<template v-if="hasSearch" #toolbar-start>
						<Input v-model="searchQuery" class="max-w-sm" placeholder="Search..." />
					</template>
				</DataTable>
			</div>

			<div v-if="hasPagination" class="px-4">
				<Pagination
					v-if="total !== null"
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

				<div v-else class="flex items-center justify-center gap-1">
					<Button
						variant="ghost"
						class="gap-1 px-2.5 sm:pr-2.5"
						:disabled="!hasPreviousPage"
						@click="pageIndex--"
					>
						<ChevronLeftIcon data-icon="inline-start" />
						<span class="hidden sm:block">Previous</span>
					</Button>
					<Button
						variant="ghost"
						class="gap-1 px-2.5 sm:pr-2.5"
						:disabled="!hasNextPage"
						@click="pageIndex++"
					>
						<span class="hidden sm:block">Next</span>
						<ChevronRightIcon data-icon="inline-end" />
					</Button>
				</div>
			</div>

			<DrawerFooter class="flex-row justify-end gap-2 border-t">
				<DrawerClose as-child>
					<Button type="button" variant="outline">Cancel</Button>
				</DrawerClose>
				<Button v-if="multiple" type="button" @click="confirmSelection">
					Select{{ selectedCount ? ` (${selectedCount})` : "" }}
				</Button>
			</DrawerFooter>
		</DrawerContent>
	</Drawer>
</template>
