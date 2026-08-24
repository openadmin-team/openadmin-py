<!--
SPDX-FileCopyrightText: 2026 OpenAdmin

SPDX-License-Identifier: AGPL-3.0-or-later
-->

<script setup lang="ts">
import type { PopoverTriggerProps } from "reka-ui"
import { PopoverTrigger } from "reka-ui"

const props = defineProps<PopoverTriggerProps>()
</script>

<template>
	<PopoverTrigger data-slot="popover-trigger" v-bind="props">
		<slot />
	</PopoverTrigger>
</template>
