<script setup lang="ts" generic="TData extends RowData">
import type { ColumnDef, RowData } from "@tanstack/vue-table"
import { FlexRender, useTable as useTanStackTable } from "@tanstack/vue-table"
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
}>()

const table = useTanStackTable({
	features,
	get data() {
		return props.data
	},
	get columns() {
		return props.columns
	},
})
</script>

<template>
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
						<TableCell :colspan="columns.length" class="h-24 text-center"> No results. </TableCell>
					</TableRow>
				</template>
			</TableBody>
		</Table>
	</div>
</template>
