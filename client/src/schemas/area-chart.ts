// SPDX-FileCopyrightText: 2026 OpenAdmin
//
// SPDX-License-Identifier: AGPL-3.0-or-later

import { z } from "zod"
import { httpMethodSchema } from "./http-method"
import { jsonSchemaSchema } from "./json-schema"

export const areaChartComponentSchema = z.object({
	type: z.literal("area-chart"),
	id: z.string(),
	name: z.string(),
	description: z.string().nullable(),
	refresh: z.number().nullable(),
	method: httpMethodSchema,
	form: jsonSchemaSchema.nullable(),
	body: jsonSchemaSchema.nullable(),
	query: jsonSchemaSchema.nullable(),
})

export type AreaChartComponent = z.infer<typeof areaChartComponentSchema>

export const areaChartSchema = areaChartComponentSchema

export type AreaChart = AreaChartComponent
