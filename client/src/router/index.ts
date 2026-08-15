// SPDX-FileCopyrightText: 2026 OpenAdmin
//
// SPDX-License-Identifier: AGPL-3.0-or-later

import { createRouter, createWebHashHistory } from "vue-router"
import { useOpenAdminSpecOptions } from "@/composables/openadmin-spec"
import { useQueryClient } from "@tanstack/vue-query"
import { statusCodes } from "@/lib/status-codes"

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
			component: () => import("@/layouts/Dashboard.vue"),
			children: [
				{
					path: "",
					name: "home",
					component: () => import("@/views/HomeView.vue"),
				},
				{
					path: ":sectionId/:pageId",
					name: "page",
					component: () => import("@/views/PageView.vue"),
				},
			],
		},
	],
})

router.beforeEach(async (to) => {
	if (to.meta.public) return true

	const queryClient = useQueryClient()

	try {
		await queryClient.ensureQueryData(useOpenAdminSpecOptions)
		return true
	} catch (error: any) {
		if (error.status === statusCodes.UNAUTHORIZED) {
			return { name: "login", query: { redirect: to.fullPath } }
		}
		throw error
	}
})
