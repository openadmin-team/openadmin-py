<!--
SPDX-FileCopyrightText: 2026 OpenAdmin

SPDX-License-Identifier: AGPL-3.0-or-later
-->

<script setup lang="ts">
import Action from "@/components/page/Action.vue"
import { usePageSpec } from "@/composables/openadmin-page"
import Form from "@/components/page/Form.vue"
import Stat from "@/components/page/Stat.vue";

const props = defineProps<{
	sectionId: string
	pageId: string
}>()
const { actions, forms, stats } = usePageSpec({ sectionId: props.sectionId, pageId: props.pageId })
</script>

<template>
	<section class="flex flex-wrap justify-end gap-2">
		<Action
			v-for="action in actions"
			:section-id="sectionId"
			:page-id="pageId"
			:action-id="action.id"
		/>
		<Form v-for="form in forms" :section-id="sectionId" :page-id="pageId" :form-id="form.id" />
	</section>
	<section class="grid grid-cols-1 gap-2 sm:grid-cols-2 lg:grid-cols-4">
		<Stat
			v-for="stat in stats"
			:section-id="sectionId"
			:page-id="pageId"
			:stat-id="stat.id"
		/>
	</section>
</template>
