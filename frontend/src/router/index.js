import Vue from 'vue'
import VueRouter from 'vue-router'
import HomeView from '../views/HomeView.vue'

import Auth from '@/components/pages/Auth'
import Application from '@/components/pages/Application'
import SingleLoanFund from '@/components/pages/SingleLoanFund'
import Admin from '@/components/pages/Admin'
Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'home',
    component: Application
  },
  {
    path: '/loan-fund',
    name: 'loan-fund',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/LoanFundView.vue')
  },
  {
    path: '/payment/:id',
    name: 'payment',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/PaymentView.vue')
  },
  {
    path: '/auth',
    name: 'Auth',
    component: Auth
  },
  {
    path: '/loan/:id',
    name: 'Single-Loan',
    component: SingleLoanFund
  },
  {
    path: '/admin',
    name: 'Admin',
    component: Admin
  }
]

const router = new VueRouter({
  routes
})

export default router
