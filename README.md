# Storyteller - AI-Powered Interactive Narratives

A LangGraph-based interactive storytelling platform that generates dynamic narratives with images and audio using RAG (Retrieval-Augmented Generation).

## Architecture Overview

### Tech Stack
- **Backend**: Python 3.11+, FastAPI, LangChain 0.1+, LangGraph
- **Vector DB**: ChromaDB for story bible embeddings
- **LLM**: OpenAI GPT-4 Turbo
- **Media Generation**:
  - Images: Replicate (Stable Diffusion XL)
  - Audio: ElevenLabs (voice narration)
- **State Management**: LangGraph with SQLite checkpointing
- **Frontend**: React 18+ with TypeScript (to be implemented in Phase 2)

### Project Structure

```
storyteller-app/
├── backend/                    # Core application logic
│   ├── storyteller/           # LangGraph state machine
│   │   ├── graph.py          # Main workflow definition
│   │   ├── nodes.py          # Individual processing nodes
│   │   └── prompts.py        # Dynamic prompt templates
│   ├── story_bible/          # RAG system
│   │   ├── rag.py           # RAG implementation
│   │   └── loader.py        # Story bible loader
│   ├── api/                 # FastAPI endpoints
│   │   ├── routes.py        # HTTP routes
│   │   └── streaming.py     # SSE implementation
│   ├── models/              # Data models
│   │   └── state.py        # Pydantic & TypedDict models
│   ├── config.py           # Application configuration
│   └── tests/              # Pytest tests
├── frontend/               # React UI (Phase 2)
├── bibles/                # Story content files
└── scripts/               # Utility scripts
```

## Key Features

1. **RAG-Powered Consistency**: Story bibles are embedded and retrieved to maintain narrative coherence
2. **LangGraph State Machine**: Proper state management for complex narrative flows
3. **Beat-Based Progression**: Stories advance through structured story beats
4. **Multi-Modal Output**: Text, images, and audio generated in parallel
5. **Session Persistence**: Save/load story progress automatically
6. **Streaming Responses**: Real-time narrative generation via SSE

## Development Phases

### Phase 0-1: Foundation (Current) - Weeks 1-2
- [x] Project structure
- [ ] RAG pipeline with ChromaDB
- [ ] LangGraph state machine (7 nodes)
- [ ] FastAPI basic endpoints
- [ ] Story bible for TFOGWF world

### Phase 2: Frontend & Streaming - Weeks 3-4
- [ ] React frontend with TypeScript
- [ ] SSE streaming implementation
- [ ] Real-time UI updates
- [ ] Media player components

### Phase 3: Advanced Features - Week 5+
- [ ] Credit system & authentication
- [ ] Multi-world support
- [ ] Parallel media generation
- [ ] Production deployment

## Getting Started

### Prerequisites
- Python 3.11+
- OpenAI API key
- (Optional) Replicate and ElevenLabs API keys for media generation

### Installation

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys
```

### Running the App

```bash
# Start the backend
cd backend
uvicorn api.main:app --reload

# API will be available at http://localhost:8000
# Docs at http://localhost:8000/docs
```

## Architecture Decisions

### Why LangGraph?
- Built-in state persistence and checkpointing
- Conditional edges perfect for choice-based branching
- Human-in-the-loop support for user choices
- Graph visualization for debugging

### Why RAG?
- Maintains consistency with established lore
- Enables dynamic story worlds without hardcoding
- Scales to multiple story worlds easily

### Why Streaming?
- Perceived performance is actual performance
- Better user experience with real-time generation
- Natural fit for token-by-token LLM output

## Development Tools
- **Primary**: Claude Code (architecture, complex logic)
- **Secondary**: Cursor (frontend, iterative refinement)
- **Tertiary**: GitHub Copilot (boilerplate, autocomplete)

## Contributing
This is currently a solo development project. See HANDOFF.md for tool transition notes.

## License
MIT (or your preferred license)
