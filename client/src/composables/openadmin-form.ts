// SPDX-FileCopyrightText: 2026 OpenAdmin
//
// SPDX-License-Identifier: AGPL-3.0-or-later

import { computed, toValue, type MaybeRefOrGetter } from "vue"
import { usePageSpec } from "./openadmin-page"
import { type FormComponent, formSchema as formResultSchema } from "@/schemas/form"
import z from "zod"
import { useMutation, useQueryClient } from "@tanstack/vue-query"
import { errorSchema } from "@/schemas/error"
import { toast } from "vue-sonner"
import { useForm as useTanstackForm } from "@tanstack/vue-form"

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

	const { mutate } = useFormMutation({ sectionId, pageId, formId, form })

	const queryKeys = computed(() => new Set(Object.keys(toValue(form)?.query?.properties ?? {})))
	const bodyKeys = computed(() => new Set(Object.keys(toValue(form)?.body?.properties ?? {})))
	const formKeys = computed(() => new Set(Object.keys(toValue(form)?.form?.properties ?? {})))

	const dataForm = useTanstackForm({
		defaultValues: {} as Record<string, unknown>,
		validators: {
			onChange: ({ value }) => {
				const fields: Record<string, string[]> = {}
				for (const [schema, keys] of [
					[querySchema.value, queryKeys.value],
					[bodySchema.value, bodyKeys.value],
					[formSchema.value, formKeys.value],
				] as const) {
					if (!schema || keys.size === 0) continue
					const slice = Object.fromEntries(Object.entries(value).filter(([key]) => keys.has(key)))
					const result = schema.safeParse(slice)
					if (result.success) continue
					for (const issue of result.error.issues) {
						const key = String(issue.path[0])
						fields[key] = [...(fields[key] ?? []), issue.message]
					}
				}
				return Object.keys(fields).length ? { fields } : undefined
			},
		},
		onSubmit: async ({ value }) => {
			const query = new URLSearchParams()
			for (const key of queryKeys.value) {
				const val = value[key]
				if (val !== undefined && val !== null) query.set(key, String(val))
			}

			const body = bodyKeys.value.size
				? Object.fromEntries(Object.entries(value).filter(([key]) => bodyKeys.value.has(key)))
				: null

			let formData: FormData | null = null
			if (formKeys.value.size) {
				formData = new FormData()
				for (const key of formKeys.value) {
					const val = value[key]
					if (val instanceof Blob) formData.append(key, val)
					else if (val !== undefined && val !== null) formData.append(key, String(val))
				}
			}

			mutate({ query: queryKeys.value.size ? query : null, body, formData })
		},
	})

	return {
		form,
		querySchema,
		formSchema,
		bodySchema,
		dataForm,
	}
}

const useFormSchema = ({ form }: { form: MaybeRefOrGetter<FormComponent | undefined> }) => {
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

const useFormMutation = ({
	sectionId,
	pageId,
	formId,
	form,
}: {
	sectionId: MaybeRefOrGetter<string>
	pageId: MaybeRefOrGetter<string>
	formId: MaybeRefOrGetter<string>
	form: MaybeRefOrGetter<FormComponent | undefined>
}) => {
	const queryClient = useQueryClient()

	return useMutation({
		mutationFn: async ({
			query,
			formData,
			body,
		}: {
			query?: URLSearchParams | null
			formData?: FormData | null
			body?: Record<string, unknown> | null
		}) => {
			const method = (toValue(form)?.method ?? "post").toUpperCase()
			const queryParams = query?.toString()
			const url = `${toValue(sectionId)}/${toValue(pageId)}/form/${toValue(formId)}${queryParams ? `?${queryParams}` : ""}`

			const response = await fetch(
				url,
				formData
					? { method, body: formData }
					: { method, headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) },
			)

			const data = await response.json()

			if (!response.ok) {
				const error = errorSchema.parse(data)
				toast.error(error.message)
				throw error
			}

			const result = formResultSchema.parse(data)
			const message = typeof result === "string" ? result : result?.toast
			if (message) toast.success(message)

			return result
		},
		onSuccess: () => {
			queryClient.invalidateQueries({ queryKey: ["openadmin-data"] })
		},
	})
}
