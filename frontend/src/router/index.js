import Vue from 'vue';
import VueRouter from 'vue-router';
import UserAuth from '../components/UserAuth.vue';
import WorkLog from '@/components/WorkLog.vue';
import AdminDashboard from '@/components/admin/AdminDashboard.vue';
import MyAccount from '@/components/admin/MyAccount.vue';
import UserManagement  from '@/components/admin/UserManagement.vue';
import WorkLogs from '@/components/admin/WorkLogs.vue';

Vue.use(VueRouter);

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', component: UserAuth },
  { path: '/worklog', component: WorkLog },
  { path: "/admin", component: AdminDashboard, meta: { requiresAdmin: true }},
  { path: '/admin/account', component: MyAccount },
  { path: '/admin/users', component: UserManagement },
  { path: '/admin/logs', component: WorkLogs },
  { path: '*', redirect: '/login' }, // Catch-all unknown routes
];

const router = new VueRouter({
  mode: 'history',
  routes
});

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("token");
  const isAdmin = localStorage.getItem("role") === "admin";

  if (!token && to.path !== '/login') {
    next("/login");
  } else if (to.meta.requiresAdmin && !isAdmin) {
    next("/login");
  } else {
    next();
  }
});

export default router;

