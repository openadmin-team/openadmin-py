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
	<li
		data-slot="sidebar-menu-item"
		data-sidebar="menu-item"
		:class="cn('group/menu-item relative', props.class)"
	>
		<slot />
	</li>
</template>
