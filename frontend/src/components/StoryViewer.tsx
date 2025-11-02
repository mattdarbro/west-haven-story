import { StoryState, Choice } from '../types/story';
import { NarrativeCard } from './NarrativeCard';
import { ChoicePanel } from './ChoicePanel';
import { LoadingState } from './LoadingState';
import { ErrorState } from './ErrorState';

interface StoryViewerProps {
  state: StoryState & {
    isStreaming?: boolean;
    streamError?: string | null;
  };
  onChoiceSelect: (choice: Choice) => void;
  onRetry: () => void;
  onReset: () => void;
}

export function StoryViewer({ 
  state, 
  onChoiceSelect, 
  onRetry, 
  onReset 
}: StoryViewerProps) {
  // Show loading state
  if (state.isLoading || state.isStreaming) {
    return <LoadingState message={state.isStreaming ? "Streaming story..." : "The story unfolds..."} />;
  }

  // Show error state
  if (state.error) {
    return (
      <ErrorState 
        error={state.error}
        onRetry={onRetry}
        onReset={onReset}
      />
    );
  }

  // Show empty state (no story started)
  if (!state.sessionId || !state.narrative) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[400px] p-8">
        <div className="text-center">
          <div className="w-16 h-16 mx-auto mb-4 opacity-50">
            <svg fill="currentColor" viewBox="0 0 24 24" className="w-full h-full text-primary-400">
              <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
            </svg>
          </div>
          <h3 className="text-lg font-fantasy text-primary-300 mb-2">
            Begin Your Journey
          </h3>
          <p className="text-sm text-dark-400 mb-6">
            Start a new story to begin your adventure
          </p>
          <button
            onClick={onRetry}
            className="px-6 py-3 bg-gradient-to-r from-primary-600 to-primary-700 hover:from-primary-700 hover:to-primary-800 text-white rounded-lg font-medium transition-all duration-200 shadow-lg hover:shadow-xl"
          >
            Start Story
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Story narrative */}
      <NarrativeCard
        narrative={state.narrative}
        currentBeat={state.currentBeat}
        imageUrl={state.imageUrl}
        audioUrl={state.audioUrl}
        isGeneratingAudio={state.isLoading && !state.audioUrl}
        isGeneratingImage={state.isLoading && !state.imageUrl}
        className="animate-fade-in"
      />
      
      {/* Player choices */}
      {state.choices.length > 0 && (
        <div className="animate-slide-up">
          <ChoicePanel
            choices={state.choices}
            onChoiceSelect={onChoiceSelect}
            disabled={state.creditsRemaining <= 0}
          />
        </div>
      )}
    </div>
  );
}
