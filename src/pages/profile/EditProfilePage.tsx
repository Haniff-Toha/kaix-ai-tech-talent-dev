import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuthStore } from '@/stores/authStore'
import { useUIStore } from '@/stores/uiStore'
import { profileService } from '@/services/backend'
import KnotLoader from '@/components/ui/KnotLoader'

export default function EditProfilePage() {
  const navigate = useNavigate()
  const { user, setAuth, token, refreshToken } = useAuthStore()
  const addToast = useUIStore((s) => s.addToast)

  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)

  // Form states
  const [name, setName] = useState('')
  const [currentRole, setCurrentRole] = useState('')
  const [targetRole, setTargetRole] = useState('')
  const [experienceLevel, setExperienceLevel] = useState('beginner')
  const [yearsExperience, setYearsExperience] = useState<number>(0)
  const [timeBudget, setTimeBudget] = useState<number>(60)
  const [learningStyle, setLearningStyle] = useState('hands-on')
  const [skills, setSkills] = useState<string[]>([])
  const [newSkill, setNewSkill] = useState('')

  useEffect(() => {
    loadProfile()
  }, [])

  const loadProfile = async () => {
    setLoading(true)
    try {
      const { data } = await profileService.getMe()
      if (data.success && data.data) {
        const p = data.data
        setName(user?.name || '')
        setCurrentRole(p.current_role || '')
        setTargetRole(p.target_role || '')
        setExperienceLevel(p.experience_level || 'beginner')
        setYearsExperience(p.years_experience || 0)
        setTimeBudget(p.time_budget_minutes || 60)
        setLearningStyle(p.preferred_learning_style || 'hands-on')
        setSkills(p.current_skills || [])
      }
    } catch (err) {
      console.error(err)
      addToast({ type: 'error', message: 'Gagal memuat profil' })
    } finally {
      setLoading(false)
    }
  }

  const handleAddSkill = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' || e.key === ',') {
      e.preventDefault()
      const trimmed = newSkill.trim()
      if (trimmed && !skills.includes(trimmed)) {
        setSkills([...skills, trimmed])
      }
      setNewSkill('')
    }
  }

  const handleRemoveSkill = (skillToRemove: string) => {
    setSkills(skills.filter((s) => s !== skillToRemove))
  }

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault()
    setSaving(true)
    try {
      const payload = {
        name,
        current_role: currentRole || null,
        target_role: targetRole || null,
        experience_level: experienceLevel,
        years_experience: yearsExperience,
        time_budget_minutes: timeBudget,
        preferred_learning_style: learningStyle,
        current_skills: skills,
      }
      const { data } = await profileService.updateProfile(payload)
      if (data.success) {
        addToast({ type: 'success', message: 'Profil berhasil diperbarui!' })
        // Update user name in local store
        if (user) {
          setAuth({ ...user, name }, token!, refreshToken || undefined)
        }
        navigate('/profile')
      } else {
        addToast({ type: 'error', message: data.message || 'Gagal memperbarui profil' })
      }
    } catch (err: any) {
      console.error(err)
      addToast({
        type: 'error',
        message: err.response?.data?.message || 'Gagal memperbarui profil',
      })
    } finally {
      setSaving(false)
    }
  }

  if (loading) {
    return (
      <div className="flex justify-center py-16 min-h-screen items-center relative bg-white">
        <div className="absolute inset-0 opacity-[0.03] pointer-events-none z-0" style={{ backgroundImage: 'radial-gradient(#09090B 1.5px, transparent 1.5px)', backgroundSize: '24px 24px' }}></div>
        <KnotLoader size="md" />
      </div>
    )
  }

  return (
    <div className="px-4 pb-24 min-h-screen relative overflow-hidden bg-white">
      <div className="absolute inset-0 opacity-[0.03] pointer-events-none z-0" style={{ backgroundImage: 'radial-gradient(#09090B 1.5px, transparent 1.5px)', backgroundSize: '24px 24px' }}></div>

      <div className="sticky top-0 z-50 bg-white/95 backdrop-blur-sm pt-5 pb-4 mb-5 flex items-center justify-between border-b-2 border-dark/10 -mx-4 px-4">
        <div className="flex items-center gap-3">
          <button type="button" onClick={() => navigate(-1)} className="w-10 h-10 rounded-full bg-white border-2 border-dark shadow-[2px_2px_0_#09090B] flex items-center justify-center text-sm hover:translate-y-[-1px] hover:shadow-[4px_4px_0_#09090B] transition-all">←</button>
          <h1 className="font-display text-2xl text-dark font-black">Edit Profil</h1>
        </div>
        <img src="/kaix_logo.png" alt="Logo" className="w-8 h-8 object-contain drop-shadow-sm" />
      </div>

      <form onSubmit={handleSave} className="relative z-10 flex flex-col gap-5">
        <div className="neo-card p-6 border-4 bg-white flex flex-col gap-4">
          {/* Name */}
          <div>
            <label className="font-display font-bold text-xs uppercase tracking-wider text-dark mb-1.5 block">Nama Lengkap</label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="Masukkan nama lengkap Anda"
              className="input-field border-2"
              required
            />
          </div>

          {/* Current Role */}
          <div>
            <label className="font-display font-bold text-xs uppercase tracking-wider text-dark mb-1.5 block">Pekerjaan / Peran Saat Ini</label>
            <input
              type="text"
              value={currentRole}
              onChange={(e) => setCurrentRole(e.target.value)}
              placeholder="Contoh: Student, Frontend Engineer"
              className="input-field border-2"
            />
          </div>

          {/* Target Role */}
          <div>
            <label className="font-display font-bold text-xs uppercase tracking-wider text-dark mb-1.5 block">Target Peran / Karir</label>
            <input
              type="text"
              value={targetRole}
              onChange={(e) => setTargetRole(e.target.value)}
              placeholder="Contoh: Senior Machine Learning Engineer"
              className="input-field border-2"
            />
          </div>

          {/* Grid for Level & Years */}
          <div className="grid grid-cols-2 gap-4">
            {/* Experience Level */}
            <div>
              <label className="font-display font-bold text-xs uppercase tracking-wider text-dark mb-1.5 block">Tingkat Pengalaman</label>
              <select
                value={experienceLevel}
                onChange={(e) => setExperienceLevel(e.target.value)}
                className="w-full font-body font-medium text-base text-dark bg-white rounded-lg px-4 py-3 outline-none border-2 border-dark shadow-[2px_2px_0_#09090B] focus:border-brand-blue"
              >
                <option value="beginner">Beginner</option>
                <option value="junior">Junior</option>
                <option value="mid">Mid-level</option>
                <option value="senior">Senior</option>
                <option value="lead">Lead</option>
              </select>
            </div>

            {/* Years of Experience */}
            <div>
              <label className="font-display font-bold text-xs uppercase tracking-wider text-dark mb-1.5 block">Tahun Pengalaman</label>
              <input
                type="number"
                value={yearsExperience}
                onChange={(e) => setYearsExperience(parseInt(e.target.value) || 0)}
                min="0"
                max="50"
                className="input-field border-2"
              />
            </div>
          </div>

          {/* Time Budget */}
          <div>
            <label className="font-display font-bold text-xs uppercase tracking-wider text-dark mb-1.5 block">Target Belajar Harian (Menit)</label>
            <div className="flex items-center gap-3">
              <input
                type="range"
                min="15"
                max="300"
                step="15"
                value={timeBudget}
                onChange={(e) => setTimeBudget(parseInt(e.target.value))}
                className="flex-1 accent-brand-blue h-2 bg-zinc-200 rounded-lg appearance-none cursor-pointer"
              />
              <span className="font-display font-black text-base text-dark bg-brand-yellow px-3 py-1.5 border-2 border-dark rounded-xl shadow-[2px_2px_0_#09090B] min-w-[70px] text-center">
                {timeBudget}m
              </span>
            </div>
          </div>

          {/* Learning Style */}
          <div>
            <label className="font-display font-bold text-xs uppercase tracking-wider text-dark mb-1.5 block">Metode Belajar Favorit</label>
            <select
              value={learningStyle}
              onChange={(e) => setLearningStyle(e.target.value)}
              className="w-full font-body font-medium text-base text-dark bg-white rounded-lg px-4 py-3 outline-none border-2 border-dark shadow-[2px_2px_0_#09090B] focus:border-brand-blue"
            >
              <option value="video">Menonton Video / Kursus Online</option>
              <option value="text">Membaca Buku / Dokumentasi</option>
              <option value="hands-on">Praktik Koding / Hands-on Project</option>
              <option value="mixed">Campuran / Interaktif</option>
            </select>
          </div>

          {/* Skills Editor */}
          <div>
            <label className="font-display font-bold text-xs uppercase tracking-wider text-dark mb-1.5 block">Skill Saat Ini</label>
            <div className="flex flex-wrap gap-2 mb-3">
              {skills.map((skill) => (
                <span
                  key={skill}
                  className="px-3 py-1.5 rounded-lg bg-[#E8F0D6] font-display font-bold text-xs text-dark border-2 border-dark shadow-[1px_1px_0_#09090B] flex items-center gap-1.5"
                >
                  {skill}
                  <button
                    type="button"
                    onClick={() => handleRemoveSkill(skill)}
                    className="text-brand-red font-black hover:scale-125 transition-transform"
                  >
                    ×
                  </button>
                </span>
              ))}
              {skills.length === 0 && (
                <p className="font-body text-xs text-text-muted italic">Belum ada skill ditambahkan.</p>
              )}
            </div>
            <div className="relative">
              <input
                type="text"
                value={newSkill}
                onChange={(e) => setNewSkill(e.target.value)}
                onKeyDown={handleAddSkill}
                placeholder="Ketik skill (contoh: PyTorch) lalu tekan Enter"
                className="input-field border-2"
              />
            </div>
          </div>
        </div>

        <button
          type="submit"
          disabled={saving}
          className="btn-neo w-full py-4 text-lg border-4 bg-brand-blue text-white shadow-neo-md"
        >
          {saving ? <KnotLoader size="sm" /> : '💾 Simpan Perubahan'}
        </button>
      </form>
    </div>
  )
}
