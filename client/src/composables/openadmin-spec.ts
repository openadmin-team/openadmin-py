import { useQuery } from "@tanstack/vue-query"
import { errorSchema } from "@/schemas/error"
import { specSchema } from "@/schemas/spec"
import { toast } from "vue-sonner"

export const useOpenAdminSpec = () => {
	return useQuery({
		queryKey: ["openadmin-spec"],
		queryFn: async () => {
			return fetch("openadmin.json")
				.catch((e) => errorSchema.parse(e))
				.then((res) => specSchema.parse(res))
				.catch((e) => toast.error(e))
		},
	})
}
