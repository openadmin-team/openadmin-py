<!--
SPDX-FileCopyrightText: 2026 OpenAdmin

SPDX-License-Identifier: AGPL-3.0-or-later
-->

<script setup lang="ts">
import type { HTMLAttributes } from "vue"
import { cn } from "@/lib/utils"

const props = defineProps<{
	class?: HTMLAttributes["class"]
}>()
</script>

<template>
	<tfoot
		data-slot="table-footer"
		:class="cn('bg-muted/50 border-t font-medium [&>tr]:last:border-b-0', props.class)"
	>
		<slot />
	</tfoot>
</template>
