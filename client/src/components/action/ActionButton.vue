<!--
SPDX-FileCopyrightText: 2026 OpenAdmin

SPDX-License-Identifier: AGPL-3.0-or-later
-->

<script setup lang="ts">
import { Icon } from "@iconify/vue"
import { ref } from "vue"
import { Button } from "@/components/ui/button"
import { useColor } from "@/composables/colors"
import { useAction } from "@/composables/openadmin-action"
import ActionDialog from "./ActionDialog.vue"

const props = defineProps<{
	sectionId: string
	pageId: string
	actionId: string
}>()

const open = ref(false)

const { action } = useAction({
	sectionId: props.sectionId,
	pageId: props.pageId,
	actionId: props.actionId,
})
const { style } = useColor(() => action.value?.color || "slate")
</script>

<template>
	<template v-if="action">
		<Button size="sm" variant="outline" @click="open = true">
			<Icon v-if="action.icon" :icon="`lucide:${action.icon}`" :class="style.text" />
			{{ action.name }}
		</Button>
		<ActionDialog
			:section-id="sectionId"
			:page-id="pageId"
			:action-id="actionId"
			v-model:open="open"
		/>
	</template>
</template>
