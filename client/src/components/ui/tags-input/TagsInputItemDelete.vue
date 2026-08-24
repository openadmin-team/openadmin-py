<!--
SPDX-FileCopyrightText: 2026 OpenAdmin

SPDX-License-Identifier: AGPL-3.0-or-later
-->

<script setup lang="ts">
import type { TagsInputItemDeleteProps } from "reka-ui"
import type { HTMLAttributes } from "vue"
import { X } from "@lucide/vue"
import { reactiveOmit } from "@vueuse/core"
import { TagsInputItemDelete, useForwardProps } from "reka-ui"
import { cn } from "@/lib/utils"

const props = defineProps<TagsInputItemDeleteProps & { class?: HTMLAttributes["class"] }>()

const delegatedProps = reactiveOmit(props, "class")

const forwardedProps = useForwardProps(delegatedProps)
</script>

<template>
	<TagsInputItemDelete
		data-slot="tags-input-item-delete"
		v-bind="forwardedProps"
		:class="cn(
      'text-muted-foreground hover:text-foreground hover:bg-accent mr-1 flex items-center justify-center rounded-xs bg-transparent transition-colors',
      props.class,
    )"
	>
		<slot>
			<X class="size-3" />
		</slot>
	</TagsInputItemDelete>
</template>
