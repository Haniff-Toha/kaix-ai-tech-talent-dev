import { create } from 'zustand'

interface Toast {
  id: string
  type: 'success' | 'error' | 'info' | 'warning'
  message: string
}

interface UIState {
  isBottomNavVisible: boolean
  toasts: Toast[]
  setBottomNavVisible: (visible: boolean) => void
  addToast: (toast: Omit<Toast, 'id'>) => void
  removeToast: (id: string) => void
}

export const useUIStore = create<UIState>((set) => ({
  isBottomNavVisible: true,
  toasts: [],
  setBottomNavVisible: (visible) => set({ isBottomNavVisible: visible }),
  addToast: (toast) => {
    const id = Date.now().toString()
    set((state) => ({ toasts: [...state.toasts, { ...toast, id }] }))
    // Auto-dismiss after 3s
    setTimeout(() => {
      set((state) => ({ toasts: state.toasts.filter((t) => t.id !== id) }))
    }, 3000)
  },
  removeToast: (id) =>
    set((state) => ({ toasts: state.toasts.filter((t) => t.id !== id) })),
}))
