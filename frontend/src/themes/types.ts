export interface Theme {
  name: string;
  displayName: string;
  description: string;
  
  // Color palette
  colors: {
    primary: string[];
    secondary: string[];
    accent: string[];
    background: {
      primary: string;
      secondary: string;
      tertiary: string;
    };
    text: {
      primary: string;
      secondary: string;
      muted: string;
    };
    border: string;
    surface: string;
  };
  
  // Typography
  typography: {
    heading: {
      font: string;
      weights: number[];
    };
    body: {
      font: string;
      weights: number[];
    };
    fantasy: {
      font: string;
      weights: number[];
    };
  };
  
  // Visual effects
  effects: {
    backgroundGradient: string;
    cardGradient: string;
    glowColor: string;
    shadowColor: string;
  };
  
  // Atmosphere
  atmosphere: {
    mood: string;
    keywords: string[];
    visualStyle: string;
  };
}

export interface ThemeContextType {
  currentTheme: Theme;
  setTheme: (themeName: string) => void;
  availableThemes: Theme[];
}
