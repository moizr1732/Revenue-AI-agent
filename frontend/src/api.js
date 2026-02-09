import axios from 'axios'

// Get API base URL from environment or default to relative path for dev
const API_BASE = import.meta.env.VITE_API_BASE || ''

const apiClient = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json'
  }
})

export default apiClient
