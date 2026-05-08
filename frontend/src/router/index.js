import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Bookshelf',
    component: () => import('../views/Bookshelf.vue')
  },
  {
    path: '/novel/:id',
    name: 'NovelDetail',
    component: () => import('../views/NovelDetail.vue')
  },
  {
    path: '/download',
    name: 'DownloadCenter',
    component: () => import('../views/DownloadCenter.vue')
  },
  {
    path: '/rules',
    name: 'RuleConfig',
    component: () => import('../views/RuleConfig.vue')
  },
  {
    path: '/settings',
    name: 'Settings',
    component: () => import('../views/Settings.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
