# Deployment Guide - West Haven Storyteller

## Current vs Production Architecture

### Development (What You're Running Now)
```
┌─────────────┐     ┌─────────────┐
│  Frontend   │────▶│   Backend   │
│  (Vite)     │     │  (FastAPI)  │
│ :3000       │     │    :8000    │
└─────────────┘     └─────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        ▼                  ▼                  ▼
   ┌────────┐      ┌──────────┐      ┌──────────┐
   │ SQLite │      │ ChromaDB │      │  Local   │
   │  .db   │      │  (files) │      │  Files   │
   └────────┘      └──────────┘      └──────────┘
```

**Issues:**
- SQLite doesn't work well on serverless platforms
- Local files disappear on restart (ephemeral filesystem)
- ChromaDB files aren't persistent
- No way to start "all servers" - they're separate processes

### Production Architecture (Recommended)

```
┌─────────────┐     ┌─────────────┐     ┌──────────────┐
│   Vercel    │────▶│   Railway   │────▶│   Supabase   │
│  (Frontend) │     │  (Backend)  │     │ (PostgreSQL) │
│   Static    │     │   Python    │     └──────────────┘
└─────────────┘     └─────────────┘
                           │
                ┌──────────┼──────────┐
                ▼                     ▼
         ┌──────────┐         ┌──────────────┐
         │ ChromaDB │         │   Supabase   │
         │  Cloud   │         │   Storage    │
         │   or     │         │ (Images/     │
         │ Embedded │         │  Audio)      │
         └──────────┘         └──────────────┘
```

---

## Step-by-Step Deployment

### Phase 1: Prepare Code for Production

#### 1.1 Update Database Configuration

Replace SQLite with PostgreSQL in `backend/config.py`:

```python
# Add to .env
DATABASE_URL=postgresql://user:password@host:5432/dbname  # From Supabase

# Update config.py to handle both SQLite (dev) and PostgreSQL (prod)
DATABASE_URL: str = Field(
    default="sqlite:///./story.db",
    description="Database URL for session persistence"
)
```

#### 1.2 Update Media Storage

Create `backend/storage.py`:
```python
"""
Media storage abstraction layer.
Supports local (dev) and Supabase Storage (prod).
"""
import os
from supabase import create_client

def upload_image(file_path: str, filename: str) -> str:
    """Upload image to Supabase Storage or local."""
    if os.getenv("ENVIRONMENT") == "production":
        # Upload to Supabase Storage
        supabase = create_client(
            os.getenv("SUPABASE_URL"),
            os.getenv("SUPABASE_KEY")
        )
        with open(file_path, "rb") as f:
            supabase.storage.from_("images").upload(filename, f)
        return f"{os.getenv('SUPABASE_URL')}/storage/v1/object/public/images/{filename}"
    else:
        # Local development
        return f"/images/{filename}"
```

#### 1.3 Add Production Dependencies

Update `requirements.txt`:
```txt
# ... existing dependencies ...

# Production database
psycopg2-binary>=2.9.9
supabase>=2.0.0

# Production server
gunicorn>=21.2.0
```

#### 1.4 Create Production Config Files

**`.env.example`** (for documentation):
```bash
# Development
ENVIRONMENT=development

# Production
# ENVIRONMENT=production
# SUPABASE_URL=https://xxx.supabase.co
# SUPABASE_KEY=your-key
# DATABASE_URL=postgresql://...

# API Keys (both dev and prod)
OPENAI_API_KEY=sk-...
REPLICATE_API_TOKEN=r8_...
ELEVENLABS_API_KEY=sk_...
```

**`Procfile`** (for Railway/Render):
```
web: gunicorn backend.api.main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
```

**`railway.toml`** (for Railway):
```toml
[build]
builder = "nixpacks"

[deploy]
startCommand = "gunicorn backend.api.main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT"
healthcheckPath = "/health"
```

---

### Phase 2: Deploy Backend (Railway - Recommended)

#### 2.1 Setup Railway

1. **Create Railway account**: https://railway.app
2. **Create new project**: "West Haven Backend"
3. **Deploy from GitHub**:
   ```bash
   # First, push to GitHub
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/west-haven.git
   git push -u origin main
   ```

4. **Connect Railway to GitHub repo**
5. **Set environment variables in Railway**:
   ```
   ENVIRONMENT=production
   OPENAI_API_KEY=sk-...
   REPLICATE_API_TOKEN=r8_...
   ELEVENLABS_API_KEY=sk_...
   DATABASE_URL=postgresql://... (from Supabase)
   SUPABASE_URL=https://xxx.supabase.co
   SUPABASE_KEY=your-anon-key
   ```

6. **Deploy**: Railway auto-deploys on push to main

**Alternative: Render**
- Free tier available (slower cold starts)
- Similar process to Railway
- Uses `render.yaml` config file

---

### Phase 3: Deploy Database (Supabase)

#### 3.1 Create Supabase Project

1. **Sign up**: https://supabase.com
2. **Create project**: "West Haven"
3. **Get credentials**:
   - Project URL: `https://xxx.supabase.co`
   - Anon Key: `eyJ...` (for client)
   - Service Role Key: `eyJ...` (for backend)
   - Database URL: `postgresql://postgres:[password]@db.xxx.supabase.co:5432/postgres`

#### 3.2 Setup Storage Buckets

In Supabase Dashboard:
1. **Go to Storage**
2. **Create buckets**:
   - `images` (public)
   - `audio` (public)
3. **Set policies** (public read):
   ```sql
   -- Allow public read access
   CREATE POLICY "Public Access" ON storage.objects FOR SELECT USING (bucket_id = 'images');
   CREATE POLICY "Public Access" ON storage.objects FOR SELECT USING (bucket_id = 'audio');
   ```

#### 3.3 Initialize Database Schema

Create migration file `backend/migrations/001_initial.sql`:
```sql
-- Story sessions table
CREATE TABLE IF NOT EXISTS story_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id VARCHAR(255) NOT NULL,
    world_id VARCHAR(50) NOT NULL,
    current_beat INTEGER NOT NULL DEFAULT 1,
    credits_remaining INTEGER NOT NULL DEFAULT 25,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Story state checkpoints (for LangGraph)
CREATE TABLE IF NOT EXISTS story_checkpoints (
    session_id UUID REFERENCES story_sessions(id),
    checkpoint_data JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
```

Run via Supabase SQL Editor or use Alembic migrations.

---

### Phase 4: Deploy Frontend (Vercel)

#### 4.1 Update Frontend Config

Update `frontend/src/config.ts`:
```typescript
export const API_URL = import.meta.env.PROD
  ? 'https://your-backend.railway.app'
  : 'http://localhost:8000';
```

#### 4.2 Deploy to Vercel

1. **Create Vercel account**: https://vercel.com
2. **Import GitHub repo**
3. **Configure**:
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
4. **Environment Variables**:
   ```
   VITE_API_URL=https://your-backend.railway.app
   ```
5. **Deploy**: Auto-deploys on push to main

---

### Phase 5: Setup ChromaDB

**Option A: Keep Embedded (Simpler)**
- ChromaDB runs inside your Railway backend
- Files persist in Railway's volume storage
- Add to `railway.toml`:
  ```toml
  [deploy]
  volumeMounts = [
    { mountPath = "/app/chroma_db", name = "chroma-data" }
  ]
  ```

**Option B: ChromaDB Cloud (Scalable)**
- Sign up: https://www.trychroma.com/cloud
- Get API key and endpoint
- Update RAG code to use remote client:
  ```python
  import chromadb
  client = chromadb.HttpClient(
      host=os.getenv("CHROMA_HOST"),
      api_key=os.getenv("CHROMA_API_KEY")
  )
  ```

---

## Running Locally (Development)

You don't "start all servers" together - they're separate:

### Terminal 1: Backend
```bash
cd /Users/mattdarbro/Desktop/Story
source venv/bin/activate
PYTHONPATH=/Users/mattdarbro/Desktop/Story python backend/api/main.py
```

### Terminal 2: Frontend
```bash
cd frontend
npm run dev
```

**Or use a process manager:**

Install **Foreman** or **Honcho**:
```bash
pip install honcho
```

Create `Procfile.dev`:
```
backend: PYTHONPATH=$PWD python backend/api/main.py
frontend: cd frontend && npm run dev
```

Run both:
```bash
honcho start -f Procfile.dev
```

---

## Production Deployment Flow

### One-Time Setup
1. ✅ Create Supabase project → Get DATABASE_URL
2. ✅ Create Railway project → Connect GitHub
3. ✅ Create Vercel project → Connect GitHub
4. ✅ Set environment variables in Railway/Vercel
5. ✅ Create Supabase Storage buckets

### Ongoing Updates
```bash
# 1. Make changes locally
git add .
git commit -m "Add new feature"
git push origin main

# 2. Automatic deployments happen
# - Railway auto-deploys backend
# - Vercel auto-deploys frontend

# 3. Check deployments
# Railway: https://railway.app/project/xxx
# Vercel: https://vercel.com/dashboard
```

**No manual server starting in production!** ✨

---

## Environment Variables Summary

### Backend (Railway)
```bash
ENVIRONMENT=production
DATABASE_URL=postgresql://...
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=eyJ...
OPENAI_API_KEY=sk-...
REPLICATE_API_TOKEN=r8_...
ELEVENLABS_API_KEY=sk_...
IMAGE_MODEL=stability-ai/sdxl:7762fd07...
```

### Frontend (Vercel)
```bash
VITE_API_URL=https://your-backend.railway.app
```

---

## Cost Estimates (Monthly)

| Service | Plan | Cost |
|---------|------|------|
| Vercel | Hobby | **Free** |
| Railway | Hobby | **$5** |
| Supabase | Free | **Free** (2GB storage, 500MB database) |
| ChromaDB Cloud | Starter | **$0-29** (optional) |
| OpenAI API | Pay-as-go | **~$10-50** (depends on usage) |
| Replicate | Pay-as-go | **~$5-20** (depends on image gen) |
| ElevenLabs | Creator | **$22** (30k chars/month) |

**Total: ~$42-96/month** (mostly API costs)

---

## Quick Deploy Commands

```bash
# 1. Initialize git (if not done)
git init
git add .
git commit -m "Initial commit"

# 2. Push to GitHub
gh repo create west-haven-story --public --source=. --remote=origin
git push -u origin main

# 3. Deploy backend (Railway CLI)
railway login
railway init
railway up

# 4. Deploy frontend (Vercel CLI)
cd frontend
vercel login
vercel --prod

# Done! 🎉
```

---

## Troubleshooting

### "Module not found" errors
- Make sure `PYTHONPATH` is set correctly
- Railway: automatic
- Render: add to `render.yaml`

### Database connection errors
- Check DATABASE_URL format
- Ensure Supabase allows connections from Railway IP

### Image/Audio not saving
- Check Supabase Storage buckets exist
- Verify storage policies allow uploads
- Check SUPABASE_KEY has correct permissions

### ChromaDB not persisting
- Railway: Add volume mount
- Check write permissions

---

## Next Steps

1. ✅ Review this guide
2. Create GitHub repository
3. Set up Supabase project
4. Deploy backend to Railway
5. Deploy frontend to Vercel
6. Test production deployment
7. Monitor costs and performance

Need help with any specific step? Let me know!
