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
import { CalendarIcon, FileIcon, PaperclipIcon, XIcon } from "@lucide/vue"
import type { AnyFieldApi } from "@tanstack/vue-form"
import type { DateValue } from "reka-ui"
import { computed } from "vue"
import {
	Attachment,
	AttachmentAction,
	AttachmentActions,
	AttachmentContent,
	AttachmentDescription,
	AttachmentGroup,
	AttachmentMedia,
	AttachmentTitle,
	AttachmentTrigger,
} from "@/components/ui/attachment"
import { Button } from "@/components/ui/button"
import { Calendar } from "@/components/ui/calendar"
import { Checkbox } from "@/components/ui/checkbox"
import { Field, FieldError, FieldGroup, FieldLabel } from "@/components/ui/field"
import { Input } from "@/components/ui/input"
import {
	NumberField,
	NumberFieldContent,
	NumberFieldDecrement,
	NumberFieldIncrement,
	NumberFieldInput,
} from "@/components/ui/number-field"
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover"
import {
	Select,
	SelectContent,
	SelectGroup,
	SelectItem,
	SelectTrigger,
	SelectValue,
} from "@/components/ui/select"
import {
	TagsInput,
	TagsInputCalendar,
	TagsInputInput,
	TagsInputItem,
	TagsInputItemDelete,
	TagsInputItemText,
	TagsInputSuggestions,
} from "@/components/ui/tags-input"
import { useForm } from "@/composables/openadmin-form"
import type { JsonSchema } from "@/schemas/json-schema"

type ArrayItemKind = "integer" | "number" | "boolean" | "date" | "date-time" | "string" | "enum"

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

const arrayItemKind = (items: JsonSchema["items"], root: JsonSchema): ArrayItemKind => {
	const item = resolveRef(Array.isArray(items) ? items[0] : items, root)
	if (item?.enum) return "enum"
	if (item?.type === "integer") return "integer"
	if (item?.type === "number") return "number"
	if (item?.type === "boolean") return "boolean"
	if (item?.type === "string" && item.format === "date") return "date"
	if (item?.type === "string" && item.format === "date-time") return "date-time"
	return "string"
}

const fieldsOf = (schema: JsonSchema | null | undefined, source: "query" | "body" | "form") => {
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

const fields = computed(() => [
	...fieldsOf(form.value?.query, "query"),
	...fieldsOf(form.value?.body, "body"),
	...fieldsOf(form.value?.form, "form"),
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

function formatFileSize(bytes: number) {
	if (bytes < 1024) return `${bytes} B`
	if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
	return `${(bytes / (1024 * 1024)).toFixed(1)} MB`
}

function isImageFile(file: File) {
	return file.type.startsWith("image/")
}

const objectUrls = new WeakMap<File, string>()

function objectUrlFor(file: File) {
	let url = objectUrls.get(file)
	if (!url) {
		url = URL.createObjectURL(file)
		objectUrls.set(file, url)
	}
	return url
}

function onFileChange(field: AnyFieldApi, event: Event) {
	const input = event.target as HTMLInputElement
	const file = input.files?.[0]
	if (file) field.handleChange(file)
	input.value = ""
}

function onFilesChange(field: AnyFieldApi, event: Event) {
	const input = event.target as HTMLInputElement
	const added = Array.from(input.files ?? [])
	if (added.length) {
		const existing = (field.state.value as File[] | undefined) ?? []
		field.handleChange([...existing, ...added])
	}
	input.value = ""
}

function removeFileAt(field: AnyFieldApi, index: number) {
	const existing = (field.state.value as File[] | undefined) ?? []
	field.handleChange(existing.filter((_, i) => i !== index))
}
</script>

<template>
	<div v-if="form" class="flex min-h-full items-center justify-center p-6">
		<form v-if="fields.length" class="w-full max-w-xl" @submit.prevent="dataForm.handleSubmit">
			<FieldGroup class="grid grid-cols-1 gap-y-4">
				<dataForm.Field v-for="f in fields" :key="f.key" :name="f.key">
					<template #default="{ field }">
						<Field v-if="f.boolean" :data-invalid="isInvalid(field)">
							<div class="flex items-center gap-2">
								<Checkbox
									:id="field.name"
									:name="field.name"
									:model-value="!!field.state.value"
									@update:model-value="(value) => field.handleChange(!!value)"
								/>
								<FieldLabel :for="field.name">
									{{ f.label }}<span v-if="f.required" class="text-destructive"> *</span>
								</FieldLabel>
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
							<TagsInputSuggestions
								v-if="f.itemKind === 'enum'"
								:id="field.name"
								:options="f.itemOptions ?? []"
								:model-value="(field.state.value as string[] | undefined) ?? []"
								:aria-invalid="isInvalid(field)"
								@update:model-value="(values) => field.handleChange(values)"
								@blur="field.handleBlur"
							/>
							<TagsInputCalendar
								v-else-if="f.itemKind === 'date' || f.itemKind === 'date-time'"
								:id="field.name"
								:model-value="(field.state.value as string[] | undefined) ?? []"
								:with-time="f.itemKind === 'date-time'"
								:aria-invalid="isInvalid(field)"
								@update:model-value="(values) => field.handleChange(values)"
								@blur="field.handleBlur"
							/>
							<TagsInput
								v-else
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
						<Field v-else-if="f.file" :data-invalid="isInvalid(field)">
							<FieldLabel :for="field.name">
								{{ f.label }}<span v-if="f.required" class="text-destructive"> *</span>
							</FieldLabel>
							<input
								:id="field.name"
								type="file"
								class="hidden"
								:aria-invalid="isInvalid(field)"
								@change="(event) => onFileChange(field, event)"
								@blur="field.handleBlur"
							>
							<Attachment :state="field.state.value ? 'done' : 'idle'">
								<AttachmentMedia
									v-if="field.state.value && isImageFile(field.state.value as File)"
									variant="image"
								>
									<img
										:src="objectUrlFor(field.state.value as File)"
										:alt="(field.state.value as File).name"
									>
								</AttachmentMedia>
								<AttachmentMedia v-else>
									<PaperclipIcon v-if="!field.state.value" />
									<FileIcon v-else />
								</AttachmentMedia>
								<AttachmentContent>
									<AttachmentTitle>
										{{ (field.state.value as File | undefined)?.name ?? "Choose a file" }}
									</AttachmentTitle>
									<AttachmentDescription v-if="field.state.value">
										{{ formatFileSize((field.state.value as File).size) }}
									</AttachmentDescription>
								</AttachmentContent>
								<AttachmentActions v-if="field.state.value">
									<AttachmentAction
										type="button"
										aria-label="Remove file"
										@click="field.handleChange(undefined)"
									>
										<XIcon />
									</AttachmentAction>
								</AttachmentActions>
								<AttachmentTrigger as="label" :for="field.name" />
							</Attachment>
							<FieldError v-if="isInvalid(field)" :errors="field.state.meta.errors" />
						</Field>
						<Field v-else-if="f.fileArray" :data-invalid="isInvalid(field)">
							<FieldLabel :for="field.name">
								{{ f.label }}<span v-if="f.required" class="text-destructive"> *</span>
							</FieldLabel>
							<input
								:id="field.name"
								type="file"
								multiple
								class="hidden"
								:aria-invalid="isInvalid(field)"
								@change="(event) => onFilesChange(field, event)"
								@blur="field.handleBlur"
							>
							<AttachmentGroup>
								<Attachment
									v-for="(file, index) in (field.state.value as File[] | undefined) ?? []"
									:key="`${index}-${file.name}`"
									state="done"
								>
									<AttachmentMedia v-if="isImageFile(file)" variant="image">
										<img :src="objectUrlFor(file)" :alt="file.name">
									</AttachmentMedia>
									<AttachmentMedia v-else>
										<FileIcon />
									</AttachmentMedia>
									<AttachmentContent>
										<AttachmentTitle>{{ file.name }}</AttachmentTitle>
										<AttachmentDescription>{{ formatFileSize(file.size) }}</AttachmentDescription>
									</AttachmentContent>
									<AttachmentActions>
										<AttachmentAction
											type="button"
											aria-label="Remove file"
											@click="removeFileAt(field, index)"
										>
											<XIcon />
										</AttachmentAction>
									</AttachmentActions>
								</Attachment>
								<Attachment state="idle">
									<AttachmentMedia>
										<PaperclipIcon />
									</AttachmentMedia>
									<AttachmentContent>
										<AttachmentTitle>Add files</AttachmentTitle>
									</AttachmentContent>
									<AttachmentTrigger as="label" :for="field.name" />
								</Attachment>
							</AttachmentGroup>
							<FieldError v-if="isInvalid(field)" :errors="field.state.meta.errors" />
						</Field>
						<Field v-else-if="f.select" :data-invalid="isInvalid(field)">
							<FieldLabel :for="field.name">
								{{ f.label }}<span v-if="f.required" class="text-destructive"> *</span>
							</FieldLabel>
							<Select
								:model-value="field.state.value as string | undefined"
								@update:model-value="(value) => field.handleChange(value)"
							>
								<SelectTrigger
									:id="field.name"
									class="w-full"
									:aria-invalid="isInvalid(field)"
									@blur="field.handleBlur"
								>
									<SelectValue placeholder="Select an option" />
								</SelectTrigger>
								<SelectContent>
									<SelectGroup>
										<SelectItem v-for="option in f.options ?? []" :key="option" :value="option">
											{{ option }}
										</SelectItem>
									</SelectGroup>
								</SelectContent>
							</Select>
							<FieldError v-if="isInvalid(field)" :errors="field.state.meta.errors" />
						</Field>
						<Field v-else-if="f.numeric" :data-invalid="isInvalid(field)">
							<FieldLabel :for="field.name">
								{{ f.label }}<span v-if="f.required" class="text-destructive"> *</span>
							</FieldLabel>
							<NumberField
								:id="field.name"
								:name="field.name"
								:step-snapping="f.integer"
								:model-value="field.state.value as number | undefined"
								@update:model-value="(value) => field.handleChange(value)"
							>
								<NumberFieldContent>
									<NumberFieldDecrement />
									<NumberFieldInput :aria-invalid="isInvalid(field)" @blur="field.handleBlur" />
									<NumberFieldIncrement />
								</NumberFieldContent>
							</NumberField>
							<FieldError v-if="isInvalid(field)" :errors="field.state.meta.errors" />
						</Field>
						<Field v-else :data-invalid="isInvalid(field)">
							<FieldLabel :for="field.name">
								{{ f.label }}<span v-if="f.required" class="text-destructive"> *</span>
							</FieldLabel>
							<Input
								:id="field.name"
								:name="field.name"
								type="text"
								:model-value="field.state.value as string | undefined"
								:aria-invalid="isInvalid(field)"
								@blur="field.handleBlur"
								@input="field.handleChange(($event.target as HTMLInputElement).value)"
							/>
							<FieldError v-if="isInvalid(field)" :errors="field.state.meta.errors" />
						</Field>
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
