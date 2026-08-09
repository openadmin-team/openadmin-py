// SPDX-FileCopyrightText: 2026 OpenAdmin
//
// SPDX-License-Identifier: AGPL-3.0-or-later

import { z } from "zod"
import { colorSchema } from "./color"
import { httpMethodSchema } from "./http-method"
import { iconSchema } from "./icon"
import { jsonSchemaSchema } from "./json-schema"

export const tableComponentSchema = z.object({
	type: z.literal("table"),
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

export type TableComponent = z.infer<typeof tableComponentSchema>

const tableRowValueSchema = z.union([z.string(), z.number(), z.boolean(), z.null()])

const tableRowSchema = z.record(z.string(), tableRowValueSchema)

export const tableDataSchema = z.array(z.union([tableRowSchema, z.unknown()]))

export type TableData = z.infer<typeof tableDataSchema>

export const tableResponseSchema = z.object({
	data: tableDataSchema,
	icon: iconSchema.optional(),
	color: colorSchema.optional(),
})

export type TableResponse = z.infer<typeof tableResponseSchema>

export const tableSchema = z.union([tableDataSchema, tableResponseSchema])

export type Table = z.infer<typeof tableSchema>
