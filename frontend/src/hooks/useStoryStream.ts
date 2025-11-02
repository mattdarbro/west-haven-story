import { useState, useCallback, useRef } from 'react';
import { StoryState } from '../types/story';
import { api } from '../services/api';

export function useStoryStream() {
  const [isStreaming, setIsStreaming] = useState(false);
  const [streamError, setStreamError] = useState<string | null>(null);
  const eventSourceRef = useRef<EventSource | null>(null);

  const startStream = useCallback(async (
    sessionId: string,
    choiceId: number,
    onUpdate: (state: Partial<StoryState>) => void
  ) => {
    if (isStreaming) {
      console.warn('Stream already in progress');
      return;
    }

    setIsStreaming(true);
    setStreamError(null);

    try {
      // For now, we'll use the regular API and simulate streaming
      // TODO: Implement proper SSE streaming when backend supports it
      const response = await api.continueStory({ session_id: sessionId, choice_id: choiceId });
      
      // Simulate streaming by updating state progressively
      onUpdate({ isLoading: true });
      
      // Simulate narrative streaming
      const words = response.narrative.split(' ');
      let currentText = '';
      
      for (let i = 0; i < words.length; i++) {
        currentText += words[i] + ' ';
        onUpdate({ 
          narrative: currentText.trim(),
          isLoading: i < words.length - 1
        });
        
        // Small delay to simulate streaming
        await new Promise(resolve => setTimeout(resolve, 50));
      }

      // Update with final state
      onUpdate({
        narrative: response.narrative,
        choices: response.choices,
        currentBeat: response.current_beat,
        creditsRemaining: response.credits_remaining,
        imageUrl: response.image_url,
        audioUrl: response.audio_url,
        isLoading: false,
        error: null,
      });

    } catch (error) {
      console.error('Streaming error:', error);
      setStreamError(error instanceof Error ? error.message : 'Streaming failed');
      onUpdate({ 
        isLoading: false, 
        error: error instanceof Error ? error.message : 'Streaming failed' 
      });
    } finally {
      setIsStreaming(false);
      if (eventSourceRef.current) {
        eventSourceRef.current.close();
        eventSourceRef.current = null;
      }
    }
  }, [isStreaming]);

  const stopStream = useCallback(() => {
    if (eventSourceRef.current) {
      eventSourceRef.current.close();
      eventSourceRef.current = null;
    }
    setIsStreaming(false);
  }, []);

  // Cleanup on unmount
  const cleanup = useCallback(() => {
    stopStream();
  }, [stopStream]);

  return {
    isStreaming,
    streamError,
    startStream,
    stopStream,
    cleanup,
  };
}
