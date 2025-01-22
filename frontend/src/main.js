import Vue from 'vue';
import App from './App.vue';
import router from './router';
import vuetify from './plugins/vuetify';
import axios from 'axios';

Vue.prototype.$http = axios.create({
    baseURL: 'http://localhost:8000/api/',
});

Vue.config.productionTip = false;

new Vue({
    vuetify,
    router,
    render: h => h(App),
}).$mount('#app');
