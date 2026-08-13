// SPDX-FileCopyrightText: 2026 OpenAdmin
//
// SPDX-License-Identifier: AGPL-3.0-or-later

import { useQuery } from "@tanstack/vue-query"
import { computed } from "vue"
import type { Error as ApiError } from "@/schemas/error"
import { errorSchema } from "@/schemas/error"
import type { Spec } from "@/schemas/spec"
import { specSchema } from "@/schemas/spec"

export const useOpenAdminSpec = () => {
	return useQuery<Spec, ApiError>({
		queryKey: ["openadmin-spec"],
		queryFn: async () => {
			const response = await fetch("api/openadmin.json")
			const data = await response.json()

			if (!response.ok) {
				throw errorSchema.parse(data)
			}

			return specSchema.parse(data)
		},
	})
}

export const useOpenAdminPageSpec = ({ id }: { id: string }) => {
	const { data: specData, ...rest } = useOpenAdminSpec()

	const data = computed(() => {
		if (!specData.value) return null
		return (
			specData.value.sections.flatMap((section) => section.pages).find((page) => page.id === id) ??
			null
		)
	})

	return {
		data,
		...rest,
	}
}
