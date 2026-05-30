import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'

export default function LandingPage() {
  const navigate = useNavigate()

  return (
    <div className="min-h-dvh bg-bg-base flex flex-col relative overflow-hidden">
      {/* Neo-brutalist background decoration */}
      <div className="absolute inset-0 pointer-events-none overflow-hidden z-0">
        <div className="absolute top-20 -right-16 w-64 h-64 rounded-full bg-brand-yellow/30 blur-3xl mix-blend-multiply" />
        <div className="absolute bottom-32 -left-20 w-72 h-72 rounded-full bg-brand-blue/20 blur-3xl mix-blend-multiply" />
        <div className="absolute top-1/2 right-10 w-40 h-40 rounded-full bg-brand-pink/20 blur-2xl mix-blend-multiply" />
        {/* Cartoonish dot grid background pattern */}
        <div className="absolute inset-0 opacity-[0.03]" style={{ backgroundImage: 'radial-gradient(#09090B 1.5px, transparent 1.5px)', backgroundSize: '24px 24px' }}></div>
      </div>

      {/* Content */}
      <div className="relative z-10 flex-1 flex flex-col items-center justify-center px-6 max-w-md mx-auto w-full">
        {/* Logo + Brand */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, ease: 'easeOut' }}
          className="text-center mb-2"
        >
          <div className="relative inline-block mb-6">
            <img src="/kaix_logo.png" alt="Kaix" className="w-28 h-28 mx-auto object-contain relative z-10 drop-shadow-xl" />
            <div className="absolute inset-0 bg-brand-yellow rounded-full blur-2xl opacity-40 z-0 animate-pulse"></div>
          </div>
          <h1 className="font-display text-5xl text-dark font-extrabold tracking-tight">kaix</h1>
          <p className="font-body font-medium text-base text-brand-blue mt-2">AI Tech Talent Companion</p>
        </motion.div>

        {/* Hero text */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2, ease: 'easeOut' }}
          className="text-center mb-12 neo-card p-6 border-4"
        >
          <h2 className="font-display text-2xl text-dark leading-tight mb-3 font-bold">
            Roadmap belajar <span className="bg-brand-yellow px-2 py-0.5 rounded-md border-2 border-dark shadow-[2px_2px_0px_#09090B] inline-block transform -rotate-2">personal</span><br />
            dibantu AI.
          </h2>
          <p className="font-body text-sm text-text-secondary leading-relaxed max-w-xs mx-auto font-medium">
            Mulai dari skill assessment hingga daily task. Capai karir impianmu di dunia tech Indonesia.
          </p>
        </motion.div>

        {/* Feature pills */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.5, delay: 0.4 }}
          className="flex flex-wrap justify-center gap-3 mb-10"
        >
          {['🎯 Roadmap', '📊 Assessment', '🔥 Streak', '🤖 AI Coach'].map((f) => (
            <span key={f} className="px-4 py-2 rounded-xl bg-white border-2 border-border-bold font-display font-bold text-sm text-dark shadow-neo-sm transform hover:-translate-y-1 hover:shadow-neo-md transition-all cursor-default">
              {f}
            </span>
          ))}
        </motion.div>

        {/* CTAs */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.5 }}
          className="w-full flex flex-col gap-4"
        >
          <button
            onClick={() => navigate('/signup')}
            className="btn-neo w-full text-lg py-4 border-4 bg-brand-blue"
          >
            🚀 Mulai Perjalanan
          </button>
          <button
            onClick={() => navigate('/login')}
            className="btn-secondary w-full text-base py-3 border-4"
          >
            Masuk ke Akun
          </button>
        </motion.div>
      </div>

      {/* Footer */}
      <div className="relative z-8 text-center pb-24 px-6">
        <p className="font-display font-bold text-xs text-text-muted uppercase tracking-wider">
          Still on Development Gaisss! 🚀
        </p>
      </div>

      {/* Floating Download APK Button */}
      <motion.a
        href="https://drive.google.com/file/d/1eo_Eo0494o3rkwaiSK4zp0uIaf40Rgls/view?usp=sharing"
        target="_blank"
        rel="noopener noreferrer"
        initial={{ opacity: 0, scale: 0.8 }}
        animate={{ 
          opacity: 1, 
          scale: 1,
          y: [0, -8, 0] // Continuous floating up/down motion
        }}
        transition={{ 
          opacity: { delay: 0.8, duration: 0.4 },
          scale: { delay: 0.8, type: 'spring', stiffness: 200 },
          y: {
            repeat: Infinity,
            duration: 2.4,
            ease: "easeInOut"
          }
        }}
        className="fixed bottom-6 right-6 z-50 flex items-center gap-2 px-5 py-3 border-4 border-dark rounded-2xl bg-brand-pink font-display font-black text-sm text-dark shadow-[4px_4px_0_#09090B] hover:bg-[#ff9cbd] active:shadow-[2px_2px_0_#09090B] active:translate-y-[2px] transition-all cursor-pointer"
      >
        <span>📲</span>
        <span>Download the App!</span>
      </motion.a>
    </div>
  )
}
