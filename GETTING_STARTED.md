# Getting Started with Storyteller

This guide will help you get the Storyteller app running on your local machine.

## Prerequisites

- Python 3.11+ installed
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))
- Terminal/command line access

## Quick Start (5 minutes)

### Step 1: Set up your API key

1. Open `.env` file in the project root
2. Replace `your-openai-api-key-here` with your actual OpenAI API key:
   ```
   OPENAI_API_KEY=sk-proj-...your-key-here...
   ```

### Step 2: Activate virtual environment

```bash
# From the project root directory
source venv/bin/activate
```

You should see `(venv)` appear in your terminal prompt.

### Step 3: Initialize the story bible

```bash
python scripts/init_rag.py tfogwf
```

Expected output:
```
Initializing RAG for world: tfogwf
✓ Indexed 45 document chunks for world 'tfogwf'

Collection Stats:
  world_id: tfogwf
  document_count: 45
  ...
```

### Step 4: Test the system

```bash
python scripts/test_story_flow.py
```

This will:
- ✓ Initialize RAG
- ✓ Create the state machine
- ✓ Generate an opening narrative
- ✓ Process a player choice
- ✓ Continue the story

**Expected time**: 10-15 seconds (first run may take longer)

If you see "✓ ALL TESTS PASSED!" - you're ready to go!

### Step 5: Start the API server

```bash
# Option 1: Using the run script (easiest)
./run_api.sh

# Option 2: Manual (if script doesn't work)
source venv/bin/activate
export PYTHONPATH=/Users/mattdarbro/Desktop/Story
python backend/api/main.py
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

## Testing the API

### Option 1: Using the interactive docs

1. Open http://localhost:8000/docs in your browser
2. Click on `POST /api/story/start`
3. Click "Try it out"
4. Click "Execute"
5. You'll see the opening narrative and choices!

### Option 2: Using curl

**Start a story:**
```bash
curl -X POST http://localhost:8000/api/story/start \
  -H "Content-Type: application/json" \
  -d '{"world_id": "tfogwf"}'
```

**Continue with a choice** (use the session_id from above):
```bash
curl -X POST http://localhost:8000/api/story/continue \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "your-session-id-here",
    "choice_id": 1
  }'
```

## Project Structure

```
storyteller-app/
├── backend/
│   ├── storyteller/      # LangGraph state machine
│   │   ├── graph.py     # Main workflow
│   │   ├── nodes.py     # Processing functions
│   │   └── prompts.py   # Dynamic prompts
│   ├── story_bible/     # RAG system
│   │   └── rag.py      # Vector retrieval
│   ├── api/            # FastAPI endpoints
│   │   ├── main.py    # App setup
│   │   └── routes.py  # Story routes
│   ├── models/        # Data models
│   │   └── state.py  # State definitions
│   └── config.py     # Configuration
├── bibles/           # Story content
│   └── tfogwf.md    # The Forgotten One Who Fell
└── scripts/         # Utility scripts
```

## Common Issues

### "ModuleNotFoundError"
**Solution**: Make sure you've activated the virtual environment:
```bash
source venv/bin/activate
```

### "OpenAI API key not set"
**Solution**: Update the `.env` file with your actual API key.

### "World 'tfogwf' not initialized"
**Solution**: Run the initialization script:
```bash
python scripts/init_rag.py tfogwf
```

### RAG indexing fails
**Solution**: Ensure the story bible exists:
```bash
ls bibles/tfogwf.md  # Should exist
```

## Configuration

All settings are in `backend/config.py` and can be overridden via `.env`:

### Key Settings

```env
# Model selection
MODEL_NAME=gpt-4-turbo-preview

# RAG configuration
RAG_SEARCH_TYPE=mmr          # or "similarity"
RAG_RETRIEVAL_K=6           # Number of docs to retrieve

# Feature toggles
ENABLE_MEDIA_GENERATION=false  # Set to true with Replicate/ElevenLabs keys
ENABLE_CREDIT_SYSTEM=false     # Enable in Phase 3
```

## What's Working

✅ **RAG System**: Story bible retrieval with ChromaDB
✅ **LangGraph**: 7-node state machine for story flow
✅ **Narrative Generation**: GPT-4 powered storytelling
✅ **Choice System**: Branching narrative based on player input
✅ **Session Persistence**: SQLite checkpointing
✅ **FastAPI Endpoints**: REST API for story interaction
✅ **Beat Progression**: 3-beat story structure

## What's Not Implemented Yet

⏳ **Streaming**: Real-time narrative generation (Phase 2)
⏳ **Frontend**: React UI (Phase 2)
⏳ **Media Generation**: Images and audio (optional)
⏳ **Credit System**: Payment/usage tracking (Phase 3)
⏳ **Authentication**: User accounts (Phase 3)

## Next Steps

### For Testing
1. Test all API endpoints with Postman or curl
2. Try completing all 3 beats of TFOGWF
3. Test error handling (invalid session, bad choices)

### For Development
1. Enable LangSmith tracing for debugging
2. Add more story beats to TFOGWF
3. Create a second story world
4. Implement streaming endpoints (Phase 2)
5. Build React frontend (Phase 2)

### For Production
1. Add proper authentication
2. Use PostgreSQL instead of SQLite
3. Deploy to cloud (Railway, Render, or Fly.io)
4. Add rate limiting
5. Set up monitoring

## Development Workflow

### Making Changes

```bash
# 1. Make code changes
# 2. Restart the server (if it's running)
#    Ctrl+C then python backend/api/main.py
# 3. Test changes
```

The server runs with auto-reload in debug mode, so most changes will be picked up automatically.

### Adding a New Story World

1. Create `bibles/newworld.md` following the TFOGWF structure
2. Run `python scripts/init_rag.py newworld`
3. Test: `POST /api/story/start` with `{"world_id": "newworld"}`

### Debugging

**Enable LangSmith tracing** (optional but recommended):
1. Get API key from https://smith.langchain.com
2. Add to `.env`:
   ```env
   LANGCHAIN_TRACING_V2=true
   LANGCHAIN_API_KEY=ls-your-key-here
   ```
3. View traces at https://smith.langchain.com

**View logs**:
```bash
# Check logs for errors
tail -f logs/storyteller.log  # (if logging is set up)
```

**Database inspection**:
```bash
# View checkpoints
sqlite3 story_checkpoints.db
> SELECT * FROM checkpoints;
```

## Cost Estimates

Per story session (3 beats, ~5 choices each):

- **GPT-4 Turbo**: ~$0.15 (narrative generation)
- **Embeddings**: <$0.01 (one-time indexing)
- **Total**: ~$0.15 per complete playthrough

Tips to reduce costs:
- Use `gpt-3.5-turbo` instead (change `MODEL_NAME` in config)
- Reduce `MAX_TOKENS` for shorter narratives
- Cache common queries

## Support

- **Documentation**: See README.md, HANDOFF.md
- **Issues**: Check error messages in terminal
- **API Docs**: http://localhost:8000/docs when server is running

## Ready to Build?

The backend is complete and functional. You can now:

1. **Test thoroughly** with the current setup
2. **Add more story content** (beats, worlds)
3. **Move to Phase 2**: Build the React frontend with Cursor
4. **Deploy**: Get this running in production

Happy storytelling! 🎭
