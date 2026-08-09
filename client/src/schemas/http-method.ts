// SPDX-FileCopyrightText: 2026 OpenAdmin
//
// SPDX-License-Identifier: AGPL-3.0-or-later

import { z } from "zod"

export const HTTP_METHODS = ["get", "post", "put", "patch", "delete", "head"] as const

export const httpMethodSchema = z.enum(HTTP_METHODS)

export type HttpMethod = z.infer<typeof httpMethodSchema>
