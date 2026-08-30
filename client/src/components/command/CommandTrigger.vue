<!--
SPDX-FileCopyrightText: 2026 OpenAdmin

SPDX-License-Identifier: AGPL-3.0-or-later
-->

<script setup lang="ts">
import { CommandIcon } from "@lucide/vue"
import { Button } from "@/components/ui/button"
import { isCommandPanelOpen } from "@/composables/command-panel"
</script>

<template>
	<Button
		type="button"
		variant="ghost"
		size="icon"
		aria-label="Open command palette"
		@click="isCommandPanelOpen = true"
	>
		<CommandIcon />
	</Button>
</template>
