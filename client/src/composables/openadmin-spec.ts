// SPDX-FileCopyrightText: 2026 OpenAdmin
//
// SPDX-License-Identifier: AGPL-3.0-or-later

import { queryOptions, useQuery } from "@tanstack/vue-query"
import { errorSchema } from "@/schemas/error"
import type { Spec } from "@/schemas/spec"
import { specSchema } from "@/schemas/spec"
import type { AppError } from "@/types/errors"

export const useSpecOptions = queryOptions<Spec, AppError>({
	queryKey: ["openadmin-spec"],
	queryFn: async () => {
		const response = await fetch("api/openadmin.json")
		const data = await response.json()

		if (!response.ok) {
			const error = errorSchema.parse(data)
			throw { ...error, status: response.status } satisfies AppError
		}

		return specSchema.parse(data)
	},
})

export const useSpec = () => {
	return useQuery<Spec, AppError>(useSpecOptions)
}
