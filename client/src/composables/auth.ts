// SPDX-FileCopyrightText: 2026 OpenAdmin
//
// SPDX-License-Identifier: AGPL-3.0-or-later

import { useForm } from "@tanstack/vue-form"
import { useMutation, useQueryClient } from "@tanstack/vue-query"
import { toast } from "vue-sonner"
import { errorSchema } from "@/schemas/error"
import { type Login, loginSchema } from "@/schemas/login"

export const useLoginForm = ({ onSuccess }: { onSuccess?: () => void } = {}) => {
	const { mutate } = useLogin({ onSuccess })

	return useForm({
		defaultValues: {
			username: "",
			password: "",
		} satisfies Login,
		validators: {
			onChange: loginSchema,
		},
		onSubmit: async ({ value }) => {
			mutate(value)
		},
	})
}

export const useLogout = () => {
	const queryClient = useQueryClient()

	return useMutation({
		mutationFn: async () => {
			const response = await fetch("auth/logout", {
				method: "POST",
			})

			if (!response.ok) {
				const data = await response.json()
				const error = errorSchema.parse(data)
				toast.error(error.message)
				throw error
			}
		},
		onSuccess: () => {
			queryClient.invalidateQueries({ queryKey: ["openadmin-spec"] })
		},
	})
}

const useLogin = ({ onSuccess }: { onSuccess?: () => void } = {}) => {
	const queryClient = useQueryClient()

	return useMutation({
		mutationFn: async (body: Login) => {
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
		onSuccess: () => {
			queryClient.invalidateQueries({ queryKey: ["openadmin-spec"] })
			onSuccess?.()
		},
	})
}
