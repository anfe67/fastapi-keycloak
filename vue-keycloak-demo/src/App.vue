<template>
  <div class="app">
    <div v-if="keycloak">
      <nav class="nav-menu">
        <button @click="callPublic" :disabled="loading">Public API</button>
        <button @click="callUser" :disabled="loading">User API</button>
        <button @click="callRoles" :disabled="loading">My Roles</button>
        <button @click="logout" class="logout-btn">Logout</button>
      </nav>

      <div class="auth-info">
        <h1>Authenticated with Keycloak</h1>
        <p><strong>User:</strong> {{ keycloak.tokenParsed?.preferred_username || keycloak.tokenParsed?.name || 'Unknown' }}</p>
        <p><strong>Email:</strong> {{ keycloak.tokenParsed?.email || 'Not provided' }}</p>
        <p><strong>Realm:</strong> {{ keycloak.realm }}</p>
        <p><strong>Client ID:</strong> {{ keycloak.clientId }}</p>
        <p><strong>Roles:</strong> {{ userRoles.join(', ') || 'No roles assigned' }}</p>
      </div>

      <div v-if="apiResponse" class="api-response">
        <h2>API Response</h2>
        <pre>{{ JSON.stringify(apiResponse, null, 2) }}</pre>
      </div>

      <div v-if="apiError" class="api-error">
        <h2>API Error</h2>
        <pre>{{ apiError }}</pre>
      </div>
    </div>
    <div v-else class="no-auth">
      <h1>Not Authenticated</h1>
      <p>Please wait while we redirect you to login...</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { inject, computed, ref } from 'vue'
import Keycloak from 'keycloak-js'
import { apiClient } from '@/boot/axios'

const keycloak = inject<Keycloak>('keycloak')

const apiResponse = ref<any>(null)
const apiError = ref<string>('')
const loading = ref(false)

const userRoles = computed(() => {
  if (!keycloak?.tokenParsed) return []
  // Get realm roles
  const realmRoles = keycloak.tokenParsed.realm_access?.roles || []
  // Get client roles (for the current client)
  const clientRoles = keycloak.tokenParsed.resource_access?.[keycloak.clientId]?.roles || []
  // Combine both
  return [...new Set([...realmRoles, ...clientRoles])]
})

const callPublic = async () => {
  loading.value = true
  apiResponse.value = null
  apiError.value = ''
  try {
    const response = await apiClient.get('/public')
    apiResponse.value = response.data
  } catch (err: any) {
    apiError.value = err.response?.data?.detail || err.message || 'Unknown error'
  } finally {
    loading.value = false
  }
}

const callUser = async () => {
  loading.value = true
  apiResponse.value = null
  apiError.value = ''
  try {
    const response = await apiClient.get('/user')
    apiResponse.value = response.data
  } catch (err: any) {
    apiError.value = err.response?.data?.detail || err.message || 'Unknown error'
  } finally {
    loading.value = false
  }
}

const callRoles = async () => {
  loading.value = true
  apiResponse.value = null
  apiError.value = ''
  try {
    const response = await apiClient.get('/me/roles')
    apiResponse.value = response.data
  } catch (err: any) {
    apiError.value = err.response?.data?.detail || err.message || 'Unknown error'
  } finally {
    loading.value = false
  }
}

const logout = () => {
  if (keycloak) {
    keycloak.logout()
  }
}
</script>

<style>
  .app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    padding: 2rem;
    max-width: 800px;
    margin: 0 auto;
  }

  .nav-menu {
    display: flex;
    gap: 1rem;
    margin-bottom: 2rem;
    padding: 1rem;
    background: #f5f5f5;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  }

  .nav-menu button {
    padding: 0.5rem 1rem;
    background: #3498db;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 1rem;
  }

  .nav-menu button:hover:not(:disabled) {
    background: #2980b9;
  }

  .nav-menu button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .logout-btn {
    margin-left: auto;
    background: #e74c3c;
  }

  .logout-btn:hover:not(:disabled) {
    background: #c0392b;
  }

  .auth-info, .no-auth {
    background: #f5f5f5;
    padding: 2rem;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  }

  h1 {
    color: #333;
    margin-bottom: 1.5rem;
  }

  h2 {
    color: #333;
    margin-top: 1.5rem;
    margin-bottom: 1rem;
  }

  p {
    margin: 0.5rem 0;
    font-size: 1rem;
  }

  strong {
    color: #555;
  }

  .api-response {
    background: #e8f5e9;
    padding: 1.5rem;
    border-radius: 8px;
    margin-top: 2rem;
    border-left: 4px solid #4caf50;
  }

  .api-response pre {
    background: white;
    padding: 1rem;
    border-radius: 4px;
    overflow-x: auto;
  }

  .api-error {
    background: #ffebee;
    padding: 1.5rem;
    border-radius: 8px;
    margin-top: 2rem;
    border-left: 4px solid #f44336;
  }

  .api-error pre {
    background: white;
    padding: 1rem;
    border-radius: 4px;
    overflow-x: auto;
    color: #c62828;
  }
</style>
