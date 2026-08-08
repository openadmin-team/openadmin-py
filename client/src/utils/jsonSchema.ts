import type { JsonSchema } from '../types/spec'

function lookupRef(root: JsonSchema, ref: string): JsonSchema | undefined {
  const path = ref.replace(/^#\//, '').split('/')
  let node: unknown = root
  for (const part of path) {
    if (node === undefined || node === null) return undefined
    node = (node as Record<string, unknown>)[part]
  }
  return node as JsonSchema | undefined
}

/** Resolve $ref (with sibling overrides) and single-item allOf wrappers. */
export function deref(root: JsonSchema, schema: JsonSchema | undefined | null): JsonSchema {
  if (!schema) return {}
  let current: JsonSchema = schema
  let guard = 0
  while (current.$ref && guard < 10) {
    guard++
    const target = lookupRef(root, current.$ref)
    if (!target) break
    const { $ref: _ref, ...rest } = current
    current = { ...target, ...rest }
  }
  if (current.allOf && current.allOf.length === 1) {
    const { allOf, ...rest } = current
    current = { ...deref(root, allOf[0]), ...rest }
  }
  return current
}

/** Unwrap a `anyOf: [T, {type: "null"}]` (Optional[T]) pattern down to T. */
export function unwrapNullable(
  root: JsonSchema,
  schema: JsonSchema,
): { schema: JsonSchema; nullable: boolean } {
  const resolved = deref(root, schema)
  if (resolved.anyOf && resolved.anyOf.length) {
    const branches = resolved.anyOf.map((s) => deref(root, s))
    const nullBranch = branches.some((b) => b.type === 'null')
    const nonNull = branches.filter((b) => b.type !== 'null')
    if (nonNull.length === 1) {
      const inner = unwrapNullable(root, nonNull[0])
      return { schema: inner.schema, nullable: nullBranch || inner.nullable }
    }
    if (nonNull.length > 1) {
      // real union - fall back to the first branch, still let it be nullable
      return { schema: nonNull[0], nullable: nullBranch }
    }
  }
  return { schema: resolved, nullable: false }
}

export type FieldWidget =
  | { kind: 'string'; format?: string }
  | { kind: 'integer' }
  | { kind: 'number' }
  | { kind: 'boolean' }
  | { kind: 'enum'; options: unknown[] }
  | { kind: 'file' }
  | { kind: 'array'; item: JsonSchema }
  | { kind: 'json' }

export function getFieldWidget(root: JsonSchema, schema: JsonSchema): FieldWidget {
  const resolved = deref(root, schema)
  if (resolved.enum && resolved.enum.length) return { kind: 'enum', options: resolved.enum }

  const type = Array.isArray(resolved.type)
    ? resolved.type.find((t) => t !== 'null')
    : resolved.type

  if (resolved.format === 'binary') return { kind: 'file' }

  switch (type) {
    case 'integer':
      return { kind: 'integer' }
    case 'number':
      return { kind: 'number' }
    case 'boolean':
      return { kind: 'boolean' }
    case 'array':
      return {
        kind: 'array',
        item: !Array.isArray(resolved.items) && resolved.items ? resolved.items : {},
      }
    case 'object':
      return { kind: 'json' }
    case 'string':
      return { kind: 'string', format: resolved.format }
    default:
      return { kind: 'string', format: resolved.format }
  }
}

export interface ResolvedField {
  name: string
  schema: JsonSchema
  widget: FieldWidget
  required: boolean
  nullable: boolean
  default: unknown
  description?: string
  title?: string
}

/** Flatten an object schema's `properties` into a list of resolved, ref-free fields. */
export function getObjectFields(schema: JsonSchema | null | undefined): ResolvedField[] {
  if (!schema) return []
  const root = schema
  const resolvedRoot = deref(root, schema)
  const properties = resolvedRoot.properties || {}
  const required = new Set(resolvedRoot.required || [])

  return Object.entries(properties).map(([name, propSchema]) => {
    const { schema: resolved, nullable } = unwrapNullable(root, propSchema)
    const hasDefault = 'default' in resolved || 'default' in deref(root, propSchema)
    const defaultValue = (deref(root, propSchema) as { default?: unknown }).default ?? resolved.default
    return {
      name,
      schema: resolved,
      widget: getFieldWidget(root, resolved),
      required: required.has(name),
      nullable,
      default: hasDefault ? defaultValue : undefined,
      description: resolved.description,
      title: resolved.title,
    }
  })
}

/** True if a query/body/form schema has any properties worth rendering as inputs. */
export function hasFields(schema: JsonSchema | null | undefined): boolean {
  return getObjectFields(schema).length > 0
}
