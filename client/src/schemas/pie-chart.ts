// SPDX-FileCopyrightText: 2026 OpenAdmin
//
// SPDX-License-Identifier: AGPL-3.0-or-later

import { z } from "zod"
import { colorSchema } from "./color"
import { httpMethodSchema } from "./http-method"
import { iconSchema } from "./icon"
import { jsonSchemaSchema } from "./json-schema"

export const pieChartConfigValueSchema = z.object({
	name: z.string().optional(),
	color: colorSchema.optional(),
	icon: iconSchema.optional(),
})

export type PieChartConfigValue = z.infer<typeof pieChartConfigValueSchema>

export const pieChartComponentSchema = z.object({
	type: z.literal("pie-chart"),
	id: z.string(),
	name: z.string(),
	config: z.record(z.string(), pieChartConfigValueSchema).nullable(),
	icon: iconSchema.nullable(),
	name_key: z.string().nullable(),
	value_key: z.string().nullable(),
	color: colorSchema.nullable(),
	description: z.string().nullable(),
	caption: z.string().nullable(),
	caption_description: z.string().nullable(),
	caption_icon: iconSchema.nullable(),
	method: httpMethodSchema,
	form: jsonSchemaSchema.nullable(),
	body: jsonSchemaSchema.nullable(),
	query: jsonSchemaSchema.nullable(),
})

export type PieChartComponent = z.infer<typeof pieChartComponentSchema>

export const pieChartDataSchema = z.union([
	z.array(z.record(z.string(), z.union([z.number(), z.string()]))),
	z.array(z.record(z.enum(["name", "value"]), z.union([z.number(), z.string()]))),
	z.unknown(),
])

export type PieChartData = z.infer<typeof pieChartDataSchema>

export const pieChartResponseSchema = z.object({
	config: z.record(z.string(), pieChartConfigValueSchema).optional(),
	icon: iconSchema.optional(),
	color: colorSchema.optional(),
	data: pieChartDataSchema,
})

export type PieChartResponse = z.infer<typeof pieChartResponseSchema>

export const pieChartSchema = z.union([pieChartDataSchema, pieChartResponseSchema])

export type PieChart = z.infer<typeof pieChartSchema>
