import { createRouter, createWebHashHistory } from 'vue-router'
import Home from '../views/Home.vue'
import PageView from '../views/PageView.vue'

export const router = createRouter({
  history: createWebHashHistory(),
  routes: [
    { path: '/', name: 'home', component: Home },
    { path: '/:sectionId/:pageId', name: 'page', component: PageView },
  ],
})
