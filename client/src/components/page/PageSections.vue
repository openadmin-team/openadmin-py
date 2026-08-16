<!--
SPDX-FileCopyrightText: 2026 OpenAdmin

SPDX-License-Identifier: AGPL-3.0-or-later
-->

<script setup lang="ts">
import Action from "@/components/page/Action.vue"
import { usePageSpec } from "@/composables/openadmin-page"
import Form from "@/components/page/Form.vue"
import Stat from "@/components/page/Stat.vue"
import Table from "./Table.vue"

const props = defineProps<{
	sectionId: string
	pageId: string
}>()
const { actions, forms, stats, tables } = usePageSpec({
	sectionId: props.sectionId,
	pageId: props.pageId,
})
</script>

<template>
	<div class="flex flex-col gap-12">
		<section class="flex flex-wrap justify-end gap-2">
			<Action
				v-for="action in actions"
				:section-id="sectionId"
				:page-id="pageId"
				:action-id="action.id"
			/>
			<Form v-for="form in forms" :section-id="sectionId" :page-id="pageId" :form-id="form.id" />
		</section>
		<section class="flex flex-wrap justify-center gap-4">
			<Stat v-for="stat in stats" :section-id="sectionId" :page-id="pageId" :stat-id="stat.id" />
		</section>
		<section>
			<Table
				v-for="table in tables"
				:section-id="sectionId"
				:page-id="pageId"
				:table-id="table.id"
			/>
		</section>
	</div>
</template>
