<!--
SPDX-FileCopyrightText: 2026 OpenAdmin

SPDX-License-Identifier: AGPL-3.0-or-later
-->

<script setup lang="ts">
import type { PopoverRootEmits, PopoverRootProps } from "reka-ui"
import { PopoverRoot, useForwardPropsEmits } from "reka-ui"

const props = defineProps<PopoverRootProps>()
const emits = defineEmits<PopoverRootEmits>()

const forwarded = useForwardPropsEmits(props, emits)
</script>

<template>
	<PopoverRoot v-slot="slotProps" data-slot="popover" v-bind="forwarded">
		<slot v-bind="slotProps" />
	</PopoverRoot>
</template>
