// SPDX-FileCopyrightText: 2026 OpenAdmin
//
// SPDX-License-Identifier: AGPL-3.0-or-later

import { z } from "zod"
import { colorSchema } from "./color"
import { httpMethodSchema } from "./http-method"
import { iconSchema } from "./icon"
import { jsonSchemaSchema } from "./json-schema"

export const statComponentSchema = z.object({
	type: z.literal("stat"),
	id: z.string(),
	icon: iconSchema.nullable(),
	color: colorSchema.nullable(),
	name: z.string(),
	refresh: z.number().nullable(),
	description: z.string().nullable(),
	method: httpMethodSchema,
	form: jsonSchemaSchema.nullable(),
	body: jsonSchemaSchema.nullable(),
	query: jsonSchemaSchema.nullable(),
})

export type StatComponent = z.infer<typeof statComponentSchema>

export const statValueSchema = z.union([z.string(), z.number(), z.boolean(), z.null()])

export type StatValue = z.infer<typeof statValueSchema>

export const statResponseSchema = z.object({
	value: statValueSchema,
	refresh: z.number().nullable().optional(),
	icon: iconSchema.optional(),
	color: colorSchema.optional(),
})

export type StatResponse = z.infer<typeof statResponseSchema>

export const statSchema = z.union([statValueSchema, statResponseSchema])

export type Stat = z.infer<typeof statSchema>
