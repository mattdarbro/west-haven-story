import { Theme } from './types';

export const tfogwfTheme: Theme = {
  name: 'tfogwf',
  displayName: 'The Forgotten One Who Fell',
  description: 'A haunting theme inspired by fallen angels and forgotten realms',
  
  colors: {
    primary: ['#7c2d12', '#dc2626', '#ef4444', '#fca5a5'],
    secondary: ['#1e40af', '#3b82f6', '#60a5fa', '#93c5fd'],
    accent: ['#d97706', '#f59e0b', '#fbbf24', '#fde68a'],
    background: {
      primary: '#0c0a09',
      secondary: '#1c1917',
      tertiary: '#292524',
    },
    text: {
      primary: '#f5f5f4',
      secondary: '#a8a29e',
      muted: '#78716c',
    },
    border: '#44403c',
    surface: '#292524',
  },
  
  typography: {
    heading: {
      font: 'Crimson Text, serif',
      weights: [400, 500, 600, 700],
    },
    body: {
      font: 'Source Sans Pro, sans-serif',
      weights: [300, 400, 500, 600],
    },
    fantasy: {
      font: 'Crimson Text, serif',
      weights: [400, 500, 600, 700],
    },
  },
  
  effects: {
    backgroundGradient: 'linear-gradient(135deg, #0c0a09 0%, #1c1917 50%, #292524 100%)',
    cardGradient: 'linear-gradient(135deg, rgba(220, 38, 38, 0.1) 0%, rgba(30, 64, 175, 0.1) 100%)',
    glowColor: '#dc2626',
    shadowColor: 'rgba(220, 38, 38, 0.4)',
  },
  
  atmosphere: {
    mood: 'haunting, tragic, ethereal, divine',
    keywords: ['fallen', 'angelic', 'tragic', 'ethereal', 'divine', 'forgotten'],
    visualStyle: 'ethereal, soft glows, divine light, tragic beauty',
  },
};
