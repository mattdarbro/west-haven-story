import { useState, useCallback, useEffect } from 'react';
import { StoryState, Choice } from '../types/story';
import { api, ApiError } from '../services/api';
import { useStoryStream } from './useStoryStream';

const STORAGE_KEY = 'storyteller_session';

export function useStory() {
  const [state, setState] = useState<StoryState>({
    sessionId: null,
    narrative: '',
    choices: [],
    currentBeat: 1,
    creditsRemaining: 0,
    isLoading: false,
    error: null,
    imageUrl: undefined,
    audioUrl: undefined,
  });

  const { startStream, isStreaming, streamError } = useStoryStream();

  // Load session from localStorage on mount
  useEffect(() => {
    const savedSessionId = localStorage.getItem(STORAGE_KEY);
    if (savedSessionId) {
      setState(prev => ({ ...prev, sessionId: savedSessionId }));
    }
  }, []);

  const startStory = useCallback(async (worldId: string = 'tfogwf') => {
    setState(prev => ({ ...prev, isLoading: true, error: null }));
    
    try {
      const response = await api.startStory({ world_id: worldId });
      
      // Save session to localStorage
      localStorage.setItem(STORAGE_KEY, response.session_id);
      
      setState({
        sessionId: response.session_id,
        narrative: response.narrative,
        choices: response.choices,
        currentBeat: response.current_beat,
        creditsRemaining: response.credits_remaining,
        isLoading: false,
        error: null,
        imageUrl: response.image_url,
        audioUrl: response.audio_url,
      });
    } catch (error) {
      const errorMessage = error instanceof ApiError 
        ? error.message 
        : 'Failed to start story. Please try again.';
      
      setState(prev => ({
        ...prev,
        isLoading: false,
        error: errorMessage,
      }));
    }
  }, []);

  const continueStory = useCallback(async (choice: Choice) => {
    if (!state.sessionId) {
      setState(prev => ({ 
        ...prev, 
        error: 'No active session. Please start a new story.' 
      }));
      return;
    }

    // Use streaming for story continuation
    await startStream(state.sessionId, choice.text, (updates) => {
      setState(prev => ({ ...prev, ...updates }));
    });
  }, [state.sessionId, startStream]);

  const clearError = useCallback(() => {
    setState(prev => ({ ...prev, error: null }));
  }, []);

  const resetStory = useCallback(() => {
    localStorage.removeItem(STORAGE_KEY);
    setState({
      sessionId: null,
      narrative: '',
      choices: [],
      currentBeat: 1,
      creditsRemaining: 0,
      isLoading: false,
      error: null,
    });
  }, []);

  return {
    ...state,
    isStreaming,
    streamError,
    startStory,
    continueStory,
    clearError,
    resetStory,
  };
}
