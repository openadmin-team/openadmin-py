<!--
SPDX-FileCopyrightText: 2026 OpenAdmin

SPDX-License-Identifier: AGPL-3.0-or-later
-->

<script setup lang="ts">
import { FileIcon, PaperclipIcon, XIcon } from "@lucide/vue"
import type { AnyFieldApi } from "@tanstack/vue-form"
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
import { Field, FieldError, FieldLabel } from "@/components/ui/field"
import { type FieldDef, formatFileSize, isImageFile, isInvalid, objectUrlFor } from "./field"
import FieldLabelText from "./FieldLabelText.vue"

const props = defineProps<{
	field: AnyFieldApi
	def: FieldDef
}>()

function onFilesChange(event: Event) {
	const input = event.target as HTMLInputElement
	const added = Array.from(input.files ?? [])
	if (added.length) {
		const existing = (props.field.state.value as File[] | undefined) ?? []
		props.field.handleChange([...existing, ...added])
	}
	input.value = ""
}

function removeFileAt(index: number) {
	const existing = (props.field.state.value as File[] | undefined) ?? []
	props.field.handleChange(existing.filter((_, i) => i !== index))
}
</script>

<template>
	<Field :data-invalid="isInvalid(props.field)">
		<FieldLabel :for="props.field.name">
			<FieldLabelText :def="props.def" />
		</FieldLabel>
		<input
			:id="props.field.name"
			type="file"
			multiple
			class="hidden"
			:aria-invalid="isInvalid(props.field)"
			@change="onFilesChange"
			@blur="props.field.handleBlur"
		>
		<AttachmentGroup>
			<Attachment
				v-for="(file, index) in (props.field.state.value as File[] | undefined) ?? []"
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
					<AttachmentAction type="button" aria-label="Remove file" @click="removeFileAt(index)">
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
				<AttachmentTrigger as="label" :for="props.field.name" />
			</Attachment>
		</AttachmentGroup>
		<FieldError v-if="isInvalid(props.field)" :errors="props.field.state.meta.errors" />
	</Field>
</template>
