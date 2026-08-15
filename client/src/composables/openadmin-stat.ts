// SPDX-FileCopyrightText: 2026 OpenAdmin
//
// SPDX-License-Identifier: AGPL-3.0-or-later

import { computed, toValue, type MaybeRefOrGetter } from "vue"
import { usePageSpec } from "./openadmin-page"
import type { StatComponent } from "@/schemas/stat"
import { useQuery } from "@tanstack/vue-query"
import { errorSchema } from "@/schemas/error"
import type { AppError } from "@/types/errors"
import { specSchema } from "@/schemas/spec"

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
	const { data } = useQuery({
		queryKey: [`data-${toValue(sectionId)}-${toValue(pageId)}-${toValue(statId)}`],
		queryFn: async () => {
			if (!stat.value) return null
			const response = await fetch(`${sectionId}/${pageId}/stat/${statId}`)
			const data = await response.json()

			if (!response.ok) {
				const error = errorSchema.parse(data)
				throw { ...error, status: response.status } satisfies AppError
			}

			return specSchema.parse(data)
		}
	})

	return {
		stat,
		data,
	}
}
