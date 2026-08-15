<!--
SPDX-FileCopyrightText: 2026 OpenAdmin

SPDX-License-Identifier: AGPL-3.0-or-later
-->

<script setup lang="ts">
import type { ActionComponent } from "@/schemas/action"
import type { FormComponent } from "@/schemas/form"
import { Button } from "@/components/ui/button"
import { Icon } from "@iconify/vue"

defineProps<{
	actions: ActionComponent[]
	forms: FormComponent[]
}>()
</script>

<template>
	<section>
		<Button
			v-for="action in actions"
			size="sm"
			:variant="action.color === 'red' ? 'destructive' : 'outline'"
			:class="COLOR(component.color).text"
		>
			<Icon v-if="action.icon" :icon="action.icon" />
			{{ action.name }}
		</Button>
	</section>
</template>
