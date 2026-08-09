<!--
SPDX-FileCopyrightText: 2026 OpenAdmin

SPDX-License-Identifier: AGPL-3.0-or-later
-->

<script setup lang="ts">
import type { TooltipProviderProps } from "reka-ui"
import { TooltipProvider } from "reka-ui"

const props = withDefaults(defineProps<TooltipProviderProps>(), {
	delayDuration: 0,
})
</script>

<template>
	<TooltipProvider v-bind="props">
		<slot />
	</TooltipProvider>
</template>
