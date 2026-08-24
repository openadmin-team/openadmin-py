<!--
SPDX-FileCopyrightText: 2026 OpenAdmin

SPDX-License-Identifier: AGPL-3.0-or-later
-->

<script setup lang="ts">
import type { TagsInputItemProps } from "reka-ui"
import type { HTMLAttributes } from "vue"
import { reactiveOmit } from "@vueuse/core"
import { TagsInputItem, useForwardProps } from "reka-ui"
import { cn } from "@/lib/utils"

const props = defineProps<TagsInputItemProps & { class?: HTMLAttributes["class"] }>()

const delegatedProps = reactiveOmit(props, "class")

const forwardedProps = useForwardProps(delegatedProps)
</script>

<template>
	<TagsInputItem
		data-slot="tags-input-item"
		v-bind="forwardedProps"
		:class="cn(
      'bg-muted text-foreground flex h-6 items-center rounded-xs',
      'data-[state=active]:ring-ring/50 data-[state=active]:ring-3',
      props.class,
    )"
	>
		<slot />
	</TagsInputItem>
</template>
