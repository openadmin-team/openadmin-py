<!--
SPDX-FileCopyrightText: 2026 OpenAdmin

SPDX-License-Identifier: AGPL-3.0-or-later
-->

<script setup lang="ts">
import { computed } from "vue"
import { Button } from "@/components/ui/button"
import { Field, FieldGroup } from "@/components/ui/field"
import { useForm } from "@/composables/openadmin-form"
import type { FieldConfig } from "@/schemas/form"
import type { JsonSchema } from "@/schemas/json-schema"
import type { ArrayItemKind, FieldDef } from "./field"
import FieldArray from "./FieldArray.vue"
import FieldBool from "./FieldBool.vue"
import FieldDate from "./FieldDate.vue"
import FieldDateTime from "./FieldDateTime.vue"
import FieldFile from "./FieldFile.vue"
import FieldFileArray from "./FieldFileArray.vue"
import FieldNumeric from "./FieldNumeric.vue"
import FieldSelect from "./FieldSelect.vue"
import FieldString from "./FieldString.vue"

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

function resolveRef(schema: JsonSchema | undefined, root: JsonSchema): JsonSchema | undefined {
	if (!schema?.$ref) return schema
	const key = schema.$ref.split("/").pop()
	const target = key ? (root.$defs?.[key] ?? root.definitions?.[key]) : undefined
	return target ? resolveRef(target, root) : schema
}

function arrayItemKind(items: JsonSchema["items"], root: JsonSchema): ArrayItemKind {
	const item = resolveRef(Array.isArray(items) ? items[0] : items, root)
	if (item?.enum) return "enum"
	if (item?.type === "integer") return "integer"
	if (item?.type === "number") return "number"
	if (item?.type === "boolean") return "boolean"
	if (item?.type === "string" && item.format === "date") return "date"
	if (item?.type === "string" && item.format === "date-time") return "date-time"
	return "string"
}

function fieldsOf(
	schema: JsonSchema | null | undefined,
	source: "query" | "body" | "form",
	fieldConfigs: Record<string, FieldConfig> | null | undefined,
): FieldDef[] {
	if (!schema?.properties) return []
	const required = new Set(schema.required ?? [])
	return Object.entries(schema.properties).map(([key, rawProperty]) => {
		const property = resolveRef(rawProperty, schema) ?? rawProperty
		const array = source !== "form" && property.type === "array"
		const itemSchema = array
			? resolveRef(Array.isArray(property.items) ? property.items[0] : property.items, schema)
			: undefined
		return {
			key,
			label: rawProperty.title ?? key,
			required: required.has(key),
			icon: fieldConfigs?.[key]?.icon,
			color: fieldConfigs?.[key]?.color,
			boolean: property.type === "boolean",
			numeric: property.type === "number" || property.type === "integer",
			integer: property.type === "integer",
			date: property.type === "string" && property.format === "date",
			datetime: property.type === "string" && property.format === "date-time",
			file: source === "form" && property.type === "string",
			fileArray: source === "form" && property.type === "array",
			array,
			itemKind: array ? arrayItemKind(property.items, schema) : undefined,
			select: !array && Array.isArray(property.enum),
			options: !array && Array.isArray(property.enum) ? property.enum.map(String) : undefined,
			itemOptions: itemSchema?.enum ? itemSchema.enum.map(String) : undefined,
		}
	})
}

const fields = computed<FieldDef[]>(() => [
	...fieldsOf(form.value?.query, "query", form.value?.fields),
	...fieldsOf(form.value?.body, "body", form.value?.fields),
	...fieldsOf(form.value?.form, "form", form.value?.fields),
])
</script>

<template>
	<div v-if="form" class="flex min-h-full items-center justify-center p-6">
		<form v-if="fields.length" class="w-full max-w-xl" @submit.prevent="dataForm.handleSubmit">
			<FieldGroup class="grid grid-cols-1 gap-y-4">
				<dataForm.Field v-for="f in fields" :key="f.key" :name="f.key">
					<template #default="{ field }">
						<FieldBool v-if="f.boolean" :field="field" :def="f" />
						<FieldDate v-else-if="f.date" :field="field" :def="f" />
						<FieldDateTime v-else-if="f.datetime" :field="field" :def="f" />
						<FieldArray v-else-if="f.array" :field="field" :def="f" />
						<FieldFile v-else-if="f.file" :field="field" :def="f" />
						<FieldFileArray v-else-if="f.fileArray" :field="field" :def="f" />
						<FieldSelect v-else-if="f.select" :field="field" :def="f" />
						<FieldNumeric v-else-if="f.numeric" :field="field" :def="f" />
						<FieldString v-else :field="field" :def="f" />
					</template>
				</dataForm.Field>
				<Field orientation="horizontal" class="col-span-full mt-12 justify-end gap-3">
					<Button size="lg" type="button" variant="outline" @click="dataForm.reset()">Clear</Button>
					<Button size="lg" type="submit">Submit</Button>
				</Field>
			</FieldGroup>
		</form>
	</div>
</template>
