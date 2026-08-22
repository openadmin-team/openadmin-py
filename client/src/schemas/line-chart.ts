// SPDX-FileCopyrightText: 2026 OpenAdmin
//
// SPDX-License-Identifier: AGPL-3.0-or-later

import { z } from "zod"
import { httpMethodSchema } from "./http-method"
import { jsonSchemaSchema } from "./json-schema"

export const lineChartComponentSchema = z.object({
	type: z.literal("line-chart"),
	id: z.string(),
	name: z.string(),
	description: z.string().nullable(),
	refresh: z.number().nullable(),
	method: httpMethodSchema,
	form: jsonSchemaSchema.nullable(),
	body: jsonSchemaSchema.nullable(),
	query: jsonSchemaSchema.nullable(),
})

export type LineChartComponent = z.infer<typeof lineChartComponentSchema>

export const lineChartSchema = lineChartComponentSchema

export type LineChart = LineChartComponent
