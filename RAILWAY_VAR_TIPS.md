# Railway Environment Variable Tips

## Why Variables Were Messed Up

Railway environment variables are **strings** by default, and they're **very picky** about format. Here's what went wrong and how to fix it:

---

## Common Mistakes

### ❌ Wrong: Extra Quotes
```
REPLICATE_API_TOKEN="r8_abc123..."  # Railway adds quotes, don't add your own
```
**Result**: Variable contains literal quotes → Auth errors

### ✅ Right: No Quotes
```
REPLICATE_API_TOKEN=r8_abc123...
```

---

### ❌ Wrong: Extra Spaces
```
IMAGE_MODEL = black-forest-labs/flux-schnell  # Space before or after =
```
**Result**: Variable value has extra spaces → "not found" errors

### ✅ Right: No Spaces
```
IMAGE_MODEL=black-forest-labs/flux-schnell
```

---

### ❌ Wrong: Leading Equals Sign
```
= ENVIRONMENT=production  # Extra = at start
```
**Result**: "Empty key" error

### ✅ Right: Just Variable Name
```
ENVIRONMENT=production
```

---

### ❌ Wrong: Typos
```
DEFAULT_WORD=west_haven  # Missing L
STORAGE_PATH=/app/storage  # Wrong capitalization (should work now)
```
**Result**: App can't find the variable → Uses defaults

---

## Best Practices for Railway

### 1. Always Delete and Re-add
If a variable isn't working:
1. **Delete** the variable completely
2. **Add** it fresh with the exact value
3. Never "edit" a broken variable

### 2. Copy-Paste Carefully
- Copy the **exact** value from your source
- Watch for hidden characters or extra spaces
- Triple-check the spelling

### 3. Test Format
For sensitive values like API keys:
1. Create the variable
2. Check Railway logs for any errors
3. If you see errors, delete and re-add

---

## Variable Checklist

Here's the **complete list** with proper formatting:

```bash
# Required
OPENAI_API_KEY=sk-proj-your-actual-key-here
ENVIRONMENT=production
STORAGE_PATH=/app/storage

# World Config (Optional - defaults shown)
DEFAULT_WORLD=west_haven

# Media Generation (Optional)
REPLICATE_API_TOKEN=r8_your-token-here
ELEVENLABS_API_KEY=your-elevenlabs-key

# Model Selection (Optional - defaults shown)
IMAGE_MODEL=black-forest-labs/flux-schnell
ELEVENLABS_VOICE_ID=AZnzlk1XvdvUeBnXmlld

# Feature Toggles (Optional)
ENABLE_MEDIA_GENERATION=true
ENABLE_CREDIT_SYSTEM=false

# Credits (Optional - only if credit system enabled)
CREDITS_PER_NEW_USER=25
CREDITS_PER_CHOICE=1
```

---

## Quick Fixes

### If You Get "Authentication Failed" Errors:

1. **Check the token format**:
   - Replicate: Must start with `r8_`
   - OpenAI: Must start with `sk-` or `sk-proj-`
   - ElevenLabs: Check their format

2. **Verify in Railway**:
   - Go to Variables tab
   - Click on the variable
   - Look at the **Value** field (not Key)
   - Make sure there are NO extra characters

3. **Common Fix**:
   - Delete the variable
   - Re-add with exact value from source
   - No quotes, no spaces around =

---

### If You Get "Model/Voice Not Found":

1. **Check spelling**: Case-sensitive!
2. **Use exact ID** from MODELS_VOICES.md
3. **Test in Railway logs** to see what it's trying to use

---

### If Variables Don't Seem to Work:

1. **Redeploy**: After changing variables, redeploy your service
2. **Check logs**: Railway logs show what variables are loaded
3. **Verify case**: All uppercase vs mixed case matters

---

## Example: Setting Up FLUX Schnell

**Step-by-step**:

1. Go to Railway → Your Service → Variables
2. Click "Raw Editor"
3. Add this line:
   ```
   IMAGE_MODEL=black-forest-labs/flux-schnell
   ```
4. Save
5. Redeploy

**Verify it worked**:
- Check deployment logs for: `Generating image with model: black-forest-labs/flux-schnell`

---

## Example: Changing Voice to Domi

**Step-by-step**:

1. Go to Railway → Variables
2. Find or add `ELEVENLABS_VOICE_ID`
3. Set value to:
   ```
   AZnzlk1XvdvUeBnXmlld
   ```
4. No quotes, no spaces
5. Save and redeploy

---

## Pro Tips

1. **Use Raw Editor**: Railway's raw editor is easier for exact values
2. **Keep a backup**: Note your working values somewhere safe
3. **Test one at a time**: Change one variable, test, then change another
4. **Read the logs**: Railway logs show exactly what the app sees

---

## Still Having Issues?

Check the logs for:
- What value Railway actually sees
- Any parsing/format errors
- Which variables are missing

The app now auto-initializes worlds and gracefully handles missing API keys, so the story should work even if some features aren't configured perfectly!

