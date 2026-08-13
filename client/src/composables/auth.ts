// SPDX-FileCopyrightText: 2026 OpenAdmin
//
// SPDX-License-Identifier: AGPL-3.0-or-later

import { useMutation, useQueryClient } from "@tanstack/vue-query"
import { openAdminSpecQueryOptions } from "@/composables/openadmin-spec"
import { ApiError, errorSchema } from "@/schemas/error"
import type { LoginReq } from "@/schemas/login"

export const useLogin = () => {
	const queryClient = useQueryClient()

	return useMutation<void, ApiError, LoginReq>({
		mutationFn: async (body) => {
			const response = await fetch("auth/login", {
				method: "POST",
				headers: { "Content-Type": "application/json" },
				body: JSON.stringify(body),
			})

			if (!response.ok) {
				const data = await response.json()
				throw new ApiError(response.status, errorSchema.parse(data).message)
			}
		},
		onSuccess: () =>
			queryClient.invalidateQueries({ queryKey: openAdminSpecQueryOptions.queryKey }),
	})
}
