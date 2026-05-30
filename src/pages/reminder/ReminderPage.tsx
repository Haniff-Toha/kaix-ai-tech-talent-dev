import { useEffect, useState, useRef } from 'react'
import { useSearchParams } from 'react-router-dom'
import { reminderService, courseService } from '@/services/backend'
import KnotLoader from '@/components/ui/KnotLoader'
import NotificationBell from '@/components/ui/NotificationBell'

const DAYS = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu']
const CHANNELS = ['in_app', 'email', 'telegram'] as const
const HOURS = Array.from({ length: 24 }, (_, i) => i)
const MINUTES = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55]

export default function ReminderPage() {
  const [searchParams] = useSearchParams()
  const [reminders, setReminders] = useState<any[]>([])
  const [userCourses, setUserCourses] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [editingId, setEditingId] = useState<string | null>(null)
  const [previewMsg, setPreviewMsg] = useState<string | null>(null)
  const [previewId, setPreviewId] = useState<string | null>(null)
  const [previewLoading, setPreviewLoading] = useState(false)
  const [saving, setSaving] = useState(false)

  // Form state
  const [time, setTime] = useState('08:00')
  const [days, setDays] = useState<string[]>(['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat'])
  const [channel, setChannel] = useState('in_app')
  const [label, setLabel] = useState('')
  const [linkedCourseId, setLinkedCourseId] = useState('')

  // Clock picker
  const [showClock, setShowClock] = useState(false)
  const [clockStep, setClockStep] = useState<'hour' | 'minute'>('hour')
  const clockRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    loadReminders(); loadCourses()
    const paramCourseId = searchParams.get('courseId')
    const paramCourseTitle = searchParams.get('courseTitle')
    if (paramCourseId) {
      setShowForm(true)
      setLinkedCourseId(paramCourseId)
      setLabel(paramCourseTitle ? `Belajar ${paramCourseTitle}` : '')
      setChannel('in_app')
    }
  }, [])

  // Close clock on outside click
  useEffect(() => {
    const handler = (e: MouseEvent) => {
      if (clockRef.current && !clockRef.current.contains(e.target as Node)) {
        setShowClock(false)
        setClockStep('hour')
      }
    }
    if (showClock) document.addEventListener('mousedown', handler)
    return () => document.removeEventListener('mousedown', handler)
  }, [showClock])

  const loadReminders = async () => {
    setLoading(true)
    try {
      const { data } = await reminderService.list()
      setReminders(data?.data?.items || data?.data || [])
    } catch (err) { console.error(err) }
    setLoading(false)
  }

  const loadCourses = async () => {
    try {
      const { data } = await courseService.list()
      setUserCourses(data?.data?.items || [])
    } catch { /* ignore */ }
  }

  const toggleDay = (d: string) => {
    setDays((prev) => prev.includes(d) ? prev.filter((x) => x !== d) : [...prev, d])
  }

  const handleSave = async () => {
    setSaving(true)
    try {
      const apiPayload = {
        scheduled_time: time,
        days: days,
        channel: channel,
        is_active: true,
        label: label || undefined,
        linked_course_id: linkedCourseId || undefined,
        type: linkedCourseId ? 'course' : 'daily_task',
      }
      if (editingId) {
        await reminderService.update(editingId, apiPayload)
      } else {
        await reminderService.create(apiPayload)
      }
      resetForm()
      loadReminders()
    } catch (err) { console.error(err) }
    setSaving(false)
  }

  const handleDelete = async (id: string) => {
    try {
      await reminderService.delete(id)
      loadReminders()
    } catch (err) { console.error(err) }
  }

  const handleToggleActive = async (r: any) => {
    try {
      // Optimistically update the local state for a snappy UI response
      setReminders((prev) =>
        prev.map((item) => (item.id === r.id ? { ...item, is_active: !item.is_active } : item))
      )
      // Call partial update API
      await reminderService.update(r.id, { is_active: !r.is_active })
    } catch (err) {
      console.error(err)
      // Revert to server state if the update fails
      loadReminders()
    }
  }

  const handlePreview = async (id: string) => {
    setPreviewId(id)
    setPreviewLoading(true)
    setPreviewMsg(null)
    try {
      const { data } = await reminderService.preview(id)
      setPreviewMsg(data?.data?.message || data?.message || 'Preview generated!')
    } catch (err) {
      setPreviewMsg('Gagal generate preview.')
    }
    setPreviewLoading(false)
  }

  const handleEdit = (r: any) => {
    setEditingId(r.id)
    setTime(r.scheduled_time || r.time || '08:00')
    setDays(r.days || r.days_of_week || [])
    setChannel(r.channel || 'in_app')
    setLabel(r.label || '')
    setLinkedCourseId(r.linked_course_id || '')
    setShowForm(false)
  }

  const resetForm = () => {
    setShowForm(false)
    setEditingId(null)
    setTime('08:00')
    setDays(['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat'])
    setChannel('in_app')
    setLabel('')
    setLinkedCourseId('')
    setPreviewMsg(null)
    setPreviewId(null)
    setShowClock(false)
    setClockStep('hour')
  }

  const getCourseName = (courseId: string) => {
    return userCourses.find((c) => c.id === courseId)?.title || 'Kursus'
  }

  const channelLabel = (c: string) =>
    c === 'in_app' ? '🔔 In-App' : c === 'telegram' ? '📨 Telegram' : '📧 Email'

  const [selHour, selMinute] = time.split(':').map(Number)

  const pickHour = (h: number) => {
    setTime(`${String(h).padStart(2, '0')}:${String(selMinute).padStart(2, '0')}`)
    setClockStep('minute')
  }
  const pickMinute = (m: number) => {
    setTime(`${String(selHour).padStart(2, '0')}:${String(m).padStart(2, '0')}`)
    // don't close — user taps outside to close
  }

  // Render the clock face
  const ClockPicker = () => (
    <div ref={clockRef} className="absolute z-50 bg-white rounded-2xl border-4 border-dark shadow-[8px_8px_0_#09090B] p-4 w-[280px]" style={{ left: '50%', transform: 'translateX(-50%)', top: '100%', marginTop: 8 }}>
      <div className="text-center mb-4">
        <span className="font-display text-4xl font-black text-dark tracking-tighter">
          <button onClick={() => setClockStep('hour')} className={`transition-colors ${clockStep === 'hour' ? 'text-brand-blue drop-shadow-sm' : 'text-dark'} hover:text-brand-blue`}>{String(selHour).padStart(2, '0')}</button>
          <span className="text-text-muted mx-1">:</span>
          <button onClick={() => setClockStep('minute')} className={`transition-colors ${clockStep === 'minute' ? 'text-brand-blue drop-shadow-sm' : 'text-dark'} hover:text-brand-blue`}>{String(selMinute).padStart(2, '0')}</button>
        </span>
        <p className="font-display font-bold text-xs text-text-muted mt-1 uppercase tracking-widest">{clockStep === 'hour' ? 'Pilih Jam' : 'Pilih Menit'}</p>
      </div>
      {/* Circular clock face */}
      <div className="relative w-[240px] h-[240px] mx-auto bg-border-light rounded-full border-4 border-dark shadow-[inset_2px_2px_0_rgba(0,0,0,0.1)]">
        {/* Center dot */}
        <div className="absolute left-1/2 top-1/2 w-3 h-3 rounded-full bg-brand-blue border-2 border-dark -translate-x-1/2 -translate-y-1/2 z-10" />
        {clockStep === 'hour' ? (
          HOURS.map((h) => {
            const angle = (h / 12) * 360 - 90
            const isInner = h >= 12
            const radius = isInner ? 65 : 95
            const rad = (angle * Math.PI) / 180
            const x = 120 + radius * Math.cos(rad)
            const y = 120 + radius * Math.sin(rad)
            const isSelected = h === selHour
            return (
              <button
                key={h}
                onClick={() => pickHour(h)}
                className={`absolute w-8 h-8 rounded-full flex items-center justify-center font-display font-bold text-sm transition-all -translate-x-1/2 -translate-y-1/2 ${isSelected ? 'bg-brand-blue text-white border-2 border-dark shadow-[2px_2px_0_#09090B] scale-110 z-20' : 'hover:bg-brand-yellow text-dark border-2 border-transparent hover:border-dark hover:shadow-[2px_2px_0_#09090B] z-10'}`}
                style={{ left: x, top: y }}
              >
                {h}
              </button>
            )
          })
        ) : (
          MINUTES.map((m) => {
            const angle = (m / 60) * 360 - 90
            const rad = (angle * Math.PI) / 180
            const x = 120 + 95 * Math.cos(rad)
            const y = 120 + 95 * Math.sin(rad)
            const isSelected = m === selMinute
            return (
              <button
                key={m}
                onClick={() => pickMinute(m)}
                className={`absolute w-10 h-10 rounded-full flex items-center justify-center font-display font-black text-sm transition-all -translate-x-1/2 -translate-y-1/2 ${isSelected ? 'bg-brand-blue text-white border-2 border-dark shadow-[2px_2px_0_#09090B] scale-110 z-20' : 'hover:bg-brand-yellow text-dark border-2 border-transparent hover:border-dark hover:shadow-[2px_2px_0_#09090B] z-10'}`}
                style={{ left: x, top: y }}
              >
                {String(m).padStart(2, '0')}
              </button>
            )
          })
        )}
      </div>
    </div>
  )

  // The form fields — rendered inline, NOT as a sub-component (fixes cursor bug)
  const renderFormFields = (isNew?: boolean) => (
    <div className={isNew ? 'neo-card p-5 border-4 border-dark shadow-[6px_6px_0_#09090B] bg-white animate-[slideUp_0.2s_ease]' : 'mt-4 p-4 bg-border-light border-4 border-dark border-dashed rounded-xl'}>
      {isNew && <h3 className="font-display text-xl font-black text-dark mb-4">Buat Reminder Baru</h3>}
      <div className="flex flex-col gap-4">
        {/* Label */}
        <div>
          <label className="font-display font-bold text-sm text-dark mb-1.5 block">📝 Deskripsi (opsional)</label>
          <input
            type="text"
            value={label}
            onChange={(e) => setLabel(e.target.value)}
            placeholder="Contoh: Review materi Python"
            className="input-field w-full py-2.5 text-base"
          />
        </div>

        {/* Linked course */}
        {userCourses.length > 0 && (
          <div>
            <label className="font-display font-bold text-sm text-dark mb-1.5 block">📚 Kursus terkait</label>
            <select
              value={linkedCourseId}
              onChange={(e) => setLinkedCourseId(e.target.value)}
              className="input-field w-full py-2.5 text-base bg-white"
            >
              <option value="">-- Tidak terkait kursus --</option>
              {userCourses.map((c) => (
                <option key={c.id} value={c.id}>📚 {c.title}</option>
              ))}
            </select>
          </div>
        )}

        {/* Time with clock picker */}
        <div>
          <label className="font-display font-bold text-sm text-dark mb-1.5 block">🕐 Waktu</label>
          <div className="relative inline-block w-full sm:w-auto">
            <button
              onClick={() => { setShowClock(!showClock); setClockStep('hour') }}
              className="flex items-center justify-between w-full sm:w-auto gap-4 px-5 py-3 rounded-xl border-4 border-dark bg-brand-yellow hover:-translate-y-1 hover:shadow-[4px_4px_0_#09090B] transition-all"
            >
              <span className="font-display font-black text-2xl text-dark tracking-tighter">{time}</span>
              <span className="font-display font-bold text-sm text-dark border-2 border-dark rounded-full w-6 h-6 flex items-center justify-center bg-white">▼</span>
            </button>
            {showClock && <ClockPicker />}
          </div>
        </div>

        {/* Days */}
        <div>
          <label className="font-display font-bold text-sm text-dark mb-1.5 block">📅 Hari</label>
          <div className="flex flex-wrap gap-2">
            {DAYS.map((d) => (
              <button
                key={d}
                onClick={() => toggleDay(d)}
                className={`px-3 py-1.5 rounded-lg font-display font-bold text-xs border-2 transition-all
                  ${days.includes(d) ? 'bg-brand-blue text-white border-dark shadow-[2px_2px_0_#09090B]' : 'bg-white border-dark text-text-secondary hover:bg-border-light'}`}
              >
                {d.slice(0, 3)}
              </button>
            ))}
          </div>
        </div>

        {/* Channel */}
        <div>
          <label className="font-display font-bold text-sm text-dark mb-1.5 block">📡 Channel</label>
          <div className="flex flex-wrap gap-2">
            {CHANNELS.map((c) => (
              <button
                key={c}
                onClick={() => setChannel(c)}
                className={`px-4 py-2 rounded-xl font-display font-bold text-sm border-2 transition-all
                  ${channel === c ? 'bg-brand-pink text-dark border-dark shadow-[2px_2px_0_#09090B]' : 'bg-white border-dark text-text-secondary hover:bg-border-light'}`}
              >
                {channelLabel(c)}
              </button>
            ))}
          </div>
        </div>

        <div className="flex gap-3 mt-2">
          <button onClick={resetForm} className="flex-1 py-3 font-display font-bold text-dark border-4 border-dark rounded-xl bg-white hover:bg-border-light transition-colors">Batal</button>
          <button onClick={handleSave} disabled={saving} className="flex-1 py-3 font-display font-black text-white border-4 border-dark rounded-xl bg-brand-green hover:-translate-y-1 hover:shadow-[4px_4px_0_#09090B] transition-all disabled:opacity-50 disabled:transform-none disabled:shadow-none">
            {saving ? '⏳ Menyimpan...' : '💾 Simpan'}
          </button>
        </div>
      </div>
    </div>
  )

  return (
    <div className="px-4 pb-24 min-h-screen relative">
      <div className="absolute inset-0 opacity-[0.03] pointer-events-none z-0" style={{ backgroundImage: 'radial-gradient(#09090B 1.5px, transparent 1.5px)', backgroundSize: '24px 24px' }}></div>
      <div className="sticky top-0 z-50 bg-bg-base/95 backdrop-blur-sm pt-5 pb-4 mb-4 flex items-center justify-between border-b-2 border-dark/10 -mx-4 px-4">
        <h1 className="font-display text-4xl text-dark font-black tracking-tight drop-shadow-sm">Reminder</h1>
        <div className="flex items-center gap-3">
          <NotificationBell />
          <img src="/kaix_logo.png" alt="Logo" className="w-8 h-8 object-contain drop-shadow-sm" />
        </div>
      </div>

      {loading ? (
        <div className="flex justify-center py-12 relative z-10"><KnotLoader size="md" /></div>
      ) : (
        <div className="relative z-10">
          {/* New reminder form at the top */}
          <div className="mb-8">
            {showForm ? (
              renderFormFields(true)
            ) : !editingId && (
              <button onClick={() => { resetForm(); setShowForm(true) }} className="btn-neo border-4 bg-brand-pink w-full py-4 text-xl">
                + Buat Reminder Baru
              </button>
            )}
          </div>

          {/* Reminder list */}
          {reminders.length > 0 ? (
            <div className="flex flex-col gap-5 mb-8">
              {reminders.map((r) => {
                const isEditing = editingId === r.id

                if (isEditing) {
                  return (
                    <div key={r.id} className="neo-card p-5 border-4 border-brand-blue bg-blue-light/20 shadow-[6px_6px_0_var(--brand-blue)]">
                      <div className="flex items-center justify-between mb-3">
                        <h3 className="font-display text-lg text-brand-blue font-black">✏️ Edit Reminder</h3>
                      </div>
                      {renderFormFields()}
                    </div>
                  )
                }

                return (
                  <div key={r.id} className="neo-card p-5 border-4 border-dark shadow-[4px_4px_0_#09090B] bg-white group hover:-translate-y-1 hover:shadow-[6px_6px_0_#09090B] transition-all">
                    <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-3">
                      <div className="flex items-center gap-4">
                        <span className="font-display text-4xl font-black text-dark tracking-tighter drop-shadow-sm">{r.scheduled_time || r.time || '08:00'}</span>
                        <span className={`px-2.5 py-1 rounded-lg border-2 border-dark font-display font-bold text-[10px] uppercase shadow-[1px_1px_0_#09090B]
                          ${r.channel === 'in_app' ? 'bg-brand-blue-light text-brand-blue' : r.channel === 'telegram' ? 'bg-[#E3F0FF] text-[#229ED9]' : 'bg-brand-pink text-dark'}
                        `}>
                          {channelLabel(r.channel)}
                        </span>
                      </div>
                      <div
                        onClick={() => handleToggleActive(r)}
                        className={`relative w-14 h-8 rounded-full cursor-pointer transition-colors border-2 border-dark shadow-[inset_1px_1px_0_rgba(0,0,0,0.1)] shrink-0
                          ${r.is_active ? 'bg-brand-green' : 'bg-border-light'}`}
                      >
                        <div className={`absolute top-0.5 left-0.5 w-6 h-6 rounded-full bg-white border-2 border-dark shadow-[1px_1px_0_#09090B] transition-transform
                          ${r.is_active ? 'translate-x-6' : 'translate-x-0'}`} />
                      </div>
                    </div>

                    {(r.label || r.linked_course_id) && (
                      <div className="mb-3">
                        {r.label && <p className="font-display font-bold text-base text-dark mb-1">{r.label}</p>}
                        {r.linked_course_id && (
                          <div className="inline-flex items-center gap-1.5 mt-1 px-2 py-0.5 bg-brand-yellow/30 border-2 border-brand-yellow rounded-md">
                            <span className="text-xs">📚</span>
                            <span className="font-display font-extrabold text-[11px] text-dark truncate max-w-[200px]">{getCourseName(r.linked_course_id)}</span>
                          </div>
                        )}
                      </div>
                    )}

                    <div className="flex flex-wrap gap-1.5 mb-4">
                      {(r.days || r.days_of_week || []).map((d: string) => (
                        <span key={d} className="px-2 py-0.5 rounded-md bg-border-light border border-dark font-display font-bold text-[10px] text-dark shadow-[1px_1px_0_#09090B]">{d}</span>
                      ))}
                    </div>

                    <div className="flex items-center gap-3 pt-3 border-t-2 border-dark border-dashed mt-auto">
                      <button onClick={() => handleEdit(r)} className="font-display font-extrabold text-xs text-brand-blue hover:text-dark hover:bg-blue-light px-2 py-1 rounded transition-colors flex-1 text-center border-2 border-transparent hover:border-dark">✏️ Edit</button>
                      <button onClick={() => handleDelete(r.id)} className="font-display font-extrabold text-xs text-brand-red hover:text-white hover:bg-brand-red px-2 py-1 rounded transition-colors flex-1 text-center border-2 border-transparent hover:border-dark">🗑 Hapus</button>
                    </div>
                  </div>
                )
              })}
            </div>
          ) : (
            <div className="neo-card p-8 text-center mb-8 border-4 border-dark border-dashed bg-white/80 shadow-[4px_4px_0_#09090B]">
              <span className="text-6xl mb-4 block drop-shadow-md">🔔</span>
              <p className="font-display text-2xl font-black text-dark mb-2">Belum ada reminder</p>
              <p className="font-body text-base font-medium text-text-secondary">Atur pengingat agar tetap konsisten belajar.</p>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
