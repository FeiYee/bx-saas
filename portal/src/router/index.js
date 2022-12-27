import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import AboutView from '../views/AboutView.vue'

import DatumView from '../views/datum/DatumView.vue'
import KeywordView from '../views/search/KeywordView.vue'
import UserView from '../views/system/UserView.vue'
import OrgView from '../views/system/OrgView.vue'
import OrgUserView from '../views/system/OrgUserView.vue'

import context from '../core/context.js'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      children: [
        {path: '', name: 'home', component: AboutView, alias: '/'},
        {path: '/datum/datum', name: 'Datum', component: DatumView},
        {path: '/search/keyword', name: 'Keyword', component: KeywordView},
        {path: '/system/user', name: 'User', component: UserView},
        {path: '/system/org', name: 'Org', component: OrgView},
        {path: '/system/orguser', name: 'OrgUser', component: OrgUserView},
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
