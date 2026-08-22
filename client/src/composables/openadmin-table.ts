// SPDX-FileCopyrightText: 2026 OpenAdmin
//
// SPDX-License-Identifier: AGPL-3.0-or-later

import { keepPreviousData, useQuery } from "@tanstack/vue-query"
import { type ColumnDef, createColumnHelper } from "@tanstack/vue-table"
import { Icon } from "@iconify/vue"
import { computed, h, type MaybeRefOrGetter, ref, toValue, watch } from "vue"
import DataTableDropDown from "@/components/page/DataTableDropDown.vue"
import { Badge } from "@/components/ui/badge"
import { Checkbox } from "@/components/ui/checkbox"
import { Kbd } from "@/components/ui/kbd"
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
import { useColor } from "./colors"
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

	const searchQuery = ref("")
	const pageIndex = ref(1)
	const perPage = ref(10)

	const hasSearch = computed(() => !!table.value?.query?.properties?.search)

	watch(searchQuery, () => {
		pageIndex.value = 1
	})

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

	const { data, isLoading, isFetching, isPlaceholderData } = useQuery<Table, AppError>({
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
		placeholderData: keepPreviousData,
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
		const dataColumns: ColumnDef<DataTableFeatures, TableRow, any>[] = [
			columnHelper.value.display({
				id: "__select__",
				header: ({ table: t }) =>
					h(Checkbox, {
						modelValue:
							t.getIsAllPageRowsSelected() || (t.getIsSomePageRowsSelected() && "indeterminate"),
						"onUpdate:modelValue": (value: boolean | "indeterminate") =>
							t.toggleAllPageRowsSelected(!!value),
						ariaLabel: "Select all",
					}),
				cell: ({ row }) =>
					h(Checkbox, {
						modelValue: row.getIsSelected(),
						"onUpdate:modelValue": (value: boolean | "indeterminate") =>
							row.toggleSelected(!!value),
						ariaLabel: "Select row",
					}),
				enableSorting: false,
				enableHiding: false,
			}),
			...columnKeys.value.map((key) => {
				const column = table.value?.columns?.[key]
				const label = column?.label ?? key
				const { style } = useColor(column?.color ?? "slate")

				return columnHelper.value.accessor((row) => row[key], {
					id: key,
					size: 100 / (columnKeys.value.length || 1),
					minSize: 10,
					header: () =>
						h("div", { class: "flex items-center gap-1.5" }, [
							column?.icon
								? h(Icon, {
										icon: `lucide:${column.icon}`,
										class: [style.value.text, "size-3.5 shrink-0"],
									})
								: null,
							label,
						]),
					cell: ({ row, getValue }) => {
						const value = getValue()
						if (value === null || value === undefined) return h(Kbd, {}, () => "null")

						const valueConfig = row.original.__values__?.[key]
						const cellStyle = valueConfig?.style ?? column?.style
						const cellLabel = valueConfig?.label ?? String(value)
						const cellIcon = valueConfig?.icon
						const { style: cellColorStyle } = useColor(
							valueConfig?.color ?? column?.color ?? "slate",
						)

						switch (cellStyle) {
							case "image":
								return h("img", {
									src: String(value),
									alt: cellLabel,
									class: "size-8 rounded-md object-cover",
								})
							case "badge":
								return h(Badge, { variant: "secondary", class: "gap-1.5" }, () => [
									cellIcon
										? h(Icon, {
												icon: `lucide:${cellIcon}`,
												class: [cellColorStyle.value.text, "size-3 shrink-0"],
											})
										: h("span", {
												class: [cellColorStyle.value.dot, "size-1.5 rounded-full shrink-0"],
											}),
									cellLabel,
								])
							case "link":
								return h(
									"a",
									{
										href: String(value),
										target: "_blank",
										rel: "noopener noreferrer",
										title: String(value),
										class: [
											"block w-full min-w-0 truncate hover:underline",
											cellColorStyle.value.text,
										],
									},
									cellLabel,
								)
							case "file":
								return h(
									"a",
									{
										href: String(value),
										target: "_blank",
										rel: "noopener noreferrer",
										title: String(value),
										class: [
											"flex items-center gap-1.5 w-full min-w-0 hover:underline",
											cellColorStyle.value.text,
										],
									},
									[
										h(Icon, { icon: `lucide:${cellIcon ?? "file"}`, class: "size-3.5 shrink-0" }),
										h("span", { class: "min-w-0 truncate" }, cellLabel),
									],
								)
							default:
								return cellLabel
						}
					},
				})
			}),
		]

		if (hasActions.value) {
			dataColumns.push(
				columnHelper.value.display({
					id: "__actions__",
					enableHiding: false,
					cell: ({ row }) => h(DataTableDropDown, { actions: row.original.__actions__ ?? [] }),
				}),
			)
		}

		return columnHelper.value.columns(dataColumns)
	})

	const total = computed<number | null>(() => {
		if (!data.value || Array.isArray(data.value)) return null
		return data.value.total ?? null
	})

	const hasPreviousPage = computed(() => pageIndex.value > 1)

	const hasNextPage = computed(() => {
		if (total.value !== null) return pageIndex.value * perPage.value < total.value
		return (rows.value?.length ?? 0) >= perPage.value
	})

	return {
		table,
		data,
		rows,
		columns,
		isLoading,
		isFetching,
		isPlaceholderData,
		hasSearch,
		hasPagination,
		searchQuery,
		pageIndex,
		perPage,
		total,
		hasPreviousPage,
		hasNextPage,
	}
}

const SPECIAL_ROW_KEYS = new Set(["__view__", "__actions__", "__values__"])

export const isTableRow = (row: TableData[number]): row is TableRow =>
	typeof row === "object" && row !== null && !Array.isArray(row)
