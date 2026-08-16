<!--
SPDX-FileCopyrightText: 2026 OpenAdmin

SPDX-License-Identifier: AGPL-3.0-or-later
-->

<script setup lang="ts">
import { ChevronLeftIcon, ChevronRightIcon } from "@lucide/vue"
import { computed } from "vue"
import { Button } from "@/components/ui/button"
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
import DataTable from "./DataTable.vue"

const props = defineProps<{
	sectionId: string
	pageId: string
	tableId: string
}>()

const {
	columns,
	rows,
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
})

const data = computed(() => (rows.value ?? []).filter(isTableRow))
</script>

<template>
	<div class="container py-10 mx-auto space-y-4">
		<div v-if="hasSearch" class="flex items-center">
			<Input v-model="searchQuery" class="max-w-sm" placeholder="Search..." />
		</div>

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

		<div v-else-if="hasPagination" class="flex items-center justify-center gap-1">
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
</template>
