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
	<tbody data-slot="table-body" :class="cn('[&_tr:last-child]:border-0', props.class)">
		<slot />
	</tbody>
</template>
