<!--
SPDX-FileCopyrightText: 2026 OpenAdmin

SPDX-License-Identifier: AGPL-3.0-or-later
-->

<script setup lang="ts">
import { CommandIcon } from "@lucide/vue"
import { computed } from "vue"
import { Button } from "@/components/ui/button"
import { Kbd, KbdGroup } from "@/components/ui/kbd"
import { Tooltip, TooltipContent, TooltipTrigger } from "@/components/ui/tooltip"
import { isCommandPanelOpen } from "@/composables/command-panel"

defineOptions({
	inheritAttrs: false,
})

const isMac = computed(() => /Mac|iPhone|iPad|iPod/.test(navigator.platform))
</script>

<template>
	<Tooltip>
		<TooltipTrigger as-child>
			<Button
				type="button"
				variant="ghost"
				size="icon"
				aria-label="Open command palette"
				v-bind="$attrs"
				@click="isCommandPanelOpen = true"
			>
				<CommandIcon />
			</Button>
		</TooltipTrigger>
		<TooltipContent class="flex items-center gap-2">
			Command Palette
			<KbdGroup>
				<Kbd>{{ isMac ? "⌘" : "Ctrl" }}</Kbd>
				<Kbd>P</Kbd>
			</KbdGroup>
		</TooltipContent>
	</Tooltip>
</template>
