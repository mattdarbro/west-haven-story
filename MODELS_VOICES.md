# Available AI Models and Voices

This document lists all the models and voices available for configuration.

## Image Generation Models (Replicate)

### Recommended Models

1. **Stability AI SDXL**
   - Model ID: `stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5555e08b`
   - Best for: General purpose, high quality
   - Cost: ~$0.04/image

2. **FLUX Schnell** (Recommended)
   - Model ID: `black-forest-labs/flux-schnell`
   - Best for: Fast generation, sci-fi, detailed
   - Cost: ~$0.003/image
   - Note: Extremely fast and cheap

3. **Nanobanana (Google)**
   - Model ID: `google/nanobanana`
   - Best for: Experimental, Google's latest
   - Cost: Varies
   - Note: New model, may have quirks

4. **FLUX Pro**
   - Model ID: `black-forest-labs/flux-pro`
   - Best for: Best quality, slower
   - Cost: ~$0.055/image

5. **Stable Diffusion 2.1**
   - Model ID: `stability-ai/stable-diffusion-2-1`
   - Best for: Budget option
   - Cost: ~$0.002/image

6. **Stable Diffusion XL**
   - Model ID: `stability-ai/sdxl:7762fd07`
   - Best for: Reliable, consistent
   - Cost: ~$0.03/image

### How to Use

Set `IMAGE_MODEL` in Railway to the model ID you want.

Example: `IMAGE_MODEL=black-forest-labs/flux-schnell`

---

## Voice Models (ElevenLabs)

### Recommended Voices

1. **Rachel** (Default)
   - Voice ID: `21m00Tcm4TlvDq8ikWAM`
   - Characteristics: Professional, clear female voice

2. **Domi** (Female)
   - Voice ID: `AZnzlk1XvdvUeBnXmlld`
   - Characteristics: Strong, confident female voice

3. **Bella** (Female)
   - Voice ID: `EXAVITQu4vr4xnSDxMaL`
   - Characteristics: Soft, warm female voice

4. **Antoni** (Male)
   - Voice ID: `ErXwobaYiN019PkySvjV`
   - Characteristics: Deep, smooth male voice

5. **Elli** (Female)
   - Voice ID: `MF3mGyEYCl7XYWbV9V6O`
   - Characteristics: Young, energetic female voice

6. **Josh** (Male)
   - Voice ID: `TxGEqnHWrfWFTfGW9XjX`
   - Characteristics: Casual, friendly male voice

7. **Arnold** (Male)
   - Voice ID: `VR6AewLTigWG4xSOukaG`
   - Characteristics: Mature, authoritative male voice

8. **Adam** (Male)
   - Voice ID: `pNInz6obpgDQGcFmaJgB`
   - Characteristics: Young, clear male voice

9. **Sam** (Male)
   - Voice ID: `yoZ06aMxZJJ28mfd3POQ`
   - Characteristics: Casual, approachable male voice

### How to Use

Set `ELEVENLABS_VOICE_ID` in Railway to the voice ID you want.

Example: `ELEVENLABS_VOICE_ID=AZnzlk1XvdvUeBnXmlld`

---

## Quick Configuration Guide

### For Railway

Add these to your environment variables:

```bash
# Image Model - Try FLUX Schnell for best speed/quality balance
IMAGE_MODEL=black-forest-labs/flux-schnell

# Or for Google Nanobanana
IMAGE_MODEL=google/nanobanana

# Voice - Try Domi for sci-fi
ELEVENLABS_VOICE_ID=AZnzlk1XvdvUeBnXmlld

# Or Antoni for deeper male voice
ELEVENLABS_VOICE_ID=ErXwobaYiN019PkySvjV
```

### Testing Locally

In your `.env` file:

```bash
REPLICATE_API_TOKEN=r8_your_key_here
ELEVENLABS_API_KEY=your_key_here

# Try different models
IMAGE_MODEL=black-forest-labs/flux-schnell
# IMAGE_MODEL=google/nanobanana
# IMAGE_MODEL=stability-ai/sdxl:latest

ELEVENLABS_VOICE_ID=AZnzlk1XvdvUeBnXmlld
# ELEVENLABS_VOICE_ID=ErXwobaYiN019PkySvjV
```

---

## Cost Comparison

| Model | Cost per Image | Speed | Quality |
|-------|---------------|-------|---------|
| FLUX Schnell | $0.003 | Very Fast | Excellent |
| Stable Diffusion 2.1 | $0.002 | Fast | Good |
| SDXL | $0.03-0.04 | Medium | Excellent |
| FLUX Pro | $0.055 | Slow | Best |
| Nanobanana | Varies | Varies | Unknown |

**Recommendation**: Start with **FLUX Schnell** for best balance of speed, quality, and cost!

---

## Troubleshooting

### "Model not found" Error
- Use exact model ID from this list
- Some models might require specific Replicate plan
- Try the full version hash (not just `:latest`)

### "Voice not found" Error
- Double-check voice ID spelling
- Voice IDs are case-sensitive
- Make sure you have ElevenLabs account with access to that voice

### Authentication Errors
- Check your API tokens are set correctly
- Make sure they start with `r8_` (Replicate) or proper ElevenLabs format
- Verify you have credits/balance in your accounts

