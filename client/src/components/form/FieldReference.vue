<!--
SPDX-FileCopyrightText: 2026 OpenAdmin

SPDX-License-Identifier: AGPL-3.0-or-later
-->

<script setup lang="ts">
import { XIcon } from "@lucide/vue"
import type { AnyFieldApi } from "@tanstack/vue-form"
import { computed, ref } from "vue"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Field, FieldError, FieldLabel } from "@/components/ui/field"
import { useReference } from "@/composables/openadmin-reference"
import type { TableRow } from "@/schemas/table"
import { type FieldDef, isInvalid } from "./field"
import FieldLabelText from "./FieldLabelText.vue"
import ReferencePicker from "./ReferencePicker.vue"

const props = defineProps<{
	field: AnyFieldApi
	def: FieldDef
}>()

const open = ref(false)

const { component, sectionId, pageId } = useReference({
	componentId: computed(() => props.def.reference ?? ""),
})

const referenceField = computed(() => props.def.referenceField ?? "id")
const title = computed(() => component.value?.name ?? props.def.label)

// The value on the field is only ever the raw reference_field scalar(s), so the
// human-readable __view__ label has to be cached client-side from whichever row
// was picked in the drawer — the form never re-fetches an existing value's row.
const cache = ref(new Map<string, TableRow>())

function rowId(row: TableRow) {
	return String(row[referenceField.value] ?? "")
}

function rowLabel(id: string) {
	const row = cache.value.get(id)
	if (!row) return id
	if (row.__view__ !== null && row.__view__ !== undefined) return String(row.__view__)
	const value = row[referenceField.value]
	return value === null || value === undefined ? id : String(value)
}

const selectedIds = computed<string[]>(() => {
	const value = props.field.state.value
	if (props.def.array) return ((value as unknown[] | undefined) ?? []).map(String)
	return value === undefined || value === null || value === "" ? [] : [String(value)]
})

const selectedItems = computed(() => selectedIds.value.map((id) => ({ id, label: rowLabel(id) })))

const initialSelection = computed(() =>
	selectedIds.value.map((id) => cache.value.get(id)).filter((row): row is TableRow => !!row),
)

function onConfirm(rows: TableRow[]) {
	if (props.def.array) {
		const next = new Map<string, TableRow>()
		for (const row of rows) next.set(rowId(row), row)
		cache.value = next
		props.field.handleChange(rows.map((row) => row[referenceField.value]))
		return
	}

	const row = rows[0]
	if (!row) return
	cache.value.set(rowId(row), row)
	props.field.handleChange(row[referenceField.value])
}

function removeAt(id: string) {
	if (props.def.array) {
		const next = new Map(cache.value)
		next.delete(id)
		cache.value = next
		props.field.handleChange(selectedIds.value.filter((existing) => existing !== id))
		return
	}

	cache.value = new Map()
	props.field.handleChange(undefined)
}
</script>

<template>
	<Field :data-invalid="isInvalid(props.field)">
		<FieldLabel :for="props.field.name">
			<FieldLabelText :def="props.def" />
		</FieldLabel>

		<div v-if="props.def.array" class="flex flex-wrap items-center gap-2">
			<Badge v-for="item in selectedItems" :key="item.id" variant="secondary" class="gap-1.5 py-1">
				{{ item.label }}
				<button type="button" aria-label="Remove" @click="removeAt(item.id)">
					<XIcon class="size-3" />
				</button>
			</Badge>
			<Button
				:id="props.field.name"
				type="button"
				variant="outline"
				size="sm"
				:disabled="!component"
				:aria-invalid="isInvalid(props.field)"
				@click="open = true"
			>
				Add
			</Button>
		</div>

		<div v-else class="flex items-center gap-2">
			<Button
				:id="props.field.name"
				type="button"
				variant="outline"
				class="w-full justify-start font-normal"
				:disabled="!component"
				:aria-invalid="isInvalid(props.field)"
				@click="open = true"
			>
				{{ selectedItems[0]?.label ?? `Select ${title}...` }}
			</Button>
			<Button
				v-if="selectedItems.length"
				type="button"
				variant="ghost"
				size="icon"
				aria-label="Clear selection"
				@click="removeAt(selectedItems[0].id)"
			>
				<XIcon />
			</Button>
		</div>

		<ReferencePicker
			v-if="sectionId && pageId"
			v-model:open="open"
			:section-id="sectionId"
			:page-id="pageId"
			:table-id="props.def.reference!"
			:reference-field="referenceField"
			:multiple="!!props.def.array"
			:title="title"
			:initial-selection="initialSelection"
			@confirm="onConfirm"
		/>

		<FieldError v-if="isInvalid(props.field)" :errors="props.field.state.meta.errors" />
	</Field>
</template>
