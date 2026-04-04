import axios from 'axios'

export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api/v1'

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 120000, // 增加到 120 秒，因为 LLM 生成可能需要较长时间
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add response interceptor to extract data
apiClient.interceptors.response.use(response => response.data)
