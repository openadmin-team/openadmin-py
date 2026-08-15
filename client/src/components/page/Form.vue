<!--
SPDX-FileCopyrightText: 2026 OpenAdmin

SPDX-License-Identifier: AGPL-3.0-or-later
-->

<script setup lang="ts">
import { useIconColor } from "@/composables/colors"
import { Button } from "@/components/ui/button"
import { Icon } from "@iconify/vue"
import { useForm } from "@/composables/openadmin-form"

const props = defineProps<{
	sectionId: string
	pageId: string
	formId: string
}>()
const { form } = useForm({
	sectionId: props.sectionId,
	pageId: props.pageId,
	formId: props.formId,
})
const { style } = useIconColor(() => form.value?.color || "slate")
</script>

<template>
	<Button v-if="form" size="sm" variant="outline">
		<Icon v-if="form.icon" :icon="`lucide:${form.icon}`" :class="style.text" />
		{{ form.name }}
	</Button>
</template>
