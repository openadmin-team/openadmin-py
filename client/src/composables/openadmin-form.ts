// SPDX-FileCopyrightText: 2026 OpenAdmin
//
// SPDX-License-Identifier: AGPL-3.0-or-later

import { computed, toValue, type MaybeRefOrGetter } from "vue"
import { usePageSpec } from "./openadmin-page"
import type { FormComponent } from "@/schemas/form"

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
		page.value?.components.find(
			(c): c is FormComponent => c.type === "form" && c.id === toValue(formId),
		),
	)

	return {
		form,
	}
}
