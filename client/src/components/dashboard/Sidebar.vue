<!--
SPDX-FileCopyrightText: 2026 OpenAdmin

SPDX-License-Identifier: AGPL-3.0-or-later
-->

<script setup lang="ts">
import { RouterLink, useRoute, useRouter } from "vue-router"
import {
	Sidebar,
	SidebarContent,
	SidebarFooter,
	SidebarGroup,
	SidebarGroupContent,
	SidebarGroupLabel,
	SidebarHeader,
	SidebarMenu,
	SidebarMenuButton,
	SidebarMenuItem,
	SidebarRail,
} from "@/components/ui/sidebar"
import { useLogout } from "@/composables/auth"
import { useSpec } from "@/composables/openadmin-spec"
import { useColor } from "@/composables/colors"
import type { Color } from "@/schemas/color"
import { Icon } from "@iconify/vue"
import logo from "@/assets/images/logo.png"

const { data: spec } = useSpec()
const route = useRoute()
const router = useRouter()
const { mutate: logout } = useLogout()

function handleLogout() {
	logout(undefined, {
		onSuccess: () => router.push({ name: "login" }),
	})
}

function pageColorStyle(color: Color | null) {
	if (!color) return null
	return useColor(color).style.value
}
</script>

<template>
	<Sidebar collapsible="icon">
		<SidebarHeader>
			<div class="flex items-center gap-2 px-2 py-1.5 group-data-[collapsible=icon]:p-0!">
				<img :src="logo" alt="Logo" class="shrink-0 rounded-md object-contain size-7">
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
									<Icon
										v-if="page.icon"
										:icon="`lucide:${page.icon}`"
										:class="pageColorStyle(page.color)?.text"
									/>
									<span
										v-else-if="page.color"
										:class="[pageColorStyle(page.color)?.dot, 'size-1.5 rounded-full shrink-0']"
									/>
									<span>{{ page.name }}</span>
								</RouterLink>
							</SidebarMenuButton>
						</SidebarMenuItem>
					</SidebarMenu>
				</SidebarGroupContent>
			</SidebarGroup>
		</SidebarContent>
		<SidebarFooter>
			<SidebarMenu>
				<SidebarMenuItem>
					<SidebarMenuButton tooltip="Logout" @click="handleLogout">
						<Icon icon="lucide:log-out" />
						<span>Logout</span>
					</SidebarMenuButton>
				</SidebarMenuItem>
			</SidebarMenu>
		</SidebarFooter>
		<SidebarRail />
	</Sidebar>
</template>
