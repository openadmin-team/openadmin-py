// SPDX-FileCopyrightText: 2026 OpenAdmin
//
// SPDX-License-Identifier: AGPL-3.0-or-later

import { computed, toValue, type MaybeRefOrGetter } from "vue"
import { usePageSpec } from "./openadmin-page"

export const useForm = ({
	sectionId,
	pageId,
	formId,
}: {
	sectionId: MaybeRefOrGetter<string>
	pageId: MaybeRefOrGetter<string>
	formId: MaybeRefOrGetter<string>
}) => {
	const { page } = usePageSpec({ sectionId, pageId })
	const form = computed(() =>
		page.value?.components.filter((c) => c.type === "form" && c.id === toValue(formId)),
	)

	return {
		form,
	}
}
