<!--
SPDX-FileCopyrightText: 2026 OpenAdmin

SPDX-License-Identifier: AGPL-3.0-or-later
-->

<script setup lang="ts">
import { computed } from "vue"
import { useRoute } from "vue-router"
import { useOpenAdminPageSpec } from "@/composables/openadmin-spec"

const route = useRoute()
const pageId = computed(() => route.params.pageId as string)
const { data: page } = useOpenAdminPageSpec({ id: pageId.value })
</script>

<template>
	<div v-if="page">
		<h1 class="text-2xl font-semibold">{{ page.name }}</h1>
		<p v-if="page.description" class="text-muted-foreground mt-1">{{ page.description }}</p>
	</div>
</template>
