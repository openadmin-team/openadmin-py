<!--
SPDX-FileCopyrightText: 2026 OpenAdmin

SPDX-License-Identifier: AGPL-3.0-or-later
-->

<script setup lang="ts">
import { Icon } from "@iconify/vue"
import { MoreHorizontal } from "@lucide/vue"
import { computed, ref } from "vue"
import ActionDialog from "@/components/action/ActionDialog.vue"
import { Button } from "@/components/ui/button"
import {
	DropdownMenu,
	DropdownMenuContent,
	DropdownMenuItem,
	DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { useColor } from "@/composables/colors"
import type { ActionConfig } from "@/schemas/table"

const props = defineProps<{
	sectionId: string
	pageId: string
	actions: ActionConfig[]
}>()

const items = computed(() =>
	props.actions.map((action) => ({
		...action,
		textClass: useColor(() => action.color ?? "slate").style.value.text,
	})),
)

const open = ref(false)
const selected = ref<ActionConfig | null>(null)

function runAction(item: ActionConfig) {
	selected.value = item
	open.value = true
}

const initialValues = computed(() => ({
	...selected.value?.query,
	...selected.value?.body,
	...selected.value?.form,
}))
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
			<DropdownMenuItem v-for="item in items" :key="item.action" @click="runAction(item)">
				<Icon v-if="item.icon" :icon="`lucide:${item.icon}`" :class="item.textClass" />
				{{ item.label ?? item.action }}
			</DropdownMenuItem>
		</DropdownMenuContent>
	</DropdownMenu>
	<ActionDialog
		v-if="selected"
		:key="selected.action"
		:section-id="sectionId"
		:page-id="pageId"
		:action-id="selected.action"
		:initial-values="initialValues"
		v-model:open="open"
	/>
</template>
