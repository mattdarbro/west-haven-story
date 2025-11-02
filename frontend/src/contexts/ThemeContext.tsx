import { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { Theme, ThemeContextType } from '../themes/types';
import { getTheme, getAvailableThemes, getThemeByWorldId } from '../themes';

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

interface ThemeProviderProps {
  children: ReactNode;
  worldId?: string;
}

export function ThemeProvider({ children, worldId }: ThemeProviderProps) {
  const [currentTheme, setCurrentTheme] = useState<Theme>(() => {
    // Initialize with world-specific theme or default
    return worldId ? getThemeByWorldId(worldId) : getTheme('default');
  });

  const availableThemes = getAvailableThemes();

  const setTheme = (themeName: string) => {
    const theme = getTheme(themeName);
    setCurrentTheme(theme);
    
    // Apply theme to CSS variables
    applyThemeToCSS(theme);
    
    // Save theme preference
    localStorage.setItem('storyteller_theme', themeName);
  };

  // Apply theme to CSS variables
  const applyThemeToCSS = (theme: Theme) => {
    const root = document.documentElement;
    
    // Apply color variables
    root.style.setProperty('--color-primary-500', theme.colors.primary[1]);
    root.style.setProperty('--color-primary-600', theme.colors.primary[0]);
    root.style.setProperty('--color-primary-700', theme.colors.primary[0]);
    root.style.setProperty('--color-primary-800', theme.colors.primary[0]);
    
    root.style.setProperty('--color-secondary-500', theme.colors.secondary[1]);
    root.style.setProperty('--color-accent-500', theme.colors.accent[1]);
    
    root.style.setProperty('--color-dark-900', theme.colors.background.primary);
    root.style.setProperty('--color-dark-800', theme.colors.background.secondary);
    root.style.setProperty('--color-dark-700', theme.colors.background.tertiary);
    root.style.setProperty('--color-dark-600', theme.colors.surface);
    
    root.style.setProperty('--color-dark-100', theme.colors.text.primary);
    root.style.setProperty('--color-dark-200', theme.colors.text.primary);
    root.style.setProperty('--color-dark-300', theme.colors.text.secondary);
    root.style.setProperty('--color-dark-400', theme.colors.text.muted);
    root.style.setProperty('--color-dark-500', theme.colors.text.muted);
    
    // Apply typography
    root.style.setProperty('--font-heading', theme.typography.heading.font);
    root.style.setProperty('--font-body', theme.typography.body.font);
    root.style.setProperty('--font-fantasy', theme.typography.fantasy.font);
    
    // Apply effects
    root.style.setProperty('--glow-color', theme.effects.glowColor);
    root.style.setProperty('--shadow-color', theme.effects.shadowColor);
  };

  // Load theme on mount
  useEffect(() => {
    const savedTheme = localStorage.getItem('storyteller_theme');
    const initialTheme = savedTheme ? getTheme(savedTheme) : getThemeByWorldId(worldId || 'default');
    
    setCurrentTheme(initialTheme);
    applyThemeToCSS(initialTheme);
  }, [worldId]);

  // Update theme when worldId changes
  useEffect(() => {
    if (worldId) {
      const worldTheme = getThemeByWorldId(worldId);
      setCurrentTheme(worldTheme);
      applyThemeToCSS(worldTheme);
    }
  }, [worldId]);

  const value: ThemeContextType = {
    currentTheme,
    setTheme,
    availableThemes,
  };

  return (
    <ThemeContext.Provider value={value}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme(): ThemeContextType {
  const context = useContext(ThemeContext);
  if (context === undefined) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
}
