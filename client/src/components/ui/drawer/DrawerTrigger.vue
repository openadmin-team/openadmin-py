<!--
SPDX-FileCopyrightText: 2026 OpenAdmin

SPDX-License-Identifier: AGPL-3.0-or-later
-->

<script lang="ts" setup>
import type { DrawerTriggerProps } from "reka-ui"
import { DrawerTrigger } from "reka-ui"

const props = defineProps<DrawerTriggerProps>()
</script>

<template>
	<DrawerTrigger data-slot="drawer-trigger" v-bind="props">
		<slot />
	</DrawerTrigger>
</template>
