export type HttpMethod = 'get' | 'post' | 'put' | 'patch' | 'delete' | 'head'

export type Color = string
export type Icon = string

export interface JsonSchema {
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

export interface ApiError {
  message: string
}

interface ComponentBase {
  id: string
  name: string
  description: string | null
  method: HttpMethod
  form: JsonSchema | null
  body: JsonSchema | null
  query: JsonSchema | null
}

export interface StatComponent extends ComponentBase {
  type: 'stat'
  icon: Icon | null
  color: Color | null
}

export interface TableComponent extends ComponentBase {
  type: 'table'
  icon: Icon | null
  color: Color | null
  is_hidden: boolean
}

export interface FieldConfig {
  reference?: string | null
  reference_field?: string
  icon?: Icon
  color?: Color
}

export interface FormComponent extends ComponentBase {
  type: 'form'
  fields: Record<string, FieldConfig> | null
  icon: Icon | null
  color: Color | null
  is_hidden: boolean
}

export interface ActionComponent extends ComponentBase {
  type: 'action'
  icon: Icon | null
  color: Color | null
  is_hidden: boolean
}

export interface MarkdownComponent extends ComponentBase {
  type: 'markdown'
  color: Color | null
  icon: Icon | null
}

export interface ChartConfigValue {
  name?: string
  color?: Color
  icon?: Icon
}

export interface BarChartComponent extends ComponentBase {
  type: 'bar-chart'
  config: Record<string, ChartConfigValue> | null
  data_key: string | null
  icon: Icon | null
  color: Color | null
  caption: string | null
  caption_description: string | null
  caption_icon: Icon | null
}

export interface PieChartComponent extends ComponentBase {
  type: 'pie-chart'
  config: Record<string, ChartConfigValue> | null
  icon: Icon | null
  name_key: string | null
  value_key: string | null
  color: Color | null
  caption: string | null
  caption_description: string | null
  caption_icon: Icon | null
}

export interface AreaChartComponent extends ComponentBase {
  type: 'area-chart'
  icon: Icon | null
  color: Color | null
}

export interface LineChartComponent extends ComponentBase {
  type: 'line-chart'
  icon: Icon | null
  color: Color | null
}

export type Component =
  | StatComponent
  | TableComponent
  | AreaChartComponent
  | BarChartComponent
  | LineChartComponent
  | PieChartComponent
  | ActionComponent
  | FormComponent
  | MarkdownComponent

export interface Page {
  id: string
  name: string
  description: string | null
  icon: Icon | null
  components: Component[]
}

export interface Section {
  id: string
  name: string
  description: string | null
  icon: Icon | null
  pages: Page[]
}

export interface Spec {
  version: string
  name: string
  id: string
  description?: string | null
  sections: Section[]
}

export interface TableResponseWrapper {
  data: unknown
  icon?: Icon
  color?: Color
}

export interface ActionOrFormResponse {
  icon?: Icon
  color?: Color
  toast?: string
  table?: unknown
  message?: string
}
