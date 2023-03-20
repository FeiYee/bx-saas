import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import MainView from '../views/MainView.vue'
import HomeView from '../views/HomeView.vue'
import DownloadView from '../views/DownloadView.vue'
import DocView from '../views/DocView.vue'
import PaperView from '../views/PaperView.vue'
import context from '../core/context.js'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'main',
      component: MainView,
      children: [
        {path: '', name: 'home', component: PaperView, alias: '/'},
        // {path: 'download', name: 'download', component: DownloadView},
        // {path: 'doc', name: 'doc', component: DocView},
        // {path: 'paper', name: 'paper', component: PaperView},
      ],
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView
    }
  ]
})

router.beforeEach(async (to, from) => {
  let token = context.getToken()
  if (!token && to.name === 'register') {
    return true
  }
  if (!token && to.name !== 'login') {
    return { name: 'login' }
  }
})

export default router
