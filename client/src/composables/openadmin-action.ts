// SPDX-FileCopyrightText: 2026 OpenAdmin
//
// SPDX-License-Identifier: AGPL-3.0-or-later

import { computed, toValue, type MaybeRefOrGetter } from "vue"
import { usePageSpec } from "./openadmin-page"
import type { ActionComponent } from "@/schemas/action"

export const useAction = ({
	sectionId,
	pageId,
	actionId,
}: {
	sectionId: MaybeRefOrGetter<string>
	pageId: MaybeRefOrGetter<string>
	actionId: MaybeRefOrGetter<string>
}) => {
	const { page } = usePageSpec({ sectionId, pageId })
	const action = computed(() =>
		page.value?.components.find(
			(c): c is ActionComponent => c.type === "action" && c.id === toValue(actionId),
		),
	)

	return {
		action,
	}
}
