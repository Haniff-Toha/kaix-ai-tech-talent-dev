import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useAuthStore } from '@/stores/authStore'
import { authService } from '@/services/backend'
import KnotLoader from '@/components/ui/KnotLoader'

export default function LoginPage() {
  const navigate = useNavigate()
  const setAuth = useAuthStore((s) => s.setAuth)
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const [showPassword, setShowPassword] = useState(false)

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      const { data } = await authService.login({ email, password })

      if (data.data?.access_token) {
        setAuth(
          data.data.user,
          data.data.access_token,
          data.data.refresh_token
        )
        navigate('/overview')
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'Login gagal. Cek email dan password.')
    } finally {
      setLoading(false)
    }
  }

  const handleGoogleLogin = async () => {
    try {
      const { data } = await authService.googleOAuth(`${window.location.origin}/auth/callback`)
      if (data.data?.url) {
        window.location.href = data.data.url
      }
    } catch (err) {
      setError('Google login gagal.')
    }
  }

  return (
    <div className="min-h-dvh bg-bg-base flex flex-col relative overflow-hidden">
      {/* Neo-brutalist background decoration */}
      <div className="absolute inset-0 pointer-events-none overflow-hidden z-0">
        <div className="absolute top-0 right-0 w-48 h-48 rounded-full bg-brand-yellow/30 blur-3xl mix-blend-multiply" />
        <div className="absolute bottom-20 left-0 w-56 h-56 rounded-full bg-brand-blue/20 blur-3xl mix-blend-multiply" />
        <div className="absolute inset-0 opacity-[0.03]" style={{ backgroundImage: 'radial-gradient(#09090B 1.5px, transparent 1.5px)', backgroundSize: '24px 24px' }}></div>
      </div>

      <div className="flex-1 flex flex-col items-center justify-center px-6 relative z-10">
        <div className="w-full max-w-sm">
          {/* Logo + Brand */}
          <div className="text-center mb-8">
            <div className="flex items-center justify-center gap-3 mb-1">
              <img src="/kaix_logo.png" alt="Kaix" className="w-14 h-14 object-contain drop-shadow-md" />
              <h1 className="font-display text-4xl text-dark font-extrabold tracking-tight">kaix</h1>
            </div>
            <p className="font-body font-bold text-sm text-brand-blue">AI Tech Talent Companion</p>
          </div>

          {/* Form card */}
          <div className="neo-card p-6 border-4">
            <h2 className="font-display text-xl text-dark text-center mb-6 font-bold">Haloo!! 👋</h2>

            <form onSubmit={handleLogin} className="flex flex-col gap-4">
              {/* Email */}
              <div>
                <label className="font-display font-bold text-xs uppercase tracking-wider text-dark mb-1 block">Email</label>
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="kamu@email.com"
                  className="input-field border-2"
                  required
                  autoComplete="email"
                />
              </div>

              {/* Password */}
              <div>
                <label className="font-display font-bold text-xs uppercase tracking-wider text-dark mb-1 block">Password</label>
                <div className="relative">
                  <input
                    type={showPassword ? 'text' : 'password'}
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="••••••••"
                    className="input-field border-2 pr-10"
                    required
                    autoComplete="current-password"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-text-secondary hover:text-dark transition-colors text-lg"
                    tabIndex={-1}
                  >
                    {showPassword ? '🙈' : '👁'}
                  </button>
                </div>
              </div>

              {error && (
                <div className="bg-brand-red text-white text-sm font-bold px-4 py-3 rounded-lg border-2 border-dark shadow-neo-sm">
                  {error}
                </div>
              )}

              <button
                type="submit"
                disabled={loading}
                className="btn-neo w-full mt-2 py-3 border-4"
              >
                {loading ? <KnotLoader size="sm" /> : 'Masuk'}
              </button>

              <Link to="/forgot-password" className="text-center font-body font-bold text-sm text-text-secondary hover:text-brand-blue transition-colors mt-2">
                Lupa password?
              </Link>
            </form>

            {/* Divider */}
            <div className="flex items-center gap-3 my-6">
              <div className="flex-1 h-0.5 bg-border-bold opacity-20" />
              <span className="font-display font-bold text-xs text-text-secondary uppercase tracking-wide">atau</span>
              <div className="flex-1 h-0.5 bg-border-bold opacity-20" />
            </div>

            {/* Google */}
            <button onClick={handleGoogleLogin} className="btn-secondary w-full flex items-center justify-center gap-2 border-4 py-3">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 0 1-2.2 3.32v2.76h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/>
                <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
                <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"/>
                <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/>
              </svg>
              Masuk dengan Google
            </button>
          </div>

          {/* Signup link */}
          <p className="text-center font-body font-bold text-sm text-text-secondary mt-8">
            Belum punya akun?{' '}
            <Link to="/signup" className="text-brand-blue font-extrabold hover:underline">Daftar sekarang</Link>
          </p>
        </div>
      </div>
    </div>
  )
}
