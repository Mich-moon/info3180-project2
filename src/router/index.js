import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue')
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/RegisterView.vue')
    },
    {
      path: '/logout',
      name: 'logout',
      component: HomeView
    },
    {
      path: '/cars/new',
      name: 'addcar',
      component: () => import('../views/AddCarView.vue')
    },
    {
      path: '/cars/:car_id',
      name: 'car',
      component: () => import('../views/CarView.vue')
    },
    {
      path: '/explore',
      name: 'explore',
      component: () => import('../views/ExploreView.vue')
    },
    {
      path: '/users/:user_id',
      name: 'profile',
      component: () => import('../views/ProfileView.vue'),
      props: true
    }
  ]
})

export default router
