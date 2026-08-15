<!--
SPDX-FileCopyrightText: 2026 OpenAdmin

SPDX-License-Identifier: AGPL-3.0-or-later
-->

<script setup lang="ts">
import { LayoutDashboardIcon } from "@lucide/vue"
import { RouterLink, useRoute } from "vue-router"
import {
	Sidebar,
	SidebarContent,
	SidebarGroup,
	SidebarGroupContent,
	SidebarGroupLabel,
	SidebarHeader,
	SidebarMenu,
	SidebarMenuButton,
	SidebarMenuItem,
	SidebarRail,
} from "@/components/ui/sidebar"
import { useOpenAdminSpec } from "@/composables/openadmin-spec"
import { Icon } from "@iconify/vue";

const { data: spec } = useOpenAdminSpec()
const route = useRoute()
</script>

<template>
	<Sidebar collapsible="icon">
		<SidebarHeader>
			<div class="flex items-center gap-2 px-2 py-1.5">
				<div
					class="bg-primary text-primary-foreground flex size-8 shrink-0 items-center justify-center rounded-md"
				>
					<LayoutDashboardIcon class="size-4" />
				</div>
				<div class="flex flex-col overflow-hidden group-data-[collapsible=icon]:hidden">
					<span class="truncate text-sm font-semibold">{{ spec?.name ?? "Admin" }}</span>
					<span v-if="spec?.description" class="text-muted-foreground truncate text-xs">
						{{ spec.description }}
					</span>
				</div>
			</div>
		</SidebarHeader>
		<SidebarContent>
			<SidebarGroup v-for="section in spec?.sections ?? []" :key="section.id">
				<SidebarGroupLabel>{{ section.name }}</SidebarGroupLabel>
				<SidebarGroupContent>
					<SidebarMenu>
						<SidebarMenuItem v-for="page in section.pages" :key="page.id">
							<SidebarMenuButton
								as-child
								:is-active="route.params.sectionId === section.id && route.params.pageId === page.id"
								:tooltip="page.name"
							>
								<RouterLink
									:to="{ name: 'page', params: { sectionId: section.id, pageId: page.id } }"
								>
									<Icon v-if="page.icon" :icon='`lucide:${page.icon}`'/>
									<span>{{ page.name }}</span>
								</RouterLink>
							</SidebarMenuButton>
						</SidebarMenuItem>
					</SidebarMenu>
				</SidebarGroupContent>
			</SidebarGroup>
		</SidebarContent>
		<SidebarRail />
	</Sidebar>
</template>
