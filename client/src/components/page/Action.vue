<!--
SPDX-FileCopyrightText: 2026 OpenAdmin

SPDX-License-Identifier: AGPL-3.0-or-later
-->

<script setup lang="ts">
import { useColor } from "@/composables/colors"
import { Button } from "@/components/ui/button"
import { Icon } from "@iconify/vue"
import { useAction } from "@/composables/openadmin-action"

const props = defineProps<{
	sectionId: string
	pageId: string
	actionId: string
}>()
const { action } = useAction({
	sectionId: props.sectionId,
	pageId: props.pageId,
	actionId: props.actionId,
})
const { style } = useColor(() => action.value?.color || "slate")
</script>

<template>
	<Button v-if="action" size="sm" variant="outline">
		<Icon v-if="action.icon" :icon="`lucide:${action.icon}`" :class="style.text" />
		{{ action.name }}
	</Button>
</template>
