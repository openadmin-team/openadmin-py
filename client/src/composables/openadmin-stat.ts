// SPDX-FileCopyrightText: 2026 OpenAdmin
//
// SPDX-License-Identifier: AGPL-3.0-or-later

import { computed, toValue, type MaybeRefOrGetter } from "vue"
import { usePageSpec } from "./openadmin-spec"

export const useStat = ({
	sectionId,
	pageId,
	statId,
}: {
	sectionId: MaybeRefOrGetter<string>
	pageId: MaybeRefOrGetter<string>
	statId: MaybeRefOrGetter<string>
}) => {
	const { page } = usePageSpec({ sectionId, pageId })
	const stat = computed(() =>
		page.value?.components.filter((c) => c.type === "stat" && c.id === toValue(statId)),
	)

	return {
		stat,
	}
}
