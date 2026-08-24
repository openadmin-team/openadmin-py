<!--
SPDX-FileCopyrightText: 2026 OpenAdmin

SPDX-License-Identifier: AGPL-3.0-or-later
-->

<script setup lang="ts">
import type { TagsInputInputProps } from "reka-ui"
import type { HTMLAttributes } from "vue"
import { reactiveOmit } from "@vueuse/core"
import { TagsInputInput, useForwardProps } from "reka-ui"
import { cn } from "@/lib/utils"

const props = defineProps<TagsInputInputProps & { class?: HTMLAttributes["class"] }>()

const delegatedProps = reactiveOmit(props, "class")

const forwardedProps = useForwardProps(delegatedProps)
</script>

<template>
	<TagsInputInput
		data-slot="tags-input-input"
		v-bind="forwardedProps"
		:class="cn(
      'placeholder:text-muted-foreground min-h-6 flex-1 bg-transparent px-1 text-sm outline-none disabled:cursor-not-allowed disabled:opacity-50',
      props.class,
    )"
	/>
</template>
