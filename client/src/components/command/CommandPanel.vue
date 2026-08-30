<!--
SPDX-FileCopyrightText: 2026 OpenAdmin

SPDX-License-Identifier: AGPL-3.0-or-later
-->

<script setup lang="ts">
import { Icon } from "@iconify/vue"
import {
	CommandDialog,
	CommandEmpty,
	CommandGroup,
	CommandInput,
	CommandItem,
	CommandList,
	CommandSeparator,
} from "@/components/ui/command"
import { isCommandPanelOpen } from "@/composables/command-panel"
import { useColor } from "@/composables/colors"
import { useSpec } from "@/composables/openadmin-spec"
import type { Color } from "@/schemas/color"
import type { Component } from "@/schemas/component"
import type { Icon as IconName } from "@/schemas/icon"

const { data: spec } = useSpec()

// area-chart and line-chart components don't carry icon/color fields at all,
// unlike every other component type, so access has to be guarded.
function componentIcon(component: Component): IconName | null {
	return "icon" in component ? (component.icon ?? null) : null
}

function componentColor(component: Component): Color | null {
	return "color" in component ? (component.color ?? null) : null
}

function textClass(color: Color | null) {
	return color ? useColor(color).style.value.text : undefined
}

function dotClass(color: Color | null) {
	return color ? [useColor(color).style.value.dot, "size-1.5 rounded-full shrink-0"] : undefined
}
</script>

<template>
	<CommandDialog
		v-model:open="isCommandPanelOpen"
		title="Command Panel"
		description="Search sections, pages, and components..."
	>
		<CommandInput placeholder="Search sections, pages, and components..." />
		<CommandList>
			<CommandEmpty>No results found.</CommandEmpty>

			<template v-for="(section, index) in spec?.sections ?? []" :key="section.id">
				<CommandSeparator v-if="index > 0" />
				<CommandGroup>
					<div
						class="text-muted-foreground flex items-center gap-1.5 px-2 py-1.5 text-xs font-medium"
					>
						<Icon v-if="section.icon" :icon="`lucide:${section.icon}`" class="size-3.5 shrink-0" />
						<span>{{ section.name }}</span>
					</div>

					<template v-for="page in section.pages" :key="page.id">
						<CommandItem :value="page.id">
							<Icon v-if="page.icon" :icon="`lucide:${page.icon}`" :class="textClass(page.color)" />
							<span v-else-if="page.color" :class="dotClass(page.color)" />
							<span>{{ page.name }}</span>
						</CommandItem>

						<CommandItem
							v-for="component in page.components"
							:key="component.id"
							:value="component.id"
							class="pl-8"
						>
							<Icon
								v-if="componentIcon(component)"
								:icon="`lucide:${componentIcon(component)}`"
								:class="textClass(componentColor(component))"
							/>
							<span
								v-else-if="componentColor(component)"
								:class="dotClass(componentColor(component))"
							/>
							<span class="text-muted-foreground">{{ component.name }}</span>
						</CommandItem>
					</template>
				</CommandGroup>
			</template>
		</CommandList>
	</CommandDialog>
</template>
