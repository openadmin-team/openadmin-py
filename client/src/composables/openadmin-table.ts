// SPDX-FileCopyrightText: 2026 OpenAdmin
//
// SPDX-License-Identifier: AGPL-3.0-or-later

import { computed, toValue, type MaybeRefOrGetter } from "vue"
import { usePageSpec } from "./openadmin-page"
import { useQuery } from "@tanstack/vue-query"
import { errorSchema } from "@/schemas/error"
import type { AppError } from "@/types/errors"
import {
	tableSchema,
	type Table,
	type TableComponent,
	type TableData,
	type TableRow,
} from "@/schemas/table"
import { createColumnHelper } from "@tanstack/vue-table"
import type { DataTableFeatures } from "@/lib/data-table"

const SPECIAL_ROW_KEYS = new Set(["__view__", "__actions__", "__style__"])

const isTableRow = (row: TableData[number]): row is TableRow =>
	typeof row === "object" && row !== null && !Array.isArray(row)

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
	
	const { data, isLoading, isFetching } = useQuery<Table, AppError>({
		queryKey: computed(() => [
			"openadmin-stat",
			toValue(sectionId),
			toValue(pageId),
			toValue(tableId),
		]),
		queryFn: async () => {
			const response = await fetch(
				`${toValue(sectionId)}/${toValue(pageId)}/table/${toValue(tableId)}`,
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

	const columns = computed(() =>
		columnHelper.value.columns(
			columnKeys.value.map((key) =>
				columnHelper.value.accessor((row) => row[key], {
					id: key,
					header: table.value?.columns?.[key]?.label ?? key,
				}),
			),
		),
	)

	return {
		table,
		data,
		rows,
		columns,
		isLoading,
		isFetching,
	}
}
