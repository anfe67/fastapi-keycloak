import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue';
import router from './router/index.ts';
import keycloak from './plugins/keycloak';

const app = createApp(App)

app.use(router)

// Initialize Keycloak with login-required - this will automatically redirect to Keycloak if not authenticated
keycloak.init({ onLoad: 'login-required', checkLoginIframe: false, silentCheckSsoFallback: false }).then((authenticated) => {
  if (authenticated) {
    // Provide keycloak instance to the app
    app.provide('keycloak', keycloak);
    app.mount('#app');
  } else {
    // If not authenticated, keycloak.login-required should have already redirected
    // This is a fallback
    keycloak.login()
  }
}).catch((err) => {
  console.error('Keycloak initialization failed', err);
});
