// SPDX-FileCopyrightText: 2026 OpenAdmin
//
// SPDX-License-Identifier: AGPL-3.0-or-later

import { errorSchema } from "@/schemas/error"
import { useMutation, useQueryClient } from "@tanstack/vue-query"
import { toast } from "vue-sonner"

export const useLogin = () => {
	const queryClient = useQueryClient()

	return useMutation({
		mutationFn: async (body) => {
			const response = await fetch("auth/login", {
				method: "POST",
				headers: { "Content-Type": "application/json" },
				body: JSON.stringify(body),
			})

			if (!response.ok) {
				const data = await response.json()
				const error = errorSchema.parse(data)
				toast.error(error.message)
				throw error
			}
		},
		onSuccess: () => queryClient.invalidateQueries({ queryKey: ["openadmin-spec"] }),
	})
}
