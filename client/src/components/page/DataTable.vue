<!--
SPDX-FileCopyrightText: 2026 OpenAdmin

SPDX-License-Identifier: AGPL-3.0-or-later
-->

<script setup lang="ts" generic="TData extends RowData">
import { Columns3 } from "@lucide/vue"
import type { Cell, ColumnDef, Header, HeaderGroup, Row, RowData } from "@tanstack/vue-table"
import { FlexRender, useTable as useTanStackTable } from "@tanstack/vue-table"
import { moveArrayElement, useSortable } from "@vueuse/integrations/useSortable"
import { type ComponentPublicInstance, computed, ref } from "vue"
import { Button } from "@/components/ui/button"
import {
	DropdownMenu,
	DropdownMenuCheckboxItem,
	DropdownMenuContent,
	DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { ResizableHandle, ResizablePanel, ResizablePanelGroup } from "@/components/ui/resizable"
import { type DataTableFeatures, features } from "@/lib/data-table"

const props = defineProps<{
	columns: ColumnDef<DataTableFeatures, TData>[]
	data: TData[]
	manualPagination?: boolean
}>()

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
		previewOrder.value = null
		draggedColumnId.value = null
	},

	onUpdate: (event) => {
		const { oldDraggableIndex, newDraggableIndex } = event
		if (oldDraggableIndex == null || newDraggableIndex == null) return
		moveArrayElement(dataColumnIds, oldDraggableIndex, newDraggableIndex, event)
	},
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

		<div class="rounded-md border overflow-hidden" role="table">
			<div role="rowgroup">
				<div
					v-for="headerGroup in table.getHeaderGroups()"
					:key="headerGroup.id"
					role="row"
					class="bg-muted/60 flex border-b"
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
				<template v-if="table.getRowModel().rows?.length">
					<div
						v-for="row in table.getRowModel().rows"
						:key="row.id"
						role="row"
						:data-state="row.getIsSelected() && 'selected'"
						class="data-[state=selected]:bg-muted flex border-b transition-colors last:border-0 hover:bg-muted/50"
					>
						<div
							v-if="getCell(row, '__select__')"
							role="cell"
							class="flex w-10 shrink-0 items-center px-4 py-3 [&:has([role=checkbox])]:pr-0"
						>
							<FlexRender :cell="getCell(row, '__select__')!" />
						</div>

						<div class="flex min-w-0 flex-1">
							<div
								v-for="cell in getDataCells(row)"
								:key="cell.id"
								role="cell"
								class="flex min-w-0 items-center truncate px-4 py-3"
								:class="{ 'bg-muted': cell.column.id === draggedColumnId }"
								:style="{ width: `${cell.column.getSize()}%` }"
							>
								<FlexRender :cell="cell" />
							</div>
						</div>

						<div
							v-if="getCell(row, '__actions__')"
							role="cell"
							class="flex w-14 shrink-0 items-center justify-end px-4 py-3"
						>
							<FlexRender :cell="getCell(row, '__actions__')!" />
						</div>
					</div>
				</template>
				<template v-else>
					<div
						role="row"
						class="flex h-24 items-center justify-center text-sm text-muted-foreground"
					>
						No results.
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
