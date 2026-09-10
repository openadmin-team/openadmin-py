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
import { useReference } from "@/composables/openadmin-reference"
import type { ActionConfig } from "@/schemas/table"

const props = defineProps<{
	actions: ActionConfig[]
}>()

const open = ref(false)
const selected = ref<ActionConfig | null>(null)

function runAction(item: ActionConfig) {
	selected.value = item
	open.value = true
}

const initialValues = computed(() => ({
	...selected.value?.params,
}))

const { find, sectionId, pageId } = useReference({
	componentId: computed(() => selected.value?.reference ?? ""),
})

const items = computed(() =>
	props.actions.map((action) => {
		const referenced = find(action.reference)?.component
		const referencedAction = referenced?.type === "action" ? referenced : null

		const icon = action.icon ?? referencedAction?.icon ?? undefined
		const color = action.color ?? referencedAction?.color ?? "slate"
		const label = action.label ?? referencedAction?.name ?? action.reference

		return {
			...action,
			icon,
			color,
			label,
			textClass: useColor(() => color).style.value.text,
		}
	}),
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
			<DropdownMenuItem v-for="item in items" :key="item.reference" @click="runAction(item)">
				<Icon v-if="item.icon" :icon="`lucide:${item.icon}`" :class="item.textClass" />
				{{ item.label }}
			</DropdownMenuItem>
		</DropdownMenuContent>
	</DropdownMenu>
	<ActionDialog
		v-if="selected && sectionId && pageId"
		:key="selected.reference"
		:section-id="sectionId"
		:page-id="pageId"
		:action-id="selected.reference"
		:initial-values="initialValues"
		v-model:open="open"
	/>
</template>
