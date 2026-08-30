<!--
SPDX-FileCopyrightText: 2026 OpenAdmin

SPDX-License-Identifier: AGPL-3.0-or-later
-->

<script setup lang="ts">
import { Icon } from "@iconify/vue"
import { computed } from "vue"
import ActionButton from "@/components/action/ActionButton.vue"
import FormButton from "@/components/form/FormButton.vue"
import Markdown from "@/components/markdown/Markdown.vue"
import Stat from "@/components/stat/Stat.vue"
import Table from "@/components/table/Table.vue"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { useColor } from "@/composables/colors"
import { usePageSpec } from "@/composables/openadmin-page"

const props = defineProps<{
	sectionId: string
	pageId: string
}>()
const { actions, forms, stats, tables, markdowns } = usePageSpec({
	sectionId: props.sectionId,
	pageId: props.pageId,
})

const tabItems = computed(() =>
	tables.value.map((table) => ({
		table,
		style: useColor(table.color ?? "slate").style.value,
	})),
)
</script>

<template>
	<div class="flex flex-col gap-24">
		<section v-if="actions.length || forms.length" class="flex flex-wrap justify-end gap-2">
			<ActionButton
				v-for="action in actions"
				:section-id="sectionId"
				:page-id="pageId"
				:action-id="action.id"
			/>
			<FormButton
				v-for="form in forms"
				:section-id="sectionId"
				:page-id="pageId"
				:form-id="form.id"
			/>
		</section>
		<section v-if="stats.length" class="flex flex-wrap justify-center gap-4">
			<Stat v-for="stat in stats" :section-id="sectionId" :page-id="pageId" :stat-id="stat.id" />
		</section>
		<section v-if="markdowns.length" class="flex flex-col items-center gap-24">
			<Markdown
				v-for="markdown in markdowns"
				:key="markdown.id"
				:section-id="sectionId"
				:page-id="pageId"
				:markdown-id="markdown.id"
			/>
		</section>
		<section v-if="tables.length > 1">
			<Tabs :key="pageId" :default-value="tables[0]?.id">
				<TabsList>
					<TabsTrigger v-for="item in tabItems" :key="item.table.id" :value="item.table.id">
						<Icon
							v-if="item.table.icon"
							:icon="`lucide:${item.table.icon}`"
							:class="item.style.text"
						/>
						{{ item.table.name }}
					</TabsTrigger>
				</TabsList>
				<TabsContent v-for="table in tables" :key="table.id" :value="table.id">
					<Table :section-id="sectionId" :page-id="pageId" :table-id="table.id" />
				</TabsContent>
			</Tabs>
		</section>
		<section v-else-if="tables.length === 1">
			<Table :section-id="sectionId" :page-id="pageId" :table-id="tables[0].id" />
		</section>
	</div>
</template>
