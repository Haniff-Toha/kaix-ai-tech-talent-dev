/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        'bg-base': '#ffffff', // clean white background
        'bg-paper': '#ffffff', // clean white cards
        'brand-brown': '#f4f4f5', // light grey instead of brown (e.g. zinc-100)
        'brand-blue': '#2563EB',
        'brand-blue-light': '#eff6ff', // light blue instead of earthy yellow (e.g. blue-50)
        'brand-yellow': '#FBBF24',
        'brand-pink': '#EC4899',
        'brand-green': '#10B981',
        'brand-red': '#EF4444',
        'dark': '#09090B', // very dark for strong contrast
        'text-secondary': '#52525B', // zinc-600
        'text-muted': '#A1A1AA', // zinc-400
        'border-bold': '#09090B', // thick black borders
        'border-light': '#E4E4E7', // zinc-200
      },
      fontFamily: {
        display: ['"Plus Jakarta Sans"', 'sans-serif'],
        body: ['"Plus Jakarta Sans"', 'sans-serif'],
        mono: ['"JetBrains Mono"', 'monospace'],
      },
      borderRadius: {
        px: '0px',
        sm: '6px',
        md: '12px',
        lg: '16px',
        xl: '24px',
        '2xl': '32px',
        pill: '999px',
      },
      boxShadow: {
        'neo-sm': '2px 2px 0px #09090B',
        'neo-md': '4px 4px 0px #09090B',
        'neo-lg': '8px 8px 0px #09090B',
        'neo-yellow': '4px 4px 0px #FBBF24',
        'neo-blue': '4px 4px 0px #2563EB',
        'neo-pink': '4px 4px 0px #EC4899',
        'glass': '0 8px 32px 0 rgba(0, 0, 0, 0.05)',
      },
      spacing: {
        '1': '4px',
        '2': '8px',
        '3': '12px',
        '4': '16px',
        '5': '20px',
        '6': '24px',
        '8': '32px',
        '10': '40px',
        '12': '48px',
        '16': '64px',
      },
      fontSize: {
        'xs': '11px',
        'sm': '13px',
        'base': '15px',
        'md': '17px',
        'lg': '20px',
        'xl': '24px',
        '2xl': '30px',
        '3xl': '38px',
      },
    },
  },
  plugins: [],
}
