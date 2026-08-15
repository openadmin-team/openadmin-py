<!--
SPDX-FileCopyrightText: 2026 OpenAdmin

SPDX-License-Identifier: AGPL-3.0-or-later
-->

<script setup lang="ts">
import Action from "@/components/page/Action.vue"
import { usePageSpec } from "@/composables/openadmin-page"

const props = defineProps<{
	sectionId: string
	pageId: string
}>()
const { actions } = usePageSpec({ sectionId: props.sectionId, pageId: props.pageId })
</script>

<template>
	<section class="flex flex-wrap justify-end gap-2">
		<Action
			v-for="action in actions"
			:section-id="sectionId"
			:page-id="pageId"
			:action-id="action.id"
		/>
	</section>
</template>
