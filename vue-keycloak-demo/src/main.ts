import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue';
import router from './router/index.ts';
import keycloak from './plugins/keycloak';

const app = createApp(App)

app.use(router)

// Initialize Keycloak
keycloak.init({ onLoad: 'login-required', checkLoginIframe: false }).then((authenticated) => {
  if (authenticated) {
    // Save token globally or to your API client if needed
    app.provide('keycloak', keycloak);
    app.mount('#app');
  } else {
    window.location.reload();
  }
}).catch((err) => {
  console.error('Keycloak initialization failed', err);
});
