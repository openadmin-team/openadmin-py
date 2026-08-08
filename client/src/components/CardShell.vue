<script setup lang="ts">
import { computed } from 'vue'
import { colorToHex } from '../utils/colors'
import { resolveIcon } from '../utils/icons'

const props = defineProps<{
  icon?: string | null
  color?: string | null
  title: string
  description?: string | null
  wide?: boolean
}>()

const IconComponent = computed(() => resolveIcon(props.icon))
const accent = computed(() => colorToHex(props.color))
</script>

<template>
  <div class="card" :class="{ 'card--wide': wide }" :style="{ '--accent': accent }">
    <div class="card__header">
      <div class="card__title-row">
        <span v-if="IconComponent" class="card__icon">
          <component :is="IconComponent" :size="18" />
        </span>
        <h3>{{ title }}</h3>
      </div>
      <div v-if="$slots.actions" class="card__actions">
        <slot name="actions" />
      </div>
    </div>
    <p v-if="description" class="card__description">{{ description }}</p>
    <div class="card__body">
      <slot />
    </div>
  </div>
</template>

<style scoped>
.card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 0.75rem;
  padding: 1rem 1.1rem;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03);
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.card--wide {
  grid-column: 1 / -1;
}

.card__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.5rem;
}

.card__title-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  min-width: 0;
}

.card__icon {
  color: var(--accent);
  display: inline-flex;
  flex-shrink: 0;
}

.card h3 {
  margin: 0;
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--text);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.card__description {
  margin: 0.2rem 0 0;
  font-size: 0.78rem;
  color: var(--text-muted);
}

.card__body {
  margin-top: 0.75rem;
  min-width: 0;
}
</style>
