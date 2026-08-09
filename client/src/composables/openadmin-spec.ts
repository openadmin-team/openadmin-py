import { useQuery } from "@tanstack/vue-query"

export const useOpenAdminSpec = () => {
	return useQuery({
		queryKey: ["openadmin-spec"],
		queryFn: async () => {
			return fetch("openadmin.json")
		},
	})
}
