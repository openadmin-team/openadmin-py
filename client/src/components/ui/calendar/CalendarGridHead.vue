<!--
SPDX-FileCopyrightText: 2026 OpenAdmin

SPDX-License-Identifier: AGPL-3.0-or-later
-->

<script lang="ts" setup>
import type { CalendarGridHeadProps } from "reka-ui"
import type { HTMLAttributes } from "vue"
import { CalendarGridHead } from "reka-ui"

const props = defineProps<CalendarGridHeadProps & { class?: HTMLAttributes["class"] }>()
</script>

<template>
	<CalendarGridHead data-slot="calendar-grid-head" v-bind="props">
		<slot />
	</CalendarGridHead>
</template>
