// SPDX-FileCopyrightText: 2026 OpenAdmin
//
// SPDX-License-Identifier: AGPL-3.0-or-later

import { createRouter, createWebHashHistory } from "vue-router"
import { openAdminSpecQueryOptions } from "@/composables/openadmin-spec"
import { queryClient } from "@/lib/query-client"
import { ApiError } from "@/schemas/error"

export const router = createRouter({
	history: createWebHashHistory(),
	routes: [
		{
			path: "/login",
			name: "login",
			component: () => import("@/views/LoginView.vue"),
			meta: { public: true },
		},
		{
			path: "/",
			name: "home",
			component: () => import("@/views/HomeView.vue"),
		},
	],
})

router.beforeEach(async (to) => {
	if (to.meta.public) return true

	try {
		await queryClient.ensureQueryData(openAdminSpecQueryOptions)
		return true
	} catch (error) {
		if (error instanceof ApiError && error.status === 401) {
			return { name: "login", query: { redirect: to.fullPath } }
		}
		throw error
	}
})
