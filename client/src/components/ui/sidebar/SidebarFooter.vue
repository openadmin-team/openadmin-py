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
		data-slot="sidebar-footer"
		data-sidebar="footer"
		:class="cn('flex flex-col gap-2 p-2', props.class)"
	>
		<slot />
	</div>
</template>
