<!--
SPDX-FileCopyrightText: 2026 OpenAdmin

SPDX-License-Identifier: AGPL-3.0-or-later
-->

<script setup lang="ts">
import { useColor } from "@/composables/colors"
import { Button } from "@/components/ui/button"
import { Icon } from "@iconify/vue"
import { RouterLink } from "vue-router"
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
const { style } = useColor(() => form.value?.color || "slate")
</script>

<template>
	<Button v-if="form" as-child size="sm" variant="outline">
		<RouterLink
			:to="{ name: 'form', params: { sectionId: props.sectionId, pageId: props.pageId, formId: props.formId } }"
		>
			<Icon v-if="form.icon" :icon="`lucide:${form.icon}`" :class="style.text" />
			{{ form.name }}
		</RouterLink>
	</Button>
</template>
