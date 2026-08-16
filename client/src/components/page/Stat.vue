<!--
SPDX-FileCopyrightText: 2026 OpenAdmin

SPDX-License-Identifier: AGPL-3.0-or-later
-->

<script setup lang="ts">
import { useColor } from "@/composables/colors"
import {
	Card,
	CardAction,
	CardDescription,
	CardFooter,
	CardHeader,
	CardTitle,
} from "@/components/ui/card"
import { Skeleton } from "@/components/ui/skeleton"
import { Spinner } from "@/components/ui/spinner"
import { Icon } from "@iconify/vue"
import { useStat } from "@/composables/openadmin-stat"

const props = defineProps<{
	sectionId: string
	pageId: string
	statId: string
}>()
const { stat, value, isFetching } = useStat({
	sectionId: props.sectionId,
	pageId: props.pageId,
	statId: props.statId,
})
const { style } = useColor(() => stat.value?.color || "slate")
</script>

<template>
	<Card v-if="stat" class="w-full sm:w-[calc(50%-0.25rem)] lg:w-[calc(25%-0.375rem)]">
		<CardHeader>
			<CardAction v-if="isFetching">
				<Spinner class="text-muted-foreground/40 size-3.5" />
			</CardAction>
			<CardDescription class="flex items-center gap-1.5">
				<Icon v-if="stat.icon" :icon="`lucide:${stat.icon}`" :class="style.text" class="size-4" />
				{{ stat.name }}
			</CardDescription>
			<CardTitle class="text-2xl font-semibold tabular-nums">
				<Skeleton v-if="value === null" class="h-7 w-16" />
				<template v-else>{{ value }}</template>
			</CardTitle>
		</CardHeader>
		<CardFooter v-if="stat.description">
			<p class="text-muted-foreground text-sm">{{ stat.description }}</p>
		</CardFooter>
	</Card>
	<Card v-else class="w-full sm:w-[calc(50%-0.25rem)] lg:w-[calc(25%-0.375rem)]">
		<CardHeader>
			<CardDescription class="flex items-center gap-1.5">
				<Skeleton class="h-4 w-24" />
			</CardDescription>
			<CardTitle>
				<Skeleton class="h-7 w-16" />
			</CardTitle>
		</CardHeader>
	</Card>
</template>
