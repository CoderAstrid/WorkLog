// main.js

import Vue from 'vue';
import App from './App.vue';
import router from './router';
import vuetify from './plugins/vuetify';
import axios from 'axios';
import './assets/style.css';
import '@mdi/font/css/materialdesignicons.css'; // Ensure MDI icons are loaded
       
const http = axios.create({
    baseURL: 'http://192.168.101.81:8000/api/',
    headers: {
        'Content-Type': 'application/json',
    },
});

// Attach token to requests dynamically
http.interceptors.request.use((config) => {
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
    render: (h) => h(App),
}).$mount('#app');
