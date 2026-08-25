// SPDX-FileCopyrightText: 2026 OpenAdmin
//
// SPDX-License-Identifier: AGPL-3.0-or-later

import { useQuery } from "@tanstack/vue-query"
import { computed, type MaybeRefOrGetter, toValue } from "vue"
import { errorSchema } from "@/schemas/error"
import { type Markdown, type MarkdownComponent, markdownSchema } from "@/schemas/markdown"
import type { AppError } from "@/types/errors"
import { usePageSpec } from "./openadmin-page"

export const useMarkdown = ({
	sectionId,
	pageId,
	markdownId,
}: {
	sectionId: MaybeRefOrGetter<string>
	pageId: MaybeRefOrGetter<string>
	markdownId: MaybeRefOrGetter<string>
}) => {
	const { page } = usePageSpec({ sectionId, pageId })

	const markdown = computed(() =>
		page.value?.components.find(
			(c): c is MarkdownComponent => c.type === "markdown" && c.id === toValue(markdownId),
		),
	)

	const { data, isLoading, isFetching } = useQuery<Markdown, AppError>({
		queryKey: computed(() => [
			"openadmin-data",
			"markdown",
			toValue(sectionId),
			toValue(pageId),
			toValue(markdownId),
		]),
		queryFn: async () => {
			const response = await fetch(
				`${toValue(sectionId)}/${toValue(pageId)}/markdown/${toValue(markdownId)}`,
			)
			const data = await response.json()

			if (!response.ok) {
				const error = errorSchema.parse(data)
				throw { ...error, status: response.status } satisfies AppError
			}

			return markdownSchema.parse(data)
		},
		refetchInterval: computed(() => markdown.value?.refresh ?? false),
	})

	const content = computed(() => {
		if (data.value === null || data.value === undefined) return null
		if (typeof data.value === "object") return data.value.content
		return data.value
	})

	const icon = computed(() => {
		if (typeof data.value === "object" && data.value?.icon) return data.value.icon
		return markdown.value?.icon ?? null
	})

	const color = computed(() => {
		if (typeof data.value === "object" && data.value?.color) return data.value.color
		return markdown.value?.color ?? null
	})

	return {
		markdown,
		data,
		content,
		isLoading,
		isFetching,
		color,
		icon,
	}
}
