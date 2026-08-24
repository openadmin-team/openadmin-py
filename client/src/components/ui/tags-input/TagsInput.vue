<!--
SPDX-FileCopyrightText: 2026 OpenAdmin

SPDX-License-Identifier: AGPL-3.0-or-later
-->

<script setup lang="ts">
import type { TagsInputRootEmits, TagsInputRootProps } from "reka-ui"
import type { HTMLAttributes } from "vue"
import { reactiveOmit } from "@vueuse/core"
import { TagsInputRoot, useForwardPropsEmits } from "reka-ui"
import { cn } from "@/lib/utils"

const props = defineProps<TagsInputRootProps & { class?: HTMLAttributes["class"] }>()
const emits = defineEmits<TagsInputRootEmits>()

const delegatedProps = reactiveOmit(props, "class")

const forwarded = useForwardPropsEmits(delegatedProps, emits)
</script>

<template>
	<TagsInputRoot
		v-slot="slotProps"
		data-slot="tags-input"
		v-bind="forwarded"
		:class="cn(
      'border-input flex min-h-9 w-full flex-wrap items-center gap-1.5 rounded-xs border bg-transparent px-2.5 py-1.5 text-sm shadow-xs transition-[color,box-shadow] outline-none',
      'dark:bg-input/30',
      'focus-within:border-ring focus-within:ring-ring/50 focus-within:ring-3',
      'aria-invalid:ring-destructive/20 dark:aria-invalid:ring-destructive/40 aria-invalid:border-destructive',
      props.class,
    )"
	>
		<slot v-bind="slotProps" />
	</TagsInputRoot>
</template>
