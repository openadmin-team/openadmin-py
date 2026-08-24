// SPDX-FileCopyrightText: 2026 OpenAdmin
//
// SPDX-License-Identifier: AGPL-3.0-or-later

import { computed, toValue, type MaybeRefOrGetter } from "vue"
import { usePageSpec } from "./openadmin-page"
import type { FormComponent } from "@/schemas/form"
import z from "zod"

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
	const { querySchema, formSchema, bodySchema } = useFormSchema({ form })

	return {
		form,
		querySchema,
		formSchema,
		bodySchema,
	}
}

export const useFormSchema = ({ form }: { form: MaybeRefOrGetter<FormComponent | undefined> }) => {
	const querySchema = computed(() => {
		const query = toValue(form)?.query
		return query ? z.fromJSONSchema(query as z.core.JSONSchema.JSONSchema) : null
	})
	
	const bodySchema = computed(() => {
		const body = toValue(form)?.body
		return body ? z.fromJSONSchema(body as z.core.JSONSchema.JSONSchema) : null
	})
	
	const formSchema = computed(() => {
		const formValue = toValue(form)?.form
		return formValue ? z.fromJSONSchema(formValue as z.core.JSONSchema.JSONSchema) : null
	})

	return {
		querySchema,
		bodySchema,
		formSchema,
	}
}
