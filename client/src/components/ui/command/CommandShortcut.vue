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
	<span
		data-slot="command-shortcut"
		:class="cn('text-muted-foreground ml-auto text-xs tracking-widest', props.class)"
	>
		<slot />
	</span>
</template>
