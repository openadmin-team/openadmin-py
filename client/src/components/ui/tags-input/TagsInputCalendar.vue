<!--
SPDX-FileCopyrightText: 2026 OpenAdmin

SPDX-License-Identifier: AGPL-3.0-or-later
-->

<script setup lang="ts">
import {
	DateFormatter,
	getLocalTimeZone,
	isSameDay,
	parseAbsoluteToLocal,
	parseDate,
	Time,
	toCalendarDate,
	toCalendarDateTime,
	toZoned,
} from "@internationalized/date"
import { CalendarIcon } from "@lucide/vue"
import type { DateValue } from "reka-ui"
import { computed, ref } from "vue"
import { Button } from "@/components/ui/button"
import { Calendar } from "@/components/ui/calendar"
import { Input } from "@/components/ui/input"
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover"
import { TagsInput, TagsInputItem, TagsInputItemDelete, TagsInputItemText } from "."

const props = withDefaults(
	defineProps<{
		id?: string
		modelValue: string[]
		withTime?: boolean
		ariaInvalid?: boolean
	}>(),
	{ withTime: false },
)

const emit = defineEmits<{
	"update:modelValue": [value: string[]]
	blur: []
}>()

const open = ref(false)
const time = ref("00:00")

const dateFormatter = new DateFormatter("en-US", { dateStyle: "medium" })
const dateTimeFormatter = new DateFormatter("en-US", { dateStyle: "medium", timeStyle: "short" })

function toCalendarDay(value: string): DateValue {
	return props.withTime ? toCalendarDate(parseAbsoluteToLocal(value)) : parseDate(value)
}

function toAbsoluteWithTime(day: DateValue, timeValue: string): string {
	const [hour, minute] = timeValue.split(":").map(Number)
	return toZoned(
		toCalendarDateTime(day, new Time(hour, minute)),
		getLocalTimeZone(),
	).toAbsoluteString()
}

const calendarDays = computed(() => props.modelValue.map(toCalendarDay))

function formatValue(value: string) {
	return props.withTime
		? dateTimeFormatter.format(parseAbsoluteToLocal(value).toDate())
		: dateFormatter.format(parseDate(value).toDate(getLocalTimeZone()))
}

function onUpdateModelValue(value: unknown) {
	emit("update:modelValue", (value as string[] | undefined) ?? [])
}

function onCalendarUpdate(values: DateValue[] | undefined) {
	const next = values ?? []
	if (next.length > props.modelValue.length) {
		const added = next.find(
			(day) => !calendarDays.value.some((existing) => isSameDay(existing, day)),
		)
		if (!added) return
		const value = props.withTime ? toAbsoluteWithTime(added, time.value) : added.toString()
		emit("update:modelValue", [...props.modelValue, value])
		return
	}
	const removed = calendarDays.value.find(
		(day) => !next.some((existing) => isSameDay(existing, day)),
	)
	if (!removed) return
	emit(
		"update:modelValue",
		props.modelValue.filter((_, index) => !isSameDay(calendarDays.value[index], removed)),
	)
}
</script>

<template>
	<TagsInput
		:id="id"
		:model-value="modelValue"
		:aria-invalid="ariaInvalid"
		@update:model-value="onUpdateModelValue"
	>
		<TagsInputItem v-for="item in modelValue" :key="item" :value="item">
			<TagsInputItemText>{{ formatValue(item) }}</TagsInputItemText>
			<TagsInputItemDelete />
		</TagsInputItem>
		<Popover v-model:open="open">
			<PopoverTrigger as-child>
				<Button
					type="button"
					size="icon-sm"
					variant="ghost"
					class="order-last ml-auto self-start"
					@blur="emit('blur')"
				>
					<CalendarIcon class="size-3.5" />
				</Button>
			</PopoverTrigger>
			<PopoverContent class="w-auto rounded-md p-0">
				<!-- reka-ui types this emit as a single DateValue regardless of `multiple`; it's an array at runtime. -->
				<Calendar
					:model-value="calendarDays"
					multiple
					@update:model-value="(value) => onCalendarUpdate(value as unknown as DateValue[] | undefined)"
				/>
				<div v-if="withTime" class="border-t p-3">
					<Input v-model="time" type="time" />
				</div>
			</PopoverContent>
		</Popover>
	</TagsInput>
</template>
