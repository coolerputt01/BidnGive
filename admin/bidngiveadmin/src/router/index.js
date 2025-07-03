import { createRouter, createWebHashHistory } from 'vue-router'
import Login from '@/views/Login.vue'
import Dashboard from '@/views/Dashboard.vue'
import CreateInvestment from '@/views/CreateInvestment.vue'
import CancelInvestment from '@/views/CancelInvestment.vue'
import UserManagement from '@/views/UserManagement.vue'
import UserPage from '@/views/UserPage.vue'
import ChangeLogins from '@/views/ChangeLogins.vue'
import ManualMerging from '@/views/ManualMerging.vue'

const routes = [
  { path: '/', name: 'Login', component: Login },
  { path: '/dashboard', name: 'Dashboard', component: Dashboard },
  { path: '/manual-merging', name: 'ManualMerging', component: ManualMerging },
  { path: '/change-logins', name: 'ChangeLogins', component: ChangeLogins },
  { path: '/create-investment', name: 'CreateInvestment', component: CreateInvestment },
  { path: '/cancel-investment', name: 'CancelInvestment', component: CancelInvestment },
  { path: '/user-details', name: 'UserManagement',component: UserManagement},
  { path: '/user-page', name: 'UserPage',component: UserPage},
  ]

const router = createRouter({
  history: createWebHashHistory(),
  routes,
})

export default router
