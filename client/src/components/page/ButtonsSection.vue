<!--
SPDX-FileCopyrightText: 2026 OpenAdmin

SPDX-License-Identifier: AGPL-3.0-or-later
-->

<script setup lang="ts">
import type { ActionComponent } from "@/schemas/action"
import type { FormComponent } from "@/schemas/form"
import Action from "@/components/page/Action.vue"

defineProps<{
	actions: ActionComponent[]
	forms: FormComponent[]
}>()
</script>

<template>
	<section class="flex flex-wrap justify-end gap-2">
		<Action v-for="action in actions" :action="action" />
	</section>
</template>
