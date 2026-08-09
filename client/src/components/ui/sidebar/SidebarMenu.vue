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
	<ul
		data-slot="sidebar-menu"
		data-sidebar="menu"
		:class="cn('flex w-full min-w-0 flex-col gap-1', props.class)"
	>
		<slot />
	</ul>
</template>
