import { useEffect, useState } from 'react'
import { NavLink, useLocation } from 'react-router-dom'
import { useUIStore } from '@/stores/uiStore'
import { notificationService } from '@/services/backend'

const navItems = [
  {
    path: '/overview',
    label: 'Overview',
    icon: (active: boolean) => (
      <svg width="22" height="22" viewBox="0 0 22 22" fill={active ? '#fff' : 'none'} stroke={active ? '#fff' : '#09090B'} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <rect x="3" y="3" width="7" height="7" rx="2"/>
        <rect x="12" y="3" width="7" height="7" rx="2"/>
        <rect x="3" y="12" width="7" height="7" rx="2"/>
        <rect x="12" y="12" width="7" height="7" rx="2"/>
      </svg>
    ),
  },
  {
    path: '/course',
    label: 'Roadmap',
    icon: (active: boolean) => (
      <svg width="22" height="22" viewBox="0 0 22 22" fill="none" stroke={active ? '#fff' : '#09090B'} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/>
        <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>
        <line x1="8" y1="7" x2="16" y2="7"/>
        <line x1="8" y1="11" x2="13" y2="11"/>
      </svg>
    ),
  },
  {
    path: '/focus',
    label: 'Focus!',
    isHero: true,
    icon: (active: boolean) => (
      <svg width="24" height="24" viewBox="0 0 24 24" fill={active ? '#09090B' : 'none'} stroke={active ? '#09090B' : '#09090B'} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>
      </svg>
    ),
  },
  {
    path: '/reminder',
    label: 'Reminder',
    hasBadge: true,
    icon: (active: boolean) => (
      <svg width="22" height="22" viewBox="0 0 22 22" fill="none" stroke={active ? '#fff' : '#09090B'} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h16s-3-2-3-9"/>
        <path d="M13.73 21a2 2 0 0 1-3.46 0"/>
      </svg>
    ),
  },
  {
    path: '/profile',
    label: 'Profile',
    icon: (active: boolean) => (
      <svg width="22" height="22" viewBox="0 0 22 22" fill="none" stroke={active ? '#fff' : '#09090B'} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M20 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/>
        <circle cx="11" cy="7" r="4"/>
      </svg>
    ),
  },
]

export default function BottomNav() {
  const isVisible = useUIStore((s) => s.isBottomNavVisible)
  const location = useLocation()
  const [unreadCount, setUnreadCount] = useState(0)

  useEffect(() => {
    const fetchCount = async () => {
      try {
        const { data } = await notificationService.unreadCount()
        setUnreadCount(data?.data?.count || 0)
      } catch {}
    }
    fetchCount()
    const interval = setInterval(fetchCount, 30000)
    return () => clearInterval(interval)
  }, [])

  if (!isVisible) return null

  return (
    <div className="fixed bottom-0 left-0 right-0 z-10 pointer-events-none flex justify-center">
      <nav
        className="pointer-events-auto bg-bg-paper/70 border-t-4 border-x-4 border-dark rounded-t-3xl shadow-[0_-4px_0_#09090B] flex items-center justify-around w-full max-w-xl backdrop-blur-xl h-[76px] px-4 pb-2"
        role="navigation"
        aria-label="Main navigation"
      >
        {navItems.map((item) => {
          const isActive = location.pathname.startsWith(item.path)
          return (
            <NavLink
              key={item.path}
              to={item.path}
              className={`flex flex-col items-center justify-center gap-1 min-w-[60px] relative px-2 py-2 rounded-xl transition-all duration-200
                ${isActive && !(item as any).isHero ? 'bg-brand-blue border-2 border-dark shadow-neo-sm transform -translate-y-1' : ''}
                ${!isActive && !(item as any).isHero ? 'hover:bg-brand-blue-light' : ''}
              `}
              aria-current={isActive ? 'page' : undefined}
            >
              {/* Icon container */}
              <div className={`flex items-center justify-center transition-all duration-200 relative w-10 h-10 ${(item as any).isHero ? '' : 'rounded-xl'}`}>
                {(item as any).isHero ? (
                  <div className="absolute bottom-2 flex flex-col items-center justify-center pointer-events-none">
                    <div
                      className={`flex items-center justify-center w-20 h-20 rounded-full bg-brand-yellow border-4 border-dark shadow-[4px_4px_0px_#09090B] transform pointer-events-auto hover:scale-105 hover:-translate-y-1 z-10 transition-all duration-200
                        ${isActive ? 'bg-brand-pink text-dark scale-105 shadow-[2px_2px_0px_#09090B] translate-y-[2px]' : ''}
                      `}
                    >
                      {item.icon(isActive)}
                    </div>
                    <span className="font-display font-black text-[13px] text-dark mt-1 bg-white px-3 py-0.5 rounded-full border-2 border-dark shadow-[2px_2px_0_#09090B] absolute -bottom-5 whitespace-nowrap pointer-events-auto z-20">Focus!</span>
                  </div>
                ) : (
                  item.icon(isActive)
                )}

                {/* Notification badge */}
                {(item as any).hasBadge && unreadCount > 0 && (
                  <span className="absolute -top-1.5 -right-1.5 min-w-[20px] h-[20px] flex items-center justify-center px-1.5 bg-brand-red text-white border-2 border-dark rounded-full font-display font-extrabold text-[10px] leading-none z-20">
                    {unreadCount > 9 ? '9+' : unreadCount}
                  </span>
                )}
              </div>

              {/* Label */}
              {!(item as any).isHero && (
                <span
                  className={`font-display tracking-wide transition-colors
                    ${isActive ? 'text-white font-bold text-[10px]' : 'text-text-secondary font-bold text-[10px]'}
                  `}
                >
                  {item.label}
                </span>
              )}
            </NavLink>
          )
        })}
      </nav>
    </div>
  )
}
