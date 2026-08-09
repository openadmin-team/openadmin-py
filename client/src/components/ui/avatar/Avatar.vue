<!--
SPDX-FileCopyrightText: 2026 OpenAdmin

SPDX-License-Identifier: AGPL-3.0-or-later
-->

<script setup lang="ts">
import type { HTMLAttributes } from "vue"
import { AvatarRoot } from "reka-ui"
import { cn } from "@/lib/utils"

const props = defineProps<{
	class?: HTMLAttributes["class"]
}>()
</script>

<template>
	<AvatarRoot
		data-slot="avatar"
		:class="cn('relative flex size-8 shrink-0 overflow-hidden rounded-full', props.class)"
	>
		<slot />
	</AvatarRoot>
</template>
