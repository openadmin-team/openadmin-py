<!--
SPDX-FileCopyrightText: 2026 OpenAdmin

SPDX-License-Identifier: AGPL-3.0-or-later
-->

<script setup lang="ts">
import { MoonIcon, SunIcon } from "@lucide/vue"
import { Button } from "@/components/ui/button"
import { isDark, toggleDark } from "@/composables/theme"
</script>

<template>
	<Button
		type="button"
		variant="ghost"
		size="icon"
		:aria-label="isDark ? 'Switch to light theme' : 'Switch to dark theme'"
		@click="toggleDark()"
	>
		<SunIcon v-if="isDark" />
		<MoonIcon v-else />
	</Button>
</template>
