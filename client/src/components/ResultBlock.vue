<script setup lang="ts">
defineProps<{ data: unknown }>()
</script>

<template>
  <pre class="result-block">{{ JSON.stringify(data, null, 2) }}</pre>
</template>

<style scoped>
.result-block {
  margin: 0.6rem 0 0;
  padding: 0.6rem 0.75rem;
  background: var(--surface-muted);
  border-radius: var(--radius-md);
  font-size: 0.75rem;
  font-family: ui-monospace, monospace;
  max-height: 12rem;
  overflow: auto;
  white-space: pre-wrap;
  word-break: break-word;
}
</style>
