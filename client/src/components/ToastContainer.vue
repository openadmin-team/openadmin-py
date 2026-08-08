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
  padding: 0.75rem 1rem;
  border-radius: 0.5rem;
  color: white;
  font-size: 0.875rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  cursor: pointer;
  word-break: break-word;
}

.toast--success {
  background: #16a34a;
}

.toast--error {
  background: #dc2626;
}

.toast--info {
  background: #334155;
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
