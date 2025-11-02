export interface Choice {
  id: number;
  text: string;
  consequence_hint: string;
}

export interface StoryResponse {
  session_id: string;
  narrative: string;
  choices: Choice[];
  current_beat: number;
  credits_remaining: number;
  image_url?: string;
  audio_url?: string;
}

export interface StartStoryRequest {
  world_id: string;
  user_id?: string;
}

export interface ContinueStoryRequest {
  session_id: string;
  choice_id: number;
}

export interface StoryState {
  sessionId: string | null;
  narrative: string;
  choices: Choice[];
  currentBeat: number;
  creditsRemaining: number;
  isLoading: boolean;
  error: string | null;
  imageUrl?: string;
  audioUrl?: string;
}
