import { useState, useEffect, useRef } from 'react'
import { useLocation } from 'react-router-dom'
import { activityService, courseService } from '@/services/backend'
import KnotLoader from '@/components/ui/KnotLoader'
import NotificationBell from '@/components/ui/NotificationBell'

export default function FocusPage() {
  const location = useLocation()
  const [isRunning, setIsRunning] = useState(false)
  const [isPaused, setIsPaused] = useState(false)
  const [duration, setDuration] = useState(25) // minutes
  const [customDuration, setCustomDuration] = useState('')
  const [elapsed, setElapsed] = useState(0) // seconds
  const [completed, setCompleted] = useState(false)
  const [taskNote, setTaskNote] = useState('')
  const [manualDesc, setManualDesc] = useState('') // manual focus description
  const [focusCourses, setFocusCourses] = useState<any[]>([])
  const [allCourses, setAllCourses] = useState<any[]>([])
  const [selectedCourse, setSelectedCourse] = useState<any>(
    (location.state as any)?.course || null
  )
  const [loadingCourses, setLoadingCourses] = useState(true)
  const [showAllCourses, setShowAllCourses] = useState(false)
  const [focusMode, setFocusMode] = useState<'free' | null>(null)
  const [toast, setToast] = useState<string | null>(null)
  const [allHistory, setAllHistory] = useState<any[]>([])
  const [historyLoading, setHistoryLoading] = useState(false)
  const [histPage, setHistPage] = useState(1)
  const HIST_PER = 5
  const [autoLogged, setAutoLogged] = useState(false)
  const intervalRef = useRef<any>(null)
  const autoLogRef = useRef(false) // prevent double auto-log

  const totalSeconds = duration * 60
  const remaining = totalSeconds - elapsed
  const minutes = Math.floor(remaining / 60)
  const seconds = remaining % 60
  const progress = elapsed / totalSeconds

  useEffect(() => {
    loadCourses()
    loadHistory()
  }, [])

  const loadCourses = async () => {
    setLoadingCourses(true)
    try {
      const [focusRes, allRes] = await Promise.allSettled([
        courseService.getTodayFocus(),
        courseService.list(),
      ])
      if (focusRes.status === 'fulfilled') setFocusCourses(focusRes.value.data?.data?.items || [])
      if (allRes.status === 'fulfilled') setAllCourses(allRes.value.data?.data?.items || [])
    } catch (err) { console.error(err) }
    setLoadingCourses(false)
  }

  const loadHistory = async () => {
    setHistoryLoading(true)
    try {
      const { data } = await activityService.list(1)
      const items = data?.data?.items || data?.data || []
      setAllHistory(items)
      setHistPage(1)
    } catch (err) { console.error(err) }
    setHistoryLoading(false)
  }

  useEffect(() => {
    if (isRunning && !isPaused && remaining > 0) {
      intervalRef.current = setInterval(() => {
        setElapsed((prev) => {
          if (prev + 1 >= totalSeconds) {
            clearInterval(intervalRef.current)
            setIsRunning(false)
            // Auto-log when timer completes naturally
            if (!autoLogRef.current) {
              autoLogRef.current = true
              handleAutoLog(totalSeconds)
            }
            return totalSeconds
          }
          return prev + 1
        })
      }, 1000)
    }
    return () => clearInterval(intervalRef.current)
  }, [isRunning, isPaused, totalSeconds])

  const start = () => {
    setElapsed(0)
    setCompleted(false)
    setAutoLogged(false)
    autoLogRef.current = false
    setIsRunning(true)
    setIsPaused(false)
  }

  const pause = () => setIsPaused(!isPaused)

  const stop = () => {
    clearInterval(intervalRef.current)
    setIsRunning(false)
    setIsPaused(false)
    if (elapsed > 60) {
      setCompleted(true) // At least 1 min — show manual log screen
    } else {
      setElapsed(0)
    }
  }

  const handleAutoLog = async (totalElapsed: number) => {
    const actualMinutes = Math.ceil(totalElapsed / 60)
    try {
      if (selectedCourse) {
        // Backend auto-classifies as activity via run_logging_classifier
        await courseService.logSession(selectedCourse.id, {
          duration_minutes: actualMinutes,
          notes: taskNote || manualDesc || `Focus session — ${actualMinutes} menit`,
        })
      } else {
        // Manual focus (no course) — log as general activity
        await activityService.log({
          raw_text: manualDesc || taskNote || `Focus session — ${actualMinutes} menit`,
          duration_minutes: actualMinutes,
        })
      }
      setAutoLogged(true)
      setCompleted(true)
      setToast(`✅ ${actualMinutes} menit tercatat otomatis!`)
      setTimeout(() => setToast(null), 4000)
      loadHistory()
    } catch (err) {
      console.error(err)
      setCompleted(true) // Show manual log as fallback
    }
  }

  const handleLog = async () => {
    const actualMinutes = Math.ceil(elapsed / 60)
    try {
      if (selectedCourse) {
        // Backend auto-classifies as activity via run_logging_classifier
        await courseService.logSession(selectedCourse.id, {
          duration_minutes: actualMinutes,
          notes: taskNote || manualDesc || `Focus session — ${actualMinutes} menit`,
        })
      } else {
        // Manual focus (no course) — log as general activity
        await activityService.log({
          raw_text: manualDesc || taskNote || `Focus session — ${actualMinutes} menit`,
          duration_minutes: actualMinutes,
        })
      }
      setCompleted(false)
      setElapsed(0)
      setTaskNote('')
      setManualDesc('')
      setSelectedCourse(null)
      setAutoLogged(false)
      autoLogRef.current = false
      setToast('✅ Aktivitas tercatat!')
      setTimeout(() => setToast(null), 3000)
      loadHistory()
    } catch (err) { console.error(err) }
  }

  const resetAll = () => {
    setCompleted(false)
    setElapsed(0)
    setTaskNote('')
    setAutoLogged(false)
    autoLogRef.current = false
    setFocusMode(null)
    setShowAllCourses(false)
  }

  const handleCustomDuration = (val: string) => {
    setCustomDuration(val)
    const num = parseInt(val)
    if (num > 0 && num <= 480) {
      setDuration(num)
    }
  }

  // ── Completed screen ──
  if (completed) {
    return (
      <div className="px-4 py-5 pb-24 flex flex-col items-center justify-center min-h-[70vh] relative">
        <div className="absolute inset-0 opacity-[0.03] pointer-events-none z-0" style={{ backgroundImage: 'radial-gradient(#09090B 1.5px, transparent 1.5px)', backgroundSize: '24px 24px' }}></div>
        {toast && <div className="fixed top-4 left-1/2 -translate-x-1/2 z-50 px-4 py-2.5 bg-brand-green text-dark rounded-xl font-display font-bold text-sm shadow-[4px_4px_0_#09090B] border-4 border-dark">{toast}</div>}
        <div className="neo-card p-8 border-4 border-dark shadow-neo-md bg-white flex flex-col items-center w-full max-w-sm relative z-10 text-center animate-[slideUp_0.3s_ease]">
          <span className="text-7xl mb-6 drop-shadow-md">🎉</span>
          <h1 className="font-display text-4xl text-dark mb-2 font-black">Sesi Selesai!</h1>
          <p className="font-body text-base font-medium text-text-secondary mb-6">
            Kamu fokus selama <span className="font-bold text-dark bg-brand-yellow px-1 rounded">{Math.ceil(elapsed / 60)} menit</span>. Hebat!
          </p>
          {selectedCourse && (
            <div className="px-4 py-2 border-2 border-dark bg-brand-blue-light/30 rounded-xl mb-6 shadow-[2px_2px_0_#09090B] transform -rotate-2">
              <p className="font-display font-bold text-sm text-brand-blue">
                📚 {selectedCourse.title}
              </p>
            </div>
          )}

          {autoLogged ? (
            <div className="w-full">
              <p className="font-display font-bold text-sm text-brand-green mb-6 bg-brand-green/10 border-2 border-brand-green px-3 py-2 rounded-lg">✅ Aktivitas sudah tercatat otomatis!</p>
              <button onClick={resetAll} className="btn-neo border-4 bg-brand-pink w-full py-3 text-lg">
                🔄 Mulai Lagi
              </button>
            </div>
          ) : (
            <div className="w-full">
              <input
                type="text"
                value={taskNote}
                onChange={(e) => setTaskNote(e.target.value)}
                placeholder="Apa yang kamu pelajari? (opsional)"
                className="input-field mb-4 w-full py-3 text-center"
              />
              <button onClick={handleLog} className="btn-neo border-4 bg-brand-green w-full mb-3 py-3 text-lg">
                📝 Log Aktivitas
              </button>
              <button onClick={resetAll} className="font-display font-bold text-sm text-text-muted hover:text-dark transition-colors">
                Lewati
              </button>
            </div>
          )}
        </div>
      </div>
    )
  }

  // ── Active session / Pre-session ──
  return (
    <div className="px-4 pb-24 flex flex-col items-center relative min-h-screen overflow-hidden">
      <div className="absolute inset-0 opacity-[0.03] pointer-events-none z-0" style={{ backgroundImage: 'radial-gradient(#09090B 1.5px, transparent 1.5px)', backgroundSize: '24px 24px' }}></div>
      {toast && <div className="fixed top-4 left-1/2 -translate-x-1/2 z-50 px-4 py-2.5 bg-brand-green text-dark rounded-xl font-display font-bold text-sm shadow-[4px_4px_0_#09090B] border-4 border-dark animate-[fadeIn_0.2s_ease]">{toast}</div>}
      
      <div className="sticky top-0 z-50 bg-bg-base/95 backdrop-blur-sm pt-5 pb-4 mb-8 w-full flex items-center justify-between border-b-2 border-dark/10 -mx-4 px-4">
        <h1 className="font-display text-4xl text-dark font-black tracking-tight drop-shadow-sm">Focus!</h1>
        <div className="flex items-center gap-3">
          <NotificationBell />
          <img src="/kaix_logo.png" alt="Logo" className="w-8 h-8 object-contain drop-shadow-sm" />
        </div>
      </div>

      {!isRunning ? (
        /* Pre-session */
        <div className="flex flex-col items-center w-full relative z-10">
          {/* Pre-selected course from navigation */}
          {selectedCourse && (
            <div className="w-full mb-6">
              <p className="font-display text-[10px] uppercase tracking-widest text-dark font-black mb-2 bg-brand-yellow inline-block px-2 py-0.5 border-2 border-dark rounded shadow-[1px_1px_0_#09090B]">Kursus Terpilih</p>
              <div className="neo-card p-4 border-4 border-dark bg-white shadow-[4px_4px_0_#09090B]">
                <div className="flex items-center gap-3">
                  <span className="w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold bg-brand-blue border-2 border-dark text-white shadow-[1px_1px_0_#09090B]">✓</span>
                  <div className="flex-1 min-w-0">
                    <p className="font-display text-base font-extrabold text-dark truncate">{selectedCourse.title}</p>
                    <div className="flex items-center gap-2 mt-1">
                      {selectedCourse.platform && <span className="font-display font-bold text-[9px] uppercase text-text-secondary border border-dark px-1.5 py-0.5 rounded bg-border-light">{selectedCourse.platform}</span>}
                      {selectedCourse.url && <a href={selectedCourse.url} target="_blank" rel="noopener noreferrer" className="font-display font-bold text-[10px] text-brand-blue underline truncate hover:text-brand-pink">🔗 Link</a>}
                    </div>
                  </div>
                  <button onClick={() => setSelectedCourse(null)} className="w-8 h-8 flex items-center justify-center border-2 border-transparent hover:border-dark hover:bg-brand-red hover:text-white rounded-lg transition-all text-text-muted font-bold">✕</button>
                </div>
              </div>
            </div>
          )}

          {/* Course selector — show 3 max + lihat lebih */}
          {!selectedCourse && (() => {
            const starred = focusCourses
            const others = allCourses.filter(c => !focusCourses.some(fc => fc.id === c.id))
            const combined = [...starred.map(c => ({ ...c, _starred: true })), ...others.map(c => ({ ...c, _starred: false }))]
            const shown = combined.slice(0, 3)
            const hasMore = combined.length > 3

            return (
              <div className="w-full mb-6">
                <p className="font-display text-lg text-dark font-extrabold mb-3">Fokus belajar apa hari ini?</p>
                <div className="flex flex-col gap-3">
                  {loadingCourses ? <KnotLoader size="md" /> : shown.map((course) => (
                    <button
                      key={course.id}
                      onClick={() => setSelectedCourse(course)}
                      className="neo-card p-4 text-left transition-all border-4 border-dark shadow-neo-sm hover:-translate-y-1 hover:shadow-neo-md bg-white group"
                    >
                      <div className="flex items-center gap-3">
                        <span className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold border-2 shadow-[1px_1px_0_#09090B] transition-colors ${course._starred ? 'bg-brand-yellow border-dark text-dark' : 'bg-border-light border-dark text-text-secondary group-hover:bg-brand-blue group-hover:text-white'}`}>
                          {course._starred ? '★' : '○'}
                        </span>
                        <div className="flex-1 min-w-0">
                          <p className="font-display text-base font-extrabold text-dark truncate">{course.title}</p>
                          {course.platform && <span className="font-display font-bold text-[9px] uppercase text-text-secondary">{course.platform}</span>}
                        </div>
                      </div>
                    </button>
                  ))}
                  {hasMore && (
                    <button
                      onClick={() => setShowAllCourses(true)}
                      className="font-display font-extrabold text-xs text-brand-blue py-3 bg-blue-light/50 border-2 border-brand-blue/30 rounded-xl mt-1 hover:bg-brand-blue hover:text-white hover:border-dark transition-all border-dashed"
                    >
                      Lihat Semua Kursus ({combined.length}) ➔
                    </button>
                  )}
                </div>

                {/* "Lihat Semua" modal */}
                {showAllCourses && (
                  <div className="fixed inset-0 z-[200] bg-dark/60 backdrop-blur-sm flex items-end justify-center" onClick={() => setShowAllCourses(false)}>
                    <div className="bg-white w-full max-w-lg rounded-t-2xl border-t-4 border-x-4 border-dark shadow-[0_-8px_0_rgba(0,0,0,0.1)] p-6 max-h-[80vh] overflow-y-auto" onClick={e => e.stopPropagation()}>
                      <div className="flex items-center justify-between mb-6 pb-2 border-b-4 border-dark">
                        <h2 className="font-display text-xl font-extrabold text-dark">Pilih Kursus</h2>
                        <button onClick={() => setShowAllCourses(false)} className="w-8 h-8 rounded-full border-2 border-dark bg-brand-red flex items-center justify-center text-white font-bold hover:scale-110 transition-transform">✕</button>
                      </div>
                      <div className="flex flex-col gap-3">
                        {combined.map((course) => (
                          <button
                            key={course.id}
                            onClick={() => { setSelectedCourse(course); setShowAllCourses(false) }}
                            className="neo-card p-4 text-left transition-all border-4 border-dark shadow-neo-sm hover:-translate-y-1 hover:shadow-neo-md bg-white group"
                          >
                            <div className="flex items-center gap-3">
                              <span className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold border-2 shadow-[1px_1px_0_#09090B] transition-colors ${course._starred ? 'bg-brand-yellow border-dark text-dark' : 'bg-border-light border-dark text-text-secondary group-hover:bg-brand-blue group-hover:text-white'}`}>
                                {course._starred ? '★' : '○'}
                              </span>
                              <div className="flex-1 min-w-0">
                                <p className="font-display text-base font-extrabold text-dark truncate">{course.title}</p>
                                {course.platform && <span className="font-display font-bold text-[9px] uppercase text-text-secondary">{course.platform}</span>}
                              </div>
                            </div>
                          </button>
                        ))}
                      </div>
                    </div>
                  </div>
                )}

                {/* Separator + Free focus option */}
                <div className="flex items-center gap-4 mt-6 mb-4">
                  <div className="flex-1 h-1 bg-dark rounded-full" />
                  <span className="font-display font-black text-xs text-dark uppercase bg-brand-yellow px-2 py-0.5 border-2 border-dark rounded shadow-[1px_1px_0_#09090B] transform -rotate-3">atau</span>
                  <div className="flex-1 h-1 bg-dark rounded-full" />
                </div>
                <button
                  onClick={() => { setSelectedCourse(null); setFocusMode('free') }}
                  className={`w-full neo-card p-4 text-left transition-all border-4 border-dark shadow-neo-sm hover:-translate-y-1 hover:shadow-neo-md ${focusMode === 'free' ? 'bg-brand-pink/20 ring-4 ring-brand-pink border-brand-pink shadow-[4px_4px_0_#FF6B6B]' : 'bg-white'}`}
                >
                  <div className="flex items-center gap-3">
                    <span className="w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold border-2 bg-brand-pink border-dark text-dark shadow-[1px_1px_0_#09090B]">✎</span>
                    <div className="flex-1">
                      <p className="font-display text-base font-extrabold text-dark">Pomodoro Timer Focus</p>
                      <p className="font-body text-xs font-semibold text-text-secondary mt-0.5">Belajar tanpa kursus tertentu</p>
                    </div>
                  </div>
                </button>
              </div>
            )
          })()}

          {/* Free focus — mandatory title */}
          {!selectedCourse && focusMode === 'free' && (
            <div className="w-full mb-6 bg-white border-4 border-dark p-4 rounded-xl shadow-neo-sm animate-[fadeIn_0.2s_ease]">
              <label className="font-display font-bold text-sm text-dark mb-2 block">Apa yang ingin kamu fokuskan? <span className="text-brand-red text-lg">*</span></label>
              <input
                type="text"
                value={manualDesc}
                onChange={(e) => setManualDesc(e.target.value)}
                placeholder="Contoh: Latihan coding..."
                className="input-field w-full py-3"
              />
              {!manualDesc.trim() && <p className="font-display font-bold text-[10px] text-brand-red bg-red-50 border border-brand-red/30 px-2 py-1 rounded inline-block mt-2">Wajib diisi untuk fokus bebas.</p>}
            </div>
          )}

          {/* Timer card — only show when a course is selected or free focus has title */}
          {(selectedCourse || (focusMode === 'free' && manualDesc.trim())) && (
            <div className="neo-card p-6 text-center w-full mb-8 border-4 border-dark shadow-neo-md bg-white">
              <span className="text-6xl mb-4 block drop-shadow-sm">⚡</span>
              <p className="font-display text-2xl font-black text-dark mb-3">Siap fokus?</p>
              <div className="inline-block px-3 py-1 border-2 border-dark bg-brand-blue-light/30 rounded-lg mb-6 shadow-[1px_1px_0_#09090B]">
                <p className="font-display font-bold text-sm text-dark">
                  {selectedCourse
                    ? `📚 ${selectedCourse.title}`
                    : `✎ ${manualDesc}`
                  }
                </p>
              </div>

              {/* Duration selector */}
              <div className="flex flex-wrap gap-3 justify-center mb-5">
                {[15, 25, 45, 60, 90].map((m) => (
                  <button
                    key={m}
                    onClick={() => { setDuration(m); setCustomDuration('') }}
                    className={`px-4 py-2 rounded-xl font-display font-black text-sm border-4 transition-all
                      ${duration === m && !customDuration
                        ? 'bg-brand-blue text-white border-dark shadow-[2px_2px_0_#09090B] -translate-y-1'
                        : 'bg-white text-dark border-dark hover:-translate-y-0.5 hover:shadow-[1px_1px_0_#09090B]'
                      }`}
                  >
                    {m} min
                  </button>
                ))}
              </div>

              {/* Custom duration input */}
              <div className="flex items-center justify-center gap-3 bg-border-light p-3 rounded-xl border-2 border-dark">
                <span className="font-display font-bold text-xs text-dark">Custom:</span>
                <input
                  type="number"
                  value={customDuration}
                  onChange={(e) => handleCustomDuration(e.target.value)}
                  placeholder="0"
                  min="1"
                  max="480"
                  className="w-20 text-center text-lg font-black py-1 px-2 border-2 border-dark rounded-lg shadow-[inset_2px_2px_0_rgba(0,0,0,0.1)] focus:outline-none focus:ring-2 focus:ring-brand-blue"
                />
                <span className="font-display font-bold text-xs text-dark">min</span>
              </div>
            </div>
          )}

          {/* Start button — only enabled when ready */}
          {(selectedCourse || (focusMode === 'free' && manualDesc.trim())) && (
            <button onClick={start} className="btn-neo border-4 bg-brand-green w-full text-xl py-4 hover:bg-green-400">
              ▶ Mulai Sesi Sekarang
            </button>
          )}

          {/* Focus History */}
          <div className="w-full mt-10">
            {(() => {
              const totalPages = Math.ceil(allHistory.length / HIST_PER)
              const pageItems = allHistory.slice((histPage-1)*HIST_PER, histPage*HIST_PER)
              return (<>
              <div className="flex items-center justify-between mb-4">
                <h3 className="font-display text-xl font-extrabold text-dark">📜 Riwayat Aktivitas</h3>
                {allHistory.length > 0 && <span className="font-display font-bold text-[10px] text-dark bg-white border-2 border-dark px-2 py-0.5 rounded-full shadow-[1px_1px_0_#09090B]">{(histPage-1)*HIST_PER+1}–{Math.min(histPage*HIST_PER, allHistory.length)} dari {allHistory.length}</span>}
              </div>
              {historyLoading ? <div className="py-6 flex justify-center"><KnotLoader size="sm" /></div> : pageItems.length > 0 ? (
                <>
                  <div className="flex flex-col gap-3">
                    {pageItems.map((h: any, i: number) => (
                      <div key={h.id || i} className="neo-card p-4 border-2 border-dark shadow-[2px_2px_0_#09090B] bg-white">
                        <div className="flex items-start justify-between">
                          <div className="flex-1 min-w-0 pr-2">
                            <p className="font-display text-sm font-bold text-dark truncate">{h.raw_text || h.activity_type || 'Focus session'}</p>
                            {h.duration_minutes && (
                              <p className="font-body text-xs font-semibold text-text-secondary mt-1">⏱ {h.duration_minutes} menit</p>
                            )}
                          </div>
                          <span className="font-display font-bold text-[9px] text-dark bg-border-light border border-dark px-1.5 py-0.5 rounded shrink-0">
                            {h.created_at ? new Date(h.created_at).toLocaleDateString('id', { day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit' }) : ''}
                          </span>
                        </div>
                        {h.matched_skills?.length > 0 && (
                          <div className="flex flex-wrap gap-2 mt-3">
                            {h.matched_skills.map((s: string) => (
                              <span key={s} className="px-2 py-1 rounded-md border-2 border-brand-blue bg-blue-light font-display font-bold text-[9px] text-brand-blue shadow-[1px_1px_0_#09090B]">{s}</span>
                            ))}
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                  {totalPages > 1 && (
                    <div className="flex items-center justify-center gap-4 mt-5">
                      <button onClick={() => setHistPage(p => Math.max(1, p-1))} disabled={histPage<=1} className="w-10 h-10 flex items-center justify-center rounded-xl font-display font-black text-dark border-2 border-dark bg-white shadow-[2px_2px_0_#09090B] disabled:opacity-40 hover:bg-brand-yellow transition-all">←</button>
                      <span className="font-display text-sm text-dark font-extrabold">Hal. {histPage}/{totalPages}</span>
                      <button onClick={() => setHistPage(p => Math.min(totalPages, p+1))} disabled={histPage>=totalPages} className="w-10 h-10 flex items-center justify-center rounded-xl font-display font-black text-dark border-2 border-dark bg-white shadow-[2px_2px_0_#09090B] disabled:opacity-40 hover:bg-brand-yellow transition-all">→</button>
                    </div>
                  )}
                </>
              ) : (
                <div className="py-6 border-4 border-dark border-dashed rounded-xl bg-white text-center">
                  <p className="font-display font-bold text-sm text-text-secondary">Belum ada riwayat aktivitas.</p>
                </div>
              )}
              </>)
            })()}
          </div>
        </div>
      ) : (
        /* Active session */
        <div className="flex flex-col items-center mt-6 relative z-10 w-full max-w-sm">
          {/* Show active course */}
          {selectedCourse && (
            <div className="px-4 py-2 border-2 border-dark bg-brand-yellow rounded-xl mb-8 shadow-[2px_2px_0_#09090B] transform -rotate-1">
              <p className="font-display font-bold text-sm text-dark">📚 {selectedCourse.title}</p>
            </div>
          )}
          {!selectedCourse && manualDesc && (
            <div className="px-4 py-2 border-2 border-dark bg-brand-pink/20 rounded-xl mb-8 shadow-[2px_2px_0_#09090B] transform -rotate-1">
              <p className="font-display font-bold text-sm text-dark">📝 {manualDesc}</p>
            </div>
          )}

          {/* Timer ring */}
          <div className="relative w-64 h-64 mb-10">
            {/* Outer neo-brutalist circle */}
            <div className="absolute inset-0 rounded-full border-8 border-dark shadow-[8px_8px_0_#09090B] bg-white"></div>
            <svg viewBox="0 0 120 120" className="w-full h-full -rotate-90 relative z-10 p-2">
              {/* Background ring */}
              <circle cx="60" cy="60" r="50" fill="none" stroke="#fbdfabff" strokeWidth="12" />
              {/* Progress ring */}
              <circle
                cx="60" cy="60" r="50" fill="none"
                stroke="var(--brand-pink)" strokeWidth="12"
                strokeLinecap="round"
                strokeDasharray={`${2 * Math.PI * 50}`}
                strokeDashoffset={`${2 * Math.PI * 50 * (1 - progress)}`}
                className="transition-all duration-1000"
              />
            </svg>
            {/* Timer text */}
            <div className="absolute inset-0 flex flex-col items-center justify-center z-20">
              <p className="font-display text-5xl text-dark font-black tracking-tighter drop-shadow-sm">
                {String(minutes).padStart(2, '0')}:{String(seconds).padStart(2, '0')}
              </p>
              {isPaused && <p className="font-display font-black text-xs text-brand-red mt-2 bg-red-50 border-2 border-brand-red px-2 py-0.5 rounded uppercase tracking-wider">Dijeda</p>}
            </div>
          </div>

          {/* Controls */}
          <div className="flex gap-4 w-full">
            <button onClick={pause} className="flex-1 py-4 rounded-xl border-4 border-dark bg-brand-yellow font-display font-black text-dark shadow-[4px_4px_0_#09090B] hover:-translate-y-1 hover:shadow-[6px_6px_0_#09090B] transition-all active:translate-y-0 active:shadow-none text-lg">
              {isPaused ? '▶ Lanjut' : '⏸ Jeda'}
            </button>
            <button onClick={stop} className="flex-1 py-4 rounded-xl border-4 border-dark bg-brand-red font-display font-black text-white shadow-[4px_4px_0_#09090B] hover:-translate-y-1 hover:shadow-[6px_6px_0_#09090B] transition-all active:translate-y-0 active:shadow-none text-lg">
              ⏹ Selesai
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
