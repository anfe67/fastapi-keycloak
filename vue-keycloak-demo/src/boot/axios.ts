import axios from 'axios';
import keycloak from '@/plugins/keycloak';

export const apiClient = axios.create({
  baseURL: 'http://localhost:8000', // Your FastAPI backend URL
});

apiClient.interceptors.request.use(async (config) => {
  // Ensure token is fresh (refreshes if it expires within 30 seconds)
  try {
    await keycloak.updateToken(30);
  } catch (error) {
    console.error('Failed to refresh token, forcing login');
    keycloak.login();
  }

  if (keycloak.token) {
    config.headers.Authorization = `Bearer ${keycloak.token}`;
  }
  return config;
});