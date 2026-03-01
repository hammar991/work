import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import CreateProjectView from '@/views/CreateProjectView.vue'
import CreateRequireView from '@/views/CreateRequireView.vue'
import CreateTaskView from '@/views/CreateTaskView.vue'
import ListTaskView from '@/views/ListTaskView.vue'
import LoginView from '@/views/LoginView.vue'
import ListRequireView from '@/views/ListRequireView.vue'

const routerMeta = [
  {
    path: '/',
    name: '主页',
    component: HomeView,
  },
  {
    path: '/create-require',
    name: '创建需求',
    component: CreateRequireView,
  },
  {
    path: '/create-project',
    name: '创建项目',
    component: CreateProjectView,
  },
  {
    path: '/create-task',
    name: '创建任务',
    component: CreateTaskView,
  },
  {
    path: '/list-task',
    name: '任务列表',
    component: ListTaskView,
  },
  {
    path: '/login',
    name: '登录',
    component: LoginView,
  },
  {
    path: '/list-require',
    name: '需求列表',
    component: ListRequireView,
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: routerMeta,
})

export default router
export { routerMeta }
