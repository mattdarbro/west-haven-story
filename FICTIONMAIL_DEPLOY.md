# FictionMail Dev Dashboard - Deployment Guide

**Quick Start**: Your changes are pushed to GitHub. Now deploy to Railway + Vercel to test!

---

## What You Just Built

**Frontend**: Simple standalone HTML dashboard (no build process!)
**Backend**: FictionMail dev API endpoints on Railway
**Flow**: Vercel (frontend) → Railway (backend) → Story generation

---

## Step 1: Deploy Backend to Railway

Railway should auto-deploy when you push to GitHub. Check:

1. Go to https://railway.app
2. Find your **west-haven-story** project
3. Check the deployment status
4. Should see: "✓ FictionMail dev routes loaded" in logs
5. Test: Visit `https://your-app.up.railway.app/health`

**Expected Response:**
```json
{
  "status": "healthy",
  "config_loaded": true,
  "routes_loaded": true
}
```

**New Endpoints Available:**
- `POST /api/dev/onboarding` - Create enhanced bible
- `POST /api/dev/generate-story` - Generate story
- `POST /api/dev/rate-story` - Rate a story
- `GET /api/dev/bible` - Get current bible
- `DELETE /api/dev/reset` - Reset dev storage

---

## Step 2: Deploy Frontend to Vercel

### Option A: Auto-Deploy (Recommended)

If Vercel is already connected to your GitHub:

1. **Push to GitHub** ✅ (Already done!)
2. **Vercel Auto-Deploys** (happens automatically)
3. **Wait 1-2 minutes** for build to complete
4. **Visit your Vercel URL** (e.g., `https://your-app.vercel.app`)

### Option B: Manual Deploy

If not connected yet:

1. Go to https://vercel.com
2. Click "Add New" → "Project"
3. Import from GitHub → Select `west-haven-story`
4. Configure:
   - **Framework Preset**: Other
   - **Root Directory**: `frontend`
   - **Build Command**: Leave empty (static file)
   - **Output Directory**: `.` (current directory)
5. **Environment Variables**: None needed! (hardcoded to Railway)
6. Click "Deploy"

---

## Step 3: Test the Dashboard

Visit your Vercel URL: `https://your-app.vercel.app`

You should see:
```
📧 FictionMail Dev Dashboard
Test story generation flow
Backend: https://west-haven-story-production.up.railway.app
```

### Complete Test Flow:

1. **Onboarding:**
   - Select genre (e.g., Sci-Fi)
   - Enter setting: "Space station on the edge of known space"
   - Enter character: "Elena"
   - Select tier: Free or Premium
   - Click "✨ Enhance Bible"

2. **Bible Preview:**
   - See AI-expanded setting
   - See protagonist details
   - View full JSON (optional)
   - Click "🎬 Generate Story"

3. **Story Generation:**
   - Watch debug logs in real-time
   - Wait 2-4 minutes (shows progress)
   - Story appears with full text

4. **Rate & Iterate:**
   - Rate the story (1-5 stars)
   - Provide feedback
   - Generate another story
   - See preferences adapt

---

## Troubleshooting

### Frontend Shows But Can't Connect

**Symptom:** Dashboard loads but gets errors when clicking "Enhance Bible"

**Check:**
1. Railway backend is running:
   - Visit `https://your-railway-url.up.railway.app/health`
   - Should return `{"status": "healthy"}`

2. CORS is enabled:
   - Backend already has `allow_origins=["*"]`
   - Should work without changes

3. Check browser console:
   - Right-click → Inspect → Console tab
   - Look for error messages
   - Should show API requests to Railway

**Fix:**
- If Railway URL is wrong, update `API_URL` in `frontend/dev-dashboard.html` line 175
- Push to GitHub, Vercel will redeploy

### Story Generation Fails

**Symptom:** Clicks "Generate Story" but gets error

**Check:**
1. Railway logs:
   - Go to Railway dashboard → Your service → Logs
   - Look for errors during generation

2. Common issues:
   - ANTHROPIC_API_KEY not set in Railway
   - Timeout (increase if needed)
   - JSON parsing error (check logs)

**Fix:**
- Set ANTHROPIC_API_KEY in Railway environment variables
- Restart Railway service

### Vercel Build Fails

**Symptom:** Vercel deployment shows error

**Check:**
1. Make sure `vercel.json` exists in `frontend/` directory
2. Check Vercel build logs

**Fix:**
- The `vercel.json` tells Vercel to serve static HTML
- No build process needed
- If still fails, try:
  - Settings → General → Build & Development Settings
  - Framework Preset: Other
  - Build Command: (leave empty)

---

## What's Hardcoded (For Now)

In `frontend/dev-dashboard.html` line 175:
```javascript
const API_URL = 'https://west-haven-story-production.up.railway.app';
```

**To Change:**
1. Update this URL to your actual Railway backend URL
2. Push to GitHub
3. Vercel will redeploy automatically

**Later:** We can add environment variables, but for MVP this is simpler!

---

## Testing Checklist

- [ ] Railway backend deployed and healthy
- [ ] Vercel frontend deployed and accessible
- [ ] Can load dashboard in browser
- [ ] Can complete onboarding (enhance bible)
- [ ] Bible enhancement shows expanded details
- [ ] Can generate free tier story (~1500 words)
- [ ] Can generate premium tier story (~4500 words)
- [ ] Can rate story and submit feedback
- [ ] Debug logs show real-time progress
- [ ] Debug panels show beat plans and JSON

---

## Next Steps After Testing

Once the dashboard is working:

1. **Test different genres** - Sci-fi, mystery, romance
2. **Test preference learning** - Rate low, generate again, see if it adapts
3. **Test both tiers** - Compare free (1500w) vs premium (4500w)
4. **Check story quality** - Are they good? Formulaic? Interesting?
5. **Tune parameters** - Adjust templates, prompts, word counts
6. **Add features** - Image generation, audio, etc.

---

## URLs Quick Reference

**Backend (Railway):**
- Health check: `https://your-app.up.railway.app/health`
- API docs: `https://your-app.up.railway.app/docs`
- Dev API: `https://your-app.up.railway.app/api/dev/*`

**Frontend (Vercel):**
- Dashboard: `https://your-app.vercel.app`
- (Will redirect all routes to dashboard)

---

## Getting Help

If you run into issues:

1. **Check Railway logs** - Most errors show there
2. **Check browser console** - Frontend errors show there
3. **Check Vercel logs** - Deployment issues show there
4. **Test health endpoint** - Make sure backend is running

---

**You're ready to test FictionMail in production!** 🚀

Push your changes, wait for deployments, and visit your Vercel URL to try it out!
