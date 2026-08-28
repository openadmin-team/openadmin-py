<!--
SPDX-FileCopyrightText: 2026 OpenAdmin

SPDX-License-Identifier: AGPL-3.0-or-later
-->

<script setup lang="ts">
import { computed } from "vue"
import { useRoute } from "vue-router"
import Page from "@/components/page/Page.vue"

const route = useRoute()
const pageId = computed(() => route.params.pageId as string)
const sectionId = computed(() => route.params.sectionId as string)
</script>

<template>
	<Page :section-id="sectionId" :page-id="pageId" />
</template>
