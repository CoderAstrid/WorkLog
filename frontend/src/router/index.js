import Vue from 'vue';
import VueRouter from 'vue-router';
import WorkLog from '../components/WorkLog.vue';
import UserAuth from '../components/UserAuth.vue';

Vue.use(VueRouter);

const routes = [
  { path: '/', component: UserAuth },
  { path: '/worklog', component: WorkLog },
];

export default new VueRouter({
  mode: 'history',
  routes
});
