<script setup lang="ts">
import { onMounted } from 'vue'
import Sidebar from './components/Sidebar.vue'
import ToastContainer from './components/ToastContainer.vue'
import { useSpec } from './composables/spec'

const { load } = useSpec()

onMounted(load)
</script>

<template>
  <div class="app-shell">
    <Sidebar />
    <main class="app-content">
      <RouterView />
    </main>
    <ToastContainer />
  </div>
</template>

<style scoped>
.app-shell {
  display: flex;
  min-height: 100vh;
}

.app-content {
  flex: 1;
  padding: 1.5rem 1.75rem 3rem;
  min-width: 0;
}
</style>
