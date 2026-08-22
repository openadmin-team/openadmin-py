// SPDX-FileCopyrightText: 2026 OpenAdmin
//
// SPDX-License-Identifier: AGPL-3.0-or-later

import type { MaybeRefOrGetter } from "vue"
import { computed, toValue } from "vue"
import { useSpec } from "./openadmin-spec"

export const useSectionSpec = (params: { sectionId: MaybeRefOrGetter<string> }) => {
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
