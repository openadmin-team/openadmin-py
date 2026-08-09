// SPDX-FileCopyrightText: 2026 OpenAdmin
//
// SPDX-License-Identifier: AGPL-3.0-or-later

import { z } from "zod"

export type JsonSchema = {
	$schema?: string
	$ref?: string
	$defs?: Record<string, JsonSchema>
	definitions?: Record<string, JsonSchema>
	title?: string
	description?: string
	type?: string | string[]
	enum?: unknown[]
	const?: unknown
	default?: unknown
	format?: string
	properties?: Record<string, JsonSchema>
	required?: string[]
	additionalProperties?: boolean | JsonSchema
	items?: JsonSchema | JsonSchema[]
	prefixItems?: JsonSchema[]
	minItems?: number
	maxItems?: number
	minLength?: number
	maxLength?: number
	pattern?: string
	minimum?: number
	maximum?: number
	exclusiveMinimum?: number
	exclusiveMaximum?: number
	multipleOf?: number
	anyOf?: JsonSchema[]
	oneOf?: JsonSchema[]
	allOf?: JsonSchema[]
	not?: JsonSchema
}

export const jsonSchemaSchema: z.ZodType<JsonSchema> = z.lazy(() =>
	z.object({
		$schema: z.string().optional(),
		$ref: z.string().optional(),
		$defs: z.record(z.string(), jsonSchemaSchema).optional(),
		definitions: z.record(z.string(), jsonSchemaSchema).optional(),
		title: z.string().optional(),
		description: z.string().optional(),
		type: z.union([z.string(), z.array(z.string())]).optional(),
		enum: z.array(z.unknown()).optional(),
		const: z.unknown().optional(),
		default: z.unknown().optional(),
		format: z.string().optional(),
		properties: z.record(z.string(), jsonSchemaSchema).optional(),
		required: z.array(z.string()).optional(),
		additionalProperties: z.union([z.boolean(), jsonSchemaSchema]).optional(),
		items: z.union([jsonSchemaSchema, z.array(jsonSchemaSchema)]).optional(),
		prefixItems: z.array(jsonSchemaSchema).optional(),
		minItems: z.number().optional(),
		maxItems: z.number().optional(),
		minLength: z.number().optional(),
		maxLength: z.number().optional(),
		pattern: z.string().optional(),
		minimum: z.number().optional(),
		maximum: z.number().optional(),
		exclusiveMinimum: z.number().optional(),
		exclusiveMaximum: z.number().optional(),
		multipleOf: z.number().optional(),
		anyOf: z.array(jsonSchemaSchema).optional(),
		oneOf: z.array(jsonSchemaSchema).optional(),
		allOf: z.array(jsonSchemaSchema).optional(),
		not: jsonSchemaSchema.optional(),
	}),
)
