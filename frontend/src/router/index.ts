import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import CreateProjectView from '@/views/CreateProjectView.vue'
import CreateRequireView from '@/views/CreateRequireView.vue'
import CreateTaskView from '@/views/CreateTaskView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/create-project',
      name: 'create-project',
      component: CreateProjectView,
    },
    {
      path: '/create-require',
      name: 'create-require',
      component: CreateRequireView,
    },
    {
      path: '/create-task',
      name: 'create-task',
      component: CreateTaskView,
    },
  ],
})

export default router
