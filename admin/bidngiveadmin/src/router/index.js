import { createRouter, createWebHistory } from 'vue-router'
import Login from '@/views/Login.vue'
import Dashboard from '@/views/Dashboard.vue'
import PendingBids from '@/views/PendingBids.vue'
import Withdrawals from '@/views/Withdrawals.vue'
import MergeSettings from '@/views/MergeSettings.vue'
import CreateInvestment from '@/views/CreateInvestment.vue'
import CancelInvestment from '@/views/CancelInvestment.vue'
import UserManagement from '@/views/UserManagement.vue'
import UserPage from '@/views/UserPage.vue'

const routes = [
  { path: '/', name: 'Login', component: Login },
  { path: '/dashboard', name: 'Dashboard', component: Dashboard },
  { path: '/pending-bids', name: 'PendingBids', component: PendingBids },
  { path: '/withdrawals', name: 'Withdrawals', component: Withdrawals },
  { path: '/merge-settings', name: 'MergeSettings', component: MergeSettings },
  { path: '/create-investment', name: 'CreateInvestment', component: CreateInvestment },
  { path: '/cancel-investment', name: 'CancelInvestment', component: CancelInvestment },
  { path: '/user-details', name: 'UserManagement',component: UserManagement},
  { path: '/user-page', name: 'UserPage',component: UserPage},
  ]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
