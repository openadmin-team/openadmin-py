<!--
SPDX-FileCopyrightText: 2026 OpenAdmin

SPDX-License-Identifier: AGPL-3.0-or-later
-->

<script setup lang="ts">
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
</script>

<template>
	<h1>Form ! {{ form }}</h1>
</template>
