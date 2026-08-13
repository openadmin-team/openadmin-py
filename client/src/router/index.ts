// SPDX-FileCopyrightText: 2026 OpenAdmin
//
// SPDX-License-Identifier: AGPL-3.0-or-later

import { createRouter, createWebHashHistory } from "vue-router"
import { useOpenAdminSpecOptions } from "@/composables/openadmin-spec"
import { useQueryClient } from "@tanstack/vue-query"

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

	const queryClient = useQueryClient()

	try {
		await queryClient.ensureQueryData(useOpenAdminSpecOptions)
		return true
	} catch (error) {
		if (error instanceof ApiError && error.status === 401) {
			return { name: "login", query: { redirect: to.fullPath } }
		}
		throw error
	}
})
