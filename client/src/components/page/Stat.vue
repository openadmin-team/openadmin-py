<!--
SPDX-FileCopyrightText: 2026 OpenAdmin

SPDX-License-Identifier: AGPL-3.0-or-later
-->

<script setup lang="ts">
import { useIconColor } from "@/composables/colors"
import { Card, CardAction, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Icon } from "@iconify/vue"
import { useStat } from "@/composables/openadmin-stat"

const props = defineProps<{
	sectionId: string
	pageId: string
	statId: string
}>()
const { stat } = useStat({
	sectionId: props.sectionId,
	pageId: props.pageId,
	statId: props.statId,
})
const { style } = useIconColor(() => stat.value?.color || "slate")
</script>

<template>
	<Card v-if="stat" class="w-56">
		<CardHeader>
			<CardDescription>{{ stat.name }}</CardDescription>
			<CardTitle class="text-2xl font-semibold tabular-nums">—</CardTitle>
			<CardAction v-if="stat.icon">
				<div class="flex size-8 items-center justify-center rounded-full" :class="style.badge">
					<Icon :icon="`lucide:${stat.icon}`" class="size-4" />
				</div>
			</CardAction>
		</CardHeader>
		<CardFooter v-if="stat.description">
			<p class="text-muted-foreground text-sm">{{ stat.description }}</p>
		</CardFooter>
	</Card>
</template>