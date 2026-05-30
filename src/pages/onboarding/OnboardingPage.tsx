import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import { useOnboardingStore, UserType } from '@/stores/onboardingStore'
import { onboardingService } from '@/services/backend'
import KnotLoader from '@/components/ui/KnotLoader'

// ── Career tracks ──
const CAREER_TRACKS = [
  { id: 'frontend_engineer', label: 'Frontend Engineer', emoji: '🎨', desc: 'React, Vue, UI/UX' },
  { id: 'backend_engineer', label: 'Backend Engineer', emoji: '⚙️', desc: 'API, Database, Server' },
  { id: 'devops_engineer', label: 'DevOps Engineer', emoji: '🚀', desc: 'CI/CD, Cloud, Infra' },
  { id: 'ml_ai_engineer', label: 'ML / AI Engineer', emoji: '🤖', desc: 'ML, Deep Learning, NLP' },
  { id: 'ui_ux_designer', label: 'UI/UX Designer', emoji: '✨', desc: 'Figma, Research, Design' },
  { id: 'data_analyst', label: 'Data Analyst', emoji: '📊', desc: 'SQL, Python, BI' },
  { id: 'cybersecurity', label: 'Cybersecurity', emoji: '🔒', desc: 'Security, Audit, Pen Test' },
  { id: 'digital_marketer', label: 'Digital Marketer', emoji: '📱', desc: 'SEO, Ads, Growth' },
]

const SKILLS_BY_TRACK: Record<string, string[]> = {
  frontend_engineer: ['HTML/CSS', 'JavaScript', 'TypeScript', 'React', 'Vue', 'Next.js', 'Tailwind', 'Figma', 'Git', 'Testing'],
  backend_engineer: ['Python', 'Node.js', 'Go', 'Java', 'SQL', 'PostgreSQL', 'REST API', 'Docker', 'Git', 'Redis'],
  devops_engineer: ['Linux', 'Docker', 'Kubernetes', 'CI/CD', 'AWS', 'GCP', 'Terraform', 'Monitoring', 'Git', 'Scripting'],
  ml_ai_engineer: ['Python', 'TensorFlow', 'PyTorch', 'Scikit-learn', 'NLP', 'Computer Vision', 'SQL', 'Statistics', 'MLOps', 'Git'],
  ui_ux_designer: ['Figma', 'User Research', 'Wireframing', 'Prototyping', 'Design System', 'Typography', 'Usability Testing', 'Information Architecture', 'Visual Design', 'Interaction Design'],
  data_analyst: ['SQL', 'Python', 'Excel', 'Tableau', 'Power BI', 'Statistics', 'Data Cleaning', 'Visualization', 'R', 'Git'],
  cybersecurity: ['Network Security', 'Linux', 'Python', 'Pen Testing', 'OWASP', 'Cryptography', 'SIEM', 'Incident Response', 'Compliance', 'Forensics'],
  digital_marketer: ['SEO', 'Google Ads', 'Meta Ads', 'Analytics', 'Content Marketing', 'Email Marketing', 'Social Media', 'Copywriting', 'A/B Testing', 'CRM'],
}

const LEARNING_FORMATS = ['Video', 'Artikel', 'Buku', 'Project', 'Kursus Online', 'Mentoring']
const STUDY_TIMES = ['Pagi (6-9)', 'Siang (12-14)', 'Sore (16-18)', 'Malam (19-22)', 'Larut (22+)']
const BLOCKERS = ['Waktu terbatas', 'Motivasi naik turun', 'Bingung mulai dari mana', 'Materi berbayar', 'Tidak ada mentor', 'Bahasa Inggris']
const SENIORITY = ['Junior', 'Mid-level', 'Senior', 'Lead']

// ── Chip Component ──
function Chip({ label, selected, onClick }: { label: string; selected: boolean; onClick: () => void }) {
  return (
    <button
      type="button"
      onClick={onClick}
      className={`px-4 py-2 rounded-xl font-display font-bold text-sm transition-all duration-150 border-2
        ${selected
          ? 'bg-brand-blue text-white border-dark shadow-neo-sm transform -translate-y-0.5'
          : 'bg-white text-dark border-border-bold hover:bg-brand-blue-light shadow-[1px_1px_0px_#09090B]'
        }`}
    >
      {label}
    </button>
  )
}

// ── Skill Dot Rating ──
function SkillDots({ level, onChange }: { level: number; onChange: (n: number) => void }) {
  return (
    <div className="flex gap-1.5">
      {[1, 2, 3].map((n) => (
        <button
          key={n}
          type="button"
          onClick={(e) => {
            e.stopPropagation()
            onChange(n)
          }}
          className={`w-4 h-4 rounded-full border-2 transition-all
            ${n <= level ? 'bg-brand-pink border-dark shadow-[1px_1px_0px_#09090B]' : 'bg-white border-border-bold'}
          `}
        />
      ))}
    </div>
  )
}

// ── Progress Bar ──
function ProgressBar({ current, total }: { current: number; total: number }) {
  return (
    <div className="flex gap-2 w-full">
      {Array.from({ length: total }).map((_, i) => (
        <div
          key={i}
          className={`h-2.5 flex-1 rounded-full border-2 transition-all duration-300
            ${i < current ? 'bg-brand-blue border-dark shadow-[1px_1px_0px_#09090B]' : 'bg-white border-border-light'}
          `}
        />
      ))}
    </div>
  )
}

// ── Slide animation wrapper ──
function SlideIn({ children, screenKey }: { children: React.ReactNode; screenKey: number }) {
  return (
    <AnimatePresence mode="wait">
      <motion.div
        key={screenKey}
        initial={{ opacity: 0, x: 40 }}
        animate={{ opacity: 1, x: 0 }}
        exit={{ opacity: 0, x: -40 }}
        transition={{ duration: 0.25, ease: 'easeOut' }}
      >
        {children}
      </motion.div>
    </AnimatePresence>
  )
}

// ═══════════════════════════════════════════
// MAIN ONBOARDING PAGE
// ═══════════════════════════════════════════
export default function OnboardingPage() {
  const navigate = useNavigate()
  const { currentScreen, answers, setScreen, setAnswer } = useOnboardingStore()
  const [isGenerating, setIsGenerating] = useState(false)
  const [loadingMsg, setLoadingMsg] = useState(0)
  const [error, setError] = useState('')
  const [customSkillInput, setCustomSkillInput] = useState('')

  const LOADING_MESSAGES = [
    'Menganalisis skill kamu...',
    'Membandingkan dengan pasar kerja Indonesia...',
    'Menyusun milestone perjalananmu...',
    'Hampir selesai...',
  ]

  const next = () => setScreen(Math.min(currentScreen + 1, 7))
  const prev = () => setScreen(Math.max(currentScreen - 1, 1))

  const toggleArrayItem = (key: keyof typeof answers, item: string) => {
    const arr = (answers[key] as string[]) || []
    if (arr.includes(item)) {
      setAnswer(key as any, arr.filter((i: string) => i !== item))
    } else {
      setAnswer(key as any, [...arr, item])
    }
  }

  const handleSubmit = async () => {
    setIsGenerating(true)
    setError('')

    const msgInterval = setInterval(() => {
      setLoadingMsg((p) => (p + 1) % LOADING_MESSAGES.length)
    }, 2000)

    try {
      const payload = {
        current_role: answers.currentRole || '',
        current_field: answers.currentField || '',
        target_role: answers.targetRole || '',
        target_field: answers.targetField || answers.targetRole || '',
        experience_level: answers.seniorityTarget?.toLowerCase() || 'beginner',
        years_experience: answers.yearsExperience || 0,
        current_skills: answers.currentSkills || [],
        time_budget_minutes: answers.timeBudgetMinutes || 60,
        preferred_learning_style: (answers.preferredLearningStyle || []).join(', '),
        preferred_study_time: answers.preferredStudyTime || '',
        blockers: answers.blockers || [],
        locale: 'id',
      }

      await onboardingService.submit(payload)
      clearInterval(msgInterval)
      navigate('/overview')
    } catch (err: any) {
      clearInterval(msgInterval)
      setIsGenerating(false)
      setError(err?.response?.data?.message || err.message || 'Terjadi kesalahan')
    }
  }

  if (isGenerating) {
    return (
      <div className="min-h-dvh bg-bg-base flex flex-col items-center justify-center gap-6 px-8 relative">
        <div className="absolute inset-0 opacity-[0.03]" style={{ backgroundImage: 'radial-gradient(#09090B 1.5px, transparent 1.5px)', backgroundSize: '24px 24px' }}></div>
        <div className="neo-card p-8 border-4 flex flex-col items-center gap-6 z-10 w-full max-w-sm text-center relative overflow-hidden">
          <div className="absolute top-0 right-0 w-32 h-32 bg-brand-yellow/30 blur-2xl rounded-full" />
          <img src="/kaix_logo.png" alt="Kaix" className="w-16 h-16 object-contain drop-shadow-md animate-bounce" />
          <KnotLoader size="lg" />
          <motion.p
            key={loadingMsg}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="font-display font-bold text-lg text-dark"
          >
            {LOADING_MESSAGES[loadingMsg]}
          </motion.p>
          {error && (
            <div className="bg-brand-red text-white text-sm font-bold px-4 py-3 rounded-lg border-2 border-dark shadow-neo-sm mt-4 w-full">
              {error}
              <button onClick={() => setIsGenerating(false)} className="block mt-2 underline w-full text-center">Coba lagi</button>
            </div>
          )}
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-dvh bg-bg-base flex flex-col relative">
      <div className="absolute inset-0 opacity-[0.03] pointer-events-none" style={{ backgroundImage: 'radial-gradient(#09090B 1.5px, transparent 1.5px)', backgroundSize: '24px 24px' }}></div>
      
      {/* Header */}
      <div className="px-6 pt-6 pb-4 relative z-10 bg-bg-base">
        <div className="flex items-center gap-3 mb-6">
          <img src="/kaix_logo.png" alt="Kaix" className="w-10 h-10 object-contain drop-shadow-sm" />
          <span className="font-display text-xl text-dark font-extrabold tracking-tight">kaix</span>
        </div>
        <ProgressBar current={currentScreen} total={7} />
        <p className="font-display font-bold text-xs text-text-muted mt-3 uppercase tracking-wider">Langkah {currentScreen} dari 7</p>
      </div>

      {/* Content */}
      <div className="flex-1 px-6 pb-24 overflow-y-auto relative z-10">
        <SlideIn screenKey={currentScreen}>
          {/* ── SCREEN 1: Welcome ── */}
          {currentScreen === 1 && (
            <div>
              <h1 className="font-display font-extrabold text-3xl text-dark mb-3">Selamat datang! 👋</h1>
              <p className="font-body font-medium text-base text-text-secondary mb-8 leading-relaxed">
                Yuk kenalan dulu. Jawab beberapa pertanyaan supaya kami bisa buatkan roadmap belajar yang pas buat kamu.
              </p>
              <div className="neo-card p-6 border-4">
                <p className="font-display font-bold text-sm text-dark mb-4">Bahasa pilihan kamu:</p>
                <div className="flex gap-3">
                  <Chip label="🇮🇩 Indonesia" selected={true} onClick={() => {}} />
                  <Chip label="🇬🇧 English" selected={false} onClick={() => {}} />
                </div>
              </div>
            </div>
          )}

          {/* ── SCREEN 2: User Type ── */}
          {currentScreen === 2 && (
            <div>
              <h1 className="font-display font-extrabold text-2xl text-dark mb-3">Kamu saat ini...</h1>
              <p className="font-body font-medium text-text-secondary mb-6">Pilih yang paling menggambarkan situasimu.</p>
              <div className="flex flex-col gap-4">
                {[
                  { type: 'student' as UserType, emoji: '🎓', title: 'Mahasiswa / Fresh Grad', desc: 'Masih kuliah atau baru lulus' },
                  { type: 'professional' as UserType, emoji: '💼', title: 'Profesional', desc: 'Sudah bekerja di bidang tertentu' },
                  { type: 'switcher' as UserType, emoji: '🔄', title: 'Career Switcher', desc: 'Mau pindah ke bidang baru' },
                ].map((opt) => (
                  <button
                    key={opt.type}
                    onClick={() => setAnswer('userType', opt.type)}
                    className={`neo-card p-5 text-left transition-all border-4 flex items-center gap-4 ${
                      answers.userType === opt.type ? 'border-brand-blue shadow-neo-blue bg-brand-blue-light/30 transform -translate-y-1' : ''
                    }`}
                  >
                    <div className="w-12 h-12 bg-white rounded-xl border-2 border-dark shadow-neo-sm flex items-center justify-center text-2xl shrink-0">
                      {opt.emoji}
                    </div>
                    <div>
                      <p className="font-display font-bold text-lg text-dark">{opt.title}</p>
                      <p className="font-body font-medium text-sm text-text-secondary">{opt.desc}</p>
                    </div>
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* ── SCREEN 3: Background ── */}
          {currentScreen === 3 && (
            <div>
              <h1 className="font-display font-extrabold text-2xl text-dark mb-3">Background kamu 📋</h1>
              <p className="font-body font-medium text-text-secondary mb-6">Ceritakan sedikit tentang pengalamanmu.</p>
              <div className="flex flex-col gap-5">
                <div>
                  <label className="font-display font-bold text-sm text-dark mb-2 block">
                    {answers.userType === 'student' ? 'Jurusan / Bidang studi' : 'Posisi / Jabatan saat ini'}
                  </label>
                  <input
                    type="text"
                    value={answers.currentRole || ''}
                    onChange={(e) => setAnswer('currentRole', e.target.value)}
                    placeholder={answers.userType === 'student' ? 'Contoh: Teknik Informatika' : 'Contoh: Junior Developer'}
                    className="input-field"
                  />
                </div>
                <div>
                  <label className="font-display font-bold text-sm text-dark mb-2 block">Bidang / Industri</label>
                  <input
                    type="text"
                    value={answers.currentField || ''}
                    onChange={(e) => setAnswer('currentField', e.target.value)}
                    placeholder="Contoh: Teknologi, Fintech"
                    className="input-field"
                  />
                </div>
                <div className="neo-card p-5 border-4 bg-brand-yellow/10">
                  <label className="font-display font-bold text-sm text-dark mb-4 block flex justify-between items-end">
                    Pengalaman
                    <span className="text-xl text-brand-blue bg-white px-2 py-1 rounded-lg border-2 border-dark shadow-neo-sm">
                      {(answers.yearsExperience && answers.yearsExperience > 15) ? '15+' : (answers.yearsExperience || 0)} tahun
                    </span>
                  </label>
                  <input
                    type="range"
                    min={0} max={15} step={1}
                    value={(answers.yearsExperience && answers.yearsExperience > 15) ? 15 : (answers.yearsExperience || 0)}
                    onChange={(e) => setAnswer('yearsExperience', Number(e.target.value))}
                    disabled={(answers.yearsExperience && answers.yearsExperience > 15) ? true : false}
                    className={`w-full accent-dark h-2 rounded-full mb-4 ${answers.yearsExperience && answers.yearsExperience > 15 ? 'opacity-50' : ''}`}
                  />
                  {(answers.yearsExperience || 0) >= 15 && (
                    <label className="flex items-center gap-3 cursor-pointer bg-white px-4 py-3 rounded-xl border-2 border-dark shadow-[2px_2px_0px_#09090B]">
                      <input
                        type="checkbox"
                        checked={(answers.yearsExperience && answers.yearsExperience > 15) ? true : false}
                        onChange={(e) => {
                          if (e.target.checked) setAnswer('yearsExperience', 16)
                          else setAnswer('yearsExperience', 15)
                        }}
                        className="w-5 h-5 rounded border-2 border-dark text-brand-blue focus:ring-brand-blue accent-brand-blue"
                      />
                      <span className="font-display font-bold text-sm text-dark">&gt; 15 tahun pengalaman</span>
                    </label>
                  )}
                </div>
              </div>
            </div>
          )}

          {/* ── SCREEN 4: Target Role ── */}
          {currentScreen === 4 && (
            <div>
              <h1 className="font-display font-extrabold text-2xl text-dark mb-3">Tujuan karir kamu 🎯</h1>
              <p className="font-body font-medium text-text-secondary mb-6">Pilih track yang ingin kamu kejar.</p>
              <div className="grid grid-cols-2 gap-3 mb-8">
                {CAREER_TRACKS.map((track) => (
                  <button
                    key={track.id}
                    onClick={() => {
                      setAnswer('targetRole', track.id)
                      setAnswer('targetField', track.label)
                    }}
                    className={`neo-card p-4 text-left transition-all border-4 flex flex-col justify-between min-h-[120px] ${
                      answers.targetRole === track.id ? 'border-brand-blue shadow-neo-blue bg-brand-blue-light/20 transform -translate-y-1' : ''
                    }`}
                  >
                    <span className="text-3xl mb-2 bg-white w-10 h-10 flex items-center justify-center rounded-xl border-2 border-dark shadow-neo-sm">{track.emoji}</span>
                    <div>
                      <p className="font-display font-bold text-sm text-dark leading-tight">{track.label}</p>
                    </div>
                  </button>
                ))}
              </div>
              <div className="neo-card p-5 border-4">
                <p className="font-display font-bold text-sm text-dark mb-3">Target Seniority:</p>
                <div className="flex flex-wrap gap-2">
                  {SENIORITY.map((s) => (
                    <Chip key={s} label={s} selected={answers.seniorityTarget === s} onClick={() => setAnswer('seniorityTarget', s)} />
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* ── SCREEN 5: Skills Audit ── */}
          {currentScreen === 5 && (
            <div>
              <h1 className="font-display font-extrabold text-2xl text-dark mb-3">Skill kamu saat ini 💪</h1>
              <p className="font-body font-medium text-text-secondary mb-6">Pilih skill yang kamu kuasai dan nilai seberapa pede kamu.</p>
              
              <div className="flex gap-2 mb-6">
                <input
                  type="text"
                  value={customSkillInput}
                  onChange={(e) => setCustomSkillInput(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === 'Enter' && customSkillInput.trim()) {
                      e.preventDefault()
                      const newSkill = customSkillInput.trim()
                      setAnswer('customSkills', [...(answers.customSkills || []), newSkill])
                      if (!(answers.currentSkills || []).includes(newSkill)) toggleArrayItem('currentSkills', newSkill)
                      if (!answers.skillLevels?.[newSkill]) setAnswer('skillLevels', { ...(answers.skillLevels || {}), [newSkill]: 1 })
                      setCustomSkillInput('')
                    }
                  }}
                  placeholder="Ketik skill lain & tekan Enter..."
                  className="input-field flex-1"
                />
                <button
                  type="button"
                  onClick={() => {
                    if (customSkillInput.trim()) {
                      const newSkill = customSkillInput.trim()
                      setAnswer('customSkills', [...(answers.customSkills || []), newSkill])
                      if (!(answers.currentSkills || []).includes(newSkill)) toggleArrayItem('currentSkills', newSkill)
                      if (!answers.skillLevels?.[newSkill]) setAnswer('skillLevels', { ...(answers.skillLevels || {}), [newSkill]: 1 })
                      setCustomSkillInput('')
                    }
                  }}
                  className="btn-secondary px-4 border-4"
                >
                  +
                </button>
              </div>

              <div className="grid grid-cols-2 gap-3 mb-4">
                {Array.from(new Set([...(SKILLS_BY_TRACK[answers.targetRole || 'frontend_engineer'] || SKILLS_BY_TRACK.frontend_engineer), ...(answers.customSkills || [])])).map((skill) => {
                  const isSelected = (answers.currentSkills || []).includes(skill)
                  const level = (answers.skillLevels || {})[skill] || 0
                  return (
                    <button
                      key={skill}
                      onClick={() => {
                        toggleArrayItem('currentSkills', skill)
                        if (!isSelected) setAnswer('skillLevels', { ...(answers.skillLevels || {}), [skill]: 1 })
                      }}
                      className={`neo-card p-3 text-left transition-all border-4 flex flex-col justify-between min-h-[90px] ${isSelected ? 'border-brand-blue shadow-neo-sm bg-brand-blue-light/20' : ''}`}
                    >
                      <p className="font-display font-bold text-sm text-dark break-words">{skill}</p>
                      <div className="mt-2 h-6 flex items-end">
                        {isSelected && (
                          <SkillDots
                            level={level}
                            onChange={(n) => setAnswer('skillLevels', { ...(answers.skillLevels || {}), [skill]: n })}
                          />
                        )}
                      </div>
                    </button>
                  )
                })}
              </div>
            </div>
          )}

          {/* ── SCREEN 6: Learning Preferences ── */}
          {currentScreen === 6 && (
            <div>
              <h1 className="font-display font-extrabold text-2xl text-dark mb-3">Gaya belajar kamu 📖</h1>
              <p className="font-body font-medium text-text-secondary mb-6">Bantu kami sesuaikan roadmap dengan kebiasaanmu.</p>

              {/* Time budget */}
              <div className="neo-card p-5 border-4 mb-6 bg-brand-blue-light/30">
                <label className="font-display font-bold text-sm text-dark mb-4 flex justify-between items-center">
                  Waktu belajar harian
                  <span className="text-sm font-extrabold bg-white px-3 py-1.5 rounded-lg border-2 border-dark shadow-neo-sm text-brand-blue">
                    {answers.timeBudgetMinutes || 60} menit <span className="text-text-muted text-xs">({Math.round((answers.timeBudgetMinutes || 60) / 60 * 10) / 10} j)</span>
                  </span>
                </label>
                <input
                  type="range"
                  min={15} max={300} step={15}
                  value={answers.timeBudgetMinutes || 60}
                  onChange={(e) => setAnswer('timeBudgetMinutes', Number(e.target.value))}
                  className="w-full accent-brand-blue h-2 rounded-full"
                />
              </div>

              {/* Format */}
              <div className="mb-6">
                <p className="font-display font-bold text-sm text-dark mb-3">Format belajar favorit:</p>
                <div className="flex flex-wrap gap-2">
                  {LEARNING_FORMATS.map((f) => (
                    <Chip key={f} label={f} selected={(answers.preferredLearningStyle || []).includes(f)} onClick={() => toggleArrayItem('preferredLearningStyle', f)} />
                  ))}
                </div>
              </div>

              {/* Study time */}
              <div className="mb-6">
                <p className="font-display font-bold text-sm text-dark mb-3">Waktu belajar favorit:</p>
                <div className="flex flex-wrap gap-2">
                  {STUDY_TIMES.map((t) => (
                    <Chip key={t} label={t} selected={answers.preferredStudyTime === t} onClick={() => setAnswer('preferredStudyTime', t)} />
                  ))}
                </div>
              </div>

              {/* Blockers */}
              <div className="neo-card p-5 border-4 bg-brand-pink/10">
                <p className="font-display font-bold text-sm text-dark mb-3">Tantangan terbesarmu saat belajar:</p>
                <div className="flex flex-wrap gap-2">
                  {BLOCKERS.map((b) => (
                    <Chip key={b} label={b} selected={(answers.blockers || []).includes(b)} onClick={() => toggleArrayItem('blockers', b)} />
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* ── SCREEN 7: Confirmation ── */}
          {currentScreen === 7 && (
            <div>
              <h1 className="font-display font-extrabold text-2xl text-dark mb-3">Konfirmasi ✅</h1>
              <p className="font-body font-medium text-text-secondary mb-6">Cek ringkasan jawabanmu sebelum kami meracik roadmapnya.</p>

              <div className="neo-card p-5 border-4 mb-6">
                <div className="flex flex-col gap-4">
                  <div className="flex justify-between items-center border-b-2 border-border-light pb-2">
                    <span className="font-display font-bold text-xs text-text-muted uppercase">Tipe</span>
                    <span className="font-display font-bold text-sm text-dark capitalize bg-white border-2 border-border-light px-2 py-1 rounded-lg">{answers.userType || '-'}</span>
                  </div>
                  <div className="flex justify-between items-center border-b-2 border-border-light pb-2">
                    <span className="font-display font-bold text-xs text-text-muted uppercase">Background</span>
                    <span className="font-display font-bold text-sm text-dark text-right max-w-[60%]">{answers.currentRole || '-'}</span>
                  </div>
                  <div className="flex justify-between items-center border-b-2 border-border-light pb-2">
                    <span className="font-display font-bold text-xs text-text-muted uppercase">Target</span>
                    <span className="font-display font-bold text-sm text-brand-blue bg-brand-blue-light/50 px-2 py-1 rounded-lg border-2 border-brand-blue/20">
                      {CAREER_TRACKS.find((t) => t.id === answers.targetRole)?.label || answers.targetRole || '-'}
                    </span>
                  </div>
                  <div className="flex justify-between items-center border-b-2 border-border-light pb-2">
                    <span className="font-display font-bold text-xs text-text-muted uppercase">Seniority</span>
                    <span className="font-display font-bold text-sm text-dark">{answers.seniorityTarget || '-'}</span>
                  </div>
                  <div className="flex justify-between items-center border-b-2 border-border-light pb-2">
                    <span className="font-display font-bold text-xs text-text-muted uppercase">Pengalaman</span>
                    <span className="font-display font-bold text-sm text-dark">{answers.yearsExperience || 0} tahun</span>
                  </div>
                  <div className="flex justify-between items-center border-b-2 border-border-light pb-2">
                    <span className="font-display font-bold text-xs text-text-muted uppercase">Skills</span>
                    <span className="font-display font-bold text-sm text-dark bg-brand-yellow/30 px-2 py-1 rounded-lg border-2 border-brand-yellow/50">{(answers.currentSkills || []).length} skill</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="font-display font-bold text-xs text-text-muted uppercase">Waktu</span>
                    <span className="font-display font-bold text-sm text-dark">{answers.timeBudgetMinutes || 60} min/hari</span>
                  </div>
                </div>
              </div>

              {error && (
                <div className="bg-brand-red text-white text-sm font-bold px-4 py-3 rounded-lg border-2 border-dark shadow-neo-sm mb-6">
                  {error}
                </div>
              )}

              <button onClick={handleSubmit} className="btn-neo w-full text-lg py-4 border-4 bg-brand-blue">
                🚀 Buat Roadmap Sekarang
              </button>
              <button onClick={() => setScreen(1)} className="btn-ghost w-full mt-3 text-sm font-bold border-2 border-transparent">
                Ada yang salah? Edit jawaban
              </button>
            </div>
          )}
        </SlideIn>
      </div>

      {/* Footer nav buttons */}
      {currentScreen < 7 && !isGenerating && (
        <div className="fixed bottom-0 left-0 right-0 bg-white border-t-4 border-dark p-4 z-50">
          <div className="max-w-lg mx-auto flex gap-3">
            {currentScreen > 1 && (
              <button onClick={prev} className="btn-secondary flex-1 py-3 border-4">Kembali</button>
            )}
            <button
              onClick={next}
              className="btn-neo flex-[2] py-3 border-4 bg-dark text-white border-dark hover:bg-black"
              disabled={currentScreen === 2 && !answers.userType}
            >
              Lanjut ➔
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
