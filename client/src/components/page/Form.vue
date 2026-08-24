<!--
SPDX-FileCopyrightText: 2026 OpenAdmin

SPDX-License-Identifier: AGPL-3.0-or-later
-->

<script setup lang="ts">
import type { AnyFieldApi } from "@tanstack/vue-form"
import { computed } from "vue"
import { Button } from "@/components/ui/button"
import { Checkbox } from "@/components/ui/checkbox"
import { Field, FieldError, FieldGroup, FieldLabel } from "@/components/ui/field"
import { Input } from "@/components/ui/input"
import { useForm } from "@/composables/openadmin-form"
import type { JsonSchema } from "@/schemas/json-schema"

const props = defineProps<{
	sectionId: string
	pageId: string
	formId: string
}>()

const { form, dataForm } = useForm({
	sectionId: props.sectionId,
	pageId: props.pageId,
	formId: props.formId,
})

const fieldsOf = (schema: JsonSchema | null | undefined) => {
	if (!schema?.properties) return []
	const required = new Set(schema.required ?? [])
	return Object.entries(schema.properties).map(([key, property]) => ({
		key,
		label: property.title ?? key,
		required: required.has(key),
		boolean: property.type === "boolean",
		numeric: property.type === "number" || property.type === "integer",
	}))
}

const fields = computed(() => [
	...fieldsOf(form.value?.query),
	...fieldsOf(form.value?.body),
	...fieldsOf(form.value?.form),
])

function isInvalid(field: AnyFieldApi) {
	return field.state.meta.isTouched && !field.state.meta.isValid
}
</script>

<template>
	<div v-if="form" class="mx-auto flex w-full max-w-2xl flex-col gap-8 p-6">
		<form v-if="fields.length" @submit.prevent="dataForm.handleSubmit">
			<FieldGroup class="grid grid-cols-[repeat(auto-fit,minmax(220px,1fr))] gap-x-8 gap-y-4">
				<dataForm.Field v-for="f in fields" :key="f.key" :name="f.key">
					<template #default="{ field }">
						<Field v-if="f.boolean" orientation="horizontal" :data-invalid="isInvalid(field)">
							<Checkbox
								:id="field.name"
								:name="field.name"
								:model-value="!!field.state.value"
								@update:model-value="(value) => field.handleChange(!!value)"
							/>
							<FieldLabel :for="field.name">{{ f.label }}</FieldLabel>
							<FieldError v-if="isInvalid(field)" :errors="field.state.meta.errors" />
						</Field>
						<Field v-else :data-invalid="isInvalid(field)">
							<FieldLabel :for="field.name">{{ f.label }}</FieldLabel>
							<Input
								:id="field.name"
								:name="field.name"
								:type="f.numeric ? 'number' : 'text'"
								:model-value="field.state.value as string | number | undefined"
								:aria-invalid="isInvalid(field)"
								@blur="field.handleBlur"
								@input="
									field.handleChange(
										f.numeric
											? Number(($event.target as HTMLInputElement).value)
											: ($event.target as HTMLInputElement).value,
									)
								"
							/>
							<FieldError v-if="isInvalid(field)" :errors="field.state.meta.errors" />
						</Field>
					</template>
				</dataForm.Field>
				<Field class="col-span-full">
					<Button type="submit">Submit</Button>
				</Field>
			</FieldGroup>
		</form>
	</div>
</template>
