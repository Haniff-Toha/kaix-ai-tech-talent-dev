import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { telegramService, notificationService } from '@/services/backend'
import KnotLoader from '@/components/ui/KnotLoader'

const TUTORIAL_ID = [
  { step: 1, title: 'Buka Telegram dan cari @BotFather', desc: 'Cari @BotFather di kolom pencarian. Pilih akun resmi dengan centang biru.', img: '/images/telegram-tutorial/1_botfather_search.png' },
  { step: 2, title: 'Klik tombol "Start"', desc: 'Klik tombol Start di bawah untuk mengaktifkan chat.', img: '/images/telegram-tutorial/2_botfather_start.png' },
  { step: 3, title: 'Buat Bot Baru', desc: 'Ketik perintah /newbot dan kirim.' },
  { step: 4, title: 'Beri Nama Bot', desc: 'BotFather akan meminta nama (contoh: My Talent Dev Companion). Ini nama tampilan yang bisa diubah nanti.' },
  { step: 5, title: 'Beri Username', desc: 'Pilih username unik. Harus diakhiri "bot" (contoh: kaix_talent_bot).', img: '/images/telegram-tutorial/3_newbot_username.jpeg' },
  { step: 6, title: 'Salin API Token', desc: 'Setelah username berhasil, BotFather akan mengirim API Token. Tap token untuk menyalin otomatis.', img: '/images/telegram-tutorial/4_bot_http_api.jpeg' },
  { step: 7, title: 'Tempel Token di Kaix', desc: 'Tempel token yang disalin ke kolom input Telegram di pengaturan Kaix di bawah.' },
  { step: 8, title: 'Kembali ke Telegram', desc: 'Setelah koneksi berhasil, kembali ke Telegram dan klik link bot yang diberikan.', img: '/images/telegram-tutorial/5_bot_link_account.jpeg' },
  { step: 9, title: 'Klik Start untuk mulai', desc: 'Klik Start untuk mulai menerima reminder & notifikasi.', img: '/images/telegram-tutorial/6_bot_start.jpeg' },
]

const TUTORIAL_EN = [
  { step: 1, title: 'Open Telegram and find @BotFather', desc: 'Search for @BotFather in the search bar. Select the official account with the blue verified checkmark.', img: '/images/telegram-tutorial/1_botfather_search.png' },
  { step: 2, title: 'Click the "Start" button', desc: 'Click the Start button at the bottom to activate the chat.', img: '/images/telegram-tutorial/2_botfather_start.png' },
  { step: 3, title: 'Create a New Bot', desc: 'Type the command /newbot and send it.' },
  { step: 4, title: 'Set a Name', desc: 'BotFather will ask for a name (e.g., My Talent Dev Companion). This display name can be changed later.' },
  { step: 5, title: 'Set a Username', desc: 'Choose a globally unique username. Must end in "bot" (e.g., kaix_talent_bot).', img: '/images/telegram-tutorial/3_newbot_username.jpeg' },
  { step: 6, title: 'Get the Token', desc: 'After setting the username, BotFather will send your API Token. Tap the token to copy it.', img: '/images/telegram-tutorial/4_bot_http_api.jpeg' },
  { step: 7, title: 'Apply Token in Kaix', desc: 'Paste the copied token into the Telegram input field in Kaix settings below.' },
  { step: 8, title: 'Return to Telegram', desc: 'Once connected, return to Telegram and click the provided bot link.', img: '/images/telegram-tutorial/5_bot_link_account.jpeg' },
  { step: 9, title: 'Click Start to begin', desc: 'Click Start to begin receiving reminders & notifications.', img: '/images/telegram-tutorial/6_bot_start.jpeg' },
]

export default function NotificationSettingsPage() {
  const nav = useNavigate()
  const [lang, setLang] = useState<'id'|'en'>('id')
  const [tgStatus, setTgStatus] = useState<any>(null)
  const [tgToken, setTgToken] = useState('')
  const [tgLoading, setTgLoading] = useState(false)
  const [tgMsg, setTgMsg] = useState('')
  const [showTutorial, setShowTutorial] = useState(false)
  const [unread, setUnread] = useState(0)
  const [notifs, setNotifs] = useState<any[]>([])
  const [notifsLoading, setNotifsLoading] = useState(false)
  const [showNotifs, setShowNotifs] = useState(false)
  const [loading, setLoading] = useState(true)

  useEffect(() => { loadAll() }, [])

  const loadAll = async () => {
    setLoading(true)
    try {
      const [tg, uc] = await Promise.allSettled([
        telegramService.status(),
        notificationService.unreadCount(),
      ])
      if (tg.status === 'fulfilled') setTgStatus(tg.value.data?.data)
      if (uc.status === 'fulfilled') setUnread(uc.value.data?.data?.count || 0)
    } catch (e) { console.error(e) }
    setLoading(false)
  }

  const connectTelegram = async () => {
    if (!tgToken.trim()) return
    setTgLoading(true); setTgMsg('')
    try {
      const { data } = await telegramService.connect(tgToken.trim())
      if (data.success) {
        setTgMsg(data.data?.message || 'Bot tervalidasi! Buka Telegram dan kirim /start.')
        setTgStatus(data.data)
        // Start polling status
        pollTgStatus()
      } else {
        setTgMsg(data.message || 'Token tidak valid.')
      }
    } catch (e: any) {
      setTgMsg(e.response?.data?.message || 'Gagal menghubungkan bot.')
    }
    setTgLoading(false)
  }

  const pollTgStatus = () => {
    let tries = 0
    const interval = setInterval(async () => {
      tries++
      try {
        const { data } = await telegramService.status()
        if (data.data?.is_verified) {
          setTgStatus(data.data)
          setTgMsg('✅ Telegram berhasil terverifikasi!')
          clearInterval(interval)
        }
      } catch {}
      if (tries > 30) clearInterval(interval) // stop after ~60s
    }, 2000)
  }

  const disconnectTelegram = async () => {
    try {
      await telegramService.disconnect()
      setTgStatus(null); setTgToken(''); setTgMsg('Disconnected.')
    } catch {}
  }

  const testTelegram = async () => {
    setTgLoading(true)
    try {
      const { data } = await telegramService.test()
      setTgMsg(data.message || 'Test sent!')
    } catch { setTgMsg('Gagal mengirim pesan tes.') }
    setTgLoading(false)
  }

  const loadNotifs = async () => {
    setNotifsLoading(true)
    try {
      const { data } = await notificationService.list()
      setNotifs(data?.data?.items || [])
    } catch {}
    setNotifsLoading(false)
  }

  const markAllRead = async () => {
    try {
      await notificationService.markAllRead()
      setUnread(0)
      setNotifs(ns => ns.map(n => ({ ...n, is_read: true })))
    } catch {}
  }

  const tutorial = lang === 'id' ? TUTORIAL_ID : TUTORIAL_EN

  if (loading) return <div className="flex justify-center py-12"><KnotLoader size="md" /></div>

  return (
    <div className="px-4 pb-24">
      <div className="sticky top-0 z-50 bg-bg-base/95 backdrop-blur-sm pt-5 pb-4 mb-5 flex items-center justify-between border-b-2 border-dark/10 -mx-4 px-4">
        <div className="flex items-center gap-3">
          <button onClick={() => nav(-1)} className="w-10 h-10 rounded-full bg-white border-2 border-dark shadow-[2px_2px_0_#09090B] flex items-center justify-center text-sm hover:translate-y-[-1px] hover:shadow-[4px_4px_0_#09090B] transition-all">←</button>
          <h1 className="font-display text-2xl text-dark font-black">Pengaturan</h1>
        </div>
        <img src="/kaix_logo.png" alt="Logo" className="w-8 h-8 object-contain drop-shadow-sm" />
      </div>

      {/* ── In-App Notifications ── */}
      <div className="neo-card p-5 mb-6 border-4 border-dark shadow-[4px_4px_0_#09090B] bg-white">
        <div className="flex items-center justify-between mb-2">
          <div className="flex items-center gap-2">
            <span className="text-xl">🔔</span>
            <h3 className="font-display text-sm text-dark font-medium">In-App Notification</h3>
          </div>
          {unread > 0 && (
            <span className="px-2 py-0.5 bg-brand-red text-white rounded-full font-body text-[10px] font-bold">{unread}</span>
          )}
        </div>
        <p className="font-body text-xs text-text-muted mb-3">Notifikasi akan muncul di halaman Reminder dan badge navigasi.</p>

        <button
          onClick={() => { setShowNotifs(!showNotifs); if (!showNotifs) loadNotifs() }}
          className="btn-secondary py-2 px-4 text-xs bg-brand-blue-light border-dark shadow-[2px_2px_0_#09090B]"
        >
          {showNotifs ? 'Tutup' : `Lihat Notifikasi (${unread} belum dibaca)`}
        </button>

        {showNotifs && (
          <div className="mt-3">
            {unread > 0 && (
              <button onClick={markAllRead} className="btn-ghost text-[10px] text-text-muted mb-2">Tandai semua dibaca</button>
            )}
            {notifsLoading ? <KnotLoader size="sm" /> : notifs.length > 0 ? (
              <div className="flex flex-col gap-2 max-h-60 overflow-y-auto">
                {notifs.map((n) => (
                  <div key={n.id} className={`p-2.5 rounded-lg border-2 transition-all ${n.is_read ? 'bg-white border-border-default' : 'bg-blue-light border-brand-blue'}`}>
                    <p className="font-display text-xs text-dark font-medium">{n.title}</p>
                    <p className="font-body text-[11px] text-text-secondary">{n.body}</p>
                    <p className="font-body text-[9px] text-text-muted mt-1">{n.created_at ? new Date(n.created_at).toLocaleString('id') : ''}</p>
                  </div>
                ))}
              </div>
            ) : (
              <p className="font-body text-xs text-text-muted text-center py-3">Belum ada notifikasi.</p>
            )}
          </div>
        )}
      </div>

      {/* ── Email ── */}
      <div className="neo-card p-5 mb-6 border-4 border-dark shadow-[4px_4px_0_#09090B] bg-white">
        <div className="flex items-center gap-2 mb-2">
          <span className="text-xl">✉️</span>
          <h3 className="font-display text-sm text-dark font-medium">Email Notification</h3>
        </div>
        <p className="font-body text-xs text-text-muted mb-2">Reminder akan dikirim ke email yang terdaftar di akun Anda.</p>
        <p className="font-body text-xs text-text-secondary bg-cream px-3 py-2 rounded-lg">Pilih channel <strong>"email"</strong> saat membuat reminder di halaman Reminder.</p>
      </div>

      {/* ── Telegram ── */}
      <div className="neo-card p-5 mb-6 border-4 border-dark shadow-[4px_4px_0_#09090B] bg-white">
        <div className="flex items-center justify-between mb-2">
          <div className="flex items-center gap-2">
            <span className="text-xl">📨</span>
            <h3 className="font-display text-sm text-dark font-medium">Telegram Bot</h3>
          </div>
          {tgStatus?.is_verified && <span className="px-3 py-1 bg-brand-green text-dark rounded-md font-display border-2 border-dark shadow-[1px_1px_0_#09090B] text-[10px] font-bold">Terhubung ✅</span>}
        </div>

        {tgStatus?.is_verified ? (
          <div>
            <p className="font-body text-xs text-text-secondary mb-2">
              Bot: <a href={tgStatus.bot_link} target="_blank" rel="noopener noreferrer" className="text-brand-blue underline">@{tgStatus.bot_username}</a>
            </p>
            <div className="flex gap-2">
              <button onClick={testTelegram} disabled={tgLoading} className="btn-secondary text-xs flex-1">
                {tgLoading ? '...' : '🧪 Kirim Tes'}
              </button>
              <button onClick={disconnectTelegram} className="btn-secondary text-xs flex-1 text-white bg-brand-red border-dark">Putuskan</button>
            </div>
          </div>
        ) : tgStatus?.connected && !tgStatus?.is_verified ? (
          <div>
            <div className="bg-brand-yellow/30 p-4 rounded-xl mb-3 border-2 border-dark shadow-[2px_2px_0_#09090B]">
              <p className="font-body text-xs text-dark font-medium">⏳ Menunggu verifikasi... Buka <a href={tgStatus.bot_link} target="_blank" rel="noopener noreferrer" className="text-brand-blue underline font-black">link bot</a> di Telegram dan kirim <code className="bg-dark text-white px-2 py-0.5 rounded-md text-[10px]">/start</code></p>
            </div>
          </div>
        ) : (
          <div>
            <p className="font-body text-xs text-text-muted mb-3">Hubungkan bot Telegram untuk menerima reminder langsung di chat.</p>
            <button onClick={() => setShowTutorial(!showTutorial)} className="btn-secondary w-full justify-center mb-4 shadow-[2px_2px_0_#09090B]">
              {showTutorial ? '▲ Tutup Tutorial' : '📖 Cara Setup Telegram Bot'}
            </button>

            {showTutorial && (
              <div className="mb-4">
                <div className="flex gap-2 mb-3">
                  <button onClick={() => setLang('id')} className={`px-3 py-1 rounded-lg font-body text-xs border-2 transition-all ${lang === 'id' ? 'bg-brand-blue text-white border-dark' : 'bg-white border-border-default text-text-muted'}`}>🇮🇩 Bahasa</button>
                  <button onClick={() => setLang('en')} className={`px-3 py-1 rounded-lg font-body text-xs border-2 transition-all ${lang === 'en' ? 'bg-brand-blue text-white border-dark' : 'bg-white border-border-default text-text-muted'}`}>🇬🇧 English</button>
                </div>
                <div className="flex flex-col gap-3">
                  {tutorial.map((s) => (
                    <div key={s.step} className="bg-cream rounded-xl p-3 border-2 border-border-default">
                      <div className="flex items-start gap-2 mb-1.5">
                        <span className="w-6 h-6 shrink-0 bg-brand-blue text-white rounded-full flex items-center justify-center font-body text-xs font-bold">{s.step}</span>
                        <p className="font-display text-xs text-dark font-medium leading-snug">{s.title}</p>
                      </div>
                      <p className="font-body text-[11px] text-text-secondary ml-8">{s.desc}</p>
                      {s.img && (
                        <img src={s.img} alt={s.title} className="mt-2 ml-8 rounded-lg border-2 border-border-default w-full max-w-[280px]" loading="lazy" />
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}

            <div className="flex gap-2">
              <input
                type="text"
                placeholder="Paste bot token here..."
                value={tgToken}
                onChange={(e) => setTgToken(e.target.value)}
                className="input-field flex-1 text-sm"
              />
              <button onClick={connectTelegram} disabled={tgLoading || !tgToken.trim()} className="btn-neo text-sm px-6">
                {tgLoading ? '...' : 'Connect'}
              </button>
            </div>
          </div>
        )}

        {tgMsg && (
          <p className={`font-body text-xs mt-2 ${tgMsg.includes('✅') || tgMsg.includes('berhasil') ? 'text-dark' : 'text-brand-red'}`}>{tgMsg}</p>
        )}
      </div>
    </div>
  )
}
