<!--
SPDX-FileCopyrightText: 2026 OpenAdmin

SPDX-License-Identifier: AGPL-3.0-or-later
-->

<script setup lang="ts">
import { CheckIcon, ChevronsUpDownIcon } from "@lucide/vue"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import {
	DropdownMenu,
	DropdownMenuContent,
	DropdownMenuGroup,
	DropdownMenuItem,
	DropdownMenuLabel,
	DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import {
	SidebarMenu,
	SidebarMenuButton,
	SidebarMenuItem,
	useSidebar,
} from "@/components/ui/sidebar"
import { Spinner } from "@/components/ui/spinner"
import { useCurrentWorkspace, useSelectWorkspace, useWorkspaces } from "@/composables/workspaces"
import type { Workspace } from "@/schemas/workspace"

const { isMobile } = useSidebar()
const { data: workspaces } = useWorkspaces()
const { data: current } = useCurrentWorkspace()
const { mutate: selectWorkspace, isPending } = useSelectWorkspace()

function initials(name: string) {
	return name.trim().slice(0, 2).toUpperCase()
}

function handleSelect(workspace: Workspace) {
	if (workspace.id === current.value?.id) return
	selectWorkspace(workspace.id)
}
</script>

<template>
	<SidebarMenu v-if="current && workspaces?.length">
		<SidebarMenuItem>
			<DropdownMenu>
				<DropdownMenuTrigger as-child>
					<SidebarMenuButton
						size="lg"
						tooltip="Switch workspace"
						class="data-[state=open]:bg-sidebar-accent data-[state=open]:text-sidebar-accent-foreground"
					>
						<Avatar class="size-8 rounded-lg">
							<AvatarImage v-if="current.avatar" :src="current.avatar" :alt="current.name" />
							<AvatarFallback class="rounded-lg">{{ initials(current.name) }}</AvatarFallback>
						</Avatar>
						<div class="grid flex-1 text-left text-sm leading-tight">
							<span class="truncate font-medium">{{ current.name }}</span>
							<span v-if="current.description" class="text-muted-foreground truncate text-xs">
								{{ current.description }}
							</span>
						</div>
						<Spinner v-if="isPending" class="ml-auto" />
						<ChevronsUpDownIcon v-else class="ml-auto" />
					</SidebarMenuButton>
				</DropdownMenuTrigger>
				<DropdownMenuContent
					class="w-(--reka-dropdown-menu-trigger-width) min-w-56 rounded-lg"
					align="start"
					:side="isMobile ? 'bottom' : 'right'"
					:side-offset="4"
				>
					<DropdownMenuLabel class="text-muted-foreground text-xs">Workspaces</DropdownMenuLabel>
					<DropdownMenuGroup>
						<DropdownMenuItem
							v-for="workspace in workspaces"
							:key="workspace.id"
							class="gap-2 p-2"
							@select="handleSelect(workspace)"
						>
							<Avatar class="size-6 rounded-md">
								<AvatarImage
									v-if="workspace.avatar"
									:src="workspace.avatar"
									:alt="workspace.name"
								/>
								<AvatarFallback class="rounded-md text-xs">
									{{ initials(workspace.name) }}
								</AvatarFallback>
							</Avatar>
							<div class="grid flex-1 leading-tight">
								<span class="truncate">{{ workspace.name }}</span>
								<span v-if="workspace.description" class="text-muted-foreground truncate text-xs">
									{{ workspace.description }}
								</span>
							</div>
							<CheckIcon v-if="workspace.id === current.id" class="ml-auto" />
						</DropdownMenuItem>
					</DropdownMenuGroup>
				</DropdownMenuContent>
			</DropdownMenu>
		</SidebarMenuItem>
	</SidebarMenu>
</template>
