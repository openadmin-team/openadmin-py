<script setup lang="ts">
import { computed } from 'vue'
import type { FieldConfig } from '../types/spec'
import type { ResolvedField } from '../utils/jsonSchema'
import MultiReferencePicker from './MultiReferencePicker.vue'
import ReferencePicker from './ReferencePicker.vue'

const props = defineProps<{
  field: ResolvedField
  fieldConfig?: FieldConfig | null
  modelValue: unknown
}>()

const emit = defineEmits<{ 'update:modelValue': [value: unknown] }>()

const reference = computed(() => props.fieldConfig?.reference ?? null)
const isMultiReference = computed(() => reference.value !== null && props.field.widget.kind === 'array')
const inputId = computed(() => `field-${props.field.name}`)

function update(value: unknown) {
  emit('update:modelValue', value)
}

function onInput(event: Event) {
  update((event.target as HTMLInputElement).value)
}

function onNumberInput(event: Event) {
  const raw = (event.target as HTMLInputElement).value
  update(raw === '' ? undefined : Number(raw))
}

function onCheckbox(event: Event) {
  update((event.target as HTMLInputElement).checked)
}

function onSelect(event: Event) {
  update((event.target as HTMLSelectElement).value)
}

function onFile(event: Event) {
  const file = (event.target as HTMLInputElement).files?.[0]
  update(file ?? undefined)
}

function onJsonInput(event: Event) {
  const raw = (event.target as HTMLTextAreaElement).value
  if (raw.trim() === '') {
    update(undefined)
    return
  }
  try {
    update(JSON.parse(raw))
  } catch {
    // keep raw text until it becomes valid JSON; submit-time validation will surface the error
    update(raw)
  }
}
</script>

<template>
  <MultiReferencePicker
    v-if="reference && isMultiReference"
    :reference-id="reference"
    :reference-field="fieldConfig?.reference_field ?? 'id'"
    :model-value="(modelValue as unknown[] | undefined)"
    :input-id="inputId"
    :input-name="field.name"
    @update:model-value="update"
  />

  <ReferencePicker
    v-else-if="reference"
    :reference-id="reference"
    :reference-field="fieldConfig?.reference_field ?? 'id'"
    :model-value="modelValue"
    :input-id="inputId"
    :input-name="field.name"
    @update:model-value="update"
  />

  <select v-else-if="field.widget.kind === 'enum'" :id="inputId" :name="field.name" :value="modelValue ?? ''" @change="onSelect">
    <option value="" disabled>select…</option>
    <option v-for="opt in field.widget.options" :key="String(opt)" :value="String(opt)">{{ opt }}</option>
  </select>

  <label v-else-if="field.widget.kind === 'boolean'" class="checkbox-field">
    <input :id="inputId" :name="field.name" type="checkbox" :checked="Boolean(modelValue)" @change="onCheckbox" />
    <span>{{ modelValue ? 'true' : 'false' }}</span>
  </label>

  <input
    v-else-if="field.widget.kind === 'integer'"
    :id="inputId"
    :name="field.name"
    type="number"
    step="1"
    :value="modelValue ?? ''"
    @input="onNumberInput"
  />

  <input
    v-else-if="field.widget.kind === 'number'"
    :id="inputId"
    :name="field.name"
    type="number"
    step="any"
    :value="modelValue ?? ''"
    @input="onNumberInput"
  />

  <input v-else-if="field.widget.kind === 'file'" :id="inputId" :name="field.name" type="file" @change="onFile" />

  <textarea
    v-else-if="field.widget.kind === 'array' || field.widget.kind === 'json'"
    :id="inputId"
    :name="field.name"
    rows="3"
    :value="typeof modelValue === 'string' ? modelValue : modelValue !== undefined ? JSON.stringify(modelValue) : ''"
    placeholder="JSON, e.g. [1, 2, 3]"
    @input="onJsonInput"
  />

  <input
    v-else-if="field.widget.format === 'date'"
    :id="inputId"
    :name="field.name"
    type="date"
    :value="modelValue ?? ''"
    @input="onInput"
  />

  <input
    v-else-if="field.widget.format === 'date-time'"
    :id="inputId"
    :name="field.name"
    type="datetime-local"
    :value="modelValue ?? ''"
    @input="onInput"
  />

  <input
    v-else-if="field.widget.format === 'password'"
    :id="inputId"
    :name="field.name"
    type="password"
    :value="modelValue ?? ''"
    @input="onInput"
  />

  <input v-else :id="inputId" :name="field.name" type="text" :value="modelValue ?? ''" @input="onInput" />
</template>

<style scoped>
.checkbox-field {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
</style>
