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

function onFileChange(event: Event) {
	const input = event.target as HTMLInputElement
	const file = input.files?.[0]
	if (file) props.field.handleChange(file)
	input.value = ""
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
			class="hidden"
			:aria-invalid="isInvalid(props.field)"
			@change="onFileChange"
			@blur="props.field.handleBlur"
		>
		<Attachment :state="props.field.state.value ? 'done' : 'idle'">
			<AttachmentMedia
				v-if="props.field.state.value && isImageFile(props.field.state.value as File)"
				variant="image"
			>
				<img
					:src="objectUrlFor(props.field.state.value as File)"
					:alt="(props.field.state.value as File).name"
				>
			</AttachmentMedia>
			<AttachmentMedia v-else>
				<PaperclipIcon v-if="!props.field.state.value" />
				<FileIcon v-else />
			</AttachmentMedia>
			<AttachmentContent>
				<AttachmentTitle>
					{{ (props.field.state.value as File | undefined)?.name ?? "Choose a file" }}
				</AttachmentTitle>
				<AttachmentDescription v-if="props.field.state.value">
					{{ formatFileSize((props.field.state.value as File).size) }}
				</AttachmentDescription>
			</AttachmentContent>
			<AttachmentActions v-if="props.field.state.value">
				<AttachmentAction
					type="button"
					aria-label="Remove file"
					@click="props.field.handleChange(undefined)"
				>
					<XIcon />
				</AttachmentAction>
			</AttachmentActions>
			<AttachmentTrigger as="label" :for="props.field.name" />
		</Attachment>
		<FieldError v-if="isInvalid(props.field)" :errors="props.field.state.meta.errors" />
	</Field>
</template>
