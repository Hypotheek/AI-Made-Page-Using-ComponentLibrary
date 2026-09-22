import { createRouter, createWebHistory } from 'vue-router'
import Overview from '../pages/Overview.vue'
import Sales from '../pages/Sales.vue'
import Customers from '../pages/Customers.vue'
import Settings from '../pages/Settings.vue'

const routes = [
  { path: '/', name: 'Overview', component: Overview },
  { path: '/sales', name: 'Sales', component: Sales },
  { path: '/customers', name: 'Customers', component: Customers },
  { path: '/settings', name: 'Settings', component: Settings },
]

export default createRouter({
  history: createWebHistory(),
  routes,
})
