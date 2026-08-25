// SPDX-FileCopyrightText: 2026 OpenAdmin
//
// SPDX-License-Identifier: AGPL-3.0-or-later

import type { AnyFieldApi } from "@tanstack/vue-form"
import type { Color } from "@/schemas/color"
import type { Icon } from "@/schemas/icon"

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
	options?: string[]
	itemOptions?: string[]
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
