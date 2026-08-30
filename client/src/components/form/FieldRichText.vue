<!--
SPDX-FileCopyrightText: 2026 OpenAdmin

SPDX-License-Identifier: AGPL-3.0-or-later
-->

<script setup lang="ts">
import {
	BoldIcon,
	CodeIcon,
	Heading1Icon,
	Heading2Icon,
	ItalicIcon,
	ListIcon,
	ListOrderedIcon,
	StrikethroughIcon,
	TextQuoteIcon,
} from "@lucide/vue"
import type { AnyFieldApi } from "@tanstack/vue-form"
import { Markdown } from "@tiptap/markdown"
import StarterKit from "@tiptap/starter-kit"
import { EditorContent, useEditor } from "@tiptap/vue-3"
import { computed, watch } from "vue"
import { Button } from "@/components/ui/button"
import { Field, FieldError, FieldLabel } from "@/components/ui/field"
import { cn } from "@/lib/utils"
import { type FieldDef, isInvalid } from "./field"
import FieldLabelText from "./FieldLabelText.vue"

const props = defineProps<{
	field: AnyFieldApi
	def: FieldDef
}>()

const editor = useEditor({
	content: (props.field.state.value as string | undefined) ?? "",
	contentType: "markdown",
	extensions: [StarterKit.configure({ heading: { levels: [1, 2, 3] } }), Markdown],
	editorProps: {
		attributes: {
			id: props.field.name,
			class: "typeset min-h-24 px-3 py-2 text-sm focus:outline-none",
		},
	},
	onUpdate: ({ editor: instance }) => {
		props.field.handleChange(instance.getMarkdown())
	},
	onBlur: () => {
		props.field.handleBlur()
	},
})

watch(
	() => props.field.state.value,
	(value) => {
		if (!editor.value) return
		const markdown = (value as string | undefined) ?? ""
		if (markdown === editor.value.getMarkdown()) return
		editor.value.commands.setContent(markdown, { contentType: "markdown" })
	},
)

type ToolbarAction = {
	label: string
	icon: typeof BoldIcon
	isActive: boolean
	run: () => void
}

const actions = computed<ToolbarAction[]>(() => {
	const instance = editor.value
	if (!instance) return []
	const chain = () => instance.chain().focus()
	return [
		{
			label: "Bold",
			icon: BoldIcon,
			isActive: instance.isActive("bold"),
			run: () => chain().toggleBold().run(),
		},
		{
			label: "Italic",
			icon: ItalicIcon,
			isActive: instance.isActive("italic"),
			run: () => chain().toggleItalic().run(),
		},
		{
			label: "Strikethrough",
			icon: StrikethroughIcon,
			isActive: instance.isActive("strike"),
			run: () => chain().toggleStrike().run(),
		},
		{
			label: "Inline code",
			icon: CodeIcon,
			isActive: instance.isActive("code"),
			run: () => chain().toggleCode().run(),
		},
		{
			label: "Heading 1",
			icon: Heading1Icon,
			isActive: instance.isActive("heading", { level: 1 }),
			run: () => chain().toggleHeading({ level: 1 }).run(),
		},
		{
			label: "Heading 2",
			icon: Heading2Icon,
			isActive: instance.isActive("heading", { level: 2 }),
			run: () => chain().toggleHeading({ level: 2 }).run(),
		},
		{
			label: "Bullet list",
			icon: ListIcon,
			isActive: instance.isActive("bulletList"),
			run: () => chain().toggleBulletList().run(),
		},
		{
			label: "Numbered list",
			icon: ListOrderedIcon,
			isActive: instance.isActive("orderedList"),
			run: () => chain().toggleOrderedList().run(),
		},
		{
			label: "Quote",
			icon: TextQuoteIcon,
			isActive: instance.isActive("blockquote"),
			run: () => chain().toggleBlockquote().run(),
		},
	]
})
</script>

<template>
	<Field :data-invalid="isInvalid(props.field)">
		<FieldLabel :for="props.field.name">
			<FieldLabelText :def="props.def" />
		</FieldLabel>
		<div
			:data-invalid="isInvalid(props.field)"
			class="rounded-xs border border-input shadow-xs transition-[color,box-shadow] focus-within:border-ring focus-within:ring-3 focus-within:ring-ring/50 data-[invalid=true]:border-destructive data-[invalid=true]:ring-destructive/20"
		>
			<div v-if="editor" class="flex flex-wrap items-center gap-0.5 border-input border-b p-1">
				<Button
					v-for="action in actions"
					:key="action.label"
					type="button"
					variant="ghost"
					size="icon-sm"
					:aria-label="action.label"
					:aria-pressed="action.isActive"
					:class="cn(action.isActive && 'bg-accent text-accent-foreground')"
					@mousedown.prevent
					@click="action.run"
				>
					<component :is="action.icon" class="size-4" />
				</Button>
			</div>
			<EditorContent :editor="editor" />
		</div>
		<FieldError v-if="isInvalid(props.field)" :errors="props.field.state.meta.errors" />
	</Field>
</template>
