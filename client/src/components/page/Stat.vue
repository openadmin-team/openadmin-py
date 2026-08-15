<!--
SPDX-FileCopyrightText: 2026 OpenAdmin

SPDX-License-Identifier: AGPL-3.0-or-later
-->

<script setup lang="ts">
import { useIconColor } from "@/composables/colors"
import { Card, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Icon } from "@iconify/vue"
import { useStat } from "@/composables/openadmin-stat"

const props = defineProps<{
	sectionId: string
	pageId: string
	statId: string
}>()
const { stat, value } = useStat({
	sectionId: props.sectionId,
	pageId: props.pageId,
	statId: props.statId,
})
const { style } = useIconColor(() => stat.value?.color || "slate")
</script>

<template>
	<Card v-if="stat" class="w-full sm:w-[calc(50%-0.25rem)] lg:w-[calc(25%-0.375rem)]">
		<CardHeader>
			<CardDescription class="flex items-center gap-1.5">
				<Icon v-if="stat.icon" :icon="`lucide:${stat.icon}`" :class="style.text" class="size-4" />
				{{ stat.name }}
			</CardDescription>
			<CardTitle class="text-2xl font-semibold tabular-nums">{{ value }}</CardTitle>
		</CardHeader>
		<CardFooter v-if="stat.description">
			<p class="text-muted-foreground text-sm">{{ stat.description }}</p>
		</CardFooter>
	</Card>
</template>