<script setup lang="ts">
import { onBeforeUnmount, watch } from 'vue'

const props = defineProps<{
  modelValue: boolean
  title: string
}>()

const emit = defineEmits<{ 'update:modelValue': [value: boolean] }>()

function close() {
  console.log('[Modal] close() called, current modelValue =', props.modelValue)
  emit('update:modelValue', false)
}

function onKeydown(event: KeyboardEvent) {
  if (event.key === 'Escape') close()
}

watch(
  () => props.modelValue,
  (open) => {
    document.documentElement.style.overflow = open ? 'hidden' : ''
    if (open) window.addEventListener('keydown', onKeydown)
    else window.removeEventListener('keydown', onKeydown)
  },
  { immediate: true },
)

onBeforeUnmount(() => {
  window.removeEventListener('keydown', onKeydown)
  document.documentElement.style.overflow = ''
})
</script>

<template>
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="modelValue" class="modal-backdrop" @mousedown.self="close">
        <div class="modal-dialog" role="dialog" aria-modal="true" :aria-label="title">
          <header class="modal-header">
            <h2>{{ title }}</h2>
            <button type="button" class="modal-close" aria-label="Close" @click="close">✕</button>
          </header>
          <div class="modal-body">
            <slot />
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: flex-start;
  justify-content: center;
  padding: 5vh 1rem;
  z-index: 1100;
  overflow-y: auto;
}

.modal-dialog {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 0.75rem;
  width: 100%;
  max-width: 32rem;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.25);
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 1.1rem;
  border-bottom: 1px solid var(--border);
}

.modal-header h2 {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
}

.modal-close {
  border: none;
  background: transparent;
  color: var(--text-muted);
  font-size: 1rem;
  line-height: 1;
  padding: 0.2rem 0.4rem;
  border-radius: 0.3rem;
}

.modal-close:hover {
  background: var(--surface-muted);
  color: var(--text);
}

.modal-body {
  padding: 1.1rem;
}

.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.15s ease;
}

.modal-enter-active .modal-dialog,
.modal-leave-active .modal-dialog {
  transition: transform 0.15s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-from .modal-dialog,
.modal-leave-to .modal-dialog {
  transform: translateY(-8px);
}
</style>
