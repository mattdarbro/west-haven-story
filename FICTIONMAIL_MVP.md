# FictionMail MVP - Development Guide

**FictionMail**: Personalized daily stories delivered to your inbox.

## What We Built

This MVP implements the core story generation engine for FictionMail - a daily fiction service where users receive personalized stories based on their preferences.

### Architecture

**Multi-Agent Story Generation:**
1. **Bible Enhancement Agent** - Expands minimal user input into rich story worlds
2. **CBA (Chapter Beat Agent)** - Plans story structure using beat templates
3. **CEA (Context Editor Agent)** - Checks consistency (simplified for MVP)
4. **PA (Prose Agent)** - Generates polished prose

**Key Features:**
- ✅ Genre-specific beat templates (scifi, mystery, romance, sitcom)
- ✅ Free tier (1500 words) and Premium tier (4500 words)
- ✅ AI bible enhancement (user gives 1-2 sentences, AI creates full world)
- ✅ Cliffhanger pattern for free tier (every 6th story after first 4)
- ✅ Cameo character system
- ✅ Rating system and preference learning
- ✅ Standalone story generation (not serialized)

### File Structure

```
backend/storyteller/
├── beat_templates.py          # Beat templates for different genres/tiers
├── bible_enhancement.py       # AI enhancement of user input
├── prompts_standalone.py      # Prompts for standalone stories
├── standalone_generation.py   # Main generation workflow
└── [existing files...]

test_fictionmail_flow.py       # Interactive test script
FICTIONMAIL_MVP.md            # This file
```

## How to Test

### Test 1: Complete User Flow

Run the complete onboarding → story generation → rating flow:

```bash
python test_fictionmail_flow.py
```

This will:
1. Prompt for minimal user input (genre, setting, character name)
2. Show AI-enhanced story bible
3. Offer to add cameo characters
4. Generate a free tier story (~1500 words)
5. Ask you to rate it (1-5 stars)
6. Update preferences based on rating
7. Optionally generate a premium story (~4500 words)

**Output files:**
- `test_bible_output.json` - Initial enhanced bible
- `test_bible_updated.json` - After rating feedback
- `test_story_output.txt` - Free tier story
- `test_story_premium.txt` - Premium story (if generated)

### Test 2: Cliffhanger Pattern

Test the free tier cliffhanger logic:

```bash
python test_fictionmail_flow.py cliffhanger
```

Shows which stories get cliffhangers:
- Stories 1-4: Complete ✓
- Story 5: Cliffhanger ✂️
- Stories 6-10: Complete ✓
- Story 11: Cliffhanger ✂️
- (Pattern continues)

### Manual Testing

You can also use the components directly:

```python
import asyncio
from backend.storyteller.bible_enhancement import enhance_story_bible
from backend.storyteller.standalone_generation import generate_standalone_story

async def test():
    # Enhance bible
    bible = await enhance_story_bible(
        genre="scifi",
        user_setting="Space station on the edge of known space",
        character_name="Elena"
    )

    # Generate story
    result = await generate_standalone_story(
        story_bible=bible,
        user_tier="free",  # or "premium"
        dev_mode=True
    )

    if result["success"]:
        print(result["story"]["title"])
        print(result["story"]["narrative"])

asyncio.run(test())
```

## Development Mode Features

When `dev_mode=True` in `generate_standalone_story()`:
- Shows verbose logging
- Generates cover images even on free tier
- Generates audio even on free tier
- Detailed timing information

## What's Working

✅ **Complete standalone story generation**
- Free tier: 4-beat structure, ~1500 words
- Premium tier: 9-beat structure, ~4500 words

✅ **AI bible enhancement**
- Takes minimal input, creates rich worlds
- Generates protagonist + supporting characters
- Establishes tone, themes, atmosphere

✅ **Beat template system**
- Genre-specific templates (scifi, mystery, romance, sitcom)
- Tier-specific word counts
- Detailed beat guidance

✅ **Cliffhanger logic**
- Pattern: Complete stories, occasional cliffhanger (free tier)
- Curiosity-based, not anxiety-based

✅ **Cameo system**
- Frequency controls (rarely, sometimes, often)
- Natural integration into stories
- Tracks appearances

✅ **Rating & preference learning**
- 5-star rating system
- Tracks liked/disliked elements
- Adjusts future stories based on feedback

## What's NOT Yet Implemented

❌ **Image generation** (Replicate integration)
❌ **Audio generation** (ElevenLabs integration)
❌ **Email delivery** (SMTP/SendGrid)
❌ **Web UI** (Frontend)
❌ **Database** (Currently in-memory)
❌ **User authentication**
❌ **Payment/subscription** (Stripe)
❌ **Daily scheduling** (Cron jobs)

## Next Steps for Full MVP

### Week 1: Core Backend
1. Add database (SQLite for dev, Postgres for prod)
2. User model + bible storage
3. Story history storage
4. Basic API endpoints (generate story, rate story, update bible)

### Week 2: Media Generation
5. Integrate Replicate for cover images
6. Integrate ElevenLabs for audio
7. File storage (S3 or similar)

### Week 3: Delivery
8. Email templates (HTML)
9. Email delivery (SendGrid)
10. Daily scheduling system

### Week 4: Frontend
11. Landing page
12. Onboarding flow
13. Story reading page
14. Bible management dashboard

### Week 5: Premium Features
15. Stripe integration
16. Tier management
17. On-demand generation (premium)
18. Story library

## Testing the Current MVP

### Recommended Test Flow

1. **First Run** - See AI enhancement
   ```bash
   python test_fictionmail_flow.py
   # Choose scifi, enter simple setting, add cameo
   # Read the generated story
   # Check test_bible_output.json to see expansion
   ```

2. **Rate and Iterate** - Test preference learning
   ```bash
   # Run again with same genre
   # Rate first story low (1-2 stars) with specific feedback
   # Generate another story
   # See if it adapts to your preferences
   ```

3. **Try Different Genres**
   ```bash
   # Test mystery genre
   # Test romance genre
   # Compare beat structures
   ```

4. **Test Premium Tier**
   ```bash
   # Generate premium story (4500 words)
   # Compare depth and structure to free tier
   ```

### What to Look For

**Bible Enhancement Quality:**
- Does the AI expand your simple setting richly?
- Are the generated characters interesting?
- Is the tone appropriate for the genre?

**Story Quality:**
- Does the story follow the beat structure?
- Is the protagonist consistent with the bible?
- Does it feel complete (or appropriately cliff-hangery)?
- Is the word count close to target?

**Preference Learning:**
- After rating several stories, does the bible show updated preferences?
- Do subsequent stories adapt to your feedback?

**Genre Differences:**
- Do scifi stories feel different from romance?
- Do beat structures vary appropriately?

## Cost Estimates (Current)

**Per Story (Free Tier - 1500 words):**
- Bible enhancement: $0.08 (one-time)
- Beat plan: $0.03
- Prose generation: $0.05
- **Total: ~$0.08 per story** (after initial bible)

**Per Story (Premium Tier - 4500 words):**
- Beat plan: $0.04
- Prose generation: $0.12
- Image (TODO): ~$0.02
- Audio (TODO): ~$0.08
- **Total: ~$0.26 per story**

## Architecture Notes

**Why Standalone vs. Serial:**
- Simpler state management (no multi-chapter continuity)
- Each story is complete (higher completion rate)
- Easier to test and iterate
- Better for daily habit formation
- Can still have recurring characters/world

**Why Beat Templates:**
- Consistent story structure across genres
- Easy to add new genres (just new template)
- Clear word count targets
- Proven storytelling frameworks

**Why AI Bible Enhancement:**
- Lower user friction (30-second onboarding)
- Higher quality stories (AI expansion is detailed)
- Users can still edit if they want control
- Solves "blank page" problem

## Known Issues

1. **LLM can miss word targets** - Sometimes generates longer/shorter than requested
2. **Bible enhancement can be slow** - Takes 10-20s, needs loading state
3. **No retry logic** - If LLM fails, whole generation fails
4. **Cameo integration is random** - Sometimes doesn't fit well
5. **No content filtering** - Needs safety checks

## Questions to Answer Through Testing

1. **Is 1500 words enough for free tier?** Too short? Too long?
2. **Is the cliffhanger pattern right?** Too frequent? Not frequent enough?
3. **Does bible enhancement work well?** Or do users need more control?
4. **Are the beat templates effective?** Do stories feel structured or formulaic?
5. **Does preference learning actually improve stories?** Or is it noise?

## How to Give Feedback

After testing, consider:
- Story quality (1-10)
- Bible enhancement quality (1-10)
- Onboarding friction (too easy? too complex?)
- Would you actually read these daily?
- What would make you upgrade to premium?
- What's missing or confusing?

---

**Ready to test!** Start with `python test_fictionmail_flow.py` and see what happens!
