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
      path: '/merge-info',
      name: 'merge-info',
      component: () => import('../views/MergedView.vue'),
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

router.beforeEach(async (to, from, next) => {
  const token = localStorage.getItem('access_token');
  
  // Skip token check for some routes like login/signup
  if (['/login', '/signup', '/otp'].includes(to.path)) {
    return next();
  }

  // If token doesn't exist or is invalid, redirect to login
  if (!token) {
    return next({ name: 'login' });
  }

  try {
    // Try to verify token by hitting a protected API endpoint
    const response = await axios.get('https://bidngive.onrender.com/api/wallet/balance', {
      headers: { Authorization: `Bearer ${token}` }
    });

    if (response.status === 200) {
      return next(); // Token is valid, proceed to the route
    }
  } catch (error) {
    console.error('Token verification failed:', error);
  }

  // If token is invalid, remove from storage and redirect to login
  localStorage.removeItem('access_token');
  return next({ name: 'login' });
});

export default router
