// SPDX-FileCopyrightText: 2026 OpenAdmin
//
// SPDX-License-Identifier: AGPL-3.0-or-later

import type { AnyFieldApi } from "@tanstack/vue-form"
import type { Color } from "@/schemas/color"
import type { Icon } from "@/schemas/icon"
import type { JsonSchema } from "@/schemas/json-schema"

export type ArrayItemKind =
	| "integer"
	| "number"
	| "boolean"
	| "date"
	| "date-time"
	| "string"
	| "enum"

export interface FieldDef {
	key: string
	label: string
	required: boolean
	icon?: Icon
	color?: Color
	boolean: boolean
	numeric: boolean
	integer: boolean
	date: boolean
	datetime: boolean
	file: boolean
	fileArray: boolean
	array: boolean
	itemKind?: ArrayItemKind
	select: boolean
	richText: boolean
	options?: string[]
	itemOptions?: string[]
}

function resolveSchemaRef(
	schema: JsonSchema | undefined,
	root: JsonSchema,
): JsonSchema | undefined {
	if (!schema?.$ref) return schema
	const key = schema.$ref.split("/").pop()
	const target = key ? (root.$defs?.[key] ?? root.definitions?.[key]) : undefined
	return target ? resolveSchemaRef(target, root) : schema
}

function arrayItemKind(items: JsonSchema["items"], root: JsonSchema): ArrayItemKind {
	const item = resolveSchemaRef(Array.isArray(items) ? items[0] : items, root)
	if (item?.enum) return "enum"
	if (item?.type === "integer") return "integer"
	if (item?.type === "number") return "number"
	if (item?.type === "boolean") return "boolean"
	if (item?.type === "string" && item.format === "date") return "date"
	if (item?.type === "string" && item.format === "date-time") return "date-time"
	return "string"
}

/**
 * Actions don't carry per-field config (icon/color/rich-text style) the way
 * forms do — there's no `ActionComponent.fields` — so every field just gets
 * its label/type derived straight from the JSON schema.
 */
export function fieldsOfSchema(
	schema: JsonSchema | null | undefined,
	source: "query" | "body" | "form",
): FieldDef[] {
	if (!schema?.properties) return []
	const required = new Set(schema.required ?? [])
	return Object.entries(schema.properties).map(([key, rawProperty]) => {
		const property = resolveSchemaRef(rawProperty, schema) ?? rawProperty
		const array = source !== "form" && property.type === "array"
		const itemSchema = array
			? resolveSchemaRef(Array.isArray(property.items) ? property.items[0] : property.items, schema)
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
			richText: false,
		}
	})
}

export function isInvalid(field: AnyFieldApi) {
	return field.state.meta.isTouched && !field.state.meta.isValid
}

export function formatFileSize(bytes: number) {
	if (bytes < 1024) return `${bytes} B`
	if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
	return `${(bytes / (1024 * 1024)).toFixed(1)} MB`
}

export function isImageFile(file: File) {
	return file.type.startsWith("image/")
}

const objectUrls = new WeakMap<File, string>()

export function objectUrlFor(file: File) {
	let url = objectUrls.get(file)
	if (!url) {
		url = URL.createObjectURL(file)
		objectUrls.set(file, url)
	}
	return url
}
