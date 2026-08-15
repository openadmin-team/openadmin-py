<!--
SPDX-FileCopyrightText: 2026 OpenAdmin

SPDX-License-Identifier: AGPL-3.0-or-later
-->

<script setup lang="ts">
import type { ActionComponent } from "@/schemas/action"
import type { FormComponent } from "@/schemas/form"

defineProps<{
	actions: ActionComponent[]
	forms: FormComponent[]
}>()
</script>

<template>
	<section>
		{{ actions }}
		{{ forms }}
	</section>
</template>
