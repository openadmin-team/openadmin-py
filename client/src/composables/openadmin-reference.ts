// SPDX-FileCopyrightText: 2026 OpenAdmin
//
// SPDX-License-Identifier: AGPL-3.0-or-later

import type { MaybeRefOrGetter } from "vue"
import { computed, toValue } from "vue"
import type { Component } from "@/schemas/component"
import { useSpec } from "./openadmin-spec"

export const useReference = ({ componentId }: { componentId: MaybeRefOrGetter<string> }) => {
	const { data, ...rest } = useSpec()

	const find = (id: string) => {
		for (const section of data.value?.sections ?? []) {
			for (const page of section.pages) {
				const component = page.components.find((component) => component.id === id)
				if (component) {
					return { component, pageId: page.id, sectionId: section.id }
				}
			}
		}

		return null
	}

	const location = computed(() => find(toValue(componentId)))

	return {
		componentId: computed(() => (location.value ? toValue(componentId) : null)),
		pageId: computed(() => location.value?.pageId ?? null),
		sectionId: computed(() => location.value?.sectionId ?? null),
		component: computed<Component | null>(() => location.value?.component ?? null),
		find,
		...rest,
	}
}
