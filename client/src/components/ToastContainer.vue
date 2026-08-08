<script setup lang="ts">
import { useToast } from '../composables/toast'

const { toasts, dismiss } = useToast()
</script>

<template>
  <div class="toast-container">
    <transition-group name="toast">
      <div v-for="toast in toasts" :key="toast.id" class="toast" :class="`toast--${toast.kind}`" @click="dismiss(toast.id)">
        {{ toast.message }}
      </div>
    </transition-group>
  </div>
</template>

<style scoped>
.toast-container {
  position: fixed;
  bottom: 1.25rem;
  right: 1.25rem;
  z-index: 1000;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  max-width: 22rem;
}

.toast {
  padding: 0.75rem 1rem 0.75rem 0.85rem;
  border-radius: var(--radius-lg);
  border: 1px solid var(--border);
  border-left: 3px solid var(--text-faint);
  background: var(--surface);
  color: var(--text);
  font-size: 0.85rem;
  box-shadow: var(--shadow-2);
  cursor: pointer;
  word-break: break-word;
}

.toast--success {
  border-left-color: var(--sticker-green);
}

.toast--error {
  border-left-color: var(--danger);
}

.toast--info {
  border-left-color: var(--primary);
}

.toast-enter-active,
.toast-leave-active {
  transition: all 0.2s ease;
}

.toast-enter-from,
.toast-leave-to {
  opacity: 0;
  transform: translateY(8px);
}
</style>
