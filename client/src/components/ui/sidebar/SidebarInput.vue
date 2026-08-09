<!--
SPDX-FileCopyrightText: 2026 OpenAdmin

SPDX-License-Identifier: AGPL-3.0-or-later
-->

<script setup lang="ts">
import type { HTMLAttributes } from "vue"
import { cn } from "@/lib/utils"
import { Input } from "@/components/ui/input"

const props = defineProps<{
	class?: HTMLAttributes["class"]
}>()
</script>

<template>
	<Input
		data-slot="sidebar-input"
		data-sidebar="input"
		:class="cn(
      'bg-background h-8 w-full shadow-none',
      props.class,
    )"
	>
		<slot />
	</Input>
</template>
