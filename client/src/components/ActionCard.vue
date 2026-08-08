<script setup lang="ts">
import { computed, reactive, ref } from 'vue'
import { ApiError, callComponent } from '../api/client'
import { useToast } from '../composables/toast'
import type { ActionComponent } from '../types/spec'
import { getObjectFields } from '../utils/jsonSchema'
import { extractResult } from '../utils/response'
import CardShell from './CardShell.vue'
import Modal from './Modal.vue'
import ResultBlock from './ResultBlock.vue'
import SchemaFields from './SchemaFields.vue'

const props = defineProps<{
  sectionId: string
  pageId: string
  component: ActionComponent
}>()

const { success, error: toastError } = useToast()

const isOpen = ref(false)

const queryValues = reactive<Record<string, unknown>>({})
const bodyValues = reactive<Record<string, unknown>>({})
const formValues = reactive<Record<string, unknown>>({})

const queryFields = computed(() => getObjectFields(props.component.query))
const bodyFields = computed(() => getObjectFields(props.component.body))
const formFields = computed(() => getObjectFields(props.component.form))
const hasFields = computed(() => queryFields.value.length + bodyFields.value.length + formFields.value.length > 0)
const isDestructive = computed(() => props.component.method === 'delete')

const running = ref(false)
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

async function run() {
  inlineError.value = null
  const missing = missingRequired()
  if (missing) {
    inlineError.value = missing
    return
  }

  running.value = true
  try {
    const hasFormData = formFields.value.length > 0
    const response = await callComponent(props.sectionId, props.pageId, props.component, {
      query: Object.keys(queryValues).length ? queryValues : undefined,
      jsonBody: !hasFormData && bodyFields.value.length ? bodyValues : undefined,
      formData: hasFormData ? buildFormData() : undefined,
    })

    const extracted = extractResult(response)
    result.value = extracted.table
    resultMessage.value = extracted.message ?? null
    success(extracted.message ?? `${props.component.name} ran successfully`)
  } catch (err) {
    const message = err instanceof ApiError ? err.message : err instanceof Error ? err.message : String(err)
    inlineError.value = message
    toastError(message)
  } finally {
    running.value = false
  }
}
</script>

<template>
  <CardShell :icon="component.icon" :color="component.color" :title="component.name" :description="component.description">
    <button
      type="button"
      class="primary-button"
      :class="{ 'primary-button--danger': isDestructive }"
      @click="isOpen = true"
    >
      {{ hasFields ? 'Configure & run' : 'Open' }}
    </button>
    <p v-if="resultMessage" class="form-message">Last: {{ resultMessage }}</p>
  </CardShell>

  <Modal v-model="isOpen" :title="component.name">
    <p v-if="isDestructive" class="danger-notice">This action may not be reversible.</p>

    <form @submit.prevent="run">
      <SchemaFields
        v-if="queryFields.length"
        :schema="component.query"
        :model-value="queryValues"
        @update:model-value="(v) => Object.assign(queryValues, v)"
      />
      <SchemaFields
        v-if="bodyFields.length"
        :schema="component.body"
        @update:model-value="(v) => Object.assign(bodyValues, v)"
        :model-value="bodyValues"
      />
      <SchemaFields
        v-if="formFields.length"
        :schema="component.form"
        :model-value="formValues"
        @update:model-value="(v) => Object.assign(formValues, v)"
      />

      <p v-if="inlineError" class="form-error">{{ inlineError }}</p>

      <button type="submit" class="primary-button" :class="{ 'primary-button--danger': isDestructive }" :disabled="running">
        {{ running ? 'Running…' : 'Run' }}
      </button>
    </form>

    <p v-if="resultMessage" class="form-message">{{ resultMessage }}</p>
    <ResultBlock v-if="result !== null && result !== undefined" :data="result" />
  </Modal>
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

.danger-notice {
  color: #dc2626;
  font-size: 0.8rem;
  margin: 0 0 0.8rem;
  padding: 0.5rem 0.65rem;
  background: rgba(220, 38, 38, 0.1);
  border-radius: 0.4rem;
}
</style>
