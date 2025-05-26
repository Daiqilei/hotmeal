/**
 * @file            src/utils/request.js
 * @description
 * @author          taichilei
 * @date            2025-05-03
 * @version         1.0.0
 */

import axios from 'axios'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/userStore'

const request = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  timeout: 5000,
  headers: {
    'Content-Type': 'application/json',
  },
})

request.interceptors.request.use((config) => {
  const userStore = useUserStore()
  const token = userStore.token // 不再用 storeToRefs

  //console.log('[Axios Request]', config.url)
  //console.log('[Token]', token)

  if (token) {
    config.headers.Authorization = `Bearer ${token}`
    //console.log('[Headers After]', config.headers)
  } else {
    //console.warn('[Axios Warning] No token found in userStore')
  }

  return config
})

request.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('[Axios Error]', error)
    ElMessage.error(error.response?.data?.message || '请求出错！')
    return Promise.reject(error)
  },
)

export default request
