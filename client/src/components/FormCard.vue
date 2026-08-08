<script setup lang="ts">
import { computed, reactive, ref } from 'vue'
import { ApiError, callComponent } from '../api/client'
import { useToast } from '../composables/toast'
import type { FormComponent } from '../types/spec'
import { getObjectFields } from '../utils/jsonSchema'
import { extractResult } from '../utils/response'
import CardShell from './CardShell.vue'
import ResultBlock from './ResultBlock.vue'
import SchemaFields from './SchemaFields.vue'

const props = defineProps<{
  sectionId: string
  pageId: string
  component: FormComponent
}>()

const { success, error: toastError } = useToast()

const queryValues = reactive<Record<string, unknown>>({})
const bodyValues = reactive<Record<string, unknown>>({})
const formValues = reactive<Record<string, unknown>>({})

const queryFields = computed(() => getObjectFields(props.component.query))
const bodyFields = computed(() => getObjectFields(props.component.body))
const formFields = computed(() => getObjectFields(props.component.form))

const submitting = ref(false)
const inlineError = ref<string | null>(null)
const result = ref<unknown>(null)
const resultMessage = ref<string | null>(null)

function missingRequired(): string | null {
  const all = [
    ...queryFields.value.map((f) => ({ f, values: queryValues })),
    ...bodyFields.value.map((f) => ({ f, values: bodyValues })),
    ...formFields.value.map((f) => ({ f, values: formValues })),
  ]
  for (const { f, values } of all) {
    if (f.required && !f.nullable) {
      const v = values[f.name]
      if (v === undefined || v === null || v === '') return `"${f.title ?? f.name}" is required`
    }
  }
  return null
}

function buildFormData(): FormData {
  const fd = new FormData()
  for (const [key, value] of Object.entries(formValues)) {
    if (value === undefined) continue
    if (value instanceof File) fd.append(key, value)
    else if (typeof value === 'object') fd.append(key, JSON.stringify(value))
    else fd.append(key, String(value))
  }
  return fd
}

async function submit() {
  inlineError.value = null
  const missing = missingRequired()
  if (missing) {
    inlineError.value = missing
    return
  }

  submitting.value = true
  try {
    const hasFormFields = formFields.value.length > 0
    const response = await callComponent(props.sectionId, props.pageId, props.component, {
      query: Object.keys(queryValues).length ? queryValues : undefined,
      jsonBody: !hasFormFields && bodyFields.value.length ? bodyValues : undefined,
      formData: hasFormFields ? buildFormData() : undefined,
    })

    const extracted = extractResult(response)
    result.value = extracted.table
    resultMessage.value = extracted.message ?? null
    success(extracted.message ?? `${props.component.name} submitted`)

    for (const key of Object.keys(bodyValues)) delete bodyValues[key]
    for (const key of Object.keys(formValues)) delete formValues[key]
  } catch (err) {
    const message = err instanceof ApiError ? err.message : err instanceof Error ? err.message : String(err)
    inlineError.value = message
    toastError(message)
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <CardShell :icon="component.icon" :color="component.color" :title="component.name" :description="component.description">
    <form @submit.prevent="submit">
      <SchemaFields
        v-if="queryFields.length"
        :schema="component.query"
        :model-value="queryValues"
        @update:model-value="(v) => Object.assign(queryValues, v)"
      />
      <SchemaFields
        v-if="bodyFields.length"
        :schema="component.body"
        :fields-config="component.fields"
        :model-value="bodyValues"
        @update:model-value="(v) => Object.assign(bodyValues, v)"
      />
      <SchemaFields
        v-if="formFields.length"
        :schema="component.form"
        :fields-config="component.fields"
        :model-value="formValues"
        @update:model-value="(v) => Object.assign(formValues, v)"
      />

      <p v-if="inlineError" class="form-error">{{ inlineError }}</p>

      <button type="submit" class="primary-button" :disabled="submitting">
        {{ submitting ? 'Submitting…' : component.name }}
      </button>
    </form>

    <p v-if="resultMessage" class="form-message">{{ resultMessage }}</p>
    <ResultBlock v-if="result !== null && result !== undefined" :data="result" />
  </CardShell>
</template>

<style scoped>
.form-error {
  color: #dc2626;
  font-size: 0.8rem;
  margin: 0 0 0.6rem;
}

.form-message {
  color: var(--text-muted);
  font-size: 0.8rem;
  margin: 0.6rem 0 0;
}
</style>
