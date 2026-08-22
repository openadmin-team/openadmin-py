// SPDX-FileCopyrightText: 2026 OpenAdmin
//
// SPDX-License-Identifier: AGPL-3.0-or-later

import type { MaybeRefOrGetter } from "vue"
import { computed, toValue } from "vue"
import { useSectionSpec } from "./openadmin-section"

export const usePageSpec = (params: {
	sectionId: MaybeRefOrGetter<string>
	pageId: MaybeRefOrGetter<string>
}) => {
	const { data: specData, ...rest } = useSectionSpec({ sectionId: params.sectionId })

	const page = computed(() => {
		if (!specData.value) return null
		const pageId = toValue(params.pageId)
		return specData.value.pages.find((page) => page.id === pageId) ?? null
	})
	const actions = computed(() => page.value?.components.filter((c) => c.type === "action") ?? [])
	const forms = computed(() => page.value?.components.filter((c) => c.type === "form") ?? [])
	const stats = computed(() => page.value?.components.filter((c) => c.type === "stat") ?? [])
	const tables = computed(() => page.value?.components.filter((c) => c.type === "table") ?? [])
	const markdowns = computed(
		() => page.value?.components.filter((c) => c.type === "markdown") ?? [],
	)

	return {
		forms,
		page,
		actions,
		stats,
		tables,
		markdowns,
		...rest,
	}
}
