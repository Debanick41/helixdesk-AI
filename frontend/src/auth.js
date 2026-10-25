
import { apiRequest } from './api'

const TOKEN_KEY = 'helixdesk_access_token'

export async function login(email, password) {
  const data = await apiRequest('/api/v1/auth/login', {
    method: 'POST',
    body: JSON.stringify({ email, password }),
  })

  if (!data?.access_token) {
    throw new Error('The server did not return an access token.')
  }

  sessionStorage.setItem(TOKEN_KEY, data.access_token)

  return data
}

export function getAccessToken() {
  return sessionStorage.getItem(TOKEN_KEY)
}

export function logout() {
  sessionStorage.removeItem(TOKEN_KEY)
}

export async function getCustomers() {
  const token = getAccessToken()

  if (!token) {
    throw new Error('Please log in to view customers.')
  }

  return apiRequest('/api/v1/customers/', {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })
}
