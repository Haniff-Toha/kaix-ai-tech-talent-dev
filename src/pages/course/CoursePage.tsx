import { useEffect, useState, Fragment } from 'react'
import { useNavigate } from 'react-router-dom'
import { courseService, recommendationService, roadmapService } from '@/services/backend'
import KnotLoader from '@/components/ui/KnotLoader'
import NotificationBell from '@/components/ui/NotificationBell'

const PLAT_C: Record<string, string> = { dicoding: 'bg-brand-blue text-white', youtube: 'bg-brand-red text-white', book: 'bg-brand-green text-dark', udemy: 'bg-brand-pink text-dark', default: 'bg-cream text-dark border-2 border-dark' }
const PBadge = ({ p }: { p?: string | null }) => <span className={`px-2 py-0.5 rounded-md font-display text-[10px] uppercase tracking-wider font-bold border-2 border-dark shadow-[1px_1px_0_#09090B] ${PLAT_C[p?.toLowerCase() || 'default'] || PLAT_C.default}`}>{p || 'Other'}</span>

function Heatmap({ days }: { days: { date: string; minutes: number }[] }) {
  const [sel, setSel] = useState<{ date: string; minutes: number } | null>(null)
  const m = new Map(days.map(d => [d.date, d.minutes]))
  const colors = ['bg-border-default/30', 'bg-[#A7F3D0]', 'bg-brand-green', 'bg-[#059669]', 'bg-dark']
  const dayLabels = ['Sen', 'Sel', 'Rab', 'Kam', 'Jum', 'Sab', 'Min']
  const fmt = (iso: string) => { const d = new Date(iso); return `${['Min', 'Sen', 'Sel', 'Rab', 'Kam', 'Jum', 'Sab'][d.getDay()]}, ${d.getDate()}/${d.getMonth() + 1}/${d.getFullYear()}` }

  // Build 13 weeks of data, ending at today
  const today = new Date()
  // Find the Monday 12 weeks ago (13 weeks total)
  const startDay = new Date(today)
  startDay.setDate(startDay.getDate() - ((startDay.getDay() + 6) % 7) - (12 * 7)) // Go to Monday, 12 weeks back

  // Build grid: 7 rows (Mon=0..Sun=6) × N columns (weeks)
  const weeks: { date: string; level: number; minutes: number; future: boolean }[][] = []
  const d = new Date(startDay)
  while (d <= today || weeks.length === 0) {
    const week: typeof weeks[0] = []
    for (let day = 0; day < 7; day++) {
      const k = d.toISOString().split('T')[0]
      const mins = m.get(k) || 0
      const future = d > today
      week.push({ date: k, level: future ? -1 : mins === 0 ? 0 : mins < 30 ? 1 : mins < 60 ? 2 : mins < 120 ? 3 : 4, minutes: mins, future })
      d.setDate(d.getDate() + 1)
    }
    weeks.push(week)
  }
  const numWeeks = weeks.length

  return (<div className="neo-card p-4 border-4 border-dark shadow-neo-sm bg-white">
    <div className="flex items-center justify-between mb-3"><h3 className="font-display text-sm font-extrabold text-dark uppercase tracking-wider">Aktivitas Terakhir</h3><span className="font-display font-bold text-[10px] text-dark bg-brand-yellow px-2 py-0.5 rounded-md border-2 border-dark shadow-[1px_1px_0_#09090B]">3 Bulan</span></div>
    <div className="flex flex-col overflow-x-auto no-scrollbar pb-2">
      <div className="grid gap-1.5" style={{ gridTemplateColumns: `repeat(${numWeeks + 1}, minmax(14px, 1fr))`, gridTemplateRows: 'repeat(7, 14px)' }}>
        {/* Render row by row */}
        {Array.from({ length: 7 }).map((_, dayIdx) => (
          <Fragment key={dayIdx}>
            {/* Column 0: Day Label */}
            <div className="flex items-center">
              <span className="font-display font-black text-[9px] text-text-secondary leading-none w-6 shrink-0">
                {dayIdx % 2 === 0 ? dayLabels[dayIdx] : ''}
              </span>
            </div>
            {/* Columns 1-N: Week boxes for this day */}
            {weeks.map((week, weekIdx) => {
              const cell = week[dayIdx]
              if (!cell || cell.future) return <div key={`${weekIdx}-${dayIdx}`} className="w-full h-full rounded-[1px] border border-transparent opacity-20 bg-dark/5" />
              return (
                <div 
                  key={`${weekIdx}-${dayIdx}`} 
                  onClick={() => setSel(sel?.date === cell.date ? null : cell)} 
                  className={`w-full h-full rounded-[1px] border border-dark cursor-pointer hover:scale-110 hover:z-10 relative transition-all ${colors[cell.level]} ${sel?.date === cell.date ? 'ring-2 ring-brand-blue ring-offset-1 z-10 scale-110 shadow-[2px_2px_0_#09090B]' : ''}`} 
                />
              )
            })}
          </Fragment>
        ))}
      </div>
    </div>
    {sel && (
      <div className="mt-4 p-4 bg-brand-blue/5 border-4 border-dark rounded-xl shadow-[4px_4px_0_#09090B] animate-[fadeIn_0.2s_ease]">
        <div className="flex items-center justify-between">
          <div className="flex flex-col">
            <span className="font-display text-xs font-black text-brand-blue uppercase">{fmt(sel.date).split(',')[0]}</span>
            <span className="font-display text-lg font-black text-dark">{fmt(sel.date).split(',')[1]}</span>
          </div>
          <div className="bg-white border-2 border-dark px-3 py-1 rounded-lg shadow-[2px_2px_0_#09090B]">
            <p className="font-display font-black text-sm text-dark">{sel.minutes > 0 ? `${sel.minutes}m` : '0m'}</p>
          </div>
        </div>
        <p className="font-body text-xs font-medium text-text-secondary mt-2 border-l-4 border-dark pl-3">{sel.minutes > 0 ? `Total waktu belajar pada hari ini.` : 'Tidak ada aktivitas tercatat.'}</p>
      </div>
    )}
    <div className="flex items-center justify-end gap-1.5 mt-3"><span className="font-display font-bold text-[9px] text-text-muted">Sedikit</span>{colors.map((c, i) => (<div key={i} className={`w-2.5 h-2.5 rounded-[1px] border border-dark ${c}`} />))}<span className="font-display font-bold text-[9px] text-text-muted">Banyak</span></div>
  </div>)
}

function SkillMastery({ mp, rm }: { mp: any[]; rm: any }) {
  const [showModal, setShowModal] = useState(false)
  const allSkills = mp.length > 0 ? mp.map(x => ({ name: x.milestone_title || x.milestone_id, pct: x.pct || 0, hours: `${(x.completed_hours || 0).toFixed(1)}/${(x.total_hours || 30).toFixed(0)}h` })) : (rm?.roadmap_json?.phases?.[0]?.milestones || []).map((m: any) => ({ name: m.title, pct: 0, hours: '0/30h' }))
  if (!allSkills.length) return null
  const shown = allSkills.slice(0, 3)
  const bc = ['#2563EB', '#EC4899', '#FBBF24', '#10B981', '#09090B']
  const SkillBar = ({ s, i }: { s: any, i: number }) => (<div className="mb-4"><div className="flex items-center justify-between mb-1.5"><span className="font-body text-sm font-bold text-dark truncate flex-1 mr-2">{s.name}</span><span className="font-display text-xs text-dark font-black">{s.pct}%</span></div><div className="h-4 border-4 border-dark bg-white rounded-full overflow-hidden shadow-[1px_1px_0_#09090B]"><div className="h-full border-r-4 border-dark transition-all duration-500 shadow-inner" style={{ width: `${s.pct}%`, background: bc[i % bc.length] }} /></div><p className="font-display text-[11px] text-text-secondary mt-1.5 font-black uppercase tracking-wider">{s.hours}</p></div>)
  return (<>
    <div className="neo-card p-4 border-4 border-dark shadow-neo-sm bg-[#F2EAC6]"><h3 className="font-display text-sm font-extrabold text-dark uppercase tracking-wider mb-4">Penguasaan Skill</h3><div className="flex flex-col">{shown.map((s: any, i: number) => (<SkillBar key={i} i={i} s={s} />))}</div>{allSkills.length > 3 && <button onClick={() => setShowModal(true)} className="w-full mt-2 font-display font-bold text-[11px] text-dark bg-white border-2 border-dark shadow-[2px_2px_0_#09090B] py-1.5 rounded-lg hover:translate-y-[1px] hover:shadow-[1px_1px_0_#09090B] transition-all">Lihat Semua ({allSkills.length})</button>}</div>
    {showModal && <div className="fixed inset-0 z-[5000] bg-dark/60 backdrop-blur-sm flex items-end justify-center" onClick={() => setShowModal(false)}><div className="bg-white w-full max-w-lg rounded-t-2xl border-t-4 border-x-4 border-dark shadow-[0_-8px_0_rgba(0,0,0,0.1)] p-6 pb-12 max-h-[85vh] overflow-y-auto" onClick={e => e.stopPropagation()}>
      <div className="flex items-center justify-between mb-6 pb-2 border-b-4 border-dark"><h2 className="font-display text-xl font-extrabold text-dark">Penguasaan Skill</h2><button onClick={() => setShowModal(false)} className="w-8 h-8 rounded-full border-2 border-dark bg-brand-red flex items-center justify-center text-white font-bold hover:scale-110 transition-transform">✕</button></div>
      <div className="flex flex-col gap-4">{allSkills.map((s: any, i: number) => (<SkillBar key={i} i={i} s={s} />))}</div>
      <div className="h-20" /> {/* Extra spacer for bottom navigation clearance */}
    </div></div>}
  </>)
}

function PlatDist({ platforms }: { platforms: { name: string; count: number; pct: number }[] }) {
  const bc = ['#2563EB', '#EC4899', '#FBBF24', '#10B981', '#09090B']
  if (!platforms.length) return null
  return (<div className="neo-card p-4 border-4 border-dark shadow-neo-sm bg-[#F8D3AF]"><h3 className="font-display text-sm font-extrabold text-dark uppercase tracking-wider mb-3">Sumber Belajar</h3><div className="h-5 border-4 border-dark rounded-full overflow-hidden flex mb-4 shadow-[1px_1px_0_#09090B]">{platforms.map((p, i) => (<div key={p.name} className="h-full border-r-2 border-dark/30 last:border-0" style={{ width: `${p.pct}%`, background: bc[i % bc.length] }} />))}</div><div className="flex flex-col gap-2">{platforms.map((p, i) => (<div key={p.name} className="flex items-center gap-2 bg-white border-2 border-dark px-2 py-1.5 rounded-md shadow-[1px_1px_0_#09090B]"><div className="w-3 h-3 rounded-[2px] border border-dark" style={{ background: bc[i % bc.length] }} /><span className="font-display font-bold text-[11px] text-dark flex-1">{p.name}</span><span className="font-display font-black text-[11px] text-dark">{p.pct}%</span></div>))}</div></div>)
}

export default function CoursePage() {
  const nav = useNavigate()
  const [tab, setTab] = useState<'my' | 'reco'>('my')
  const [courses, setCourses] = useState<any[]>([])
  const [recoPhases, setRecoPhases] = useState<any[]>([]) // from by-roadmap endpoint
  const [roadmap, setRoadmap] = useState<any>(null)
  const [stats, setStats] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const [showAdd, setShowAdd] = useState(false)
  const [sesForm, setSesForm] = useState<string | null>(null)
  const [recoPhaseFilter, setRecoPhaseFilter] = useState<number | null>(null)
  const [nT, sNT] = useState(''), [nP, sNP] = useState(''), [nU, sNU] = useState(''), [nH, sNH] = useState(''), [nM, sNM] = useState('')
  const [sMin, sSMin] = useState(''), [sNotes, sSNotes] = useState('')
  const [addingRecoId, setAddingRecoId] = useState<string | null>(null)
  const [toast, setToast] = useState<string | null>(null)
  const [loggingSesId, setLoggingSesId] = useState<string | null>(null)
  const [togglingId, setTogglingId] = useState<string | null>(null)
  const [deletingId, setDeletingId] = useState<string | null>(null)

  useEffect(() => { load() }, [tab, recoPhaseFilter])

  const load = async () => {
    setLoading(true)
    try {
      const rr = await roadmapService.get().catch(() => null)
      if (rr?.data?.data) setRoadmap(rr.data.data)
      if (tab === 'my') {
        const [c, s] = await Promise.allSettled([courseService.list(), courseService.getStats()])
        if (c.status === 'fulfilled') setCourses(c.value.data?.data?.items || [])
        if (s.status === 'fulfilled') setStats(s.value.data?.data || null)
      } else {
        // Use the new by-roadmap endpoint
        const { data } = await recommendationService.getByRoadmap(recoPhaseFilter ?? undefined)
        setRecoPhases(data?.data?.phases || [])
      }
    } catch (e) { console.error(e) }
    setLoading(false)
  }

  const addCourse = async () => { if (!nT) return; try { await courseService.create({ title: nT, platform: nP || undefined, url: nU || undefined, estimated_hours: nH ? Number(nH) : undefined, linked_milestone_id: nM || undefined }); setShowAdd(false); sNT(''); sNP(''); sNU(''); sNH(''); sNM(''); load() } catch (e) { console.error(e) } }
  const logSes = async (id: string) => { if (!sMin) return; setLoggingSesId(id); try { const res = await courseService.logSession(id, { duration_minutes: Number(sMin), notes: sNotes || undefined }); const updatedCourse = res?.data?.data?.course; if (updatedCourse) { setCourses(prev => prev.map(c => c.id === id ? { ...c, ...updatedCourse } : c)) } setSesForm(null); sSMin(''); sSNotes(''); setToast('✅ Sesi belajar tercatat!'); setTimeout(() => setToast(null), 3000) } catch (e) { console.error(e); setToast('❌ Gagal mencatat sesi'); setTimeout(() => setToast(null), 3000) } finally { setLoggingSesId(null) } }
  const toggleFocus = async (id: string) => { setTogglingId(id); try { await courseService.toggleFocus(id); setCourses(prev => prev.map(c => c.id === id ? { ...c, is_today_focus: !c.is_today_focus } : c)); setToast('✅ Fokus diperbarui!') } catch (e) { console.error(e); setToast('❌ Gagal memperbarui fokus') } finally { setTogglingId(null); setTimeout(() => setToast(null), 2500) } }
  const delCourse = async (id: string) => { setDeletingId(id); try { await courseService.delete(id); setCourses(prev => prev.filter(c => c.id !== id)); setToast('✅ Kursus dihapus!') } catch (e) { console.error(e); setToast('❌ Gagal menghapus kursus') } finally { setDeletingId(null); setTimeout(() => setToast(null), 2500) } }
  const addReco = async (r: any, msId?: string) => { setAddingRecoId(r.id); try { await courseService.create({ title: r.title, platform: r.source, url: r.url || undefined, linked_milestone_id: msId || undefined }); setToast('✅ Kursus berhasil ditambahkan!'); setTimeout(() => setToast(null), 3000) } catch (e) { console.error(e); setToast('❌ Gagal menambahkan kursus') } finally { setAddingRecoId(null) } }
  const phases = () => roadmap?.roadmap_json?.phases || []
  const allMs = () => { const ms: { id: string; title: string; phase: string; phaseNum: number }[] = []; for (const p of phases()) for (const m of p.milestones || []) ms.push({ id: m.milestone_id, title: m.title, phase: `Fase ${p.phase_number}: ${p.phase_title}`, phaseNum: p.phase_number }); return ms }

  const groupByPhase = () => {
    const ph = phases(), groups: any[] = [], used = new Set<string>()
    for (const p of ph) {
      const msIds = new Set((p.milestones || []).map((m: any) => m.milestone_id))
      const pc = courses.filter(c => c.linked_milestone_id && msIds.has(c.linked_milestone_id))
      if (pc.length > 0) { groups.push({ phaseNum: p.phase_number, title: `Fase ${p.phase_number}: ${p.phase_title}`, courses: pc }); pc.forEach(c => used.add(c.id)) }
    }
    const ug = courses.filter(c => !used.has(c.id))
    if (ug.length > 0) groups.push({ phaseNum: 0, title: 'Lainnya', courses: ug })
    return groups
  }

  return (
    <div className="relative min-h-screen pt-[84px]">
      {/* Truly Full-width Fixed Header */}
      <div className="fixed top-0 left-0 right-0 z-40 bg-bg-base/80 backdrop-blur-xl border-b-2 border-dark/10">
        <div className="max-w-lg mx-auto px-4 pt-5 pb-4 flex items-center justify-between">
          <h1 className="font-display text-4xl text-dark font-black tracking-tight">Roadmap & Courses</h1>
          <div className="flex items-center gap-3">
            <NotificationBell />
            <img src="/kaix_logo.png" alt="Logo" className="w-8 h-8 object-contain drop-shadow-sm" />
          </div>
        </div>
      </div>

      <div className="px-4 pb-24 relative">
        <div className="absolute inset-0 opacity-[0.03] pointer-events-none z-0" style={{ backgroundImage: 'radial-gradient(#09090B 1.5px, transparent 1.5px)', backgroundSize: '24px 24px' }}></div>
        {toast && <div className="fixed top-4 left-1/2 -translate-x-1/2 z-50 px-4 py-2.5 bg-brand-green text-dark font-display font-bold text-sm shadow-[4px_4px_0_#09090B] border-4 border-dark animate-[fadeIn_0.2s_ease]">{toast}</div>}

        <div className="flex gap-2 mb-6 relative z-10">
          <button onClick={() => setTab('my')} className={`flex-1 py-3 rounded-xl border-4 font-display font-black text-sm transition-all ${tab === 'my' ? 'bg-brand-yellow text-dark border-dark shadow-[2px_2px_0_#09090B] translate-y-[-2px]' : 'bg-white text-text-muted border-border-strong hover:border-dark hover:text-dark'}`}>📋 Kursus Saya</button>
          <button onClick={() => setTab('reco')} className={`flex-1 py-3 rounded-xl border-4 font-display font-black text-sm transition-all ${tab === 'reco' ? 'bg-brand-pink text-dark border-dark shadow-[2px_2px_0_#09090B] translate-y-[-2px]' : 'bg-white text-text-muted border-border-strong hover:border-dark hover:text-dark'}`}>💡 Rekomendasi</button>
        </div>

        {loading ? (
          <div className="flex flex-col justify-center items-center py-20 relative z-10">
            <KnotLoader size="md" />
            <p className="mt-4 font-display font-bold text-dark text-lg">Memuat Data...</p>
          </div>
        ) : tab === 'my' ? (
          <div className="relative z-10">
            {stats && (
              <div className="flex flex-col gap-4 mb-8">
                <Heatmap days={stats.activity_days || []} />
                <div className="grid grid-cols-2 gap-4">
                  <SkillMastery mp={stats.milestone_progress || []} rm={roadmap} />
                  <PlatDist platforms={stats.platforms || []} />
                </div>
              </div>
            )}

        {courses.length > 0 ? (<div>
          <div className="flex flex-col gap-1 mb-6">
            <h2 className="font-display text-2xl text-dark font-black flex items-center gap-2"><span className="text-3xl">🗺️</span> Roadmap Saya</h2>
            <button onClick={() => setTab('reco')} className="flex items-center gap-1.5 text-brand-blue font-display font-black text-xs hover:text-brand-pink transition-colors w-fit group">
              lihat roadmap rekomendasi <span className="group-hover:translate-x-1 transition-transform">➔</span>
            </button>
          </div>
          {groupByPhase().map((g: any) => (<div key={g.phaseNum} className="mb-8">
            {/* Phase header */}
            <div className="flex items-center gap-3 mb-4 bg-brand-blue border-4 border-dark shadow-[4px_4px_0_#09090B] p-3 rounded-xl">
              <div className="w-10 h-10 rounded-full bg-brand-yellow border-2 border-dark flex items-center justify-center shadow-[1px_1px_0_#09090B]"><span className="font-display text-lg text-dark font-black">{g.phaseNum || '•'}</span></div>
              <h3 className="font-display text-lg text-white font-black">{g.title}</h3>
            </div>
            {/* Timeline */}
            <div className="ml-5 border-l-4 border-dark border-dashed pl-6 flex flex-col gap-6 py-2">
              {g.courses.map((c: any, ci: number) => {
                return (<div key={c.id} className="relative">
                  {/* Checkpoint dot */}
                  <div className={`absolute -left-[45px] top-4 w-6 h-6 rounded-full border-4 flex items-center justify-center font-bold text-[10px] shadow-[2px_2px_0_#09090B] ${c.status === 'completed' ? 'bg-brand-green border-dark text-dark' : c.status === 'in_progress' ? 'bg-brand-blue border-dark text-white' : 'bg-white border-dark text-dark'}`}>
                    {c.status === 'completed' ? '✓' : c.status === 'in_progress' ? '→' : ''}
                  </div>
                  {/* Card */}
                  <div className="neo-card p-4 border-4 border-dark shadow-neo-sm bg-white hover:-translate-y-1 hover:shadow-neo-md transition-all">
                    <div className="flex items-start justify-between mb-2">
                      <div className="flex-1 mr-3">
                        <div className="flex items-center gap-2 mb-2 flex-wrap">
                          <PBadge p={c.platform} />
                          <span className={`px-2 py-0.5 rounded-md font-display font-bold text-[10px] uppercase border-2 border-dark shadow-[1px_1px_0_#09090B] ${c.status === 'completed' ? 'bg-brand-green text-dark' : c.status === 'in_progress' ? 'bg-brand-yellow text-dark' : 'bg-border-light text-text-secondary'}`}>{c.status?.replace('_', ' ')}</span>
                        </div>
                        <p className="font-display text-base text-dark font-extrabold leading-snug">{c.title}</p>
                      </div>
                      <div className="flex items-center gap-2 mt-1">
                        <button onClick={() => toggleFocus(c.id)} disabled={togglingId === c.id} className={`w-9 h-9 rounded-xl flex items-center justify-center text-lg font-bold transition-all border-2 shadow-[1px_1px_0_#09090B] ${c.is_today_focus ? 'bg-brand-yellow border-dark text-dark' : 'bg-white border-dark text-text-secondary hover:bg-brand-yellow/30'} ${togglingId === c.id ? 'opacity-50' : ''}`}>{togglingId === c.id ? '⏳' : c.is_today_focus ? '★' : '☆'}</button>
                        {c.status === 'not_started' && <button onClick={() => delCourse(c.id)} disabled={deletingId === c.id} className={`w-9 h-9 rounded-xl flex items-center justify-center text-sm font-bold bg-brand-red border-2 border-dark shadow-[1px_1px_0_#09090B] text-white hover:bg-red-600 transition-all ${deletingId === c.id ? 'opacity-50' : ''}`} title="Hapus kursus">{deletingId === c.id ? '⏳' : '✕'}</button>}
                      </div>
                    </div>
                    {c.url && <a href={c.url} target="_blank" rel="noopener noreferrer" className="font-body text-xs font-bold text-brand-blue underline truncate block mb-3 hover:text-brand-pink transition-colors">🔗 {c.url.replace(/https?:\/\//, '').substring(0, 40)}...</a>}
                    {c.estimated_hours && <div className="mb-3"><div className="h-2.5 border-2 border-dark bg-border-light rounded-full overflow-hidden"><div className="h-full bg-brand-blue border-r-2 border-dark transition-all" style={{ width: `${Math.min((c.completed_hours / c.estimated_hours) * 100, 100)}%` }} /></div><p className="font-display text-[10px] font-black uppercase tracking-wider text-dark mt-1 text-right">{c.completed_hours?.toFixed(1)} / {c.estimated_hours} JAM</p></div>}
                    <div className="flex items-center gap-2 mt-2 flex-wrap">
                      <button onClick={() => nav('/focus', { state: { course: c } })} className="btn-neo border-4 px-3 py-1.5 text-xs bg-dark text-white border-dark">▶ Fokus</button>
                      <button onClick={() => setSesForm(sesForm === c.id ? null : c.id)} className="font-display font-bold text-xs px-3 py-1.5 border-2 border-dark rounded-xl bg-brand-green/20 hover:bg-brand-green shadow-[1px_1px_0_#09090B] transition-all">+ Sesi</button>
                      <button onClick={() => nav(`/reminder?courseId=${c.id}&courseTitle=${encodeURIComponent(c.title)}`)} className="font-display font-bold text-xs px-3 py-1.5 border-2 border-dark rounded-xl bg-brand-pink/20 hover:bg-brand-pink shadow-[1px_1px_0_#09090B] transition-all">🔔 Reminder</button>
                    </div>
                    {sesForm === c.id && <div className="mt-4 p-4 border-4 border-dark bg-brand-yellow/20 rounded-xl shadow-[2px_2px_0_#09090B] flex flex-col gap-3">
                      <label className="font-display font-extrabold text-sm text-dark">Log Aktivitas Baru</label>
                      <input type="number" placeholder="Durasi (menit)" value={sMin} onChange={e => sSMin(e.target.value)} className="input-field py-2 text-sm" />
                      <input type="text" placeholder="Catatan (opsional)" value={sNotes} onChange={e => sSNotes(e.target.value)} className="input-field py-2 text-sm" />
                      <button onClick={() => logSes(c.id)} disabled={loggingSesId === c.id} className="btn-neo border-4 bg-brand-blue py-2 mt-1">{loggingSesId === c.id ? '⏳ Menyimpan...' : 'Simpan'}</button>
                    </div>}
                  </div>
                </div>)
              })}
            </div>
          </div>))}
        </div>) : (
          <div className="neo-card p-8 border-4 border-dark shadow-neo-sm bg-white text-center"><span className="text-6xl mb-4 block">📚</span><p className="font-display text-2xl font-black text-dark mb-2">Belum ada kursus</p><p className="font-body text-base font-medium text-text-secondary">Tambah dari rekomendasi atau manual.</p></div>
        )}

        {showAdd ? (<div className="neo-card p-5 mt-6 border-4 border-dark shadow-neo-md bg-brand-green/10"><h3 className="font-display text-xl font-black text-dark mb-4 border-b-4 border-dark pb-2 inline-block">Tambah Kursus</h3><div className="flex flex-col gap-4">
          <div><label className="font-display font-bold text-xs mb-1 block">Judul Kursus *</label><input type="text" placeholder="Masukkan judul..." value={nT} onChange={e => sNT(e.target.value)} className="input-field" /></div>
          <div><label className="font-display font-bold text-xs mb-2 block">Platform</label><div className="flex flex-wrap gap-2">{['Dicoding', 'YouTube', 'Udemy', 'Buku', 'Lainnya'].map(p => (<button key={p} onClick={() => sNP(p.toLowerCase())} className={`px-4 py-2 rounded-xl font-display font-bold text-xs border-2 shadow-[2px_2px_0_#09090B] transition-transform hover:-translate-y-0.5 active:translate-y-0 active:shadow-none ${nP === p.toLowerCase() ? 'bg-dark text-white border-dark' : 'bg-white text-dark border-dark'}`}>{p}</button>))}</div></div>
          <div><label className="font-display font-bold text-xs mb-1 block">URL (opsional)</label><input type="url" placeholder="https://..." value={nU} onChange={e => sNU(e.target.value)} className="input-field" /></div>
          <div><label className="font-display font-bold text-xs mb-1 block">Estimasi Jam Total</label><input type="number" placeholder="Contoh: 10" value={nH} onChange={e => sNH(e.target.value)} className="input-field" /></div>
          {allMs().length > 0 && <div><label className="font-display font-bold text-xs mb-1 block">Tautkan ke Milestone</label><select value={nM} onChange={e => sNM(e.target.value)} className="input-field text-sm font-medium"><option value="">-- Tidak Ditautkan --</option>{allMs().map(ms => (<option key={ms.id} value={ms.id}>{ms.phase} — {ms.title}</option>))}</select></div>}
          <div className="flex gap-3 mt-2"><button onClick={() => setShowAdd(false)} className="flex-1 px-4 py-3 border-4 border-dark bg-white font-display font-black rounded-xl hover:bg-border-light transition-colors">Batal</button><button onClick={addCourse} className="flex-1 px-4 py-3 border-4 border-dark bg-brand-pink text-dark font-display font-black rounded-xl shadow-[2px_2px_0_#09090B] hover:-translate-y-1 hover:shadow-[4px_4px_0_#09090B] transition-all">Simpan</button></div>
        </div></div>) : (<button onClick={() => setShowAdd(true)} className="btn-neo border-4 bg-brand-yellow w-full mt-6 py-4 text-base shadow-[4px_4px_0_#09090B]">+ Tambah Kursus Baru</button>)}
      </div>
    ) : (
      /* ── RECOMMENDATIONS TAB — now uses by-roadmap endpoint ── */
      <div className="relative z-10">
        {/* Phase filter chips */}
        {phases().length > 0 && (<div className="flex gap-3 overflow-x-auto py-3 mb-1 -mx-4 px-4 no-scrollbar">
          <button onClick={() => setRecoPhaseFilter(null)} className={`shrink-0 px-4 py-2 rounded-xl font-display font-bold text-xs border-2 transition-all ${recoPhaseFilter === null ? 'bg-brand-blue text-white border-dark shadow-[2px_2px_0_#09090B] -translate-y-1' : 'bg-white border-dark text-dark hover:-translate-y-0.5 hover:shadow-[1px_1px_0_#09090B]'}`}>Semua Fase</button>
          {phases().map((p: any) => (<button key={p.phase_number} onClick={() => setRecoPhaseFilter(p.phase_number)} className={`shrink-0 px-4 py-2 rounded-xl font-display font-bold text-xs border-2 transition-all ${recoPhaseFilter === p.phase_number ? 'bg-brand-blue text-white border-dark shadow-[2px_2px_0_#09090B] -translate-y-1' : 'bg-white border-dark text-dark hover:-translate-y-0.5 hover:shadow-[1px_1px_0_#09090B]'}`}>Fase {p.phase_number}</button>))}
        </div>)}

        {/* Roadmap-grouped recommendations */}
        {recoPhases.length > 0 ? (<div className="flex flex-col gap-8 mt-2">
          {recoPhases.map((phase: any) => (<div key={phase.phase_number} className="bg-brand-blue/5 border-4 border-dark rounded-xl px-4 pb-4 pt-2 shadow-[4px_4px_0_#09090B] mt-8">
            <div className="-mt-8 mb-4">
              <h3 className="font-display text-lg text-dark font-black bg-brand-yellow inline-block px-3 py-1 border-2 border-dark rounded-lg shadow-[2px_2px_0_#09090B]">Fase {phase.phase_number}: {phase.phase_title}</h3>
            </div>
            <p className="font-body text-sm font-medium text-text-secondary mb-5 border-l-4 border-dark pl-3 py-1">{phase.description}</p>

            {(phase.milestones || []).map((ms: any) => {
              if (!ms.courses?.length) return null
              return (<div key={ms.milestone_id} className="mb-6 last:mb-0">
                <div className="flex items-center gap-3 mb-3">
                  <div className="w-2.5 h-2.5 rounded-full border-2 border-dark bg-brand-pink shrink-0" />
                  <p className="font-display text-lg text-dark font-extrabold leading-tight">{ms.title}</p>
                </div>
                <div className="flex flex-wrap gap-2 mb-4 ml-5">{(ms.skills || []).map((s: string) => (<span key={s} className="px-2 py-1 border-2 border-dark rounded-md bg-white font-display font-bold text-[10px] text-dark shadow-[1px_1px_0_#09090B]">{s}</span>))}</div>
                <div className="flex flex-col gap-4 ml-5">{ms.courses.map((r: any) => (<div key={r.id} className="neo-card p-4 border-4 border-dark shadow-neo-sm bg-white hover:-translate-y-1 hover:shadow-neo-md transition-all">
                  <div className="flex flex-wrap items-center gap-2 mb-3"><PBadge p={r.source} />{r.is_free && <span className="px-2 py-0.5 border-2 border-dark rounded-md bg-brand-green font-display font-bold text-[10px] text-dark shadow-[1px_1px_0_#09090B]">Gratis</span>}{r.level && <span className="px-2 py-0.5 border-2 border-dark rounded-md bg-white font-display font-bold text-[10px] text-text-secondary shadow-[1px_1px_0_#09090B]">{r.level}</span>}</div>
                  <p className="font-display text-lg text-dark font-black mb-1 leading-snug">{r.title}</p>
                  {r.instructor && <p className="font-body text-xs font-semibold text-text-muted mb-2">oleh <span className="text-dark">{r.instructor}</span></p>}
                  {r.description_short && <p className="font-body text-xs text-text-secondary line-clamp-2 mb-3 border-l-2 border-dark pl-2">{r.description_short}</p>}
                  <div className="flex items-center justify-between mt-auto pt-2">
                    <div className="flex flex-col gap-1">
                      {r.rating && <p className="font-display text-xs font-black text-brand-yellow drop-shadow-[1px_1px_0_#09090B]">{'★'.repeat(Math.round(r.rating))} <span className="text-dark text-[10px] ml-1">{r.rating.toFixed(1)}</span></p>}
                      {r.url && <a href={r.url} target="_blank" rel="noopener noreferrer" className="font-body text-[10px] font-bold text-brand-blue underline max-w-[150px] truncate hover:text-brand-pink">Lihat Kursus ➔</a>}
                    </div>
                    <button onClick={() => addReco(r, ms.milestone_id)} disabled={addingRecoId === r.id} className={`font-display font-bold text-xs px-4 py-2 border-4 border-dark rounded-xl shadow-[2px_2px_0_#09090B] transition-all ${addingRecoId === r.id ? 'bg-border-light text-text-muted' : 'bg-brand-pink hover:-translate-y-1 hover:shadow-[4px_4px_0_#09090B] active:translate-y-0 active:shadow-[1px_1px_0_#09090B]'}`}>{addingRecoId === r.id ? '⏳' : 'Tambah ✚'}</button>
                  </div>
                </div>))}</div>
              </div>)
            })}
          </div>))}
        </div>) : (
          <div className="neo-card p-8 border-4 border-dark shadow-neo-sm bg-white text-center"><span className="text-6xl mb-4 block">🔍</span><p className="font-display text-2xl font-black text-dark mb-2">Belum Ada Rekomendasi</p><p className="font-body text-base font-medium text-text-secondary">Tidak ada rekomendasi yang cocok untuk fase ini.</p></div>
        )}
      </div>
    )}
    </div>
    </div>
  )
}
