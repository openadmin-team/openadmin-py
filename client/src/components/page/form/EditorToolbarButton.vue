<!--
SPDX-FileCopyrightText: 2026 OpenAdmin

SPDX-License-Identifier: AGPL-3.0-or-later
-->

<script setup lang="ts">
import type { Component } from "vue"
import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"

const props = defineProps<{
	icon: Component
	label: string
	active?: boolean
	disabled?: boolean
}>()
</script>

<template>
	<Button
		type="button"
		variant="ghost"
		size="icon-sm"
		:title="props.label"
		:aria-label="props.label"
		:aria-pressed="props.active"
		:disabled="props.disabled"
		:class="cn(props.active && 'bg-accent text-accent-foreground')"
	>
		<component :is="props.icon" />
	</Button>
</template>
