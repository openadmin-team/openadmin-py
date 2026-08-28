<!--
SPDX-FileCopyrightText: 2026 OpenAdmin

SPDX-License-Identifier: AGPL-3.0-or-later
-->

<script setup lang="ts">
import { Icon } from "@iconify/vue"
import { useColor } from "@/composables/colors"
import type { FieldDef } from "./field"

const props = defineProps<{
	def: FieldDef
}>()

const { style } = useColor(() => props.def.color || "slate")
</script>

<template>
	<Icon v-if="props.def.icon" :icon="`lucide:${props.def.icon}`" :class="style.text" />
	{{ props.def.label }}<span v-if="props.def.required" class="text-destructive"> *</span>
</template>
