import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuthStore } from '@/stores/authStore'
import { overviewService, statsService, roadmapService, activityService, courseService } from '@/services/backend'
import KnotLoader from '@/components/ui/KnotLoader'
import NotificationBell from '@/components/ui/NotificationBell'

export default function OverviewPage() {
  const user = useAuthStore((s) => s.user)
  const navigate = useNavigate()
  const [loading, setLoading] = useState(true)
  const [streak, setStreak] = useState({ current_streak: 0, longest_streak: 0 })
  const [roadmap, setRoadmap] = useState<any>(null)
  const [allActivities, setAllActivities] = useState<any[]>([])
  const [focusCourses, setFocusCourses] = useState<any[]>([])
  const [note, setNote] = useState('')
  const [savingNote, setSavingNote] = useState(false)
  const [actPage, setActPage] = useState(1)
  const PER_PAGE = 5

  useEffect(() => {
    loadData()
  }, [])

  // Auto-poll for roadmap if still generating
  useEffect(() => {
    if (roadmap || loading) return
    const interval = setInterval(async () => {
      try {
        const res = await roadmapService.get()
        if (res.data?.data) {
          setRoadmap(res.data.data)
          clearInterval(interval)
        }
      } catch { /* still pending */ }
    }, 8000)
    // Stop polling after 2 minutes
    const timeout = setTimeout(() => clearInterval(interval), 120_000)
    return () => { clearInterval(interval); clearTimeout(timeout) }
  }, [roadmap, loading])

  const loadData = async () => {
    setLoading(true)
    try {
      const [streakRes, roadmapRes, actRes, focusRes] = await Promise.allSettled([
        statsService.streak(),
        roadmapService.get(),
        activityService.list(1),
        courseService.getTodayFocus(),
      ])
      if (streakRes.status === 'fulfilled') setStreak(streakRes.value.data?.data || { current_streak: 0, longest_streak: 0 })
      if (roadmapRes.status === 'fulfilled') setRoadmap(roadmapRes.value.data?.data)
      if (actRes.status === 'fulfilled') {
        const items = actRes.value.data?.data?.items || []
        setAllActivities(items)
        setActPage(1)
      }
      if (focusRes.status === 'fulfilled') setFocusCourses(focusRes.value.data?.data?.items || [])
    } catch (err) {
      console.error('Failed to load overview:', err)
    }
    setLoading(false)
  }

  const handleSaveNote = async () => {
    if (!note.trim()) return
    setSavingNote(true)
    try {
      await overviewService.saveNote(note)
      setNote('')
    } catch (err) { console.error(err) }
    setSavingNote(false)
  }

  const currentPhase = roadmap?.roadmap_json?.phases?.[0]
  const currentMilestones = currentPhase?.milestones || []

  // Week dots helper
  const dayLabels = ['S', 'S', 'R', 'K', 'J', 'S', 'M']
  const today = new Date().getDay() // 0=Sun

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center h-[60vh] gap-6 px-8 relative">
        <div className="absolute inset-0 opacity-[0.03]" style={{ backgroundImage: 'radial-gradient(#09090B 1.5px, transparent 1.5px)', backgroundSize: '24px 24px' }}></div>
        <div className="neo-card p-8 border-4 border-dark flex flex-col items-center z-10 w-full text-center">
          <KnotLoader size="md" />
          <p className="font-display font-bold text-lg text-dark mt-4">Memuat dashboard...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="px-4 pb-24 relative overflow-hidden">
      <div className="absolute inset-0 opacity-[0.03] pointer-events-none" style={{ backgroundImage: 'radial-gradient(#09090B 1.5px, transparent 1.5px)', backgroundSize: '24px 24px' }}></div>

      {/* Top bar */}
      <div className="sticky top-0 z-50 bg-bg-base/95 backdrop-blur-sm pt-5 pb-4 mb-2 flex items-center justify-between border-b-2 border-dark/10 -mx-4 px-4">
        <div className="flex items-center gap-3">
          <img src="/kaix_logo.png" alt="Kaix" className="w-10 h-10 object-contain drop-shadow-sm" />
          <span className="font-display text-xl text-dark font-extrabold tracking-tight">kaix</span>
        </div>
        <div className="flex items-center gap-3">
          <NotificationBell />
          <button onClick={() => navigate('/profile')} className="w-11 h-11 rounded-full border-2 border-dark shadow-[2px_2px_0px_#09090B] bg-brand-blue text-white flex items-center justify-center font-display font-bold text-base hover:shadow-[4px_4px_0px_#09090B] hover:-translate-y-0.5 transition-all">
            {user?.name?.charAt(0)?.toUpperCase() || 'K'}
          </button>
        </div>
      </div>

      {/* Greeting */}
      <div className="relative z-10 mb-6 mt-4">
        <h1 className="font-display text-3xl text-dark font-extrabold mb-1">Halo, {user?.name?.split(' ')[0] || 'User'}! 👋</h1>
        <p className="font-body text-base font-medium text-text-secondary">Mari lanjutkan perjalanan belajarmu hari ini.</p>
      </div>

      {/* Daily quote card */}
      <div className="neo-card p-5 border-4 border-dark shadow-neo-sm bg-brand-yellow relative mb-6 overflow-hidden">
        <span className="absolute -top-4 -right-2 font-display text-[100px] leading-none opacity-20 text-white select-none pointer-events-none" aria-hidden="true">"</span>
        <div className="flex items-center gap-2 mb-3 relative z-10">
          <div className="w-2.5 h-2.5 rounded-full bg-dark" />
          <span className="font-display text-xs tracking-widest text-dark font-black uppercase">Quote buatmu!</span>
        </div>
        <p className="font-body text-sm font-semibold leading-relaxed text-dark relative z-10">
          {roadmap?.roadmap_json?.daily_quote
            ? `"${roadmap.roadmap_json.daily_quote}"`
            : '"Langkah kecil yang konsisten lebih baik daripada lompatan besar yang jarang dilakukan."'
          }
        </p>
      </div>

      {/* Streak card */}
      <div className="neo-card p-5 border-4 border-dark shadow-neo-sm mb-6 bg-white relative z-10">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-4">
            <span className="text-4xl">🔥</span>
            <div>
              <p className="font-display text-lg font-extrabold text-dark">Konsistensi</p>
              <p className="font-body text-xs font-semibold text-text-secondary">Terus pertahankan semangatmu!</p>
            </div>
          </div>
          <div className="text-right flex flex-col items-end">
            <div className="bg-brand-pink border-2 border-dark px-3 py-1 rounded-xl shadow-[2px_2px_0px_#09090B] -rotate-3">
              <p className="font-display text-3xl text-dark font-black leading-none">{streak.current_streak}</p>
            </div>
            <p className="font-display text-[10px] font-extrabold uppercase text-dark tracking-wider mt-2">Total Streak</p>
          </div>
        </div>

        <div className="flex items-center justify-between mt-6 px-2">
          {dayLabels.map((day, i) => {
            const dayIndex = (i + 1) % 7 // Mon=1..Sun=0 mapped to JS getDay()
            const isToday = dayIndex === today
            // today's position in the Mon-Sun array (0-indexed)
            const todayIdx = (today + 6) % 7 // Fri(5) → 4, Mon(1) → 0, Sun(0) → 6
            // Only fill past days within streak range (not future days this week)
            const isPast = i < todayIdx
            const daysAgoFromToday = todayIdx - i
            const filled = isPast && daysAgoFromToday < streak.current_streak
            return (
              <div key={i} className="flex flex-col items-center gap-2">
                <div className={`w-9 h-9 rounded-full border-[3px] flex items-center justify-center transition-all shadow-[2px_2px_0px_#09090B]
                  ${isToday ? 'border-dark bg-brand-yellow transform scale-110' : filled ? 'border-dark bg-green-300' : 'border-dark bg-white'}
                `}>
                  {isToday && <span className="text-base">🔥</span>}
                  {filled && !isToday && <span className="text-base">✓</span>}
                </div>
                <span className={`font-display text-xs font-extrabold ${isToday ? 'text-brand-blue' : 'text-dark'}`}>{day}</span>
              </div>
            )
          })}
        </div>
      </div>

      {/* Agent Setting Up Journey Placeholder (shown when roadmap is not ready yet) */}
      {!roadmap ? (
        <div className="neo-card p-6 border-4 border-dark shadow-neo-md bg-white mb-6 relative overflow-hidden z-10">
          <div className="absolute top-0 right-0 w-24 h-24 rounded-full bg-brand-yellow/10 blur-xl pointer-events-none" />
          <div className="flex items-center gap-4 mb-4">
            <div className="w-12 h-12 rounded-full border-2 border-dark bg-brand-yellow flex items-center justify-center shadow-[2px_2px_0_#09090B] shrink-0">
              <span className="text-2xl animate-bounce">🤖</span>
            </div>
            <div>
              <h3 className="font-display text-base font-black text-dark leading-snug">Menyiapkan Perjalanan Karirmu</h3>
              <p className="font-body text-xs font-semibold text-text-secondary mt-0.5">Agent AI kami sedang merancang kurikulum belajar personalmu...</p>
            </div>
          </div>
          <div className="bg-[#EFF6FF] border-2 border-dashed border-brand-blue/30 rounded-xl p-4 flex flex-col gap-3">
            <div className="flex items-center gap-2.5">
              <div className="w-2.5 h-2.5 rounded-full bg-brand-green border border-dark" />
              <span className="font-body text-xs font-bold text-dark">Menganalisis skill gap...</span>
            </div>
            <div className="flex items-center gap-2.5">
              <div className="w-2.5 h-2.5 rounded-full bg-brand-green border border-dark" />
              <span className="font-body text-xs font-bold text-dark">Mengumpulkan rekomendasi kursus...</span>
            </div>
            <div className="flex items-center gap-2.5">
              <div className="w-2.5 h-2.5 rounded-full bg-brand-blue border border-dark animate-ping" />
              <span className="font-body text-xs font-bold text-brand-blue">Membuat roadmap belajar modular (~1 menit)...</span>
            </div>
          </div>
          <div className="flex items-center gap-2 justify-center mt-5 text-[11px] font-display font-black text-text-muted">
            <KnotLoader size="sm" /> Halaman ini akan memuat ulang secara otomatis / Autopolling active
          </div>
        </div>
      ) : (
        <>
          {/* Fokus Hari Ini — from user's focus courses */}
          <div className="mb-6 relative z-10">
            <div className="flex items-center justify-between mb-3">
              <h2 className="font-display text-xl font-extrabold text-dark">Fokus Hari Ini</h2>
              {focusCourses.length > 0 && (
                <span onClick={() => navigate('/focus')} className="font-display font-bold text-xs text-brand-pink bg-brand-pink/10 cursor-pointer hover:bg-brand-pink/20 border-2 border-brand-pink px-2 py-1 rounded-lg transition-colors">
                  Mulai ➔
                </span>
              )}
            </div>
            <div className="neo-card p-5 border-4 border-dark shadow-neo-sm bg-white">
              {focusCourses.length > 0 ? (
                <div className="flex flex-col gap-3">
                  {focusCourses.slice(0, 4).map((course: any) => (
                    <div key={course.id} className="flex items-center gap-3 p-3 bg-brand-yellow/10 rounded-xl border-2 border-brand-yellow border-dashed">
                      <div className="w-8 h-8 rounded-lg border-2 border-dark bg-brand-yellow flex items-center justify-center shadow-[1px_1px_0px_#09090B] shrink-0">
                        <span className="text-sm font-bold text-dark">★</span>
                      </div>
                      <div className="flex-1 min-w-0">
                        <p className="font-display font-bold text-sm text-dark truncate">{course.title}</p>
                        <div className="flex items-center gap-2 mt-1">
                          {course.platform && (
                            <span className="font-body font-bold text-[10px] uppercase text-brand-blue bg-blue-light px-1.5 py-0.5 rounded border border-brand-blue/20">{course.platform}</span>
                          )}
                          {course.estimated_hours && course.completed_hours !== undefined && (
                            <span className="font-body font-semibold text-[10px] text-text-muted">
                              {course.completed_hours?.toFixed(1)}/{course.estimated_hours}h
                            </span>
                          )}
                        </div>
                      </div>
                      <button
                        onClick={() => navigate('/focus')}
                        className="px-3 py-1.5 rounded-lg bg-dark text-white font-display font-bold text-xs border-2 border-dark hover:bg-brand-blue hover:text-white transition-colors"
                      >
                        Mulai
                      </button>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="py-4 text-center">
                  <span className="text-3xl mb-2 block">🎯</span>
                  <p className="font-body font-medium text-sm text-text-secondary">
                    Tandai kursus dengan ★ di halaman Course untuk fokus hari ini!
                  </p>
                </div>
              )}
            </div>
          </div>

          {/* Winding Road / Roadmap section */}
          <div className="neo-card p-5 border-4 border-dark shadow-neo-sm mb-6 bg-brand-blue-light/10 relative z-10">
            <div className="flex items-center justify-between mb-4">
              <h2 className="font-display text-xl font-extrabold text-dark">Perjalananmu</h2>
              <span onClick={() => navigate('/course')} className="font-display font-bold text-xs text-brand-blue cursor-pointer hover:underline border-2 border-brand-blue px-2 py-1 rounded-lg">Detail →</span>
            </div>

            {currentPhase && (
              <div className="bg-white border-2 border-dark rounded-xl p-4 shadow-[2px_2px_0px_#09090B]">
                <p className="font-display text-[11px] uppercase tracking-widest text-brand-blue font-black mb-4">
                  Fase {currentPhase.phase_number} · {currentPhase.phase_title}
                </p>

                {/* Simple milestone list */}
                <div className="flex flex-col gap-3">
                  {currentMilestones.slice(0, 5).map((ms: any, i: number) => (
                    <div key={ms.milestone_id || i} className="flex items-center gap-3">
                      <div className={`w-7 h-7 rounded-full border-2 flex items-center justify-center text-xs font-bold shadow-[1px_1px_0px_#09090B] shrink-0
                        ${ms.status === 'completed' ? 'bg-brand-green border-dark text-dark' : ''}
                        ${ms.status === 'in_progress' ? 'bg-brand-blue border-dark text-white' : ''}
                        ${!ms.status || ms.status === 'locked' ? 'bg-border-light border-dark text-text-muted opacity-60' : ''}
                      `}>
                        {ms.status === 'completed' ? '✓' : ms.status === 'in_progress' ? '→' : '🔒'}
                      </div>
                      <div className="flex-1 min-w-0">
                        <p className={`font-body text-sm font-semibold truncate ${ms.status === 'completed' ? 'line-through text-text-muted' : 'text-dark'}`}>
                          {ms.title}
                        </p>
                      </div>
                      {ms.progress_pct > 0 && (
                        <span className="font-display font-bold text-xs text-brand-blue bg-blue-light px-1.5 py-0.5 rounded-md border border-brand-blue/30">{Math.round(ms.progress_pct)}%</span>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </>
      )}

      {/* Activity log */}
      {allActivities.length > 0 && (() => {
        const totalPages = Math.ceil(allActivities.length / PER_PAGE)
        const pageItems = allActivities.slice((actPage-1)*PER_PAGE, actPage*PER_PAGE)
        return (
        <div className="mb-6 relative z-10">
          <div className="flex items-center justify-between mb-3">
            <h2 className="font-display text-xl font-extrabold text-dark">Aktivitas Terakhir</h2>
            <span className="font-display font-bold text-xs bg-white border-2 border-dark px-2 py-0.5 rounded-full shadow-[1px_1px_0px_#09090B]">{(actPage-1)*PER_PAGE+1}–{Math.min(actPage*PER_PAGE,allActivities.length)} / {allActivities.length}</span>
          </div>
          <div className="flex flex-col gap-3">
            {pageItems.map((act: any) => (
              <div key={act.id} className="neo-card p-4 border-2 border-dark shadow-[2px_2px_0px_#09090B] bg-white flex items-start gap-3">
                <div className="w-8 h-8 bg-cream border-2 border-dark rounded-full flex items-center justify-center shrink-0 text-sm">📝</div>
                <div className="flex-1">
                  <p className="font-body font-bold text-sm text-dark">{act.raw_text}</p>
                  <div className="flex items-center flex-wrap gap-2 mt-2">
                    {act.classified_skill && <span className="font-display font-bold text-[10px] bg-brand-pink/20 text-brand-pink px-2 py-0.5 rounded-md border border-brand-pink/30">{act.classified_skill}</span>}
                    {act.duration_minutes && <span className="font-body font-semibold text-[10px] text-text-muted">⏱ {act.duration_minutes} menit</span>}
                  </div>
                </div>
              </div>
            ))}
          </div>
          {totalPages > 1 && (
            <div className="flex items-center justify-center gap-4 mt-4">
              <button onClick={() => setActPage(p => Math.max(1, p-1))} disabled={actPage <= 1} className="w-10 h-10 rounded-xl font-display font-black text-dark border-2 border-dark bg-white shadow-[2px_2px_0px_#09090B] disabled:opacity-40 hover:bg-brand-blue-light transition-all">←</button>
              <span className="font-display text-sm text-dark font-extrabold">Hal. {actPage}/{totalPages}</span>
              <button onClick={() => setActPage(p => Math.min(totalPages, p+1))} disabled={actPage >= totalPages} className="w-10 h-10 rounded-xl font-display font-black text-dark border-2 border-dark bg-white shadow-[2px_2px_0px_#09090B] disabled:opacity-40 hover:bg-brand-blue-light transition-all">→</button>
            </div>
          )}
        </div>
      )})()}

      {/* Quick note */}
      <div className="mb-4 flex gap-2 relative z-10">
        <input
          type="text"
          value={note}
          onChange={(e) => setNote(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSaveNote()}
          placeholder="Catat sesuatu hari ini... 📝"
          className="input-field flex-1 text-sm font-medium"
        />
        {note && (
          <button onClick={handleSaveNote} disabled={savingNote} className="btn-neo text-sm px-4 border-4 bg-brand-green">
            {savingNote ? '...' : 'Simpan'}
          </button>
        )}
      </div>
    </div>
  )
}
