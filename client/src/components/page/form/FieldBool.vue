<!--
SPDX-FileCopyrightText: 2026 OpenAdmin

SPDX-License-Identifier: AGPL-3.0-or-later
-->

<script setup lang="ts">
import type { AnyFieldApi } from "@tanstack/vue-form"
import { Checkbox } from "@/components/ui/checkbox"
import { Field, FieldError, FieldLabel } from "@/components/ui/field"
import { type FieldDef, isInvalid } from "./field"
import FieldLabelText from "./FieldLabelText.vue"

const props = defineProps<{
	field: AnyFieldApi
	def: FieldDef
}>()
</script>

<template>
	<Field :data-invalid="isInvalid(props.field)">
		<FieldLabel :for="props.field.name">
			<FieldLabelText :def="props.def" />
		</FieldLabel>
		<div class="flex h-9 items-center">
			<Checkbox
				:id="props.field.name"
				:name="props.field.name"
				:model-value="!!props.field.state.value"
				@update:model-value="(value) => props.field.handleChange(!!value)"
			/>
		</div>
		<FieldError v-if="isInvalid(props.field)" :errors="props.field.state.meta.errors" />
	</Field>
</template>
