<!--
SPDX-FileCopyrightText: 2026 OpenAdmin

SPDX-License-Identifier: AGPL-3.0-or-later
-->

<script setup lang="ts">
import {
	AlignCenter,
	AlignJustify,
	AlignLeft,
	AlignRight,
	Bold,
	ChevronDown,
	Code,
	Columns3,
	Eraser,
	Heading1,
	Heading2,
	Heading3,
	ImageIcon,
	Italic,
	Link2,
	List,
	ListOrdered,
	ListTodo,
	Minus,
	Pilcrow,
	Quote,
	Redo2,
	Rows3,
	SquareCode,
	Strikethrough,
	TableIcon,
	Trash2,
	Underline,
	Undo2,
	X,
} from "@lucide/vue"
import type { AnyFieldApi } from "@tanstack/vue-form"
import { Image as TiptapImage } from "@tiptap/extension-image"
import { Placeholder } from "@tiptap/extension-placeholder"
import { TableKit } from "@tiptap/extension-table"
import { TaskItem } from "@tiptap/extension-task-item"
import { TaskList } from "@tiptap/extension-task-list"
import { TextAlign } from "@tiptap/extension-text-align"
import { StarterKit } from "@tiptap/starter-kit"
import { EditorContent, useEditor } from "@tiptap/vue-3"
import type { Component } from "vue"
import { computed, onBeforeUnmount, watch } from "vue"
import { Button } from "@/components/ui/button"
import {
	DropdownMenu,
	DropdownMenuContent,
	DropdownMenuItem,
	DropdownMenuSeparator,
	DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { Field, FieldError, FieldLabel } from "@/components/ui/field"
import { Input } from "@/components/ui/input"
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover"
import { Separator } from "@/components/ui/separator"
import EditorToolbarButton from "./EditorToolbarButton.vue"
import { type FieldDef, isInvalid } from "./field"
import FieldLabelText from "./FieldLabelText.vue"
import { useLinkImagePopovers } from "./rich-text-popovers"

const props = defineProps<{
	field: AnyFieldApi
	def: FieldDef
}>()

interface ToolbarItem {
	key: string
	icon: Component
	label: string
	active?: boolean
	disabled?: boolean
	run: () => void
}

const editor = useEditor({
	content: (props.field.state.value as string | undefined) || "",
	extensions: [
		StarterKit.configure({
			link: {
				openOnClick: false,
				autolink: true,
				defaultProtocol: "https",
			},
		}),
		Placeholder.configure({ placeholder: "Write something…" }),
		TiptapImage.configure({ inline: false }),
		TaskList,
		TaskItem.configure({ nested: true }),
		TextAlign.configure({ types: ["heading", "paragraph"] }),
		TableKit.configure({ table: { resizable: true } }),
	],
	editorProps: {
		attributes: {
			id: props.field.name,
			class: "typeset typeset-docs max-w-none min-h-40 px-3 py-2 focus:outline-none",
		},
	},
	onUpdate: ({ editor: instance }) => {
		props.field.handleChange(instance.isEmpty ? "" : instance.getHTML())
	},
	onBlur: () => {
		props.field.handleBlur()
	},
})

watch(
	() => props.field.state.value,
	(value) => {
		const instance = editor.value
		if (!instance) return
		const next = (value as string | undefined) || ""
		if (instance.isEmpty ? next === "" : next === instance.getHTML()) return
		instance.commands.setContent(next, { emitUpdate: false })
	},
)

onBeforeUnmount(() => editor.value?.destroy())

const historyActions = computed<ToolbarItem[]>(() => {
	const e = editor.value
	if (!e) return []
	return [
		{
			key: "undo",
			icon: Undo2,
			label: "Undo",
			disabled: !e.can().undo(),
			run: () => e.chain().focus().undo().run(),
		},
		{
			key: "redo",
			icon: Redo2,
			label: "Redo",
			disabled: !e.can().redo(),
			run: () => e.chain().focus().redo().run(),
		},
	]
})

const markActions = computed<ToolbarItem[]>(() => {
	const e = editor.value
	if (!e) return []
	return [
		{
			key: "bold",
			icon: Bold,
			label: "Bold",
			active: e.isActive("bold"),
			run: () => e.chain().focus().toggleBold().run(),
		},
		{
			key: "italic",
			icon: Italic,
			label: "Italic",
			active: e.isActive("italic"),
			run: () => e.chain().focus().toggleItalic().run(),
		},
		{
			key: "underline",
			icon: Underline,
			label: "Underline",
			active: e.isActive("underline"),
			run: () => e.chain().focus().toggleUnderline().run(),
		},
		{
			key: "strike",
			icon: Strikethrough,
			label: "Strikethrough",
			active: e.isActive("strike"),
			run: () => e.chain().focus().toggleStrike().run(),
		},
		{
			key: "code",
			icon: Code,
			label: "Inline code",
			active: e.isActive("code"),
			run: () => e.chain().focus().toggleCode().run(),
		},
	]
})

const ALIGNMENTS = [
	{ value: "left", icon: AlignLeft, label: "Align left" },
	{ value: "center", icon: AlignCenter, label: "Align center" },
	{ value: "right", icon: AlignRight, label: "Align right" },
	{ value: "justify", icon: AlignJustify, label: "Justify" },
] as const

const alignActions = computed<ToolbarItem[]>(() => {
	const e = editor.value
	if (!e) return []
	return ALIGNMENTS.map(({ value, icon, label }) => ({
		key: `align-${value}`,
		icon,
		label,
		active: e.isActive({ textAlign: value }),
		run: () => e.chain().focus().setTextAlign(value).run(),
	}))
})

const listActions = computed<ToolbarItem[]>(() => {
	const e = editor.value
	if (!e) return []
	return [
		{
			key: "bulletList",
			icon: List,
			label: "Bullet list",
			active: e.isActive("bulletList"),
			run: () => e.chain().focus().toggleBulletList().run(),
		},
		{
			key: "orderedList",
			icon: ListOrdered,
			label: "Numbered list",
			active: e.isActive("orderedList"),
			run: () => e.chain().focus().toggleOrderedList().run(),
		},
		{
			key: "taskList",
			icon: ListTodo,
			label: "Task list",
			active: e.isActive("taskList"),
			run: () => e.chain().focus().toggleTaskList().run(),
		},
	]
})

const blockActions = computed<ToolbarItem[]>(() => {
	const e = editor.value
	if (!e) return []
	return [
		{
			key: "blockquote",
			icon: Quote,
			label: "Blockquote",
			active: e.isActive("blockquote"),
			run: () => e.chain().focus().toggleBlockquote().run(),
		},
		{
			key: "codeBlock",
			icon: SquareCode,
			label: "Code block",
			active: e.isActive("codeBlock"),
			run: () => e.chain().focus().toggleCodeBlock().run(),
		},
		{
			key: "horizontalRule",
			icon: Minus,
			label: "Divider",
			run: () => e.chain().focus().setHorizontalRule().run(),
		},
	]
})

const clearAction = computed<ToolbarItem | null>(() => {
	const e = editor.value
	if (!e) return null
	return {
		key: "clear",
		icon: Eraser,
		label: "Clear formatting",
		run: () => e.chain().focus().clearNodes().unsetAllMarks().run(),
	}
})

const HEADING_LEVELS = [1, 2, 3] as const
const HEADING_ICONS: Record<(typeof HEADING_LEVELS)[number], Component> = {
	1: Heading1,
	2: Heading2,
	3: Heading3,
}

const activeHeadingLevel = computed<(typeof HEADING_LEVELS)[number] | null>(() => {
	const e = editor.value
	if (!e) return null
	return HEADING_LEVELS.find((level) => e.isActive("heading", { level })) ?? null
})

const headingIcon = computed(() =>
	activeHeadingLevel.value ? HEADING_ICONS[activeHeadingLevel.value] : Pilcrow,
)

const isInTable = computed(() => !!editor.value?.isActive("table"))

const {
	linkPopoverOpen,
	linkUrl,
	applyLink,
	removeLink,
	imagePopoverOpen,
	imageUrl,
	imageAlt,
	insertImage,
} = useLinkImagePopovers(editor)
</script>

<template>
	<Field :data-invalid="isInvalid(props.field)">
		<FieldLabel :for="props.field.name">
			<FieldLabelText :def="props.def" />
		</FieldLabel>
		<div
			:aria-invalid="isInvalid(props.field)"
			class="border-input dark:bg-input/30 focus-within:border-ring focus-within:ring-ring/50 aria-invalid:ring-destructive/20 dark:aria-invalid:ring-destructive/40 aria-invalid:border-destructive w-full rounded-md border bg-transparent shadow-xs transition-[color,box-shadow] focus-within:ring-3"
		>
			<div v-if="editor" class="flex flex-wrap items-center gap-0.5 border-b p-1">
				<EditorToolbarButton
					v-for="item in historyActions"
					:key="item.key"
					:icon="item.icon"
					:label="item.label"
					:disabled="item.disabled"
					@click="item.run()"
				/>

				<Separator orientation="vertical" class="mx-1 h-5" />

				<DropdownMenu>
					<DropdownMenuTrigger as-child>
						<Button type="button" variant="ghost" size="sm" title="Text style" class="gap-1 px-2">
							<component :is="headingIcon" class="size-4" />
							<ChevronDown class="size-3" />
						</Button>
					</DropdownMenuTrigger>
					<DropdownMenuContent align="start">
						<DropdownMenuItem
							:data-active="activeHeadingLevel === null"
							@click="editor?.chain().focus().setParagraph().run()"
						>
							<Pilcrow />
							Paragraph
						</DropdownMenuItem>
						<DropdownMenuItem
							v-for="level in HEADING_LEVELS"
							:key="level"
							:data-active="activeHeadingLevel === level"
							@click="editor?.chain().focus().toggleHeading({ level }).run()"
						>
							<component :is="HEADING_ICONS[level]" />
							Heading {{ level }}
						</DropdownMenuItem>
					</DropdownMenuContent>
				</DropdownMenu>

				<Separator orientation="vertical" class="mx-1 h-5" />

				<EditorToolbarButton
					v-for="item in markActions"
					:key="item.key"
					:icon="item.icon"
					:label="item.label"
					:active="item.active"
					:disabled="item.disabled"
					@click="item.run()"
				/>

				<Separator orientation="vertical" class="mx-1 h-5" />

				<EditorToolbarButton
					v-for="item in alignActions"
					:key="item.key"
					:icon="item.icon"
					:label="item.label"
					:active="item.active"
					@click="item.run()"
				/>

				<Separator orientation="vertical" class="mx-1 h-5" />

				<EditorToolbarButton
					v-for="item in listActions"
					:key="item.key"
					:icon="item.icon"
					:label="item.label"
					:active="item.active"
					@click="item.run()"
				/>

				<Separator orientation="vertical" class="mx-1 h-5" />

				<EditorToolbarButton
					v-for="item in blockActions"
					:key="item.key"
					:icon="item.icon"
					:label="item.label"
					:active="item.active"
					@click="item.run()"
				/>

				<Separator orientation="vertical" class="mx-1 h-5" />

				<Popover v-model:open="linkPopoverOpen">
					<PopoverTrigger as-child>
						<EditorToolbarButton :icon="Link2" label="Link" :active="editor?.isActive('link')" />
					</PopoverTrigger>
					<PopoverContent class="w-72 space-y-2">
						<form class="flex items-center gap-2" @submit.prevent="applyLink">
							<Input v-model="linkUrl" placeholder="https://example.com" class="h-8" autofocus />
							<Button type="submit" size="sm">Apply</Button>
						</form>
						<Button
							v-if="editor?.isActive('link')"
							type="button"
							variant="ghost"
							size="sm"
							class="text-destructive w-full justify-start"
							@click="removeLink"
						>
							<X />
							Remove link
						</Button>
					</PopoverContent>
				</Popover>

				<Popover v-model:open="imagePopoverOpen">
					<PopoverTrigger as-child>
						<EditorToolbarButton :icon="ImageIcon" label="Image" />
					</PopoverTrigger>
					<PopoverContent class="w-72 space-y-2">
						<Input
							v-model="imageUrl"
							placeholder="https://example.com/image.png"
							class="h-8"
							autofocus
						/>
						<Input v-model="imageAlt" placeholder="Alt text (optional)" class="h-8" />
						<Button type="button" size="sm" class="w-full" @click="insertImage"
							>Insert image</Button
						>
					</PopoverContent>
				</Popover>

				<DropdownMenu>
					<DropdownMenuTrigger as-child>
						<EditorToolbarButton :icon="TableIcon" label="Table" :active="isInTable" />
					</DropdownMenuTrigger>
					<DropdownMenuContent align="start">
						<DropdownMenuItem
							v-if="!isInTable"
							@click="editor?.chain().focus().insertTable({ rows: 3, cols: 3, withHeaderRow: true }).run()"
						>
							<TableIcon />
							Insert table
						</DropdownMenuItem>
						<template v-else>
							<DropdownMenuItem @click="editor?.chain().focus().addColumnAfter().run()">
								<Columns3 />
								Add column after
							</DropdownMenuItem>
							<DropdownMenuItem @click="editor?.chain().focus().addRowAfter().run()">
								<Rows3 />
								Add row after
							</DropdownMenuItem>
							<DropdownMenuItem @click="editor?.chain().focus().deleteColumn().run()">
								<Columns3 />
								Delete column
							</DropdownMenuItem>
							<DropdownMenuItem @click="editor?.chain().focus().deleteRow().run()">
								<Rows3 />
								Delete row
							</DropdownMenuItem>
							<DropdownMenuItem @click="editor?.chain().focus().mergeOrSplit().run()">
								<TableIcon />
								Merge / split cells
							</DropdownMenuItem>
							<DropdownMenuSeparator />
							<DropdownMenuItem
								variant="destructive"
								@click="editor?.chain().focus().deleteTable().run()"
							>
								<Trash2 />
								Delete table
							</DropdownMenuItem>
						</template>
					</DropdownMenuContent>
				</DropdownMenu>

				<Separator orientation="vertical" class="mx-1 h-5" />

				<EditorToolbarButton
					v-if="clearAction"
					:icon="clearAction.icon"
					:label="clearAction.label"
					@click="clearAction.run()"
				/>
			</div>
			<EditorContent :editor="editor" />
		</div>
		<FieldError v-if="isInvalid(props.field)" :errors="props.field.state.meta.errors" />
	</Field>
</template>

<style scoped>
:deep(.ProseMirror) {
	outline: none;
}

:deep(.ProseMirror p.is-editor-empty:first-child::before) {
	content: attr(data-placeholder);
	float: left;
	height: 0;
	color: var(--color-muted-foreground);
	pointer-events: none;
}

:deep(.ProseMirror ul[data-type="taskList"]) {
	list-style: none;
	padding-left: 0.25em;
}

:deep(.ProseMirror ul[data-type="taskList"] li) {
	display: flex;
	align-items: flex-start;
	gap: 0.5em;
}

:deep(.ProseMirror ul[data-type="taskList"] li > label) {
	margin-top: 0.35em;
	flex: 0 0 auto;
	user-select: none;
}

:deep(.ProseMirror ul[data-type="taskList"] li > div) {
	flex: 1 1 auto;
}

:deep(.ProseMirror ul[data-type="taskList"] li[data-checked="true"] > div) {
	color: var(--color-muted-foreground);
	text-decoration: line-through;
}

:deep(.ProseMirror .tableWrapper) {
	overflow-x: auto;
}

:deep(.ProseMirror table) {
	border-collapse: collapse;
	table-layout: fixed;
	width: 100%;
}

:deep(.ProseMirror td),
:deep(.ProseMirror th) {
	position: relative;
	border: 1px solid var(--color-border);
}

:deep(.ProseMirror .selectedCell) {
	background-color: color-mix(in oklab, var(--color-primary) 12%, transparent);
}

:deep(.ProseMirror .column-resize-handle) {
	position: absolute;
	top: 0;
	bottom: -2px;
	right: -2px;
	width: 2px;
	background-color: var(--color-primary);
	pointer-events: none;
}

:deep(.ProseMirror.resize-cursor) {
	cursor: col-resize;
}

:deep(.ProseMirror img.ProseMirror-selectednode) {
	outline: 2px solid var(--color-ring);
	outline-offset: 2px;
}

:deep([data-slot="dropdown-menu-item"][data-active="true"]) {
	background-color: var(--color-accent);
	color: var(--color-accent-foreground);
}
</style>
