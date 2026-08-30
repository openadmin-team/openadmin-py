// SPDX-FileCopyrightText: 2026 OpenAdmin
//
// SPDX-License-Identifier: AGPL-3.0-or-later

import { useForm as useTanstackForm } from "@tanstack/vue-form"
import { useMutation, useQueryClient } from "@tanstack/vue-query"
import { computed, toValue, type MaybeRefOrGetter } from "vue"
import { toast } from "vue-sonner"
import z from "zod"
import { actionSchema as actionResultSchema, type ActionComponent } from "@/schemas/action"
import { errorSchema } from "@/schemas/error"
import { usePageSpec } from "./openadmin-page"

function toValidatable(value: unknown): unknown {
	if (value instanceof File) return value.name
	if (Array.isArray(value)) return value.map(toValidatable)
	return value
}

function propertyType(action: ActionComponent | undefined, key: string): string | undefined {
	const property =
		action?.query?.properties?.[key] ??
		action?.body?.properties?.[key] ??
		action?.form?.properties?.[key]
	const type = property?.type
	return Array.isArray(type) ? type.find((t) => t !== "null") : type
}

// Row actions prefill from raw backend values (e.g. a numeric id), which may not
// match the type the target field's schema declares (e.g. `id: str`) — coerce so
// client-side validation sees the same type a user filling the field in would.
function coerceInitialValue(type: string | undefined, value: unknown): unknown {
	if (value === null || value === undefined) return value
	if (type === "string") return typeof value === "string" ? value : String(value)
	if ((type === "number" || type === "integer") && typeof value !== "number") {
		const parsed = Number(value)
		return Number.isNaN(parsed) ? value : parsed
	}
	if (type === "boolean" && typeof value !== "boolean") return value === "true" || value === true
	return value
}

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

export const useActionForm = ({
	sectionId,
	pageId,
	actionId,
	initialValues,
	onSuccess,
}: {
	sectionId: MaybeRefOrGetter<string>
	pageId: MaybeRefOrGetter<string>
	actionId: MaybeRefOrGetter<string>
	initialValues?: Record<string, unknown>
	onSuccess?: () => void
}) => {
	const { action } = useAction({ sectionId, pageId, actionId })
	const { querySchema, formSchema, bodySchema } = useActionSchema({ action })

	const { mutate, isPending } = useActionMutation({
		sectionId,
		pageId,
		actionId,
		action,
		onSuccess,
	})

	const queryKeys = computed(() => new Set(Object.keys(toValue(action)?.query?.properties ?? {})))
	const bodyKeys = computed(() => new Set(Object.keys(toValue(action)?.body?.properties ?? {})))
	const formKeys = computed(() => new Set(Object.keys(toValue(action)?.form?.properties ?? {})))

	const defaultValues = Object.fromEntries(
		Object.entries(initialValues ?? {}).map(([key, value]) => [
			key,
			coerceInitialValue(propertyType(toValue(action), key), value),
		]),
	)

	const dataForm = useTanstackForm({
		defaultValues: defaultValues as Record<string, unknown>,
		validators: {
			onChange: ({ value }) => {
				const fields: Record<string, string[]> = {}
				for (const [schema, keys] of [
					[querySchema.value, queryKeys.value],
					[bodySchema.value, bodyKeys.value],
					[formSchema.value, formKeys.value],
				] as const) {
					if (!schema || keys.size === 0) continue
					const slice = Object.fromEntries(
						Object.entries(value)
							.filter(([key]) => keys.has(key))
							.map(([key, val]) => [key, toValidatable(val)]),
					)
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

			let formData: FormData | null = null
			if (formKeys.value.size) {
				formData = new FormData()
				const append = (key: string, val: unknown) => {
					if (Array.isArray(val)) for (const item of val) append(key, item)
					else if (val instanceof Blob) formData?.append(key, val)
					else if (val !== undefined && val !== null) formData?.append(key, String(val))
				}
				// A request body can't be both multipart and JSON, so once there's a
				// file to upload, body fields ride along as regular multipart parts.
				for (const key of formKeys.value) append(key, value[key])
				for (const key of bodyKeys.value) append(key, value[key])
			}

			const body =
				!formData && bodyKeys.value.size
					? Object.fromEntries(Object.entries(value).filter(([key]) => bodyKeys.value.has(key)))
					: null

			mutate({ query: queryKeys.value.size ? query : null, body, formData })
		},
	})

	return {
		action,
		querySchema,
		bodySchema,
		formSchema,
		dataForm,
		isPending,
	}
}

const useActionSchema = ({ action }: { action: MaybeRefOrGetter<ActionComponent | undefined> }) => {
	const querySchema = computed(() => {
		const query = toValue(action)?.query
		return query ? z.fromJSONSchema(query as z.core.JSONSchema.JSONSchema) : null
	})

	const bodySchema = computed(() => {
		const body = toValue(action)?.body
		return body ? z.fromJSONSchema(body as z.core.JSONSchema.JSONSchema) : null
	})

	const formSchema = computed(() => {
		const formValue = toValue(action)?.form
		return formValue ? z.fromJSONSchema(formValue as z.core.JSONSchema.JSONSchema) : null
	})

	return {
		querySchema,
		bodySchema,
		formSchema,
	}
}

const useActionMutation = ({
	sectionId,
	pageId,
	actionId,
	action,
	onSuccess,
}: {
	sectionId: MaybeRefOrGetter<string>
	pageId: MaybeRefOrGetter<string>
	actionId: MaybeRefOrGetter<string>
	action: MaybeRefOrGetter<ActionComponent | undefined>
	onSuccess?: () => void
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
			const method = (toValue(action)?.method ?? "post").toUpperCase()
			const queryParams = query?.toString()
			const url = `${toValue(sectionId)}/${toValue(pageId)}/action/${toValue(actionId)}${queryParams ? `?${queryParams}` : ""}`

			// Fetch throws synchronously if a GET/HEAD request carries a body, so
			// those methods are sent bare — their params already rode along above
			// as query string, since only query params can reach a GET/HEAD action.
			const hasBody = method !== "GET" && method !== "HEAD"
			const response = await fetch(
				url,
				formData
					? { method, body: formData }
					: {
							method,
							headers: hasBody ? { "Content-Type": "application/json" } : undefined,
							body: hasBody ? JSON.stringify(body) : undefined,
						},
			)

			const data = await response.json()

			if (!response.ok) {
				const error = errorSchema.parse(data)
				toast.error(error.message)
				throw error
			}

			const result = actionResultSchema.parse(data)
			const message = typeof result === "string" ? result : (result?.toast ?? result?.message)
			if (message) toast.success(message)

			return result
		},
		onSuccess: () => {
			queryClient.invalidateQueries({ queryKey: ["openadmin-data"] })
			onSuccess?.()
		},
	})
}
