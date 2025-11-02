import { StoryResponse, StartStoryRequest, ContinueStoryRequest } from '../types/story';

// Get API URL from environment variable, fallback to localhost for development
const API_BASE_URL = import.meta.env.VITE_API_URL 
  ? `${import.meta.env.VITE_API_URL}/api`
  : 'http://localhost:8000/api';

class ApiError extends Error {
  constructor(
    message: string,
    public status: number,
    public statusText: string
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

async function fetchWithErrorHandling<T>(
  url: string,
  options: RequestInit = {}
): Promise<T> {
  try {
    const response = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new ApiError(
        errorData.detail || errorData.error || `HTTP ${response.status}`,
        response.status,
        response.statusText
      );
    }

    return await response.json();
  } catch (error) {
    if (error instanceof ApiError) {
      throw error;
    }
    
    // Network or other errors
    throw new ApiError(
      'Network error - please check your connection',
      0,
      'Network Error'
    );
  }
}

export const api = {
  /**
   * Start a new story session
   */
  async startStory(request: StartStoryRequest): Promise<StoryResponse> {
    return fetchWithErrorHandling<StoryResponse>(
      `${API_BASE_URL}/story/start`,
      {
        method: 'POST',
        body: JSON.stringify(request),
      }
    );
  },

  /**
   * Continue the story with a player choice
   */
  async continueStory(request: ContinueStoryRequest): Promise<StoryResponse> {
    return fetchWithErrorHandling<StoryResponse>(
      `${API_BASE_URL}/story/continue`,
      {
        method: 'POST',
        body: JSON.stringify(request),
      }
    );
  },

  /**
   * Get current session state
   */
  async getSession(sessionId: string): Promise<StoryResponse> {
    return fetchWithErrorHandling<StoryResponse>(
      `${API_BASE_URL}/story/session/${sessionId}`
    );
  },

  /**
   * List available story worlds
   */
  async listWorlds(): Promise<string[]> {
    return fetchWithErrorHandling<string[]>(`${API_BASE_URL}/worlds`);
  },

  /**
   * Health check
   */
  async healthCheck(): Promise<{ status: string; config: any }> {
    return fetchWithErrorHandling<{ status: string; config: any }>(
      `${API_BASE_URL.replace('/api', '')}/health`
    );
  }
};

export { ApiError };
