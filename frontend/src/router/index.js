import Vue from 'vue';
import VueRouter from 'vue-router';
import UserAuth from '../components/auth/UserAuth.vue';
import WorkLog from '../components/logs/WorkLog.vue';
import AdminDashboard from '../components/dashboard/AdminDashboard.vue';
import MyAccount from '../components/dashboard/MyAccount.vue';
import UserManagement  from '../components/dashboard/UserManagement.vue';
import WorkLogs from '../components/dashboard/WorkLogs.vue';

Vue.use(VueRouter);

const routes = [
  { path: '/', redirect: '/login' },   // Redirect to login by default
  { path: '/login', component: UserAuth },
  { path: '/worklog', component: WorkLog },
  { 
    path: '/admin', 
    component: AdminDashboard, 
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  { path: '/admin/account', component: MyAccount, meta: { requiresAuth: true, requiresAdmin: true } },
  { path: '/admin/users', component: UserManagement, meta: { requiresAuth: true, requiresAdmin: true } },
  { path: '/admin/worklogs', component: WorkLogs, meta: { requiresAuth: true, requiresAdmin: true } },
  { path: '*', redirect: '/login' }  // Catch-all unknown routes
];

const router = new VueRouter({
  mode: 'history',
  routes
});

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("token");
  const isAdmin = localStorage.getItem("role") === "admin";

  if (!token && to.path !== '/login') {
    // Redirect unauthenticated users to login page
    next("/login");
  } else if (token && to.path === '/login') {
    // Redirect authenticated users away from login page
    next("/worklog");
  } else if (to.meta.requiresAuth && !token) {
    // Protect authenticated routes
    next("/login");
  } else if (to.meta.requiresAdmin && !isAdmin) {
    // Protect admin routes
    next("/login");
  } else {
    next();
  }
});

export default router;
