<!--
SPDX-FileCopyrightText: 2026 OpenAdmin

SPDX-License-Identifier: AGPL-3.0-or-later
-->

<script setup lang="ts">
import AppSidebar from "@/components/dashboard/Sidebar.vue"

import { SidebarInset, SidebarProvider } from "@/components/ui/sidebar"
</script>

<template>
	<SidebarProvider>
		<AppSidebar />
		<SidebarInset>
			<main class="flex-1 overflow-auto p-4 md:p-6">
				<router-view />
			</main>
		</SidebarInset>
	</SidebarProvider>
</template>
