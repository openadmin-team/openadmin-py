<!--
SPDX-FileCopyrightText: 2026 OpenAdmin

SPDX-License-Identifier: AGPL-3.0-or-later
-->

<script setup lang="ts" generic="TData extends RowData">
import { Columns3 } from "@lucide/vue"
import type { Cell, ColumnDef, Header, HeaderGroup, Row, RowData } from "@tanstack/vue-table"
import { FlexRender, useTable as useTanStackTable } from "@tanstack/vue-table"
import { useSortable } from "@vueuse/integrations/useSortable"
import { type ComponentPublicInstance, computed, ref } from "vue"
import { Button } from "@/components/ui/button"
import {
	DropdownMenu,
	DropdownMenuCheckboxItem,
	DropdownMenuContent,
	DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { ResizableHandle, ResizablePanel, ResizablePanelGroup } from "@/components/ui/resizable"
import { Skeleton } from "@/components/ui/skeleton"
import { type DataTableFeatures, features } from "@/lib/data-table"

const props = withDefaults(
	defineProps<{
		columns: ColumnDef<DataTableFeatures, TData>[]
		data: TData[]
		manualPagination?: boolean
		/** Rows per page, used to keep the table's height stable across page/search transitions. */
		pageSize?: number
		/** True only on the very first load, before any data has ever been shown. */
		isLoading?: boolean
		/** True while a newer page/search is loading and `data` still holds the previous result. */
		isPlaceholderData?: boolean
		emptyMessage?: string
	}>(),
	{ emptyMessage: "No results." },
)

const table = useTanStackTable({
	features,
	get data() {
		return props.data
	},
	get columns() {
		return props.columns
	},
	get manualPagination() {
		return props.manualPagination
	},
})

const FIXED_COLUMN_IDS = new Set(["__select__", "__actions__"])

type TableHeaderGroup = HeaderGroup<DataTableFeatures, TData>
type TableHeader = Header<DataTableFeatures, TData>
type TableRow = Row<DataTableFeatures, TData>

const getHeader = (headerGroup: TableHeaderGroup, id: string): TableHeader | undefined =>
	headerGroup.headers.find((header) => header.column.id === id)

const getDataHeaders = (headerGroup: TableHeaderGroup): TableHeader[] =>
	headerGroup.headers.filter((header) => !FIXED_COLUMN_IDS.has(header.column.id))

const getCell = (row: TableRow, id: string): Cell<DataTableFeatures, TData> | undefined =>
	row.getVisibleCells().find((cell) => cell.column.id === id)

const previewOrder = ref<string[] | null>(null)
const draggedColumnId = ref<string | null>(null)

const getDataCells = (row: TableRow) => {
	const cells = row.getVisibleCells().filter((cell) => !FIXED_COLUMN_IDS.has(cell.column.id))
	const cellsById = new Map(cells.map((cell) => [cell.column.id, cell]))
	const order = previewOrder.value ?? dataColumnIds.value
	return order.map((id) => cellsById.get(id)).filter((cell) => cell != null)
}

const onLayout = (headerGroup: TableHeaderGroup, sizes: number[]) => {
	const dataHeaders = getDataHeaders(headerGroup)
	table.setColumnSizing((previous) => ({
		...previous,
		...Object.fromEntries(dataHeaders.map((header, index) => [header.column.id, sizes[index]])),
	}))
}

const dataColumnIds = computed<string[]>({
	get: () => {
		const headerGroup = table.getHeaderGroups()[0]
		return headerGroup ? getDataHeaders(headerGroup).map((header) => header.column.id) : []
	},
	set: (ids) => {
		const headerGroup = table.getHeaderGroups()[0]
		if (!headerGroup) return

		let cursor = 0
		table.setColumnOrder(
			headerGroup.headers.map((header) =>
				FIXED_COLUMN_IDS.has(header.column.id) ? header.column.id : ids[cursor++],
			),
		)
	},
})

// Below this width per column, text starts getting uncomfortably cramped —
// beyond that point the table should grow wider and scroll instead of squeezing columns.
const MIN_COLUMN_WIDTH = 150
const SELECT_COLUMN_WIDTH = 40
const ACTIONS_COLUMN_WIDTH = 56

const hasSelectColumn = computed(() => table.getAllLeafColumns().some((c) => c.id === "__select__"))
const hasActionsColumn = computed(() =>
	table.getAllLeafColumns().some((c) => c.id === "__actions__"),
)

const bodyRows = computed(() => table.getRowModel().rows)

const firstHeaderGroup = computed<TableHeaderGroup | undefined>(() => table.getHeaderGroups()[0])
const skeletonHeaders = computed<TableHeader[]>(() =>
	firstHeaderGroup.value ? getDataHeaders(firstHeaderGroup.value) : [],
)

// While loading (no data ever shown yet) or showing a stale placeholder page (mid page/search
// transition), mask row values with skeletons instead of letting the table shrink to "No results."
const showSkeleton = computed(() => props.isLoading || props.isPlaceholderData)

// True first load only: there are no previous rows to reuse the shape/height of, so fall back
// to a generic page's worth of skeleton rows built from the column headers.
const initialSkeletonRowCount = computed(() => props.pageSize || 5)

// Once real data lands, pad a short last page back up to a full page so the table doesn't
// shrink just because this page has fewer rows than usual.
const fillerRowCount = computed(() => {
	if (showSkeleton.value || !props.manualPagination || !props.pageSize) return 0
	const count = bodyRows.value.length
	if (count === 0 || count >= props.pageSize) return 0
	return props.pageSize - count
})

// Same idea for a page with zero rows: the empty-state message takes up one row, and the
// rest is padded out to a full page instead of collapsing to a small fixed-height box.
const emptyFillerRowCount = computed(() => {
	if (!props.manualPagination || !props.pageSize) return 0
	return Math.max(props.pageSize - 1, 0)
})

// Rows are at least as wide as the table container, but grow past it (and scroll)
// once there isn't enough room to give every column its minimum width.
const rowWidthStyle = computed(() => {
	const fixedWidth =
		(hasSelectColumn.value ? SELECT_COLUMN_WIDTH : 0) +
		(hasActionsColumn.value ? ACTIONS_COLUMN_WIDTH : 0)
	const dataWidth = (dataColumnIds.value.length || 1) * MIN_COLUMN_WIDTH
	return { width: `max(100%, ${fixedWidth + dataWidth}px)` }
})

let headerRowEl: HTMLElement | null = null

const setHeaderRowEl = (component: ComponentPublicInstance | Element | null) => {
	headerRowEl = ((component as ComponentPublicInstance | null)?.$el ??
		component) as HTMLElement | null
}

const readDraggedOrder = (): string[] =>
	headerRowEl
		? Array.from(headerRowEl.querySelectorAll<HTMLElement>("[data-column-header]")).map(
				(el) => el.dataset.columnHeader ?? "",
			)
		: []

useSortable(() => headerRowEl, dataColumnIds, {
	draggable: "[data-column-header]",
	animation: 150,
	onStart: (event) => {
		draggedColumnId.value = event.item.dataset.columnHeader ?? null
	},
	onChange: () => {
		previewOrder.value = readDraggedOrder()
	},
	onEnd: () => {
		// Commit whatever order the DOM actually ended up in, rather than replaying
		// SortableJS's oldIndex/newIndex math ourselves — that counts every sibling
		// (including the interleaved `ResizableHandle`s) and drifted out of sync with
		// `dataColumnIds`, producing the wrong final order.
		const finalOrder = readDraggedOrder()
		if (finalOrder.length === dataColumnIds.value.length) {
			dataColumnIds.value = finalOrder
		}
		previewOrder.value = null
		draggedColumnId.value = null
	},
	// The default `onUpdate` would also try to commit a reorder using the mismatched
	// oldIndex/newIndex above; disable it so only the `onEnd` commit above applies.
	onUpdate: () => {},
})
</script>

<template>
	<div class="flex flex-col gap-2">
		<div class="flex items-center gap-2">
			<slot name="toolbar-start" />

			<DropdownMenu>
				<DropdownMenuTrigger as-child>
					<Button variant="outline" class="ml-auto">
						<Columns3 data-icon="inline-end" />
					</Button>
				</DropdownMenuTrigger>
				<DropdownMenuContent align="end">
					<DropdownMenuCheckboxItem
						v-for="column in table.getAllColumns().filter((column) => column.getCanHide())"
						:key="column.id"
						:model-value="column.getIsVisible()"
						@update:model-value="(value) => column.toggleVisibility(!!value)"
						@select="(event) => event.preventDefault()"
					>
						<FlexRender :render="column.columnDef.header" :props="{ table, column }" />
					</DropdownMenuCheckboxItem>
				</DropdownMenuContent>
			</DropdownMenu>
		</div>

		<div class="rounded-md border overflow-x-auto" role="table">
			<div role="rowgroup">
				<div
					v-for="headerGroup in table.getHeaderGroups()"
					:key="headerGroup.id"
					role="row"
					class="bg-muted/60 flex border-b"
					:style="rowWidthStyle"
				>
					<div
						v-if="getHeader(headerGroup, '__select__')"
						role="columnheader"
						class="text-muted-foreground flex h-10 w-10 shrink-0 items-center px-4 text-xs font-semibold tracking-wide [&:has([role=checkbox])]:pr-0"
					>
						<FlexRender :header="getHeader(headerGroup, '__select__')!" />
					</div>

					<ResizablePanelGroup
						:ref="setHeaderRowEl"
						direction="horizontal"
						class="h-10 flex-1"
						@layout="(sizes) => onLayout(headerGroup, sizes)"
					>
						<template v-for="(header, index) in getDataHeaders(headerGroup)" :key="header.id">
							<ResizableHandle
								v-if="index > 0"
								with-handle
								class="opacity-0 transition-opacity focus-visible:opacity-100 data-[state=hover]:opacity-100 data-[state=drag]:opacity-100"
							/>
							<ResizablePanel
								:default-size="header.getSize()"
								:min-size="10"
								:data-column-header="header.column.id"
								class="min-w-0"
							>
								<div
									role="columnheader"
									class="text-muted-foreground flex h-10 min-w-0 cursor-grab items-center truncate px-4 text-xs font-semibold tracking-wide active:cursor-grabbing"
									:class="{ 'bg-muted': header.column.id === draggedColumnId }"
								>
									<FlexRender v-if="!header.isPlaceholder" :header="header" />
								</div>
							</ResizablePanel>
						</template>
					</ResizablePanelGroup>

					<div
						v-if="getHeader(headerGroup, '__actions__')"
						role="columnheader"
						class="flex h-10 w-14 shrink-0 items-center justify-end px-4"
					>
						<FlexRender
							v-if="!getHeader(headerGroup, '__actions__')!.isPlaceholder"
							:header="getHeader(headerGroup, '__actions__')!"
						/>
					</div>
				</div>
			</div>

			<div role="rowgroup">
				<template v-if="bodyRows.length">
					<div
						v-for="row in bodyRows"
						:key="row.id"
						role="row"
						:data-state="row.getIsSelected() && 'selected'"
						class="data-[state=selected]:bg-muted flex border-b transition-colors last:border-0"
						:class="{ 'hover:bg-muted/50': !showSkeleton }"
						:style="rowWidthStyle"
					>
						<div
							v-if="getCell(row, '__select__')"
							role="cell"
							class="relative flex w-10 shrink-0 items-center px-4 py-3 [&:has([role=checkbox])]:pr-0"
						>
							<span :class="{ invisible: showSkeleton }">
								<FlexRender :cell="getCell(row, '__select__')!" />
							</span>
							<Skeleton
								v-if="showSkeleton"
								class="absolute left-4 top-1/2 size-4 -translate-y-1/2 rounded-sm"
							/>
						</div>

						<div class="flex min-w-0 flex-1">
							<div
								v-for="cell in getDataCells(row)"
								:key="cell.id"
								role="cell"
								class="relative flex min-w-0 items-center px-4 py-3"
								:class="{ 'bg-muted': cell.column.id === draggedColumnId }"
								:style="{ width: `${cell.column.getSize()}%` }"
							>
								<span class="min-w-0 truncate" :class="{ invisible: showSkeleton }">
									<FlexRender :cell="cell" />
								</span>
								<Skeleton
									v-if="showSkeleton"
									class="absolute left-4 top-1/2 h-4 w-[calc(100%-2rem)] max-w-40 -translate-y-1/2"
								/>
							</div>
						</div>

						<div
							v-if="getCell(row, '__actions__')"
							role="cell"
							class="relative flex w-14 shrink-0 items-center justify-end px-4 py-3"
						>
							<span :class="{ invisible: showSkeleton }">
								<FlexRender :cell="getCell(row, '__actions__')!" />
							</span>
							<Skeleton
								v-if="showSkeleton"
								class="absolute right-4 top-1/2 size-5 -translate-y-1/2 rounded-sm"
							/>
						</div>
					</div>

					<div
						v-for="n in fillerRowCount"
						:key="`filler-${n}`"
						role="row"
						aria-hidden="true"
						class="flex border-b last:border-0"
						:style="rowWidthStyle"
					>
						<div class="px-4 py-3 text-sm">&nbsp;</div>
					</div>
				</template>
				<template v-else-if="isLoading">
					<div
						v-for="n in initialSkeletonRowCount"
						:key="`skeleton-${n}`"
						role="row"
						aria-hidden="true"
						class="flex border-b last:border-0"
						:style="rowWidthStyle"
					>
						<div
							v-if="hasSelectColumn"
							role="cell"
							class="flex w-10 shrink-0 items-center px-4 py-3"
						>
							<Skeleton class="size-4 rounded-sm" />
						</div>

						<div class="flex min-w-0 flex-1">
							<div
								v-for="header in skeletonHeaders"
								:key="header.id"
								role="cell"
								class="flex min-w-0 items-center px-4 py-3"
								:style="{ width: `${header.column.getSize()}%` }"
							>
								<Skeleton class="h-4 w-full max-w-40" />
							</div>
						</div>

						<div
							v-if="hasActionsColumn"
							role="cell"
							class="flex w-14 shrink-0 items-center justify-end px-4 py-3"
						>
							<Skeleton class="size-5 rounded-sm" />
						</div>
					</div>
				</template>
				<template v-else-if="manualPagination && pageSize">
					<div
						role="row"
						class="flex items-center justify-center px-4 py-3 text-sm text-muted-foreground"
						:style="rowWidthStyle"
					>
						{{ emptyMessage }}
					</div>
					<div
						v-for="n in emptyFillerRowCount"
						:key="`empty-filler-${n}`"
						role="row"
						aria-hidden="true"
						class="flex"
						:style="rowWidthStyle"
					>
						<div class="px-4 py-3 text-sm">&nbsp;</div>
					</div>
				</template>
				<template v-else>
					<div
						role="row"
						class="flex h-24 items-center justify-center text-sm text-muted-foreground"
					>
						{{ emptyMessage }}
					</div>
				</template>
			</div>
		</div>

		<div class="text-sm text-muted-foreground">
			{{ table.getFilteredSelectedRowModel().rows.length }}
			of
			{{ table.getFilteredRowModel().rows.length }}
			row(s) selected.
		</div>
	</div>
</template>
