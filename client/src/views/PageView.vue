<!--
SPDX-FileCopyrightText: 2026 OpenAdmin

SPDX-License-Identifier: AGPL-3.0-or-later
-->

<script setup lang="ts">
import { computed } from "vue"
import { useRoute } from "vue-router"
import { usePageSpec } from "@/composables/openadmin-spec"
import ButtonsSection from "@/components/page/ButtonsSection.vue"

const route = useRoute()
const pageId = computed(() => route.params.pageId as string)
const sectionId = computed(() => route.params.sectionId as string)
const { data: page } = usePageSpec({ sectionId, pageId })

const actions = computed(() => page.value?.components.filter((c) => c.type === 'action') ?? [])
const forms = computed(() => page.value?.components.filter((c) => c.type === 'form') ?? [])
</script>

<template>
	<ButtonsSection :actions="actions" :forms="forms" />
</template>
