// SPDX-FileCopyrightText: 2026 OpenAdmin
//
// SPDX-License-Identifier: AGPL-3.0-or-later

import { z } from "zod"
import { sectionSchema } from "./section"

export const specSchema = z.object({
	version: z.string(),
	name: z.string(),
	id: z.string(),
	description: z.string().nullable().optional(),
	sections: z.array(sectionSchema),
})

export type Spec = z.infer<typeof specSchema>
