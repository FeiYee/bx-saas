import { createRouter, createWebHistory } from 'vue-router'
import MainView from '../views/MainView.vue'
import LoginView from '../views/LoginView.vue'
import HomeView from '../views/HomeView.vue'
import DownloadView from '../views/DownloadView.vue'
import context from '../core/context.js'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'main',
      component: MainView,
      children: [
        {path: '', name: 'home', component: HomeView, alias: '/'},
        {path: 'download', component: DownloadView},
      ],
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    }
  ]
})

router.beforeEach(async (to, from) => {

  let token = context.getToken()
  if (!token && to.name !== 'login') {
    return { name: 'login' }
  }
})

export default router
