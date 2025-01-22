import Vue from 'vue';
import VueRouter from 'vue-router';
import UserAuth from '../components/UserAuth.vue';

Vue.use(VueRouter);

const routes = [
  { path: '/', component: UserAuth },
];

export default new VueRouter({
  mode: 'history',
  routes
});
