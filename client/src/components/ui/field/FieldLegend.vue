<!--
SPDX-FileCopyrightText: 2026 OpenAdmin

SPDX-License-Identifier: AGPL-3.0-or-later
-->

<script setup lang="ts">
import type { HTMLAttributes } from "vue"
import { cn } from "@/lib/utils"

const props = defineProps<{
	class?: HTMLAttributes["class"]
	variant?: "legend" | "label"
}>()
</script>

<template>
	<legend
		data-slot="field-legend"
		:data-variant="variant"
		:class="cn(
      'mb-3 font-medium',
      'data-[variant=legend]:text-base',
      'data-[variant=label]:text-sm',
      props.class,
    )"
	>
		<slot />
	</legend>
</template>
