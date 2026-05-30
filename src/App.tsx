import { useEffect } from 'react'
import { BrowserRouter, Routes, Route, Navigate, Outlet } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { useAuthStore } from '@/stores/authStore'
import KnotLoader from '@/components/ui/KnotLoader'
import AppShell from '@/components/layout/AppShell'

// Pages
import LoginPage from '@/pages/auth/LoginPage'
import SignupPage from '@/pages/auth/SignupPage'
import LandingPage from '@/pages/LandingPage'
import AppLandingPage from '@/pages/AppLandingPage'
import OnboardingPage from '@/pages/onboarding/OnboardingPage'
import OverviewPage from '@/pages/overview/OverviewPage'
import CoursePage from '@/pages/course/CoursePage'
import FocusPage from '@/pages/focus/FocusPage'
import ReminderPage from '@/pages/reminder/ReminderPage'
import ProfilePage from '@/pages/profile/ProfilePage'
import NotificationSettingsPage from '@/pages/profile/NotificationSettingsPage'
import EditProfilePage from '@/pages/profile/EditProfilePage'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 60_000,
      retry: 1,
    },
  },
})

// ── Route Guards ──

function PrivateRoute() {
  const { isAuthenticated, isLoading } = useAuthStore()

  if (isLoading) {
    return (
      <div className="min-h-dvh bg-white flex flex-col items-center justify-center gap-4">
        <img src="/kaix_logo.png" alt="Kaix" className="w-20 h-20 object-contain" />
        <KnotLoader size="md" />
        <p className="font-display text-base text-text-muted">Memuat...</p>
      </div>
    )
  }

  return isAuthenticated ? <Outlet /> : <Navigate to="/login" replace />
}

function PublicOnlyRoute() {
  const { isAuthenticated, isLoading } = useAuthStore()

  if (isLoading) {
    return (
      <div className="min-h-dvh bg-white flex flex-col items-center justify-center gap-4">
        <img src="/kaix_logo.png" alt="Kaix" className="w-20 h-20 object-contain" />
        <KnotLoader size="md" />
      </div>
    )
  }

  return isAuthenticated ? <Navigate to="/overview" replace /> : <Outlet />
}

// ── Main App ──

export default function App() {
  const initialize = useAuthStore((s) => s.initialize)

  useEffect(() => {
    initialize()
  }, [initialize])

  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          {/* Public routes — redirect to /overview if already logged in */}
          <Route element={<PublicOnlyRoute />}>
            <Route path="/" element={<LandingPage />} />
            <Route path="/applanding" element={<AppLandingPage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/signup" element={<SignupPage />} />
          </Route>

          {/* Protected routes — redirect to /login if not authenticated */}
          <Route element={<PrivateRoute />}>
            {/* Onboarding (no bottom nav) */}
            <Route path="/onboarding" element={<OnboardingPage />} />

            {/* Main app with bottom nav */}
            <Route element={<AppShell />}>
              <Route path="/overview" element={<OverviewPage />} />
              <Route path="/course" element={<CoursePage />} />
              <Route path="/focus" element={<FocusPage />} />
              <Route path="/reminder" element={<ReminderPage />} />
              <Route path="/profile" element={<ProfilePage />} />
              <Route path="/profile/edit" element={<EditProfilePage />} />
              <Route path="/notification-settings" element={<NotificationSettingsPage />} />
            </Route>
          </Route>

          {/* Catch-all redirect */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  )
}
