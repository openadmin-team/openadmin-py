<!--
SPDX-FileCopyrightText: 2026 OpenAdmin

SPDX-License-Identifier: AGPL-3.0-or-later
-->

<script setup lang="ts">
import type { AnyFieldApi } from "@tanstack/vue-form"
import { Field, FieldError, FieldLabel } from "@/components/ui/field"
import {
	NumberField,
	NumberFieldContent,
	NumberFieldDecrement,
	NumberFieldIncrement,
	NumberFieldInput,
} from "@/components/ui/number-field"
import { type FieldDef, isInvalid } from "./field"

const props = defineProps<{
	field: AnyFieldApi
	def: FieldDef
}>()
</script>

<template>
	<Field :data-invalid="isInvalid(props.field)">
		<FieldLabel :for="props.field.name">
			{{ props.def.label }}<span v-if="props.def.required" class="text-destructive"> *</span>
		</FieldLabel>
		<NumberField
			:id="props.field.name"
			:name="props.field.name"
			:step-snapping="props.def.integer"
			:model-value="props.field.state.value as number | undefined"
			@update:model-value="(value) => props.field.handleChange(value)"
		>
			<NumberFieldContent>
				<NumberFieldDecrement />
				<NumberFieldInput :aria-invalid="isInvalid(props.field)" @blur="props.field.handleBlur" />
				<NumberFieldIncrement />
			</NumberFieldContent>
		</NumberField>
		<FieldError v-if="isInvalid(props.field)" :errors="props.field.state.meta.errors" />
	</Field>
</template>
