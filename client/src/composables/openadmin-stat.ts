// SPDX-FileCopyrightText: 2026 OpenAdmin
//
// SPDX-License-Identifier: AGPL-3.0-or-later

import { computed, toValue, type MaybeRefOrGetter } from "vue"
import { usePageSpec } from "./openadmin-page"
import { statSchema, type Stat, type StatComponent } from "@/schemas/stat"
import { useQuery } from "@tanstack/vue-query"
import { errorSchema } from "@/schemas/error"
import type { AppError } from "@/types/errors"

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
		page.value?.components.find(
			(c): c is StatComponent => c.type === "stat" && c.id === toValue(statId),
		),
	)
	const { data, isLoading, isFetching } = useQuery<Stat, AppError>({
		queryKey: computed(() => [
			"openadmin-stat",
			toValue(sectionId),
			toValue(pageId),
			toValue(statId),
		]),
		queryFn: async () => {
			const response = await fetch(
				`${toValue(sectionId)}/${toValue(pageId)}/stat/${toValue(statId)}`,
			)
			const data = await response.json()

			if (!response.ok) {
				const error = errorSchema.parse(data)
				throw { ...error, status: response.status } satisfies AppError
			}

			return statSchema.parse(data)
		},
	})
	const value = computed(() => {
		if (data.value === null || data.value === undefined) return null
		if (typeof data.value === "object") return data.value.value
		return data.value
	})

	return {
		stat,
		data,
		value,
		isLoading,
		isFetching,
	}
}
