// Design System Tokens for Storyteller App
// Dark Fantasy Theme with Mobile-First Approach

export const colors = {
  // Primary - Deep purples and blues for mystical atmosphere
  primary: {
    50: '#f0f4ff',
    100: '#e0e7ff',
    200: '#c7d2fe',
    300: '#a5b4fc',
    400: '#818cf8',
    500: '#6366f1',
    600: '#4f46e5',
    700: '#4338ca',
    800: '#3730a3',
    900: '#312e81',
    950: '#1e1b4b',
  },
  // Secondary - Amber/gold for magical accents
  secondary: {
    50: '#fefce8',
    100: '#fef9c3',
    200: '#fef08a',
    300: '#fde047',
    400: '#facc15',
    500: '#eab308',
    600: '#ca8a04',
    700: '#a16207',
    800: '#854d0e',
    900: '#713f12',
    950: '#422006',
  },
  // Accent - Purple for magical elements
  accent: {
    50: '#faf5ff',
    100: '#f3e8ff',
    200: '#e9d5ff',
    300: '#d8b4fe',
    400: '#c084fc',
    500: '#a855f7',
    600: '#9333ea',
    700: '#7c3aed',
    800: '#6b21a8',
    900: '#581c87',
    950: '#3b0764',
  },
  // Dark - Grays for backgrounds and text
  dark: {
    50: '#f8fafc',
    100: '#f1f5f9',
    200: '#e2e8f0',
    300: '#cbd5e1',
    400: '#94a3b8',
    500: '#64748b',
    600: '#475569',
    700: '#334155',
    800: '#1e293b',
    900: '#0f172a',
    950: '#020617',
  }
} as const;

export const typography = {
  // Font families
  fontFamily: {
    fantasy: ['Cinzel', 'serif'],
    sans: ['Inter', 'system-ui', 'sans-serif'],
  },
  // Font sizes with mobile-first approach
  fontSize: {
    xs: ['0.75rem', { lineHeight: '1rem' }],
    sm: ['0.875rem', { lineHeight: '1.25rem' }],
    base: ['1rem', { lineHeight: '1.5rem' }],
    lg: ['1.125rem', { lineHeight: '1.75rem' }],
    xl: ['1.25rem', { lineHeight: '1.75rem' }],
    '2xl': ['1.5rem', { lineHeight: '2rem' }],
    '3xl': ['1.875rem', { lineHeight: '2.25rem' }],
    '4xl': ['2.25rem', { lineHeight: '2.5rem' }],
    '5xl': ['3rem', { lineHeight: '1' }],
  },
  // Font weights
  fontWeight: {
    light: '300',
    normal: '400',
    medium: '500',
    semibold: '600',
    bold: '700',
  }
} as const;

export const spacing = {
  // Consistent spacing scale
  xs: '0.25rem',    // 4px
  sm: '0.5rem',     // 8px
  md: '1rem',       // 16px
  lg: '1.5rem',     // 24px
  xl: '2rem',       // 32px
  '2xl': '3rem',    // 48px
  '3xl': '4rem',    // 64px
  '4xl': '6rem',    // 96px
} as const;

export const shadows = {
  // Elevation system for cards and components
  sm: '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
  base: '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)',
  md: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
  lg: '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
  xl: '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
  // Magical glow effects
  glow: '0 0 20px rgba(168, 85, 247, 0.4)',
  glowStrong: '0 0 30px rgba(168, 85, 247, 0.6)',
} as const;

export const animations = {
  // Animation presets
  fadeIn: 'fadeIn 0.6s ease-out',
  slideUp: 'slideUp 0.4s ease-out',
  glow: 'glow 2s ease-in-out infinite alternate',
  pulseSlow: 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
} as const;

export const breakpoints = {
  // Mobile-first breakpoints
  sm: '640px',
  md: '768px',
  lg: '1024px',
  xl: '1280px',
  '2xl': '1536px',
} as const;

// Component-specific design tokens
export const components = {
  card: {
    padding: spacing.lg,
    borderRadius: '0.75rem',
    shadow: shadows.md,
    background: 'rgba(15, 23, 42, 0.8)',
    border: '1px solid rgba(168, 85, 247, 0.2)',
  },
  button: {
    primary: {
      background: `linear-gradient(135deg, ${colors.primary[600]}, ${colors.primary[700]})`,
      hover: `linear-gradient(135deg, ${colors.primary[700]}, ${colors.primary[800]})`,
      shadow: shadows.glow,
    },
    secondary: {
      background: `linear-gradient(135deg, ${colors.secondary[600]}, ${colors.secondary[700]})`,
      hover: `linear-gradient(135deg, ${colors.secondary[700]}, ${colors.secondary[800]})`,
    },
    choice: {
      background: 'rgba(30, 41, 59, 0.8)',
      hover: 'rgba(51, 65, 85, 0.9)',
      border: '1px solid rgba(168, 85, 247, 0.3)',
      shadow: shadows.base,
    }
  },
  narrative: {
    fontSize: typography.fontSize.lg,
    lineHeight: '1.75rem',
    color: colors.dark[100],
    fontFamily: typography.fontFamily.sans,
  },
  choice: {
    fontSize: typography.fontSize.base,
    lineHeight: '1.5rem',
    color: colors.dark[200],
    fontFamily: typography.fontFamily.sans,
  }
} as const;
