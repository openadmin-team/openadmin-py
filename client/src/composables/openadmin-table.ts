// SPDX-FileCopyrightText: 2026 OpenAdmin
//
// SPDX-License-Identifier: AGPL-3.0-or-later

import { useQuery } from "@tanstack/vue-query"
import { type ColumnDef, createColumnHelper } from "@tanstack/vue-table"
import { computed, h, type MaybeRefOrGetter, ref, toValue } from "vue"
import DataTableDropDown from "@/components/page/DataTableDropDown.vue"
import type { DataTableFeatures } from "@/lib/data-table"
import { errorSchema } from "@/schemas/error"
import {
	type Table,
	type TableComponent,
	type TableData,
	type TableRow,
	tableSchema,
} from "@/schemas/table"
import type { AppError } from "@/types/errors"
import { usePageSpec } from "./openadmin-page"

export const useTable = ({
	sectionId,
	pageId,
	tableId,
}: {
	sectionId: MaybeRefOrGetter<string>
	pageId: MaybeRefOrGetter<string>
	tableId: MaybeRefOrGetter<string>
}) => {
	const { page } = usePageSpec({ sectionId, pageId })

	const table = computed(() =>
		page.value?.components.find(
			(c): c is TableComponent => c.type === "table" && c.id === toValue(tableId),
		),
	)

	const searchQuery = ref('')
	const pageIndex = ref(1)
	const perPage = ref(10)

	const hasSearch = computed(() => !!table.value?.query?.properties?.search)

	const hasPagination = computed(() => {
		const properties = table.value?.query?.properties
		return !!properties && "page" in properties && "per_page" in properties
	})

	const queryParams = computed(() => {
		const params = new URLSearchParams()

		if (hasSearch.value && searchQuery.value) {
			params.set("search", searchQuery.value)
		}

		if (hasPagination.value) {
			params.set("page", String(pageIndex.value))
			params.set("per_page", String(perPage.value))
		}

		return params
	})

	const { data, isLoading, isFetching } = useQuery<Table, AppError>({
		queryKey: computed(() => [
			"openadmin-stat",
			toValue(sectionId),
			toValue(pageId),
			toValue(tableId),
			queryParams.value.toString(),
		]),
		queryFn: async () => {
			const query = queryParams.value.toString()
			const response = await fetch(
				`${toValue(sectionId)}/${toValue(pageId)}/table/${toValue(tableId)}${query ? `?${query}` : ""}`,
			)
			const data = await response.json()

			if (!response.ok) {
				const error = errorSchema.parse(data)
				throw { ...error, status: response.status } satisfies AppError
			}

			return tableSchema.parse(data)
		},
		refetchInterval: computed(() => table.value?.refresh ?? false),
	})

	const rows = computed<TableData | null>(() => {
		if (!data.value) return null
		if (Array.isArray(data.value)) return data.value
		return data.value.data
	})

	const columnHelper = computed(() => createColumnHelper<DataTableFeatures, TableRow>())

	const columnKeys = computed(() => {
		const sample = rows.value?.find(isTableRow)
		if (!sample) return []
		return Object.keys(sample).filter((key) => !SPECIAL_ROW_KEYS.has(key))
	})

	const hasActions = computed(() =>
		(rows.value ?? []).some((row) => isTableRow(row) && (row.__actions__?.length ?? 0) > 0),
	)

	const columns = computed(() => {
		const dataColumns: ColumnDef<DataTableFeatures, TableRow, any>[] = columnKeys.value.map((key) =>
			columnHelper.value.accessor((row) => row[key], {
				id: key,
				header: table.value?.columns?.[key]?.label ?? key,
			}),
		)

		if (hasActions.value) {
			dataColumns.push(
				columnHelper.value.display({
					id: "__actions__",
					cell: ({ row }) => h(DataTableDropDown, { actions: row.original.__actions__ ?? [] }),
				}),
			)
		}

		return columnHelper.value.columns(dataColumns)
	})

	return {
		table,
		data,
		rows,
		columns,
		isLoading,
		isFetching,
	}
}

const SPECIAL_ROW_KEYS = new Set(["__view__", "__actions__", "__style__"])

export const isTableRow = (row: TableData[number]): row is TableRow =>
	typeof row === "object" && row !== null && !Array.isArray(row)
