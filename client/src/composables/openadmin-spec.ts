// SPDX-FileCopyrightText: 2026 OpenAdmin
//
// SPDX-License-Identifier: AGPL-3.0-or-later

import { queryOptions, useQuery } from "@tanstack/vue-query"
import { computed } from "vue"
import type { AppError } from "@/types/errors"
import { errorSchema } from "@/schemas/error"
import type { Spec } from "@/schemas/spec"
import { specSchema } from "@/schemas/spec"

export const useOpenAdminSpecOptions = queryOptions<Spec, AppError>({
	queryKey: ["openadmin-spec"],
	queryFn: async () => {
		const response = await fetch("api/openadmin.json")
		const data = await response.json()

		if (!response.ok) {
			const error = errorSchema.parse(data)
			throw { ...error, status: response.status } satisfies AppError
		}

		return specSchema.parse(data)
	},
})

export const useSpec = () => {
	return useQuery<Spec, AppError>(useOpenAdminSpecOptions)
}

export const useSectionSpec = ({ sectionId }: { sectionId: string }) => {
	const { data: specData, ...rest } = useSpec()

	const data = computed(() => {
		if (!specData.value) return null
		return specData.value.sections.find((section) => section.id === sectionId) ?? null
	})

	return {
		data,
		...rest,
	}
}

export const usePageSpec = ({ sectionId, pageId }: { sectionId: string; pageId: string }) => {
	const { data: specData, ...rest } = useSectionSpec({ sectionId })

	const data = computed(() => {
		if (!specData.value) return null
		return specData.value.pages.find((page) => page.id === pageId) ?? null
	})

	return {
		data,
		...rest,
	}
}
