/**
 * API service layer — all backend calls go through here.
 * Each function maps to a backend endpoint.
 */
import api from './api'

// ── Auth / Profile ──
export const authService = {
  signup: (data: { name: string; email: string; password: string; locale?: string }) =>
    api.post('/auth/signup', data),
  login: (data: { email: string; password: string }) =>
    api.post('/auth/login', data),
  googleOAuth: (redirectUrl?: string) =>
    api.post('/auth/google', { redirect_url: redirectUrl }),
  refreshToken: (refreshToken: string) =>
    api.post('/auth/refresh', null, { params: { refresh_token: refreshToken } }),
}

// ── Profile ──
export const profileService = {
  getMe: () => api.get('/profile/me'),
  updateProfile: (data: any) => api.put('/profile', data),
}

// ── Onboarding ──
export const onboardingService = {
  submit: (data: any) => api.post('/onboarding', data),
}

// ── Jobs (async task polling) ──
export const jobService = {
  getStatus: (jobId: string) => api.get(`/jobs/${jobId}/status`),
  pollUntilDone: async (
    jobId: string,
    onProgress?: (status: string) => void,
    intervalMs = 2000
  ): Promise<any> => {
    while (true) {
      const { data } = await api.get(`/jobs/${jobId}/status`)
      if (data.data?.status === 'done') return data.data?.result
      if (data.data?.status === 'failed') throw new Error(data.data?.error || 'Job failed')
      onProgress?.(data.data?.status || 'running')
      await new Promise((r) => setTimeout(r, intervalMs))
    }
  },
}

// ── Roadmap ──
export const roadmapService = {
  get: () => api.get('/roadmap'),
  regenerate: () => api.post('/roadmap/regenerate'),
}

// ── Activities ──
export const activityService = {
  log: (data: { raw_text: string; duration_minutes?: number }) =>
    api.post('/activities', data),
  list: (page = 1) => api.get(`/activities?page=${page}`),
  confirm: (id: string, data: any) => api.patch(`/activities/${id}/confirm`, data),
}

// ── Courses ──
export const courseService = {
  list: (status?: string, page = 1) =>
    api.get('/courses', { params: { status, page } }),
  create: (data: any) => api.post('/courses', data),
  update: (id: string, data: any) => api.patch(`/courses/${id}`, data),
  delete: (id: string) => api.delete(`/courses/${id}`),
  logSession: (courseId: string, data: { duration_minutes: number; notes?: string }) =>
    api.post(`/courses/${courseId}/sessions`, data),
  getSessions: (courseId: string, page = 1) =>
    api.get(`/courses/${courseId}/sessions?page=${page}`),
  getTodayFocus: () => api.get('/courses/today-focus'),
  toggleFocus: (id: string) => api.patch(`/courses/${id}/toggle-focus`),
  getStats: () => api.get('/courses/stats'),
}

// ── Recommendations ──
export const recommendationService = {
  getCourses: (params?: { level?: string; source?: string; free_only?: boolean; page?: number }) =>
    api.get('/recommendations/courses', { params }),
  getByRoadmap: (phase?: number) =>
    api.get('/recommendations/courses/by-roadmap', { params: phase ? { phase } : {} }),
}

// ── Reminders ──
export const reminderService = {
  list: () => api.get('/reminders'),
  create: (data: any) => api.post('/reminders', data),
  update: (id: string, data: any) => api.patch(`/reminders/${id}`, data),
  delete: (id: string) => api.delete(`/reminders/${id}`),
  preview: (id: string) => api.post(`/reminders/${id}/preview`),
}

// ── Notifications ──
export const notificationService = {
  list: (page = 1) => api.get('/notifications', { params: { page } }),
  markRead: (id: string) => api.patch(`/notifications/${id}/read`),
  markAllRead: () => api.post('/notifications/read-all'),
  unreadCount: () => api.get('/notifications/unread-count'),
}

// ── Telegram ──
export const telegramService = {
  connect: (botToken: string) => api.post('/telegram/connect', { bot_token: botToken }),
  status: () => api.get('/telegram/status'),
  disconnect: () => api.delete('/telegram/disconnect'),
  test: () => api.post('/telegram/test'),
}

// ── Overview ──
export const overviewService = {
  get: () => api.get('/overview'),
  saveNote: (content: string) => api.post('/overview/notes', { content }),
  getNotes: () => api.get('/overview/notes'),
  deleteNote: (id: string) => api.delete(`/overview/notes/${id}`),
}

// ── Stats ──
export const statsService = {
  streak: () => api.get('/stats/streak'),
  progress: () => api.get('/stats/progress'),
  time: () => api.get('/stats/time'),
}

// ── Chat ──
export const chatService = {
  send: (message: string, locale = 'id') =>
    api.post('/chat', { message, locale }),
  // Streaming version
  stream: async function* (message: string, token: string) {
    const response = await fetch(`${api.defaults.baseURL}/chat`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ message, locale: 'id' }),
    })
    const reader = response.body!.getReader()
    const decoder = new TextDecoder()
    while (true) {
      const { done, value } = await reader.read()
      if (done) break
      yield decoder.decode(value)
    }
  },
}
