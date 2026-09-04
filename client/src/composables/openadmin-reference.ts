// SPDX-FileCopyrightText: 2026 OpenAdmin
//
// SPDX-License-Identifier: AGPL-3.0-or-later

import type { MaybeRefOrGetter } from "vue"
import { computed, toValue } from "vue"
import { useSpec } from "./openadmin-spec"

export const useReference = ({ componentId }: { componentId: MaybeRefOrGetter<string> }) => {
	const { data, ...rest } = useSpec()

	const location = computed(() => {
		const id = toValue(componentId)

		for (const section of data.value?.sections ?? []) {
			for (const page of section.pages) {
				if (page.components.some((component) => component.id === id)) {
					return { componentId: id, pageId: page.id, sectionId: section.id }
				}
			}
		}

		return null
	})

	return {
		componentId: computed(() => location.value?.componentId ?? null),
		pageId: computed(() => location.value?.pageId ?? null),
		sectionId: computed(() => location.value?.sectionId ?? null),
		...rest,
	}
}
