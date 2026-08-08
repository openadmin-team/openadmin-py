<script setup lang="ts">
import { computed } from 'vue'
import type { FieldConfig, JsonSchema } from '../types/spec'
import { getObjectFields } from '../utils/jsonSchema'
import { humanize } from '../utils/text'
import DynamicField from './DynamicField.vue'

const props = defineProps<{
  schema: JsonSchema | null | undefined
  fieldsConfig?: Record<string, FieldConfig> | null
  modelValue: Record<string, unknown>
}>()

const emit = defineEmits<{ 'update:modelValue': [value: Record<string, unknown>] }>()

const fields = computed(() => getObjectFields(props.schema))

function set(name: string, value: unknown) {
  emit('update:modelValue', { ...props.modelValue, [name]: value })
}
</script>

<template>
  <div v-for="field in fields" :key="field.name" class="form-field">
    <label :for="`field-${field.name}`">
      {{ field.title ?? humanize(field.name) }}
      <span v-if="field.required" class="required">*</span>
    </label>
    <DynamicField
      :field="field"
      :field-config="fieldsConfig?.[field.name]"
      :model-value="modelValue[field.name]"
      @update:model-value="(v) => set(field.name, v)"
    />
    <p v-if="field.description" class="field-hint">{{ field.description }}</p>
  </div>
</template>

<style scoped>
.form-field {
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
  margin-bottom: 0.9rem;
}

label {
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--text-muted);
}

.required {
  color: var(--danger);
}

.field-hint {
  font-size: 0.75rem;
  color: var(--text-muted);
  margin: 0;
}
</style>
