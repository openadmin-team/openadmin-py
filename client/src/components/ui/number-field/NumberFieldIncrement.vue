<!--
SPDX-FileCopyrightText: 2026 OpenAdmin

SPDX-License-Identifier: AGPL-3.0-or-later
-->

<script setup lang="ts">
import type { NumberFieldIncrementProps } from "reka-ui"
import type { HTMLAttributes } from "vue"
import { Plus } from "@lucide/vue"
import { reactiveOmit } from "@vueuse/core"
import { NumberFieldIncrement, useForwardProps } from "reka-ui"
import { cn } from "@/lib/utils"

const props = defineProps<NumberFieldIncrementProps & { class?: HTMLAttributes["class"] }>()

const delegatedProps = reactiveOmit(props, "class")

const forwarded = useForwardProps(delegatedProps)
</script>

<template>
	<NumberFieldIncrement
		data-slot="increment"
		v-bind="forwarded"
		:class="cn('absolute inset-y-1 right-1 flex w-7 items-center justify-center rounded-xs text-muted-foreground transition-all outline-none hover:bg-accent hover:text-accent-foreground active:scale-[0.97] disabled:pointer-events-none disabled:cursor-not-allowed disabled:opacity-50 disabled:active:scale-100', props.class)"
	>
		<slot>
			<Plus class="h-4 w-4" />
		</slot>
	</NumberFieldIncrement>
</template>
