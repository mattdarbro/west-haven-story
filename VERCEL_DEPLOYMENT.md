# Vercel Frontend Deployment Guide

## Quick Setup Steps

### 1. Get Your Railway Backend URL

From Railway dashboard:
- Go to your **Story** service
- Find your **Public Domain** (e.g., `your-app.railway.app`)
- Copy the full URL (including `https://`)

Example: `https://storyteller-production-abc123.railway.app`

---

### 2. Deploy to Vercel

#### Option A: Via Vercel Dashboard (Recommended)

1. **Sign up/Login**: Go to https://vercel.com
2. **Import Project**:
   - Click "Add New" → "Project"
   - Import from GitHub
   - Select your `Story` repository
3. **Configure Project**:
   - **Framework Preset**: `Vite`
   - **Root Directory**: `frontend` (click "Edit" and set to `frontend`)
   - **Build Command**: `npm run build` (should auto-detect)
   - **Output Directory**: `dist` (should auto-detect)
4. **Environment Variables**:
   - Add: `VITE_API_URL` = `https://your-backend.railway.app`
     - ⚠️ **Important**: Use your actual Railway URL (no trailing slash)
     - Example: `https://storyteller-production-abc123.railway.app`
5. **Deploy**: Click "Deploy"

#### Option B: Via Vercel CLI

```bash
cd frontend
npm install -g vercel
vercel login
vercel

# When prompted:
# - Set up and deploy? Yes
# - Which scope? (your account)
# - Link to existing project? No
# - Project name: storyteller-frontend
# - Directory: ./
# - Override settings? No

# Set environment variable:
vercel env add VITE_API_URL
# Enter value: https://your-backend.railway.app
# Select: Production, Preview, Development

# Deploy to production:
vercel --prod
```

---

### 3. Verify Deployment

1. **Check Vercel Dashboard**: Should show "Ready" status
2. **Visit Your Site**: Click the deployment URL (e.g., `your-app.vercel.app`)
3. **Test the App**: 
   - Try starting a story
   - Check browser console for errors
   - Verify API calls are going to Railway backend

---

### 4. Update CORS in Railway (If Needed)

If you get CORS errors, make sure Railway backend allows your Vercel domain:

In Railway → Your Service → Variables:
- Currently set to `allow_origins=["*"]` which should work
- If issues persist, we can configure specific origins

---

## Environment Variables Summary

### Vercel Environment Variables

| Variable | Value | Example |
|----------|-------|---------|
| `VITE_API_URL` | Your Railway backend URL | `https://storyteller-abc123.railway.app` |

⚠️ **Important Notes**:
- Must start with `https://` (Railway provides HTTPS)
- No trailing slash
- No `/api` suffix (code adds it automatically)
- Available in Vercel Dashboard → Your Project → Settings → Environment Variables

---

## Troubleshooting

### "Network Error" or CORS Issues

**Check:**
1. `VITE_API_URL` is set correctly in Vercel
2. Railway backend is running (check Railway dashboard)
3. Railway backend URL is correct (should be `https://...`)
4. Browser console for specific error messages

**Fix:**
- Verify Railway URL: `https://your-app.railway.app/health` should return `{"status":"healthy"}`
- Rebuild Vercel deployment after changing `VITE_API_URL`

### Frontend Shows But API Calls Fail

**Check:**
1. Browser DevTools → Network tab
2. See what URL it's trying to call
3. Verify it's calling your Railway URL, not localhost

**Common Issues:**
- `VITE_API_URL` not set → defaults to localhost
- Wrong URL format → should be `https://...` not `http://...`
- CORS blocking → check Railway logs

### Build Fails

**Check:**
1. Root directory is set to `frontend` in Vercel
2. Build command: `npm run build`
3. Output directory: `dist`
4. Node version (should be 18+)

---

## After Deployment

Once deployed, your frontend will:
- ✅ Auto-deploy on every push to `main`
- ✅ Use Railway backend for API calls
- ✅ Work with your West Haven story world

**Your Live URLs:**
- **Frontend**: `https://your-app.vercel.app`
- **Backend**: `https://your-backend.railway.app`
- **API Docs**: `https://your-backend.railway.app/docs`

---

## Next Steps

1. Test the full flow (start story, make choices)
2. Initialize `west_haven` world in ChromaDB if needed
3. Configure custom domain (optional)
4. Set up monitoring/alerts (optional)

---

## Quick Reference

**Frontend Code Changes Made:**
- ✅ Updated `frontend/src/services/api.ts` to use `VITE_API_URL` env var
- ✅ Falls back to `localhost:8000` for local development

**Local Development:**
- Still works with `npm run dev` in `frontend/` directory
- Uses localhost backend by default
- Can override with `.env.local` file

**Production:**
- Uses Railway backend via `VITE_API_URL`
- No code changes needed after initial setup

