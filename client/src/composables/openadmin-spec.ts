import { useQuery } from "@tanstack/vue-query"
import type { Error } from "@/schemas/error"
import { errorSchema } from "@/schemas/error"
import type { Spec } from "@/schemas/spec"
import { specSchema } from "@/schemas/spec"

export const useOpenAdminSpec = () => {
	return useQuery<Spec, Error>({
		queryKey: ["openadmin-spec"],
		queryFn: async () => {
			const response = await fetch("openadmin.json")
			const data = await response.json()

			if (!response.ok) {
				const error = errorSchema.parse(data)
				throw error
			}

			return specSchema.parse(data)
		},
	})
}
