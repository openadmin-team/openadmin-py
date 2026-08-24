<!--
SPDX-FileCopyrightText: 2026 OpenAdmin

SPDX-License-Identifier: AGPL-3.0-or-later
-->

<script setup lang="ts">
import { ChevronDown } from "@lucide/vue"
import { ListboxContent, ListboxFilter, ListboxItem, ListboxRoot, useFilter } from "reka-ui"
import { computed, ref } from "vue"
import { Button } from "@/components/ui/button"
import { Popover, PopoverAnchor, PopoverContent, PopoverTrigger } from "@/components/ui/popover"
import { TagsInput, TagsInputInput, TagsInputItem, TagsInputItemDelete, TagsInputItemText } from "."

const props = withDefaults(
	defineProps<{
		id?: string
		options: string[]
		modelValue: string[]
		placeholder?: string
		ariaInvalid?: boolean
	}>(),
	{ placeholder: "Add an option..." },
)

const emit = defineEmits<{
	"update:modelValue": [value: string[]]
	blur: []
}>()

const open = ref(false)
const searchTerm = ref("")
const { contains } = useFilter({ sensitivity: "base" })

const filteredOptions = computed(() =>
	props.options.filter(
		(option) => !props.modelValue.includes(option) && contains(option, searchTerm.value),
	),
)

function onUpdateModelValue(value: unknown) {
	emit("update:modelValue", (value as string[] | undefined) ?? [])
}
</script>

<template>
	<Popover v-model:open="open">
		<ListboxRoot
			:model-value="modelValue"
			highlight-on-hover
			multiple
			@update:model-value="onUpdateModelValue"
		>
			<PopoverAnchor class="inline-flex w-full">
				<TagsInput
					:id="id"
					:model-value="modelValue"
					:aria-invalid="ariaInvalid"
					@update:model-value="onUpdateModelValue"
				>
					<TagsInputItem v-for="item in modelValue" :key="item" :value="item">
						<TagsInputItemText />
						<TagsInputItemDelete />
					</TagsInputItem>
					<ListboxFilter v-model="searchTerm" as-child>
						<TagsInputInput
							:placeholder="placeholder"
							@keydown.enter.prevent
							@keydown.down="open = true"
							@blur="emit('blur')"
						/>
					</ListboxFilter>
					<PopoverTrigger as-child>
						<Button
							type="button"
							size="icon-sm"
							variant="ghost"
							class="order-last ml-auto self-start"
						>
							<ChevronDown class="size-3.5" />
						</Button>
					</PopoverTrigger>
				</TagsInput>
			</PopoverAnchor>
			<PopoverContent class="p-1" @open-auto-focus.prevent>
				<ListboxContent
					class="max-h-[300px] scroll-py-1 overflow-x-hidden overflow-y-auto empty:p-1 empty:after:block empty:after:content-['No_options']"
					tabindex="0"
				>
					<ListboxItem
						v-for="option in filteredOptions"
						:key="option"
						:value="option"
						class="data-[highlighted]:bg-accent data-[highlighted]:text-accent-foreground relative flex cursor-default items-center gap-2 rounded-sm px-2 py-1.5 text-sm outline-hidden select-none data-[disabled]:pointer-events-none data-[disabled]:opacity-50"
						@select="searchTerm = ''"
					>
						{{ option }}
					</ListboxItem>
				</ListboxContent>
			</PopoverContent>
		</ListboxRoot>
	</Popover>
</template>
