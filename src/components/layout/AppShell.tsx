import { Outlet } from 'react-router-dom'
import BottomNav from './BottomNav'
import { useUIStore } from '@/stores/uiStore'
import { AnimatePresence, motion } from 'framer-motion'

export default function AppShell() {
  const toasts = useUIStore((s) => s.toasts)
  const removeToast = useUIStore((s) => s.removeToast)

  return (
    <div className="flex flex-col min-h-dvh bg-bg-base relative">
      {/* Background dot pattern */}
      <div className="fixed inset-0 opacity-[0.02] pointer-events-none z-0" style={{ backgroundImage: 'radial-gradient(#09090B 1.5px, transparent 1.5px)', backgroundSize: '24px 24px' }}></div>

      {/* Main content */}
      <main className="flex-1 pb-safe max-w-lg mx-auto w-full relative">
        <Outlet />
      </main>

      {/* Bottom Nav */}
      <BottomNav />

      {/* Toast notifications */}
      <div className="fixed top-4 left-1/2 -translate-x-1/2 z-[100] flex flex-col gap-3 w-[90%] max-w-sm">
        <AnimatePresence>
          {toasts.map((toast) => (
            <motion.div
              key={toast.id}
              initial={{ opacity: 0, y: -20, scale: 0.95 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0, y: -10, scale: 0.95 }}
              className={`px-4 py-3 rounded-xl font-display font-bold text-sm border-2 border-dark cursor-pointer shadow-neo-sm transition-all
                ${toast.type === 'success' ? 'bg-brand-green text-white' : ''}
                ${toast.type === 'error' ? 'bg-brand-red text-white' : ''}
                ${toast.type === 'info' ? 'bg-brand-blue text-white' : ''}
                ${toast.type === 'warning' ? 'bg-brand-yellow text-dark' : ''}
              `}
              onClick={() => removeToast(toast.id)}
            >
              {toast.message}
            </motion.div>
          ))}
        </AnimatePresence>
      </div>
    </div>
  )
}
