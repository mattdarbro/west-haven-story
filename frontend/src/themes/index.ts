import { Theme } from './types';
import { defaultTheme } from './default';
import { tfogwfTheme } from './tfogwf';

export const themes: Record<string, Theme> = {
  default: defaultTheme,
  tfogwf: tfogwfTheme,
};

export const getTheme = (themeName: string): Theme => {
  return themes[themeName] || themes.default;
};

export const getAvailableThemes = (): Theme[] => {
  return Object.values(themes);
};

export const getThemeByWorldId = (worldId: string): Theme => {
  // Map world IDs to themes
  const worldThemeMap: Record<string, string> = {
    'tfogwf': 'tfogwf',
    'default': 'default',
  };
  
  const themeName = worldThemeMap[worldId] || 'default';
  return getTheme(themeName);
};

export { defaultTheme, tfogwfTheme };
export type { Theme } from './types';
