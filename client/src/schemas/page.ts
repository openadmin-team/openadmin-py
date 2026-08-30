// SPDX-FileCopyrightText: 2026 OpenAdmin
//
// SPDX-License-Identifier: AGPL-3.0-or-later

import { z } from "zod"
import { componentSchema } from "./component"
import { iconSchema } from "./icon"
import { colorSchema } from "./color"

export const pageSchema = z.object({
	id: z.string(),
	name: z.string(),
	description: z.string().nullable(),
	icon: iconSchema.nullable(),
	color: colorSchema.nullable(),
	components: z.array(componentSchema),
})

export type Page = z.infer<typeof pageSchema>
