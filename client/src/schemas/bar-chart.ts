// SPDX-FileCopyrightText: 2026 OpenAdmin
//
// SPDX-License-Identifier: AGPL-3.0-or-later

import { z } from "zod"
import { colorSchema } from "./color"
import { httpMethodSchema } from "./http-method"
import { iconSchema } from "./icon"
import { jsonSchemaSchema } from "./json-schema"

export const barChartConfigValueSchema = z.object({
	name: z.string().optional(),
	color: colorSchema.optional(),
	icon: iconSchema.optional(),
})

export type BarChartConfigValue = z.infer<typeof barChartConfigValueSchema>

export const barChartComponentSchema = z.object({
	type: z.literal("bar-chart"),
	id: z.string(),
	name: z.string(),
	description: z.string().nullable(),
	config: z.record(z.string(), barChartConfigValueSchema).nullable(),
	data_key: z.string().nullable(),
	icon: iconSchema.nullable(),
	color: colorSchema.nullable(),
	caption: z.string().nullable(),
	caption_description: z.string().nullable(),
	caption_icon: iconSchema.nullable(),
	refresh: z.number().nullable(),
	method: httpMethodSchema,
	form: jsonSchemaSchema.nullable(),
	body: jsonSchemaSchema.nullable(),
	query: jsonSchemaSchema.nullable(),
})

export type BarChartComponent = z.infer<typeof barChartComponentSchema>

export const barChartDataSchema = z.union([
	z.array(z.record(z.string(), z.union([z.number(), z.string()]))),
	z.array(z.record(z.enum(["data", "value"]), z.union([z.number(), z.string()]))),
	z.unknown(),
])

export type BarChartData = z.infer<typeof barChartDataSchema>

export const barChartResponseSchema = z.object({
	config: z.record(z.string(), barChartConfigValueSchema).optional(),
	icon: iconSchema.optional(),
	color: colorSchema.optional(),
	refresh: z.number().nullable().optional(),
	data: barChartDataSchema,
})

export type BarChartResponse = z.infer<typeof barChartResponseSchema>

export const barChartSchema = z.union([barChartDataSchema, barChartResponseSchema])

export type BarChart = z.infer<typeof barChartSchema>
