<!--
SPDX-FileCopyrightText: 2026 OpenAdmin

SPDX-License-Identifier: AGPL-3.0-or-later
-->

<script setup lang="ts">
import type { SelectGroupProps } from "reka-ui"
import { SelectGroup } from "reka-ui"

const props = defineProps<SelectGroupProps>()
</script>

<template>
	<SelectGroup data-slot="select-group" v-bind="props">
		<slot />
	</SelectGroup>
</template>
