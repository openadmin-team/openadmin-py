<!--
SPDX-FileCopyrightText: 2026 OpenAdmin

SPDX-License-Identifier: AGPL-3.0-or-later
-->

<script setup lang="ts">
import type { PrimitiveProps } from "reka-ui"
import type { HTMLAttributes } from "vue"
import type { BadgeVariants } from "."
import { reactiveOmit } from "@vueuse/core"
import { Primitive } from "reka-ui"
import { cn } from "@/lib/utils"
import { badgeVariants } from "."

const props = defineProps<
	PrimitiveProps & {
		variant?: BadgeVariants["variant"]
		class?: HTMLAttributes["class"]
	}
>()

const delegatedProps = reactiveOmit(props, "class")
</script>

<template>
	<Primitive
		data-slot="badge"
		:class="cn(badgeVariants({ variant }), props.class)"
		v-bind="delegatedProps"
	>
		<slot />
	</Primitive>
</template>
