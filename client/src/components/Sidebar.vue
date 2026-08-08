<script setup lang="ts">
import { useRoute } from 'vue-router'
import { useSpec } from '../composables/spec'
import { resolveIcon } from '../utils/icons'

const route = useRoute()
const { state } = useSpec()

function isActive(sectionId: string, pageId: string): boolean {
  return route.params.sectionId === sectionId && route.params.pageId === pageId
}
</script>

<template>
  <aside class="sidebar">
    <div class="sidebar__brand">
      <span class="sidebar__brand-name">{{ state.spec?.name ?? 'Admin' }}</span>
      <span v-if="state.spec?.description" class="sidebar__brand-desc">{{ state.spec.description }}</span>
    </div>

    <nav class="sidebar__nav">
      <div v-for="section in state.spec?.sections ?? []" :key="section.id" class="sidebar__section">
        <div class="sidebar__section-title">
          <component :is="resolveIcon(section.icon)" v-if="resolveIcon(section.icon)" :size="14" />
          <span>{{ section.name }}</span>
        </div>
        <RouterLink
          v-for="page in section.pages"
          :key="page.id"
          :to="{ name: 'page', params: { sectionId: section.id, pageId: page.id } }"
          class="sidebar__link"
          :class="{ 'sidebar__link--active': isActive(section.id, page.id) }"
        >
          <component :is="resolveIcon(page.icon)" v-if="resolveIcon(page.icon)" :size="15" />
          <span>{{ page.name }}</span>
        </RouterLink>
      </div>
    </nav>
  </aside>
</template>

<style scoped>
.sidebar {
  width: 15.5rem;
  flex-shrink: 0;
  background: var(--surface);
  border-right: 1px solid var(--border);
  display: flex;
  flex-direction: column;
  height: 100vh;
  position: sticky;
  top: 0;
  overflow-y: auto;
}

.sidebar__brand {
  padding: 1.1rem 1.1rem 0.9rem;
  border-bottom: 1px solid var(--border);
}

.sidebar__brand-name {
  display: block;
  font-weight: 700;
  letter-spacing: -0.01em;
  font-size: 0.95rem;
  color: var(--text);
}

.sidebar__brand-desc {
  display: block;
  font-size: 0.72rem;
  color: var(--text-muted);
  margin-top: 0.2rem;
}

.sidebar__nav {
  padding: 0.75rem 0.6rem;
  flex: 1;
}

.sidebar__section {
  margin-bottom: 0.9rem;
}

.sidebar__section-title {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.3rem 0.6rem;
  font-size: 0.7rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-muted);
}

.sidebar__link {
  display: flex;
  align-items: center;
  gap: 0.55rem;
  padding: 0.45rem 0.6rem;
  margin: 1px 0;
  border-radius: var(--radius-sm);
  border-left: 2px solid transparent;
  font-size: 0.83rem;
  color: var(--text);
  text-decoration: none;
}

.sidebar__link:hover {
  background: var(--surface-muted);
}

.sidebar__link--active {
  background: var(--primary-soft);
  border-left-color: var(--primary);
  color: var(--primary);
  font-weight: 600;
}
</style>
