<!--
SPDX-FileCopyrightText: 2026 OpenAdmin

SPDX-License-Identifier: AGPL-3.0-or-later
-->

<script setup lang="ts">
import {
	DateFormatter,
	getLocalTimeZone,
	parseAbsoluteToLocal,
	parseDate,
	Time,
	toCalendarDateTime,
	today,
	toZoned,
} from "@internationalized/date"
import { CalendarIcon } from "@lucide/vue"
import type { AnyFieldApi } from "@tanstack/vue-form"
import type { DateValue } from "reka-ui"
import { computed } from "vue"
import { Button } from "@/components/ui/button"
import { Calendar } from "@/components/ui/calendar"
import { Checkbox } from "@/components/ui/checkbox"
import { Field, FieldError, FieldGroup, FieldLabel } from "@/components/ui/field"
import { Input } from "@/components/ui/input"
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover"
import {
	TagsInput,
	TagsInputInput,
	TagsInputItem,
	TagsInputItemDelete,
	TagsInputItemText,
} from "@/components/ui/tags-input"
import { useForm } from "@/composables/openadmin-form"
import type { JsonSchema } from "@/schemas/json-schema"

type ArrayItemKind = "integer" | "number" | "boolean" | "date" | "date-time" | "string"

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

const arrayItemKind = (items: JsonSchema["items"]): ArrayItemKind => {
	const item = Array.isArray(items) ? items[0] : items
	if (item?.type === "integer") return "integer"
	if (item?.type === "number") return "number"
	if (item?.type === "boolean") return "boolean"
	if (item?.type === "string" && item.format === "date") return "date"
	if (item?.type === "string" && item.format === "date-time") return "date-time"
	return "string"
}

const fieldsOf = (schema: JsonSchema | null | undefined) => {
	if (!schema?.properties) return []
	const required = new Set(schema.required ?? [])
	return Object.entries(schema.properties).map(([key, property]) => ({
		key,
		label: property.title ?? key,
		required: required.has(key),
		boolean: property.type === "boolean",
		numeric: property.type === "number" || property.type === "integer",
		date: property.type === "string" && property.format === "date",
		datetime: property.type === "string" && property.format === "date-time",
		array: property.type === "array",
		itemKind: property.type === "array" ? arrayItemKind(property.items) : undefined,
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

const dateFormatter = new DateFormatter("en-US", { dateStyle: "long" })
const dateTimeFormatter = new DateFormatter("en-US", { dateStyle: "long", timeStyle: "short" })

function toDateValue(value: unknown) {
	return typeof value === "string" && value ? parseDate(value) : undefined
}

function toDateTimeValue(value: unknown) {
	return typeof value === "string" && value ? parseAbsoluteToLocal(value) : undefined
}

function formatDate(value: unknown) {
	const date = toDateValue(value)
	return date ? dateFormatter.format(date.toDate(getLocalTimeZone())) : undefined
}

function formatDateTime(value: unknown) {
	const date = toDateTimeValue(value)
	return date ? dateTimeFormatter.format(date.toDate()) : undefined
}

function onDateTimeCalendarChange(field: AnyFieldApi, value: DateValue | undefined) {
	if (!value) {
		field.handleChange(undefined)
		return
	}
	const existing = toDateTimeValue(field.state.value)
	const time = existing ? new Time(existing.hour, existing.minute, existing.second) : undefined
	const dateTime = toCalendarDateTime(value, time)
	field.handleChange(toZoned(dateTime, getLocalTimeZone()).toAbsoluteString())
}

function timeOfDateTime(value: unknown) {
	const date = toDateTimeValue(value)
	if (!date) return ""
	return `${String(date.hour).padStart(2, "0")}:${String(date.minute).padStart(2, "0")}`
}

function onTimeInput(field: AnyFieldApi, event: Event) {
	const raw = (event.target as HTMLInputElement).value
	if (!raw) return
	const [hour, minute] = raw.split(":").map(Number)
	const base =
		toDateTimeValue(field.state.value) ?? toZoned(today(getLocalTimeZone()), getLocalTimeZone())
	field.handleChange(base.set({ hour, minute, second: 0 }).toAbsoluteString())
}

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

function arrayValues(field: AnyFieldApi) {
	return ((field.state.value as unknown[] | undefined) ?? []).map(formatArrayItem)
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
	<div v-if="form" class="flex min-h-full items-center justify-center p-6">
		<form v-if="fields.length" class="w-full max-w-5xl" @submit.prevent="dataForm.handleSubmit">
			<FieldGroup class="grid grid-cols-[repeat(auto-fit,minmax(350px,1fr))] gap-x-8 gap-y-4">
				<dataForm.Field v-for="f in fields" :key="f.key" :name="f.key">
					<template #default="{ field }">
						<Field v-if="f.boolean" :data-invalid="isInvalid(field)">
							<FieldLabel :for="field.name">
								{{ f.label }}<span v-if="f.required" class="text-destructive"> *</span>
							</FieldLabel>
							<div class="flex h-9 items-center">
								<Checkbox
									:id="field.name"
									:name="field.name"
									:model-value="!!field.state.value"
									@update:model-value="(value) => field.handleChange(!!value)"
								/>
							</div>
							<FieldError v-if="isInvalid(field)" :errors="field.state.meta.errors" />
						</Field>
						<Field v-else-if="f.date" :data-invalid="isInvalid(field)">
							<FieldLabel :for="field.name">
								{{ f.label }}<span v-if="f.required" class="text-destructive"> *</span>
							</FieldLabel>
							<Popover>
								<PopoverTrigger as-child>
									<Button
										:id="field.name"
										type="button"
										variant="outline"
										class="w-full justify-start font-normal"
										:aria-invalid="isInvalid(field)"
										@blur="field.handleBlur"
									>
										<CalendarIcon data-icon="inline-start" />
										{{ formatDate(field.state.value) ?? "Pick a date" }}
									</Button>
								</PopoverTrigger>
								<PopoverContent class="w-auto p-0">
									<Calendar
										:model-value="toDateValue(field.state.value)"
										@update:model-value="(value) => field.handleChange(value ? value.toString() : undefined)"
									/>
								</PopoverContent>
							</Popover>
							<FieldError v-if="isInvalid(field)" :errors="field.state.meta.errors" />
						</Field>
						<Field v-else-if="f.datetime" :data-invalid="isInvalid(field)">
							<FieldLabel :for="field.name">
								{{ f.label }}<span v-if="f.required" class="text-destructive"> *</span>
							</FieldLabel>
							<Popover>
								<PopoverTrigger as-child>
									<Button
										:id="field.name"
										type="button"
										variant="outline"
										class="w-full justify-start font-normal"
										:aria-invalid="isInvalid(field)"
										@blur="field.handleBlur"
									>
										<CalendarIcon data-icon="inline-start" />
										{{ formatDateTime(field.state.value) ?? "Pick a date and time" }}
									</Button>
								</PopoverTrigger>
								<PopoverContent class="w-auto p-0">
									<Calendar
										:model-value="toDateTimeValue(field.state.value)"
										@update:model-value="(value) => onDateTimeCalendarChange(field, value)"
									/>
									<div class="border-t p-3">
										<Input
											type="time"
											:model-value="timeOfDateTime(field.state.value)"
											@input="onTimeInput(field, $event)"
										/>
									</div>
								</PopoverContent>
							</Popover>
							<FieldError v-if="isInvalid(field)" :errors="field.state.meta.errors" />
						</Field>
						<Field v-else-if="f.array" :data-invalid="isInvalid(field)">
							<FieldLabel :for="field.name">
								{{ f.label }}<span v-if="f.required" class="text-destructive"> *</span>
							</FieldLabel>
							<TagsInput
								:id="field.name"
								:model-value="arrayValues(field)"
								:aria-invalid="isInvalid(field)"
								@update:model-value="
									(values) =>
										field.handleChange(values.map((value) => parseArrayItem(f.itemKind, formatArrayItem(value))))
								"
							>
								<TagsInputItem
									v-for="(value, index) in arrayValues(field)"
									:key="index"
									:value="value"
								>
									<TagsInputItemText />
									<TagsInputItemDelete />
								</TagsInputItem>
								<TagsInputInput
									:placeholder="arrayPlaceholder(f.itemKind)"
									@blur="field.handleBlur"
								/>
							</TagsInput>
							<FieldError v-if="isInvalid(field)" :errors="field.state.meta.errors" />
						</Field>
						<Field v-else :data-invalid="isInvalid(field)">
							<FieldLabel :for="field.name">
								{{ f.label }}<span v-if="f.required" class="text-destructive"> *</span>
							</FieldLabel>
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
				<Field orientation="horizontal" class="col-span-full mt-48 justify-end gap-3">
					<Button size="lg" type="button" variant="outline" @click="dataForm.reset()">Clear</Button>
					<Button size="lg" type="submit">Submit</Button>
				</Field>
			</FieldGroup>
		</form>
	</div>
</template>
