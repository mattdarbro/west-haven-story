/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Dynamic theming with CSS variables
        primary: {
          50: 'var(--color-primary-50, #f0f4ff)',
          100: 'var(--color-primary-100, #e0e7ff)',
          200: 'var(--color-primary-200, #c7d2fe)',
          300: 'var(--color-primary-300, #a5b4fc)',
          400: 'var(--color-primary-400, #818cf8)',
          500: 'var(--color-primary-500, #6366f1)',
          600: 'var(--color-primary-600, #4f46e5)',
          700: 'var(--color-primary-700, #4338ca)',
          800: 'var(--color-primary-800, #3730a3)',
          900: 'var(--color-primary-900, #312e81)',
          950: 'var(--color-primary-950, #1e1b4b)',
        },
        secondary: {
          50: 'var(--color-secondary-50, #fefce8)',
          100: 'var(--color-secondary-100, #fef9c3)',
          200: 'var(--color-secondary-200, #fef08a)',
          300: 'var(--color-secondary-300, #fde047)',
          400: 'var(--color-secondary-400, #facc15)',
          500: 'var(--color-secondary-500, #eab308)',
          600: 'var(--color-secondary-600, #ca8a04)',
          700: 'var(--color-secondary-700, #a16207)',
          800: 'var(--color-secondary-800, #854d0e)',
          900: 'var(--color-secondary-900, #713f12)',
          950: 'var(--color-secondary-950, #422006)',
        },
        accent: {
          50: 'var(--color-accent-50, #faf5ff)',
          100: 'var(--color-accent-100, #f3e8ff)',
          200: 'var(--color-accent-200, #e9d5ff)',
          300: 'var(--color-accent-300, #d8b4fe)',
          400: 'var(--color-accent-400, #c084fc)',
          500: 'var(--color-accent-500, #a855f7)',
          600: 'var(--color-accent-600, #9333ea)',
          700: 'var(--color-accent-700, #7c3aed)',
          800: 'var(--color-accent-800, #6b21a8)',
          900: 'var(--color-accent-900, #581c87)',
          950: 'var(--color-accent-950, #3b0764)',
        },
        dark: {
          50: 'var(--color-dark-50, #f8fafc)',
          100: 'var(--color-dark-100, #f1f5f9)',
          200: 'var(--color-dark-200, #e2e8f0)',
          300: 'var(--color-dark-300, #cbd5e1)',
          400: 'var(--color-dark-400, #94a3b8)',
          500: 'var(--color-dark-500, #64748b)',
          600: 'var(--color-dark-600, #475569)',
          700: 'var(--color-dark-700, #334155)',
          800: 'var(--color-dark-800, #1e293b)',
          900: 'var(--color-dark-900, #0f172a)',
          950: 'var(--color-dark-950, #020617)',
        }
      },
      fontFamily: {
        'fantasy': ['var(--font-fantasy, Cinzel)', 'serif'],
        'sans': ['var(--font-body, Inter)', 'system-ui', 'sans-serif'],
        'heading': ['var(--font-heading, Cinzel)', 'serif'],
      },
      animation: {
        'fade-in': 'fadeIn 0.6s ease-out',
        'slide-up': 'slideUp 0.4s ease-out',
        'glow': 'glow 2s ease-in-out infinite alternate',
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0', transform: 'translateY(10px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        slideUp: {
          '0%': { opacity: '0', transform: 'translateY(20px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        glow: {
          '0%': { boxShadow: '0 0 5px rgba(168, 85, 247, 0.4)' },
          '100%': { boxShadow: '0 0 20px rgba(168, 85, 247, 0.8)' },
        }
      },
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'gradient-conic': 'conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))',
        'story-bg': 'linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #312e81 100%)',
      }
    },
  },
  plugins: [],
}
