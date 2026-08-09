// SPDX-FileCopyrightText: 2026 OpenAdmin
//
// SPDX-License-Identifier: AGPL-3.0-or-later

import { z } from "zod"

export const errorSchema = z.object({
	message: z.string(),
})

export type Error = z.infer<typeof errorSchema>
