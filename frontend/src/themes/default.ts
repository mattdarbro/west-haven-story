import { Theme } from './types';

export const defaultTheme: Theme = {
  name: 'default',
  displayName: 'Dark Fantasy',
  description: 'A mysterious dark fantasy theme with deep purples and mystical elements',
  
  colors: {
    primary: ['#4338ca', '#6366f1', '#818cf8', '#a5b4fc'],
    secondary: ['#7c3aed', '#8b5cf6', '#a78bfa', '#c4b5fd'],
    accent: ['#f59e0b', '#fbbf24', '#fcd34d', '#fde68a'],
    background: {
      primary: '#0f0f23',
      secondary: '#1a1a2e',
      tertiary: '#16213e',
    },
    text: {
      primary: '#e2e8f0',
      secondary: '#94a3b8',
      muted: '#64748b',
    },
    border: '#334155',
    surface: '#1e293b',
  },
  
  typography: {
    heading: {
      font: 'Cinzel, serif',
      weights: [400, 500, 600, 700],
    },
    body: {
      font: 'Inter, sans-serif',
      weights: [300, 400, 500, 600],
    },
    fantasy: {
      font: 'Cinzel, serif',
      weights: [400, 500, 600, 700],
    },
  },
  
  effects: {
    backgroundGradient: 'linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%)',
    cardGradient: 'linear-gradient(135deg, rgba(67, 56, 202, 0.1) 0%, rgba(124, 58, 237, 0.1) 100%)',
    glowColor: '#6366f1',
    shadowColor: 'rgba(99, 102, 241, 0.3)',
  },
  
  atmosphere: {
    mood: 'mysterious, ancient, magical',
    keywords: ['dark', 'mystical', 'ancient', 'magical', 'ethereal'],
    visualStyle: 'cinematic, high contrast, glowing elements',
  },
};
