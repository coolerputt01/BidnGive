import { createRouter, createWebHistory } from 'vue-router';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/signup',
      name: 'signup',
      component: () => import('../views/SignupView.vue'),
    },
    {
      path: '/',
      name: 'login',
      component: () => import('../views/LoginView.vue'),
    },
    {
      path: '/terms-of-service',
      name: 'tos',
      component: () => import('../views/TermsOfService.vue'),
    },
    {
      path: '/otp',
      name: 'otp',
      component: () => import('../views/OneTimePassword.vue'),
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: () => import('../views/DashboardView.vue'),
    },
    {
      path: '/bid',
      name: 'bid',
      component: () => import('../views/BidsView.vue'),
    },
    {
      path: '/auction',
      name: 'auction',
      component: () => import('../views/AuctionView.vue'),
    },
    {
      path: '/withdraw',
      name: 'withdraw',
      component: () => import('../views/WithdrawView.vue'),
    },
    {
      path: '/profile',
      name: 'profile',
      component: () => import('../views/ProfileView.vue'),
    },
    {
      path: '/:pathMatch(.*)*',
      name: '404',
      component: () => import('../views/NotFoundView.vue'),
    }
  ],
});

export default router
