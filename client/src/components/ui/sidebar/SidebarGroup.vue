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
	<div
		data-slot="sidebar-group"
		data-sidebar="group"
		:class="cn('relative flex w-full min-w-0 flex-col p-2', props.class)"
	>
		<slot />
	</div>
</template>
