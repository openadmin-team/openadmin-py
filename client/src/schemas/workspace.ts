// SPDX-FileCopyrightText: 2026 OpenAdmin
//
// SPDX-License-Identifier: AGPL-3.0-or-later

import { z } from "zod"

export const workspaceSchema = z.object({
	id: z.string(),
	name: z.string(),
	avatar: z.string().nullable().optional(),
	description: z.string().nullable().optional(),
})

export const workspacesSchema = z.array(workspaceSchema)

export type Workspace = z.infer<typeof workspaceSchema>
