import { create } from 'zustand'

interface AuthUser {
  id: string
  name: string
  email: string
  locale: string
}

interface AuthState {
  user: AuthUser | null
  token: string | null
  refreshToken: string | null
  isAuthenticated: boolean
  isLoading: boolean
  setAuth: (user: AuthUser, token: string, refreshToken?: string) => void
  logout: () => void
  initialize: () => void
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  token: null,
  refreshToken: null,
  isAuthenticated: false,
  isLoading: true,

  setAuth: (user, token, refreshToken) => {
    // Persist to localStorage
    localStorage.setItem('kaix_token', token)
    localStorage.setItem('kaix_user', JSON.stringify(user))
    if (refreshToken) localStorage.setItem('kaix_refresh_token', refreshToken)

    set({
      user,
      token,
      refreshToken: refreshToken || null,
      isAuthenticated: true,
      isLoading: false,
    })
  },

  logout: () => {
    localStorage.removeItem('kaix_token')
    localStorage.removeItem('kaix_user')
    localStorage.removeItem('kaix_refresh_token')

    set({
      user: null,
      token: null,
      refreshToken: null,
      isAuthenticated: false,
      isLoading: false,
    })
  },

  initialize: () => {
    // Restore from localStorage
    const token = localStorage.getItem('kaix_token')
    const userJson = localStorage.getItem('kaix_user')
    const refreshToken = localStorage.getItem('kaix_refresh_token')

    if (token && userJson) {
      try {
        const user = JSON.parse(userJson)
        set({
          user,
          token,
          refreshToken,
          isAuthenticated: true,
          isLoading: false,
        })
      } catch {
        set({ isLoading: false })
      }
    } else {
      set({ isLoading: false })
    }
  },
}))
