import Vue from 'vue';
import App from './App.vue';
import router from './router';
import vuetify from './plugins/vuetify';
import axios from 'axios';
import './assets/style.css';

const http = axios.create({
    baseURL: 'http://localhost:8000/api/',
    headers: {
        'Content-Type': 'application/json'
    }
});

http.interceptors.request.use(config => {
    const token = localStorage.getItem('token');
    if (token) {
        config.headers.Authorization = `Token ${token}`;
    }
    return config;
});

Vue.prototype.$http = http;

Vue.config.productionTip = false;

new Vue({
    vuetify,
    router,
    render: h => h(App),
}).$mount('#app');
