<!--
SPDX-FileCopyrightText: 2026 OpenAdmin

SPDX-License-Identifier: AGPL-3.0-or-later
-->

<script setup lang="ts">
import {
	DateFormatter,
	getLocalTimeZone,
	parseAbsoluteToLocal,
	Time,
	toCalendarDateTime,
	today,
	toZoned,
} from "@internationalized/date"
import { CalendarIcon } from "@lucide/vue"
import type { AnyFieldApi } from "@tanstack/vue-form"
import type { DateValue } from "reka-ui"
import { Button } from "@/components/ui/button"
import { Calendar } from "@/components/ui/calendar"
import { Field, FieldError, FieldLabel } from "@/components/ui/field"
import { Input } from "@/components/ui/input"
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover"
import { type FieldDef, isInvalid } from "./field"

const props = defineProps<{
	field: AnyFieldApi
	def: FieldDef
}>()

const dateTimeFormatter = new DateFormatter("en-US", { dateStyle: "long", timeStyle: "short" })

function toDateTimeValue(value: unknown) {
	return typeof value === "string" && value ? parseAbsoluteToLocal(value) : undefined
}

function formatDateTime(value: unknown) {
	const date = toDateTimeValue(value)
	return date ? dateTimeFormatter.format(date.toDate()) : undefined
}

function onCalendarChange(value: DateValue | undefined) {
	if (!value) {
		props.field.handleChange(undefined)
		return
	}
	const existing = toDateTimeValue(props.field.state.value)
	const time = existing ? new Time(existing.hour, existing.minute, existing.second) : undefined
	const dateTime = toCalendarDateTime(value, time)
	props.field.handleChange(toZoned(dateTime, getLocalTimeZone()).toAbsoluteString())
}

function timeOfDateTime(value: unknown) {
	const date = toDateTimeValue(value)
	if (!date) return ""
	return `${String(date.hour).padStart(2, "0")}:${String(date.minute).padStart(2, "0")}`
}

function onTimeInput(event: Event) {
	const raw = (event.target as HTMLInputElement).value
	if (!raw) return
	const [hour, minute] = raw.split(":").map(Number)
	const base =
		toDateTimeValue(props.field.state.value) ??
		toZoned(today(getLocalTimeZone()), getLocalTimeZone())
	props.field.handleChange(base.set({ hour, minute, second: 0 }).toAbsoluteString())
}
</script>

<template>
	<Field :data-invalid="isInvalid(props.field)">
		<FieldLabel :for="props.field.name">
			{{ props.def.label }}<span v-if="props.def.required" class="text-destructive"> *</span>
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
					{{ formatDateTime(props.field.state.value) ?? "Pick a date and time" }}
				</Button>
			</PopoverTrigger>
			<PopoverContent class="w-auto p-0">
				<Calendar
					:model-value="toDateTimeValue(props.field.state.value)"
					@update:model-value="onCalendarChange"
				/>
				<div class="border-t p-3">
					<Input
						type="time"
						:model-value="timeOfDateTime(props.field.state.value)"
						@input="onTimeInput"
					/>
				</div>
			</PopoverContent>
		</Popover>
		<FieldError v-if="isInvalid(props.field)" :errors="props.field.state.meta.errors" />
	</Field>
</template>
