<!--
SPDX-FileCopyrightText: 2026 OpenAdmin

SPDX-License-Identifier: AGPL-3.0-or-later
-->

<script lang="ts" setup>
import type { DrawerCloseProps } from "reka-ui"
import { DrawerClose } from "reka-ui"

const props = defineProps<DrawerCloseProps>()
</script>

<template>
	<DrawerClose data-slot="drawer-close" v-bind="props">
		<slot />
	</DrawerClose>
</template>
