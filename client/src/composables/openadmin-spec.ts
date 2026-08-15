// SPDX-FileCopyrightText: 2026 OpenAdmin
//
// SPDX-License-Identifier: AGPL-3.0-or-later

import { queryOptions, useQuery } from "@tanstack/vue-query"
import type { MaybeRefOrGetter } from "vue"
import { computed, toValue } from "vue"
import { errorSchema } from "@/schemas/error"
import type { Spec } from "@/schemas/spec"
import { specSchema } from "@/schemas/spec"
import type { AppError } from "@/types/errors"

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

export const useSectionSpec = (params: { sectionId: MaybeRefOrGetter<string | undefined> }) => {
	const { data: specData, ...rest } = useSpec()

	const data = computed(() => {
		if (!specData.value) return null
		const sectionId = toValue(params.sectionId)
		return specData.value.sections.find((section) => section.id === sectionId) ?? null
	})

	return {
		data,
		...rest,
	}
}

export const usePageSpec = (params: {
	sectionId: MaybeRefOrGetter<string | undefined>
	pageId: MaybeRefOrGetter<string | undefined>
}) => {
	const { data: specData, ...rest } = useSectionSpec({ sectionId: params.sectionId })

	const page = computed(() => {
		if (!specData.value) return null
		const pageId = toValue(params.pageId)
		return specData.value.pages.find((page) => page.id === pageId) ?? null
	})
	const actions = computed(() => page.value?.components.filter((c) => c.type === "action") ?? [])
	const forms = computed(() => page.value?.components.filter((c) => c.type === "form") ?? [])

	return {
		page,
		actions,
		forms,
		...rest,
	}
}
