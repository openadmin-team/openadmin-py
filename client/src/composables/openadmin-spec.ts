import { useQuery } from "@tanstack/vue-query"
import type { Error as ApiError } from "@/schemas/error"
import { errorSchema } from "@/schemas/error"
import type { Spec } from "@/schemas/spec"
import { specSchema } from "@/schemas/spec"

export const useOpenAdminSpec = () => {
	return useQuery<Spec, ApiError>({
		queryKey: ["openadmin-spec"],
		queryFn: async () => {
			const response = await fetch("openadmin.json")
			const data = await response.json()

			if (!response.ok) {
				throw errorSchema.parse(data)
			}

			return specSchema.parse(data)
		},
	})
}
