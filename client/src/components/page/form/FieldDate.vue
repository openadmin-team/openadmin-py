<!--
SPDX-FileCopyrightText: 2026 OpenAdmin

SPDX-License-Identifier: AGPL-3.0-or-later
-->

<script setup lang="ts">
import { DateFormatter, getLocalTimeZone, parseDate } from "@internationalized/date"
import { CalendarIcon } from "@lucide/vue"
import type { AnyFieldApi } from "@tanstack/vue-form"
import { Button } from "@/components/ui/button"
import { Calendar } from "@/components/ui/calendar"
import { Field, FieldError, FieldLabel } from "@/components/ui/field"
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover"
import { type FieldDef, isInvalid } from "./field"
import FieldLabelText from "./FieldLabelText.vue"

const props = defineProps<{
	field: AnyFieldApi
	def: FieldDef
}>()

const dateFormatter = new DateFormatter("en-US", { dateStyle: "long" })

function toDateValue(value: unknown) {
	return typeof value === "string" && value ? parseDate(value) : undefined
}

function formatDate(value: unknown) {
	const date = toDateValue(value)
	return date ? dateFormatter.format(date.toDate(getLocalTimeZone())) : undefined
}
</script>

<template>
	<Field :data-invalid="isInvalid(props.field)">
		<FieldLabel :for="props.field.name">
			<FieldLabelText :def="props.def" />
		</FieldLabel>
		<Popover>
			<PopoverTrigger as-child>
				<Button
					:id="props.field.name"
					type="button"
					variant="outline"
					class="w-full justify-start font-normal"
					:aria-invalid="isInvalid(props.field)"
					@blur="props.field.handleBlur"
				>
					<CalendarIcon data-icon="inline-start" />
					{{ formatDate(props.field.state.value) ?? "Pick a date" }}
				</Button>
			</PopoverTrigger>
			<PopoverContent class="w-auto p-0">
				<Calendar
					:model-value="toDateValue(props.field.state.value)"
					@update:model-value="(value) => props.field.handleChange(value ? value.toString() : undefined)"
				/>
			</PopoverContent>
		</Popover>
		<FieldError v-if="isInvalid(props.field)" :errors="props.field.state.meta.errors" />
	</Field>
</template>
