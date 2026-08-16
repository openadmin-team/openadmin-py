<!--
SPDX-FileCopyrightText: 2026 OpenAdmin

SPDX-License-Identifier: AGPL-3.0-or-later
-->

<script setup lang="ts" generic="TData extends RowData">
import type { ColumnDef, RowData } from "@tanstack/vue-table"
import { FlexRender, useTable as useTanStackTable } from "@tanstack/vue-table"
import { ChevronDownIcon } from "@lucide/vue"
import { Button } from "@/components/ui/button"
import {
	DropdownMenu,
	DropdownMenuCheckboxItem,
	DropdownMenuContent,
	DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import {
	Table,
	TableBody,
	TableCell,
	TableHead,
	TableHeader,
	TableRow,
} from "@/components/ui/table"
import { features, type DataTableFeatures } from "@/lib/data-table"

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
</script>

<template>
	<div class="flex flex-col gap-2">
		<div class="flex items-center gap-2">
			<slot name="toolbar-start" />

			<DropdownMenu>
				<DropdownMenuTrigger as-child>
					<Button variant="outline" class="ml-auto">
						Columns
						<ChevronDownIcon data-icon="inline-end" />
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
						{{ column.columnDef.header ?? column.id }}
					</DropdownMenuCheckboxItem>
				</DropdownMenuContent>
			</DropdownMenu>
		</div>

		<div class="border rounded-md">
			<Table>
				<TableHeader>
					<TableRow v-for="headerGroup in table.getHeaderGroups()" :key="headerGroup.id">
						<TableHead v-for="header in headerGroup.headers" :key="header.id">
							<FlexRender v-if="!header.isPlaceholder" :header="header" />
						</TableHead>
					</TableRow>
				</TableHeader>
				<TableBody>
					<template v-if="table.getRowModel().rows?.length">
						<TableRow
							v-for="row in table.getRowModel().rows"
							:key="row.id"
							:data-state="row.getIsSelected() && 'selected'"
						>
							<TableCell v-for="cell in row.getVisibleCells()" :key="cell.id">
								<FlexRender :cell="cell" />
							</TableCell>
						</TableRow>
					</template>
					<template v-else>
						<TableRow>
							<TableCell :colspan="columns.length" class="h-24 text-center">
								No results.
							</TableCell>
						</TableRow>
					</template>
				</TableBody>
			</Table>
		</div>
	</div>
</template>
