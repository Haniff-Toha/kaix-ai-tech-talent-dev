import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuthStore } from '@/stores/authStore'
import { profileService, statsService } from '@/services/backend'
import KnotLoader from '@/components/ui/KnotLoader'
import NotificationBell from '@/components/ui/NotificationBell'

export default function ProfilePage() {
  const user = useAuthStore((s) => s.user)
  const logout = useAuthStore((s) => s.logout)
  const navigate = useNavigate()
  const [profile, setProfile] = useState<any>(null)
  const [stats, setStats] = useState<any>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadProfile()
  }, [])

  const loadProfile = async () => {
    setLoading(true)
    try {
      const [profileRes, statsRes] = await Promise.allSettled([
        profileService.getMe(),
        statsService.streak(),
      ])
      if (profileRes.status === 'fulfilled') setProfile(profileRes.value.data?.data)
      if (statsRes.status === 'fulfilled') setStats(statsRes.value.data?.data)
    } catch (err) { console.error(err) }
    setLoading(false)
  }

  const handleLogout = async () => {
    await logout()
    navigate('/login')
  }

  if (loading) {
    return (
      <div className="flex justify-center py-16 min-h-screen items-center relative">
        <div className="absolute inset-0 opacity-[0.03] pointer-events-none z-0" style={{ backgroundImage: 'radial-gradient(#09090B 1.5px, transparent 1.5px)', backgroundSize: '24px 24px' }}></div>
        <KnotLoader size="md" />
      </div>
    )
  }

  const p = profile || {}

  return (
    <div className="px-4 pb-24 min-h-screen relative overflow-hidden">
      <div className="absolute inset-0 opacity-[0.03] pointer-events-none z-0" style={{ backgroundImage: 'radial-gradient(#09090B 1.5px, transparent 1.5px)', backgroundSize: '24px 24px' }}></div>
      
      <div className="sticky top-0 z-50 bg-bg-base/95 backdrop-blur-sm pt-5 pb-4 mb-4 flex items-center justify-between border-b-2 border-dark/10 -mx-4 px-4">
        <h1 className="font-display text-4xl text-dark font-black tracking-tight drop-shadow-sm">Profile</h1>
        <div className="flex items-center gap-3">
          <NotificationBell />
          <img src="/kaix_logo.png" alt="Logo" className="w-8 h-8 object-contain drop-shadow-sm" />
        </div>
      </div>

      <div className="relative z-10">
        {/* Profile header */}
        <div className="neo-card p-6 mb-6 text-center border-4 border-dark shadow-[4px_4px_0_#09090B] bg-white">
          <div className="relative inline-block mb-4">
            <div className="w-24 h-24 rounded-full bg-brand-blue border-4 border-dark text-white flex items-center justify-center font-display text-4xl mx-auto shadow-[4px_4px_0_#09090B] font-black">
              {(p.name || user?.name)?.charAt(0)?.toUpperCase() || 'K'}
            </div>
            <div className="absolute -bottom-2 -right-2 bg-brand-yellow border-2 border-dark rounded-full w-8 h-8 flex items-center justify-center shadow-[2px_2px_0_#09090B]">
              <span className="text-sm">🌟</span>
            </div>
          </div>
          <h2 className="font-display text-2xl font-black text-dark tracking-tight">{p.name || user?.name || 'User'}</h2>
          <p className="font-display font-bold text-sm text-text-secondary mt-1">{p.email || user?.email}</p>

          {/* Career track badge */}
          {p.target_role && (
            <div className="mt-4 inline-block px-4 py-1.5 rounded-xl bg-brand-pink border-2 border-dark text-dark font-display font-black text-xs shadow-[2px_2px_0_#09090B] transform -rotate-2">
              🎯 {p.target_role}
            </div>
          )}
        </div>

        {/* Stats row */}
        <div className="grid grid-cols-2 gap-3 mb-6">
          <div className="neo-card p-4 text-center border-4 border-dark shadow-[4px_4px_0_#09090B] bg-brand-brown relative overflow-hidden flex flex-col justify-center items-start pl-5">
            <span className="absolute -right-2 -bottom-2 text-6xl opacity-20">🔥</span>
            <p className="font-display text-3xl font-black text-brand-blue drop-shadow-sm mb-1 z-10">{stats?.current_streak || 0}</p>
            <p className="font-display font-bold text-[10px] text-dark uppercase tracking-wider z-10">Streak Saat Ini</p>
          </div>
          <div className="neo-card p-4 text-center border-4 border-dark shadow-[4px_4px_0_#09090B] bg-brand-sand relative overflow-hidden flex flex-col justify-center items-start pl-5">
            <span className="absolute -right-2 -bottom-2 text-6xl opacity-20">🏆</span>
            <p className="font-display text-3xl font-black text-dark drop-shadow-sm mb-1 z-10">{stats?.longest_streak || 0}</p>
            <p className="font-display font-bold text-[10px] text-text-secondary uppercase tracking-wider z-10">Streak Terbaik</p>
          </div>
          <div className="neo-card p-4 text-center border-4 border-dark shadow-[4px_4px_0_#09090B] bg-[#E8F0D6] relative overflow-hidden flex flex-col justify-center items-start pl-5">
            <span className="absolute -right-2 -bottom-2 text-6xl opacity-20">⏱️</span>
            <p className="font-display text-3xl font-black text-dark drop-shadow-sm mb-1 z-10">{stats?.total_study_minutes ? Math.round(stats.total_study_minutes / 60) : 0}</p>
            <p className="font-display font-bold text-[10px] text-text-secondary uppercase tracking-wider z-10">Jam Belajar</p>
          </div>
          <div className="neo-card p-4 text-center border-4 border-dark shadow-[4px_4px_0_#09090B] bg-brand-sand relative overflow-hidden flex flex-col justify-center items-start pl-5">
            <span className="absolute -right-2 -bottom-2 text-6xl opacity-20">🚩</span>
            <p className="font-display text-3xl font-black text-dark drop-shadow-sm mb-1 z-10">{stats?.milestones_completed || 0}</p>
            <p className="font-display font-bold text-[10px] text-dark uppercase tracking-wider z-10">Milestone</p>
          </div>
        </div>

        {/* Skills */}
        {p.current_skills && p.current_skills.length > 0 && (
          <div className="neo-card p-5 mb-6 border-4 border-dark shadow-[4px_4px_0_#09090B] bg-white">
            <h3 className="font-display text-xl font-black text-dark mb-4">Skill Saya</h3>
            <div className="flex flex-wrap gap-2">
              {p.current_skills.map((skill: string) => (
                <span key={skill} className="px-3 py-1.5 rounded-lg bg-border-light font-display font-bold text-xs text-dark border-2 border-dark shadow-[1px_1px_0_#09090B]">
                  {skill}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Settings */}
        <div className="neo-card overflow-hidden mb-6 border-4 border-dark shadow-[4px_4px_0_#09090B] bg-white flex flex-col">
          <button className="w-full px-5 py-4 text-left font-display font-bold text-base text-dark hover:bg-border-light transition-colors border-b-2 border-dark flex items-center justify-between gap-4 group">
            <div className="flex items-center gap-4 min-w-0">
              <span className="w-8 h-8 rounded-full border-2 border-dark bg-white flex items-center justify-center text-sm shadow-[1px_1px_0_#09090B] group-hover:bg-brand-blue group-hover:text-white transition-colors shrink-0">🌐</span> 
              <span className="truncate">Bahasa: Indonesia</span>
            </div>
            <span className="font-display font-bold text-[10px] uppercase text-brand-pink bg-brand-pink/10 border-2 border-brand-pink px-2.5 py-1 rounded-md shadow-[1px_1px_0px_#09090B] shrink-0">
              Lainnya Segera Hadir
            </span>
          </button>
          <button
            onClick={() => navigate('/notification-settings')}
            className="w-full px-5 py-4 text-left font-display font-bold text-base text-dark hover:bg-border-light transition-colors border-b-2 border-dark flex items-center gap-4 group"
          >
            <span className="w-8 h-8 rounded-full border-2 border-dark bg-white flex items-center justify-center text-sm shadow-[1px_1px_0_#09090B] group-hover:bg-brand-blue group-hover:text-white transition-colors">🔔</span> 
            Pengaturan Notifikasi
          </button>
          <button
            onClick={() => navigate('/profile/edit')}
            className="w-full px-5 py-4 text-left font-display font-bold text-base text-dark hover:bg-border-light transition-colors border-b-2 border-dark flex items-center gap-4 group"
          >
            <span className="w-8 h-8 rounded-full border-2 border-dark bg-white flex items-center justify-center text-sm shadow-[1px_1px_0_#09090B] group-hover:bg-brand-blue group-hover:text-white transition-colors">👤</span> 
            Edit Profil
          </button>
          <button
            onClick={handleLogout}
            className="w-full px-5 py-4 text-left font-display font-black text-brand-red hover:bg-red-50 transition-colors flex items-center gap-4 group"
          >
            <span className="w-8 h-8 rounded-full border-2 border-brand-red bg-white flex items-center justify-center text-sm shadow-[1px_1px_0_#FF6B6B] group-hover:bg-brand-red group-hover:text-white transition-colors">🚪</span> 
            Keluar
          </button>
        </div>
      </div>
    </div>
  )
}
