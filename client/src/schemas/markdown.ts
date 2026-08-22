// SPDX-FileCopyrightText: 2026 OpenAdmin
//
// SPDX-License-Identifier: AGPL-3.0-or-later

import { z } from "zod"
import { colorSchema } from "./color"
import { httpMethodSchema } from "./http-method"
import { iconSchema } from "./icon"
import { jsonSchemaSchema } from "./json-schema"

export const markdownComponentSchema = z.object({
	type: z.literal("markdown"),
	id: z.string(),
	name: z.string(),
	description: z.string().nullable(),
	color: colorSchema.nullable(),
	icon: iconSchema.nullable(),
	refresh: z.number().nullable(),
	method: httpMethodSchema,
	form: jsonSchemaSchema.nullable(),
	body: jsonSchemaSchema.nullable(),
	query: jsonSchemaSchema.nullable(),
})

export type MarkdownComponent = z.infer<typeof markdownComponentSchema>

export const markdownContentSchema = z.string()

export type MarkdownContent = z.infer<typeof markdownContentSchema>

export const markdownResponseSchema = z.object({
	icon: iconSchema.optional(),
	color: colorSchema.optional(),
	refresh: z.number().nullable().optional(),
	content: markdownContentSchema,
})

export type MarkdownResponse = z.infer<typeof markdownResponseSchema>

export const markdownSchema = z.union([markdownContentSchema, markdownResponseSchema])

export type Markdown = z.infer<typeof markdownSchema>
