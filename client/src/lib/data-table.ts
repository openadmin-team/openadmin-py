// SPDX-FileCopyrightText: 2026 OpenAdmin
//
// SPDX-License-Identifier: AGPL-3.0-or-later

import {
	columnFilteringFeature,
	columnVisibilityFeature,
	createExpandedRowModel,
	createFilteredRowModel,
	createPaginatedRowModel,
	createSortedRowModel,
	filterFn_includesString,
	rowExpandingFeature,
	rowPaginationFeature,
	rowSelectionFeature,
	rowSortingFeature,
	sortFn_alphanumeric,
	sortFn_text,
	tableFeatures,
} from "@tanstack/vue-table"

export const features = tableFeatures({
	columnFilteringFeature,
	columnVisibilityFeature,
	rowExpandingFeature,
	rowPaginationFeature,
	rowSelectionFeature,
	rowSortingFeature,
	expandedRowModel: createExpandedRowModel(),
	filteredRowModel: createFilteredRowModel(),
	paginatedRowModel: createPaginatedRowModel(),
	sortedRowModel: createSortedRowModel(),
	filterFns: { includesString: filterFn_includesString },
	sortFns: { alphanumeric: sortFn_alphanumeric, text: sortFn_text },
})

export type DataTableFeatures = typeof features
