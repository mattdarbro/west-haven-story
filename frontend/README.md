# Storyteller Frontend

A beautiful, mobile-first React frontend for the Storyteller interactive narrative platform.

## Features

- 🎭 **Dark Fantasy Design** - Immersive UI with magical theming
- 📱 **Mobile-First** - Optimized for mobile devices
- ⚡ **Real-time Story** - Connect to backend API for live storytelling
- 🎨 **Smooth Animations** - Delightful micro-interactions
- ♿ **Accessible** - Screen reader friendly with keyboard navigation

## Tech Stack

- **React 18** with TypeScript
- **Vite** for fast development
- **Tailwind CSS** for styling
- **Custom Design System** with dark fantasy theme

## Getting Started

### Prerequisites

- Node.js 18+ 
- Backend API running on `http://localhost:8000`

### Installation

```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

The app will be available at `http://localhost:3000`

### Building for Production

```bash
# Build the app
npm run build

# Preview production build
npm run preview
```

## Project Structure

```
src/
├── components/          # React components
│   ├── StoryViewer.tsx  # Main story interface
│   ├── NarrativeCard.tsx # Story text display
│   ├── ChoicePanel.tsx  # Player choices
│   ├── LoadingState.tsx # Loading animations
│   └── ErrorState.tsx   # Error handling
├── hooks/              # Custom React hooks
│   └── useStory.ts     # Story state management
├── services/           # API client
│   └── api.ts          # Backend integration
├── types/              # TypeScript types
│   └── story.ts        # Story data models
├── styles/             # Design system
│   └── design-system.ts # Theme tokens
├── App.tsx             # Main app component
└── main.tsx             # Entry point
```

## Design System

The app uses a custom dark fantasy design system with:

- **Colors**: Deep purples, blues, and amber accents
- **Typography**: Cinzel for headings, Inter for body text
- **Animations**: Fade-in, slide-up, and magical glow effects
- **Components**: Cards, buttons, and interactive elements

## API Integration

The frontend connects to the backend API with:

- **Start Story**: `POST /api/story/start`
- **Continue Story**: `POST /api/story/continue`
- **Session Management**: Automatic localStorage persistence
- **Error Handling**: User-friendly error messages

## Mobile Optimization

- Touch-friendly 44px minimum touch targets
- Responsive typography scaling
- Optimized for portrait and landscape
- Smooth scrolling and animations

## Development

### Code Style

- TypeScript with strict mode
- ESLint for code quality
- Prettier for formatting
- Component-based architecture

### Adding Features

1. Create components in `src/components/`
2. Add types in `src/types/`
3. Update API client in `src/services/`
4. Test on mobile devices

## Future Enhancements

- [ ] SSE streaming for real-time text
- [ ] Image and audio media players
- [ ] Multiple story world support
- [ ] User authentication
- [ ] Offline story caching
