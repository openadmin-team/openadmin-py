<script setup lang="ts">
import type { Component } from '../types/spec'
import CardShell from './CardShell.vue'

defineProps<{ component: Component }>()
</script>

<template>
  <CardShell :icon="'color' in component ? component.icon : null" :color="'color' in component ? component.color : null" :title="component.name" :description="component.description">
    <p class="unsupported">Component type "{{ component.type }}" is not yet supported by this client.</p>
  </CardShell>
</template>

<style scoped>
.unsupported {
  color: var(--text-muted);
  font-size: 0.82rem;
  font-style: italic;
}
</style>
