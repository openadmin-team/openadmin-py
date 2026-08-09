<!--
SPDX-FileCopyrightText: 2026 OpenAdmin

SPDX-License-Identifier: AGPL-3.0-or-later
-->

<script setup lang="ts">
import type { DropdownMenuSeparatorProps } from "reka-ui"
import type { HTMLAttributes } from "vue"
import { reactiveOmit } from "@vueuse/core"
import { DropdownMenuSeparator } from "reka-ui"
import { cn } from "@/lib/utils"

const props = defineProps<
	DropdownMenuSeparatorProps & {
		class?: HTMLAttributes["class"]
	}
>()

const delegatedProps = reactiveOmit(props, "class")
</script>

<template>
	<DropdownMenuSeparator
		data-slot="dropdown-menu-separator"
		v-bind="delegatedProps"
		:class="cn('bg-border -mx-1 my-1 h-px', props.class)"
	/>
</template>
