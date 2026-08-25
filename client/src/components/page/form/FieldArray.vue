<!--
SPDX-FileCopyrightText: 2026 OpenAdmin

SPDX-License-Identifier: AGPL-3.0-or-later
-->

<script setup lang="ts">
import type { AnyFieldApi } from "@tanstack/vue-form"
import { Field, FieldError, FieldLabel } from "@/components/ui/field"
import {
	TagsInput,
	TagsInputCalendar,
	TagsInputInput,
	TagsInputItem,
	TagsInputItemDelete,
	TagsInputItemText,
	TagsInputSuggestions,
} from "@/components/ui/tags-input"
import { type ArrayItemKind, type FieldDef, isInvalid } from "./field"

const props = defineProps<{
	field: AnyFieldApi
	def: FieldDef
}>()

function formatArrayItem(value: unknown) {
	return value === null || value === undefined ? "" : String(value)
}

function parseArrayItem(kind: ArrayItemKind | undefined, raw: string) {
	const text = raw.trim()
	if (kind === "integer") {
		const value = Number.parseInt(text, 10)
		return Number.isNaN(value) ? text : value
	}
	if (kind === "number") {
		const value = Number.parseFloat(text)
		return Number.isNaN(value) ? text : value
	}
	if (kind === "boolean") {
		if (text.toLowerCase() === "true") return true
		if (text.toLowerCase() === "false") return false
		return text
	}
	return text
}

function arrayValues() {
	return ((props.field.state.value as unknown[] | undefined) ?? []).map(formatArrayItem)
}

function arrayPlaceholder(kind: ArrayItemKind | undefined) {
	if (kind === "integer" || kind === "number") return "Add a number and press Enter..."
	if (kind === "boolean") return "Add true or false and press Enter..."
	if (kind === "date") return "Add a date (YYYY-MM-DD) and press Enter..."
	if (kind === "date-time") return "Add a date-time (YYYY-MM-DDTHH:mm:ss) and press Enter..."
	return "Add a value and press Enter..."
}
</script>

<template>
	<Field :data-invalid="isInvalid(props.field)">
		<FieldLabel :for="props.field.name">
			{{ props.def.label }}<span v-if="props.def.required" class="text-destructive"> *</span>
		</FieldLabel>
		<TagsInputSuggestions
			v-if="props.def.itemKind === 'enum'"
			:id="props.field.name"
			:options="props.def.itemOptions ?? []"
			:model-value="(props.field.state.value as string[] | undefined) ?? []"
			:aria-invalid="isInvalid(props.field)"
			@update:model-value="(values) => props.field.handleChange(values)"
			@blur="props.field.handleBlur"
		/>
		<TagsInputCalendar
			v-else-if="props.def.itemKind === 'date' || props.def.itemKind === 'date-time'"
			:id="props.field.name"
			:model-value="(props.field.state.value as string[] | undefined) ?? []"
			:with-time="props.def.itemKind === 'date-time'"
			:aria-invalid="isInvalid(props.field)"
			@update:model-value="(values) => props.field.handleChange(values)"
			@blur="props.field.handleBlur"
		/>
		<TagsInput
			v-else
			:id="props.field.name"
			:model-value="arrayValues()"
			:aria-invalid="isInvalid(props.field)"
			@update:model-value="
				(values) =>
					props.field.handleChange(
						values.map((value) => parseArrayItem(props.def.itemKind, formatArrayItem(value))),
					)
			"
		>
			<TagsInputItem v-for="(value, index) in arrayValues()" :key="index" :value="value">
				<TagsInputItemText />
				<TagsInputItemDelete />
			</TagsInputItem>
			<TagsInputInput
				:placeholder="arrayPlaceholder(props.def.itemKind)"
				@blur="props.field.handleBlur"
			/>
		</TagsInput>
		<FieldError v-if="isInvalid(props.field)" :errors="props.field.state.meta.errors" />
	</Field>
</template>
