# Tool Handoff Documentation

## Current Phase: Phase 0-1 (Claude Code)
**Status**: Foundation setup in progress
**Last Updated**: 2025-10-24

## Completed Tasks
- [x] Project directory structure created
- [x] README with architecture overview
- [ ] Virtual environment setup
- [ ] Core dependencies installed
- [ ] RAG pipeline implementation
- [ ] LangGraph state machine
- [ ] FastAPI endpoints

## Architecture Decisions Made

### 1. State Management
- **Decision**: Use LangGraph with SQLite checkpointing
- **Rationale**: Built-in persistence, perfect for stateful conversations
- **Impact**: All story sessions auto-save, easy resume capability

### 2. RAG Strategy
- **Decision**: MMR (Maximum Marginal Relevance) retrieval with k=6, fetch_k=20
- **Rationale**: Balances relevance with diversity for richer context
- **Impact**: Better narrative variety while maintaining consistency

### 3. Story Beat Structure
- **Decision**: Beat-based progression with explicit success criteria
- **Rationale**: Provides clear narrative structure and progression tracking
- **Impact**: Easier to measure player progress and story completion

### 4. Metadata Architecture
- **Decision**: Enrich all vector store documents with world_id and source metadata
- **Rationale**: Enables multi-world support from day 1
- **Impact**: Can filter retrievals by world, scales easily

## Critical Files to Understand (When Implemented)

### Backend Core
- `backend/models/state.py` - StoryState TypedDict (central to everything)
- `backend/config.py` - Single source of truth for configuration
- `backend/storyteller/graph.py` - LangGraph workflow definition
- `backend/storyteller/nodes.py` - Individual processing functions
- `backend/story_bible/rag.py` - RAG implementation with ChromaDB

### Story Content
- `bibles/tfogwf.md` - The Forgotten One Who Fell story bible
- `bibles/template.md` - Template for new story worlds

## Implementation Notes

### LangGraph Node Structure
The storyteller graph has 7 nodes:
1. `retrieve_context` - RAG retrieval from story bible
2. `generate_narrative` - LLM generates story segment
3. `parse_output` - Extract choices and metadata from JSON
4. `generate_image` - Create scene image (Replicate)
5. `generate_audio` - Create voice narration (ElevenLabs)
6. `check_beat_complete` - Evaluate beat progression
7. `deduct_credits` - Handle credit system

### Conditional Edges
- After `parse_output`: Check credits → generate media or skip
- After `check_beat_complete`: Advance beat or continue current

### State Flow
```
Entry → retrieve_context → generate_narrative → parse_output
                                                      ↓
                                        [has credits?]
                                         ↓           ↓
                              generate_image    check_beat_complete
                                         ↓           ↓
                              generate_audio  [beat done?]
                                         ↓           ↓
                              check_beat_complete  deduct_credits → END
```

## Known Limitations (Current Phase)

### Phase 0-1 Scope
- No frontend yet (using curl/Postman for testing)
- No streaming (basic request/response)
- Media generation may be stubbed initially (focus on text flow)
- Single world only (TFOGWF)

## Next Phase Handoff: Claude Code → Cursor

### When to Transition
Transition to Cursor when:
- [ ] Backend endpoints work in Postman
- [ ] All tests pass (`pytest backend/tests/`)
- [ ] Type checking passes (`mypy backend/`)
- [ ] Can generate complete story beat end-to-end
- [ ] Documentation is complete

### What Cursor Should Build
1. React + TypeScript frontend
2. SSE streaming implementation
3. Real-time UI components (StoryViewer, ChoicePanel)
4. Custom hooks (useStoryStream)
5. Tailwind CSS styling

### Handoff Checklist
- [ ] Update this file with final backend status
- [ ] Create PROJECT_STATE.md with current metrics
- [ ] Push all code to Git with semantic commits
- [ ] Create `tests/manual_tests.http` with example API calls
- [ ] Document any backend quirks or workarounds
- [ ] Run full test suite and document results

## API Contract (For Frontend)

### Endpoints (Planned)
```
POST /story/start
- Body: {"world_id": "tfogwf", "user_id": "string"}
- Returns: {"session_id": "uuid", "narrative": "string", "choices": [...]}

POST /story/continue
- Body: {"session_id": "uuid", "choice_id": number}
- Returns: {"narrative": "string", "choices": [...], "image_url": "string", "audio_url": "string"}

GET /story/session/{session_id}
- Returns: Current story state
```

## Environment Variables Required
```
OPENAI_API_KEY=sk-...
REPLICATE_API_TOKEN=r8-...         # Optional for MVP
ELEVENLABS_API_KEY=...             # Optional for MVP
DATABASE_URL=sqlite:///./story.db  # For checkpointing
```

## Debugging Tips

### Testing RAG Retrieval
```bash
python scripts/test_retrieval.py --world tfogwf --query "Tell me about Elena"
```

### Visualizing LangGraph
```python
from storyteller.graph import create_storyteller_graph
graph = create_storyteller_graph("tfogwf")
graph.get_graph().draw_mermaid_png(output_file_path="graph.png")
```

### Checking State Persistence
```python
from langgraph.checkpoint.sqlite import SqliteSaver
memory = SqliteSaver.from_conn_string("story.db")
checkpoints = memory.list(config={"thread_id": "test-session"})
```

## Questions for Next Developer/Phase

1. Should we implement rate limiting on endpoints?
2. What's the ideal streaming chunk size for narrative text?
3. Do we want image generation to be blocking or async with polling?
4. Should beat progression be automatic or require explicit confirmation?

## Resources
- [LangGraph Docs](https://langchain-ai.github.io/langgraph/)
- [FastAPI Streaming](https://fastapi.tiangolo.com/advanced/custom-response/#streamingresponse)
- [LangSmith Tracing](https://docs.smith.langchain.com/)
