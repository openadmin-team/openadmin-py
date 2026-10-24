// SPDX-FileCopyrightText: 2026 OpenAdmin
//
// SPDX-License-Identifier: AGPL-3.0-or-later

import { queryOptions, useMutation, useQuery, useQueryClient } from "@tanstack/vue-query"
import { toast } from "vue-sonner"
import { errorSchema } from "@/schemas/error"
import { type Workspace, workspaceSchema, workspacesSchema } from "@/schemas/workspace"
import type { AppError } from "@/types/errors"

// Workspaces are optional on the server, so a failed request means "no workspaces"
// rather than something worth retrying.
export const useWorkspacesOptions = queryOptions<Workspace[], AppError>({
	queryKey: ["workspaces"],
	retry: false,
	queryFn: async () => {
		const response = await fetch("workspaces")
		const data = await response.json()

		if (!response.ok) {
			const error = errorSchema.parse(data)
			throw { ...error, status: response.status } satisfies AppError
		}

		return workspacesSchema.parse(data)
	},
})

export const useCurrentWorkspaceOptions = queryOptions<Workspace, AppError>({
	queryKey: ["workspaces", "current"],
	retry: false,
	queryFn: async () => {
		const response = await fetch("workspaces/current")
		const data = await response.json()

		if (!response.ok) {
			const error = errorSchema.parse(data)
			throw { ...error, status: response.status } satisfies AppError
		}

		return workspaceSchema.parse(data)
	},
})

export const useWorkspaces = () => {
	return useQuery<Workspace[], AppError>(useWorkspacesOptions)
}

export const useCurrentWorkspace = () => {
	return useQuery<Workspace, AppError>(useCurrentWorkspaceOptions)
}

export const useSelectWorkspace = () => {
	const queryClient = useQueryClient()

	return useMutation({
		mutationFn: async (id: string) => {
			const response = await fetch(`workspaces?id=${encodeURIComponent(id)}`, {
				method: "POST",
			})

			if (!response.ok) {
				const data = await response.json()
				const error = errorSchema.parse(data)
				toast.error(error.message)
				throw error
			}
		},
		// everything the panel shows may be scoped to the workspace, so refetch it all
		onSuccess: () => queryClient.invalidateQueries(),
	})
}
