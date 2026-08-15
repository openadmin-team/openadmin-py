// SPDX-FileCopyrightText: 2026 OpenAdmin
//
// SPDX-License-Identifier: AGPL-3.0-or-later

import { z } from "zod"
import { colorSchema } from "./color"
import { httpMethodSchema } from "./http-method"
import { iconSchema } from "./icon"
import { jsonSchemaSchema } from "./json-schema"

export const COLUMN_STYLES = ["avatar", "image", "badge", "link"] as const

export const columnStyleSchema = z.enum(COLUMN_STYLES)

export type ColumnStyle = z.infer<typeof columnStyleSchema>

export const columnConfigValueSchema = z.object({
	style: columnStyleSchema.optional(),
	label: z.string().optional(),
	icon: iconSchema.optional(),
	color: colorSchema.optional(),
})

export type ColumnConfigValue = z.infer<typeof columnConfigValueSchema>

export const actionConfigSchema = z.object({
	action: z.string(),
	label: z.string().optional(),
	icon: iconSchema.optional(),
	color: colorSchema.optional(),
	query: z.record(z.string(), z.unknown()),
	body: z.record(z.string(), z.unknown()),
	form: z.record(z.string(), z.unknown()),
})

export type ActionConfig = z.infer<typeof actionConfigSchema>

export const tableComponentSchema = z.object({
	type: z.literal("table"),
	id: z.string(),
	name: z.string(),
	description: z.string().nullable(),
	columns: z.record(z.string(), columnConfigValueSchema).nullable(),
	icon: iconSchema.nullable(),
	color: colorSchema.nullable(),
	method: httpMethodSchema,
	is_hidden: z.boolean(),
	refresh: z.number().nullable(),
	form: jsonSchemaSchema.nullable(),
	body: jsonSchemaSchema.nullable(),
	query: jsonSchemaSchema.nullable(),
})

export type TableComponent = z.infer<typeof tableComponentSchema>

const tableRowValueSchema = z.union([z.string(), z.number(), z.boolean(), z.null()])

const tableRowSchema = z
	.object({
		__view__: tableRowValueSchema.optional(),
		__actions__: z.array(actionConfigSchema).optional(),
		__style__: columnStyleSchema.nullable().optional(),
	})
	.catchall(tableRowValueSchema)

export const tableDataSchema = z.array(z.union([tableRowSchema, z.unknown()]))

export type TableData = z.infer<typeof tableDataSchema>

export const tableResponseSchema = z.object({
	data: tableDataSchema,
	icon: iconSchema.optional(),
	color: colorSchema.optional(),
	refresh: z.number().nullable().optional(),
	total: z.number().optional(),
})

export type TableResponse = z.infer<typeof tableResponseSchema>

export const tableSchema = z.union([tableDataSchema, tableResponseSchema])

export type Table = z.infer<typeof tableSchema>
