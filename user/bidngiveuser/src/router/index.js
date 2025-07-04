import { createRouter, createWebHashHistory } from 'vue-router'
import axios from 'axios'

const router = createRouter({
  history: createWebHashHistory(),
  routes: [
    {
      path: '/signup',
      name: 'signup',
      component: () => import('@/views/SignupView.vue'),
    },
    {
      path: '/',
      name: 'login',
      component: () => import('@/views/LoginView.vue'),
    },
    {
      path: '/terms-of-service',
      name: 'tos',
      component: () => import('@/views/TermsOfService.vue'),
    },
    {
      path: '/otp',
      name: 'otp',
      component: () => import('@/views/OneTimePassword.vue'),
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: () => import('@/views/DashBoardView.vue'),
    },
    {
      path: '/bid',
      name: 'bid',
      component: () => import('@/views/BidsView.vue'),
    },
    {
      path: '/merge-info',
      name: 'merge-info',
      component: () => import('@/views/MergedView.vue'),
    },
    {
      path: '/withdraw',
      name: 'withdraw',
      component: () => import('@/views/WithdrawView.vue'),
    },
    {
      path: '/profile',
      name: 'profile',
      component: () => import('@/views/ProfileView.vue'),
    },
    {
      path: '/banned',
      name: 'banned',
      component: () => import('@/views/BannedView.vue'),
    },
    {
      path: '/:pathMatch(.*)*',
      name: '404',
      component: () => import('@/views/NotfoundView.vue'),
    },
    {
      path: '/create-bid',
      name: 'create-bid',
      component: () => import('@/views/CreateBidView.vue'),
    },{
      path: '/referrals',
      name: 'referrals',
      component: () => import('@/views/ReferralView.vue')
    }
  ]
})

router.beforeEach(async (to, from, next) => {
  const token = localStorage.getItem('access_token')

  const publicRoutes = ['login', 'signup', 'otp', 'tos', '404', 'banned']
  if (publicRoutes.includes(to.name)) {
    return next()
  }

  if (!token) {
    return next({ name: 'login' })
  }

  try {
    const userRes = await axios.get('https://bidngive.onrender.com/api/accounts/me/', {
      headers: { Authorization: `Bearer ${token}` }
    })

    const user = userRes.data
    if (user.is_disabled) {
      return next({ name: 'banned' })
    }

    return next()
  } catch (error) {
    console.error('User auth check failed:', error)
    localStorage.removeItem('access_token')
    return next({ name: 'login' })
  }
})

export default router
