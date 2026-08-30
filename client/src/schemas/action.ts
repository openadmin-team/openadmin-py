// SPDX-FileCopyrightText: 2026 OpenAdmin
//
// SPDX-License-Identifier: AGPL-3.0-or-later

import { z } from "zod"
import { colorSchema } from "./color"
import { httpMethodSchema } from "./http-method"
import { iconSchema } from "./icon"
import { jsonSchemaSchema } from "./json-schema"

export const actionComponentSchema = z.object({
	type: z.literal("action"),
	id: z.string(),
	name: z.string(),
	description: z.string().nullable(),
	icon: iconSchema.nullable(),
	color: colorSchema.nullable(),
	method: httpMethodSchema,
	is_hidden: z.boolean(),
	form: jsonSchemaSchema.nullable(),
	body: jsonSchemaSchema.nullable(),
	query: jsonSchemaSchema.nullable(),
})

export type ActionComponent = z.infer<typeof actionComponentSchema>

export const actionResponseSchema = z.object({
	toast: z.string().optional(),
	clipboard: z.string().optional(),
})

export type ActionResponse = z.infer<typeof actionResponseSchema>

export const actionSchema = z.union([actionResponseSchema, z.null(), z.string()])

export type Action = z.infer<typeof actionSchema>
