<!--
SPDX-FileCopyrightText: 2026 OpenAdmin

SPDX-License-Identifier: AGPL-3.0-or-later
-->

<script setup lang="ts">
import type { HTMLAttributes } from "vue"
import { cn } from "@/lib/utils"

const props = defineProps<{
	class?: HTMLAttributes["class"]
}>()
</script>

<template>
	<div data-slot="table-container" class="relative w-full overflow-auto">
		<table data-slot="table" :class="cn('w-full caption-bottom text-sm', props.class)">
			<slot />
		</table>
	</div>
</template>
