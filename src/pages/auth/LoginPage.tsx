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
