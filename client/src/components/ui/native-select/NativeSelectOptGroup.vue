<!--
SPDX-FileCopyrightText: 2026 OpenAdmin

SPDX-License-Identifier: AGPL-3.0-or-later
-->

<script setup lang="ts">
import type { HTMLAttributes } from "vue"
import { cn } from "@/lib/utils"

const props = defineProps<{ class?: HTMLAttributes["class"] }>()
</script>

<template>
	<optgroup
		data-slot="native-select-optgroup"
		:class="cn('bg-popover text-popover-foreground', props.class)"
	>
		<slot />
	</optgroup>
</template>
