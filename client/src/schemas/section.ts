// SPDX-FileCopyrightText: 2026 OpenAdmin
//
// SPDX-License-Identifier: AGPL-3.0-or-later

import { z } from "zod"
import { iconSchema } from "./icon"
import { pageSchema } from "./page"

export const sectionSchema = z.object({
	id: z.string(),
	name: z.string(),
	description: z.string().nullable(),
	icon: iconSchema.nullable(),
	pages: z.array(pageSchema),
})

export type Section = z.infer<typeof sectionSchema>
