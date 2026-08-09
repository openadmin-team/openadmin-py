// SPDX-FileCopyrightText: 2026 OpenAdmin
//
// SPDX-License-Identifier: AGPL-3.0-or-later

import { z } from "zod"
import { colorSchema } from "./color"
import { httpMethodSchema } from "./http-method"
import { iconSchema } from "./icon"
import { jsonSchemaSchema } from "./json-schema"

export const fieldConfigSchema = z.object({
	reference: z.string().nullable().optional(),
	reference_field: z.string().optional(),
	icon: iconSchema.optional(),
	color: colorSchema.optional(),
})

export type FieldConfig = z.infer<typeof fieldConfigSchema>

export const formComponentSchema = z.object({
	type: z.literal("form"),
	id: z.string(),
	name: z.string(),
	description: z.string().nullable(),
	fields: z.record(z.string(), fieldConfigSchema).nullable(),
	icon: iconSchema.nullable(),
	color: colorSchema.nullable(),
	method: httpMethodSchema,
	is_hidden: z.boolean(),
	form: jsonSchemaSchema.nullable(),
	body: jsonSchemaSchema.nullable(),
	query: jsonSchemaSchema.nullable(),
})

export type FormComponent = z.infer<typeof formComponentSchema>

export const formResponseSchema = z.object({
	icon: iconSchema.optional(),
	color: colorSchema.optional(),
	toast: z.string().optional(),
	table: z.unknown().optional(),
	message: z.string().optional(),
})

export type FormResponse = z.infer<typeof formResponseSchema>

export const formSchema = z.union([formResponseSchema, z.null(), z.string()])

export type Form = z.infer<typeof formSchema>
