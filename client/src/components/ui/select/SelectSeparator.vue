<!--
SPDX-FileCopyrightText: 2026 OpenAdmin

SPDX-License-Identifier: AGPL-3.0-or-later
-->

<script setup lang="ts">
import { reactiveOmit } from "@vueuse/core"
import type { SelectSeparatorProps } from "reka-ui"
import { SelectSeparator } from "reka-ui"
import type { HTMLAttributes } from "vue"
import { cn } from "@/lib/utils"

const props = defineProps<SelectSeparatorProps & { class?: HTMLAttributes["class"] }>()

const delegatedProps = reactiveOmit(props, "class")
</script>

<template>
	<SelectSeparator
		data-slot="select-separator"
		v-bind="delegatedProps"
		:class="cn('bg-border pointer-events-none -mx-1 my-1 h-px', props.class)"
	/>
</template>
