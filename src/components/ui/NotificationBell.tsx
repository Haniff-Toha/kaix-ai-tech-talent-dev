import { useEffect, useState, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import { notificationService } from '@/services/backend'

interface Notification {
  id: string
  title: string
  body: string
  channel: string
  is_read: boolean
  created_at: string | null
}

export default function NotificationBell() {
  const navigate = useNavigate()
  const [open, setOpen] = useState(false)
  const [unread, setUnread] = useState(0)
  const [notifications, setNotifications] = useState<Notification[]>([])
  const [loading, setLoading] = useState(false)
  const ref = useRef<HTMLDivElement>(null)

  // Poll unread count
  useEffect(() => {
    fetchUnread()
    const interval = setInterval(fetchUnread, 30000)
    return () => clearInterval(interval)
  }, [])

  // Close dropdown on outside click
  useEffect(() => {
    const handler = (e: MouseEvent) => {
      if (ref.current && !ref.current.contains(e.target as Node)) setOpen(false)
    }
    document.addEventListener('mousedown', handler)
    return () => document.removeEventListener('mousedown', handler)
  }, [])

  const fetchUnread = async () => {
    try {
      const { data } = await notificationService.unreadCount()
      setUnread(data?.data?.count || 0)
    } catch {}
  }

  const loadNotifications = async () => {
    setLoading(true)
    try {
      const { data } = await notificationService.list(1)
      setNotifications((data?.data?.items || []).slice(0, 5))
    } catch {}
    setLoading(false)
  }

  const handleToggle = () => {
    if (!open) loadNotifications()
    setOpen(!open)
  }

  const handleMarkAllRead = async () => {
    try {
      await notificationService.markAllRead()
      setUnread(0)
      setNotifications(prev => prev.map(n => ({ ...n, is_read: true })))
    } catch {}
  }

  const timeAgo = (iso: string | null) => {
    if (!iso) return ''
    const diff = Date.now() - new Date(iso).getTime()
    const mins = Math.floor(diff / 60000)
    if (mins < 1) return 'Baru saja'
    if (mins < 60) return `${mins} menit lalu`
    const hrs = Math.floor(mins / 60)
    if (hrs < 24) return `${hrs} jam lalu`
    const days = Math.floor(hrs / 24)
    return `${days} hari lalu`
  }

  return (
    <div ref={ref} className="relative">
      {/* Bell Button */}
      <button
        onClick={handleToggle}
        className="relative w-9 h-9 rounded-full flex items-center justify-center bg-cream border-2 border-border-default hover:border-brand-blue transition-all"
        aria-label="Notifications"
      >
        <svg width="18" height="18" viewBox="0 0 22 22" fill="none" stroke="#1A1A2E" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
          <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h16s-3-2-3-9"/>
          <path d="M13.73 21a2 2 0 0 1-3.46 0"/>
        </svg>
        {unread > 0 && (
          <span className="absolute -top-0.5 -right-0.5 min-w-[16px] h-[16px] flex items-center justify-center px-1 bg-brand-red text-white rounded-full font-body text-[8px] font-bold leading-none">
            {unread > 9 ? '9+' : unread}
          </span>
        )}
      </button>

      {/* Dropdown */}
      {open && (
        <div className="absolute right-0 top-11 w-[320px] max-h-[400px] bg-white border-2 border-dark rounded-xl shadow-pixel-sm overflow-hidden z-[100]">
          {/* Header */}
          <div className="flex items-center justify-between px-3 py-2.5 border-b-2 border-border-default bg-cream">
            <span className="font-display text-sm font-semibold text-dark">🔔 Notifikasi</span>
            {unread > 0 && (
              <button onClick={handleMarkAllRead} className="font-body text-[10px] text-brand-blue hover:underline">
                Tandai semua dibaca
              </button>
            )}
          </div>

          {/* List */}
          <div className="overflow-y-auto max-h-[300px]">
            {loading ? (
              <div className="flex justify-center py-6">
                <div className="w-5 h-5 border-2 border-brand-blue border-t-transparent rounded-full animate-spin" />
              </div>
            ) : notifications.length === 0 ? (
              <div className="py-8 text-center">
                <span className="text-2xl block mb-1">🌿</span>
                <p className="font-body text-sm text-text-muted">Belum ada notifikasi</p>
              </div>
            ) : (
              notifications.map((n) => (
                <div
                  key={n.id}
                  className={`px-3 py-2.5 border-b border-border-default/50 cursor-pointer hover:bg-cream/60 transition-colors ${!n.is_read ? 'bg-blue-light/20' : ''}`}
                  onClick={() => {
                    setOpen(false)
                    navigate('/profile/notifications')
                  }}
                >
                  <div className="flex items-start gap-2">
                    {!n.is_read && (
                      <div className="w-2 h-2 rounded-full bg-brand-blue mt-1.5 shrink-0" />
                    )}
                    <div className="flex-1 min-w-0">
                      <p className="font-body text-xs text-dark font-semibold truncate">{n.title}</p>
                      <p className="font-body text-[11px] text-text-muted mt-0.5 line-clamp-2" style={{ whiteSpace: 'pre-line' }}>{n.body}</p>
                      <p className="font-body text-[9px] text-text-muted mt-1">{timeAgo(n.created_at)}</p>
                    </div>
                  </div>
                </div>
              ))
            )}
          </div>

          {/* Footer */}
          <div className="px-3 py-2 border-t-2 border-border-default bg-cream">
            <button
              onClick={() => {
                setOpen(false)
                navigate('/profile/notifications')
              }}
              className="font-body text-xs text-brand-blue hover:underline w-full text-center"
            >
              Lihat semua →
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
