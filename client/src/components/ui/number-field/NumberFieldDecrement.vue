<!--
SPDX-FileCopyrightText: 2026 OpenAdmin

SPDX-License-Identifier: AGPL-3.0-or-later
-->

<script setup lang="ts">
import type { NumberFieldDecrementProps } from "reka-ui"
import type { HTMLAttributes } from "vue"
import { Minus } from "@lucide/vue"
import { reactiveOmit } from "@vueuse/core"
import { NumberFieldDecrement, useForwardProps } from "reka-ui"
import { cn } from "@/lib/utils"

const props = defineProps<NumberFieldDecrementProps & { class?: HTMLAttributes["class"] }>()

const delegatedProps = reactiveOmit(props, "class")

const forwarded = useForwardProps(delegatedProps)
</script>

<template>
	<NumberFieldDecrement
		data-slot="decrement"
		v-bind="forwarded"
		:class="cn('absolute inset-y-1 left-1 flex w-7 items-center justify-center rounded-xs text-muted-foreground transition-all outline-none hover:bg-accent hover:text-accent-foreground active:scale-[0.97] disabled:pointer-events-none disabled:cursor-not-allowed disabled:opacity-50 disabled:active:scale-100', props.class)"
	>
		<slot>
			<Minus class="h-4 w-4" />
		</slot>
	</NumberFieldDecrement>
</template>
