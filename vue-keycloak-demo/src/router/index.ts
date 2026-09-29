import {
  createRouter,
  createMemoryHistory,
  createWebHistory,
  createWebHashHistory
} from 'vue-router'

import keycloak from '../plugins/keycloak'

// Define routes manually since auto-routes is not available
const routes = [
  {
    path: '/',
    name: 'index',
    component: () => import('../App.vue')
  },
  {
    path: '/unauthorized',
    name: 'unauthorized',
    component: () => import('../App.vue')
  }
]

const Router = createRouter({
  scrollBehavior: () => ({ left: 0, top: 0 }),
  routes,
  history: createWebHistory()
})

// Router guard - main.ts already handles authentication with login-required
Router.beforeEach((to, from, next) => {
  // If Keycloak is not initialized yet, let main.ts handle it
  if (!keycloak.authenticated) {
    next()
    return
  }
  next()
})

export default Router
