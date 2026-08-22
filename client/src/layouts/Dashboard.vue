<!--
SPDX-FileCopyrightText: 2026 OpenAdmin

SPDX-License-Identifier: AGPL-3.0-or-later
-->

<script setup lang="ts">
import { useRoute } from "vue-router"
import AppSidebar from "@/components/dashboard/Sidebar.vue"
import TopPanel from "@/components/dashboard/TopPanel.vue"
import { SidebarInset, SidebarProvider } from "@/components/ui/sidebar"

const route = useRoute()
</script>

<template>
	<SidebarProvider>
		<AppSidebar />
		<SidebarInset>
			<TopPanel />
			<main class="flex-1 overflow-auto p-4 md:p-6">
				<router-view :key="route.fullPath" />
			</main>
		</SidebarInset>
	</SidebarProvider>
</template>
