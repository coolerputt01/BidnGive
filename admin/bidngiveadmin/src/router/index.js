import { createRouter, createWebHashHistory } from 'vue-router'
import Login from '@/views/Login.vue'
import Dashboard from '@/views/Dashboard.vue'
import CreateInvestment from '@/views/CreateInvestment.vue'
import UserManagement from '@/views/UserManagement.vue'
import UserPage from '@/views/UserPage.vue'
import ChangeLogins from '@/views/ChangeLogins.vue'
import ManualMerging from '@/views/ManualMerging.vue'
import AllBidsView from '@/views/AllBidsView.vue'
import CreateWithdrawal from '@/views/CreateWithdrawal.vue'
import MergeSettings from '@/views/MergeSettings.vue'

const routes = [
  { path: '/', name: 'Login', component: Login },
  { path: '/dashboard', name: 'Dashboard', component: Dashboard },
  { path: '/manual-merging', name: 'ManualMerging', component: ManualMerging },
  { path: '/change-logins', name: 'ChangeLogins', component: ChangeLogins },
  { path: '/create-investment', name: 'CreateInvestment', component: CreateInvestment },
  { path: '/all-bids', name: 'allBids', component: AllBidsView },
  { path: '/user-details', name: 'UserManagement',component: UserManagement},
  { path: '/user-page', name: 'UserPage',component: UserPage},
  { path: '/create-withdrawal', name:"CreateWithdrawal",component: CreateWithdrawal},
  { path: '/merge-settings',name:'MergeSettings',component: MergeSettings},
  {
      path: '/:pathMatch(.*)*',
      name: '404',
      component: () => import('@/views/NotfoundView.vue'),
    },
  ]

const router = createRouter({
  history: createWebHashHistory(),
  routes,
})

export default router
