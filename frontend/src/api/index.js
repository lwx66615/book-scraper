import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 30000
})

// 响应拦截器
api.interceptors.response.use(
  response => response.data,
  error => {
    const message = error.response?.data?.detail || error.message || '请求失败'
    return Promise.reject(new Error(message))
  }
)

// 小说相关API
export const novelApi = {
  getList: (params) => api.get('/novels', { params }),
  getDetail: (id) => api.get(`/novels/${id}`),
  delete: (id) => api.delete(`/novels/${id}`),
  getChapters: (id, params) => api.get(`/novels/${id}/chapters`, { params }),
  getChapter: (id) => api.get(`/novels/chapters/${id}`)
}

// 下载相关API
export const downloadApi = {
  start: (data) => api.post('/download/start', data),
  pause: (id) => api.post(`/download/${id}/pause`),
  resume: (id) => api.post(`/download/${id}/resume`),
  cancel: (id) => api.post(`/download/${id}/cancel`),
  getTasks: () => api.get('/download/tasks'),
  getTask: (id) => api.get(`/download/${id}`)
}

// 导出相关API
export const exportApi = {
  txt: (id) => api.post(`/export/txt/${id}`, null, { responseType: 'blob' }),
  epub: (id) => api.post(`/export/epub/${id}`, null, { responseType: 'blob' })
}

// 规则相关API
export const ruleApi = {
  getList: () => api.get('/rules'),
  getDetail: (id) => api.get(`/rules/${id}`),
  create: (data) => api.post('/rules', data),
  update: (id, data) => api.put(`/rules/${id}`, data),
  delete: (id) => api.delete(`/rules/${id}`),
  test: (data) => api.post('/rules/test', data)
}

// 搜索API
export const searchApi = {
  search: (params) => api.get('/search', { params })
}

// 设置API
export const settingsApi = {
  getAutoUpdate: () => api.get('/settings/auto-update'),
  setAutoUpdate: (data) => api.post('/settings/auto-update', data),
  getProxy: () => api.get('/settings/proxy'),
  setProxy: (data) => api.post('/settings/proxy', data)
}

export default api
