// SPDX-FileCopyrightText: 2026 OpenAdmin
//
// SPDX-License-Identifier: AGPL-3.0-or-later

import { z } from "zod"
import { actionComponentSchema } from "./action"
import { areaChartComponentSchema } from "./area-chart"
import { barChartComponentSchema } from "./bar-chart"
import { formComponentSchema } from "./form"
import { lineChartComponentSchema } from "./line-chart"
import { markdownComponentSchema } from "./markdown"
import { pieChartComponentSchema } from "./pie-chart"
import { statComponentSchema } from "./stat"
import { tableComponentSchema } from "./table"

export const componentSchema = z.discriminatedUnion("type", [
	statComponentSchema,
	tableComponentSchema,
	areaChartComponentSchema,
	barChartComponentSchema,
	lineChartComponentSchema,
	pieChartComponentSchema,
	actionComponentSchema,
	formComponentSchema,
	markdownComponentSchema,
])

export type Component = z.infer<typeof componentSchema>
