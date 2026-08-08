<script setup lang="ts">
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useSpec } from '../composables/spec'

const router = useRouter()
const { state, load } = useSpec()

onMounted(async () => {
  await load()
  const firstSection = state.spec?.sections[0]
  const firstPage = firstSection?.pages[0]
  if (firstSection && firstPage) {
    router.replace({ name: 'page', params: { sectionId: firstSection.id, pageId: firstPage.id } })
  }
})
</script>

<template>
  <div class="home-status">
    <p v-if="state.loading">Loading admin panel…</p>
    <p v-else-if="state.error">Failed to load spec.json: {{ state.error }}</p>
    <p v-else-if="state.spec && state.spec.sections.length === 0">This admin panel has no sections configured.</p>
  </div>
</template>

<style scoped>
.home-status {
  padding: 2rem;
  color: var(--text-muted);
}
</style>
