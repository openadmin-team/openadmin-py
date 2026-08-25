<!--
SPDX-FileCopyrightText: 2026 OpenAdmin

SPDX-License-Identifier: AGPL-3.0-or-later
-->

<script setup lang="ts">
import type { AnyFieldApi } from "@tanstack/vue-form"
import { Field, FieldError, FieldLabel } from "@/components/ui/field"
import {
	Select,
	SelectContent,
	SelectGroup,
	SelectItem,
	SelectTrigger,
	SelectValue,
} from "@/components/ui/select"
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
		<Select
			:model-value="props.field.state.value as string | undefined"
			@update:model-value="(value) => props.field.handleChange(value)"
		>
			<SelectTrigger
				:id="props.field.name"
				class="w-full"
				:aria-invalid="isInvalid(props.field)"
				@blur="props.field.handleBlur"
			>
				<SelectValue placeholder="Select an option" />
			</SelectTrigger>
			<SelectContent>
				<SelectGroup>
					<SelectItem v-for="option in props.def.options ?? []" :key="option" :value="option">
						{{ option }}
					</SelectItem>
				</SelectGroup>
			</SelectContent>
		</Select>
		<FieldError v-if="isInvalid(props.field)" :errors="props.field.state.meta.errors" />
	</Field>
</template>
