<!--
SPDX-FileCopyrightText: 2026 OpenAdmin

SPDX-License-Identifier: AGPL-3.0-or-later
-->

<script setup lang="ts">
import { computed } from "vue"
import { useRoute } from "vue-router"
import Form from "@/components/page/form/Form.vue"

const route = useRoute()

const pageId = computed(() => route.params.pageId as string)
const sectionId = computed(() => route.params.sectionId as string)
const formId = computed(() => route.params.formId as string)
</script>

<template>
	<Form :section-id="sectionId" :page-id="pageId" :form-id="formId" />
</template>
