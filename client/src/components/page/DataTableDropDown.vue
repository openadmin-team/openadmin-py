<!--
SPDX-FileCopyrightText: 2026 OpenAdmin

SPDX-License-Identifier: AGPL-3.0-or-later
-->

<script setup lang="ts">
import { computed } from "vue"
import { MoreHorizontal } from "@lucide/vue"
import { Icon } from "@iconify/vue"
import { Button } from "@/components/ui/button"
import {
	DropdownMenu,
	DropdownMenuContent,
	DropdownMenuItem,
	DropdownMenuLabel,
	DropdownMenuSeparator,
	DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { useColor } from "@/composables/colors"
import type { ActionConfig } from "@/schemas/table"

const props = defineProps<{
	actions: ActionConfig[]
}>()

const items = computed(() =>
	props.actions.map((action) => ({
		...action,
		textClass: useColor(() => action.color ?? "slate").style.value.text,
	})),
)
</script>

<template>
	<DropdownMenu v-if="items.length">
		<DropdownMenuTrigger as-child>
			<Button variant="ghost" class="w-8 h-8 p-0">
				<span class="sr-only">Open menu</span>
				<MoreHorizontal class="w-4 h-4" />
			</Button>
		</DropdownMenuTrigger>
		<DropdownMenuContent align="end">
			<DropdownMenuItem v-for="item in items" :key="item.action">
				<Icon v-if="item.icon" :icon="`lucide:${item.icon}`" :class="item.textClass" />
				{{ item.label ?? item.action }}
			</DropdownMenuItem>
		</DropdownMenuContent>
	</DropdownMenu>
</template>
