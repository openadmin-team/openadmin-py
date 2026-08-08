<script setup lang="ts">
import { marked } from 'marked'
import { computed, onMounted, ref } from 'vue'
import { callComponent } from '../api/client'
import type { MarkdownComponent } from '../types/spec'
import { sanitizeHtml } from '../utils/sanitizeHtml'
import CardShell from './CardShell.vue'

const props = defineProps<{
  sectionId: string
  pageId: string
  component: MarkdownComponent
}>()

const loading = ref(true)
const error = ref<string | null>(null)
const content = ref('')
const icon = ref<string | null | undefined>(props.component.icon)
const color = ref<string | null | undefined>(props.component.color)

async function load() {
  loading.value = true
  error.value = null
  try {
    const response = await callComponent(props.sectionId, props.pageId, props.component)
    if (response && typeof response === 'object' && 'content' in (response as Record<string, unknown>)) {
      const wrapped = response as { content: string; icon?: string; color?: string }
      content.value = wrapped.content
      if (wrapped.icon) icon.value = wrapped.icon
      if (wrapped.color) color.value = wrapped.color
    } else {
      content.value = String(response ?? '')
    }
  } catch (err) {
    error.value = err instanceof Error ? err.message : String(err)
  } finally {
    loading.value = false
  }
}

const html = computed(() => sanitizeHtml(marked.parse(content.value, { async: false }) as string))

onMounted(load)
</script>

<template>
  <CardShell :icon="icon" :color="color" :title="component.name" :description="component.description" wide>
    <p v-if="loading" class="markdown-status">Loading…</p>
    <p v-else-if="error" class="markdown-status markdown-status--error">{{ error }}</p>
    <div v-else class="markdown-body" v-html="html" />
  </CardShell>
</template>

<style scoped>
.markdown-status {
  color: var(--text-muted);
  font-size: 0.85rem;
}

.markdown-status--error {
  color: var(--danger);
}

.markdown-body {
  font-size: 0.88rem;
  line-height: 1.55;
  color: var(--text);
}

.markdown-body :deep(h1),
.markdown-body :deep(h2),
.markdown-body :deep(h3) {
  margin-top: 1.2em;
  margin-bottom: 0.4em;
}

.markdown-body :deep(p) {
  margin: 0.5em 0;
}

.markdown-body :deep(code) {
  background: var(--surface-muted);
  padding: 0.1em 0.35em;
  border-radius: 0.3em;
  font-size: 0.85em;
}

.markdown-body :deep(pre) {
  background: var(--surface-muted);
  padding: 0.75em;
  border-radius: 0.5em;
  overflow-x: auto;
}

.markdown-body :deep(ul),
.markdown-body :deep(ol) {
  padding-left: 1.4em;
}
</style>
