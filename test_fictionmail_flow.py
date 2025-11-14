"""
Test script for FictionMail MVP flow.

This lets you test the complete story generation flow:
1. Create/enhance story bible
2. Generate standalone story
3. Rate and provide feedback
4. See how preferences adapt

Run with: python test_fictionmail_flow.py
"""

import asyncio
import json
from backend.storyteller.bible_enhancement import (
    enhance_story_bible,
    add_cameo_characters,
    update_story_history
)
from backend.storyteller.standalone_generation import generate_standalone_story


async def test_onboarding_and_first_story():
    """Test the complete onboarding → first story flow."""

    print("="*70)
    print("FICTIONMAIL MVP - COMPLETE FLOW TEST")
    print("="*70)

    # STEP 1: Simulate user onboarding (minimal input)
    print("\n" + "="*70)
    print("STEP 1: USER ONBOARDING (Minimal Input)")
    print("="*70)

    user_input = {
        "genre": "scifi",
        "setting": "Space station on the edge of known space",
        "character_name": "Elena",
        "tier": "free"  # Start with free tier
    }

    print(f"\nUser provides:")
    print(f"  Genre: {user_input['genre']}")
    print(f"  Setting: {user_input['setting']}")
    print(f"  Character: {user_input.get('character_name', 'Surprise me!')}")
    print(f"  Tier: {user_input['tier']}")

    # STEP 2: AI Enhancement
    print("\n" + "="*70)
    print("STEP 2: AI BIBLE ENHANCEMENT")
    print("="*70)

    bible = await enhance_story_bible(
        genre=user_input["genre"],
        user_setting=user_input["setting"],
        character_name=user_input.get("character_name")
    )

    print(f"\n✓ Bible enhanced!")
    print(f"\nExpanded Setting:")
    print(f"  Name: {bible['setting']['name']}")
    print(f"  Description: {bible['setting']['description'][:200]}...")
    print(f"\nProtagonist:")
    print(f"  Name: {bible['protagonist']['name']}")
    print(f"  Role: {bible['protagonist']['role']}")
    print(f"  Defining trait: {bible['protagonist']['defining_characteristic']}")
    print(f"\nSupporting Characters: {len(bible.get('supporting_characters', []))}")
    for char in bible.get('supporting_characters', [])[:2]:
        print(f"  - {char['name']}: {char['role']}")

    # STEP 3: Optional - Add cameo
    print("\n" + "="*70)
    print("STEP 3: ADD CAMEO CHARACTER (Optional)")
    print("="*70)

    add_cameo = input("\nAdd yourself as a cameo? (y/n): ").strip().lower()

    if add_cameo == 'y':
        cameo_name = input("Your name: ").strip() or "Alex"
        cameo_desc = input("Describe yourself in 2-3 words: ").strip() or "Friendly engineer"

        bible = add_cameo_characters(bible, [
            {
                "name": cameo_name,
                "description": cameo_desc,
                "frequency": "sometimes"
            }
        ])

        print(f"\n✓ Added cameo: {cameo_name} ({cameo_desc})")

    # Save bible for inspection
    with open("test_bible_output.json", "w") as f:
        json.dump(bible, f, indent=2)

    print(f"\n✓ Bible saved to: test_bible_output.json")

    # STEP 4: Generate first story (FREE tier)
    print("\n" + "="*70)
    print("STEP 4: GENERATE FIRST STORY (FREE TIER)")
    print("="*70)
    print("\nGenerating your first story...")
    print("This will take ~2-3 minutes...\n")

    result = await generate_standalone_story(
        story_bible=bible,
        user_tier="free",
        dev_mode=True
    )

    if result["success"]:
        story = result["story"]
        metadata = result["metadata"]

        print(f"\n✓ Story generated successfully!")
        print(f"\nTitle: {story['title']}")
        print(f"Word count: {story['word_count']} (target: ~1500)")
        print(f"Generation time: {metadata['generation_time_seconds']:.2f}s")
        print(f"Plot type: {metadata['plot_type']}")

        # Save story
        with open("test_story_output.txt", "w") as f:
            f.write(f"{story['title']}\n")
            f.write(f"{'='*len(story['title'])}\n\n")
            f.write(story['narrative'])

        print(f"\n✓ Story saved to: test_story_output.txt")

        # Display first 500 chars
        print(f"\nPreview:")
        print(f"{'-'*70}")
        print(story['narrative'][:500] + "...")
        print(f"{'-'*70}")

        # STEP 5: Rate the story
        print("\n" + "="*70)
        print("STEP 5: RATE YOUR STORY")
        print("="*70)

        rating = input("\nHow was this story? (1-5 stars): ").strip()
        try:
            rating = int(rating)
            rating = max(1, min(5, rating))  # Clamp to 1-5
        except:
            rating = 3  # Default

        feedback = {}
        if rating >= 4:
            print("\nWhat did you like?")
            print("1. Great pacing")
            print("2. Loved the characters")
            print("3. Good mystery")
            print("4. Surprising twist")
            print("5. Emotional moments")
            liked = input("Enter numbers separated by commas (or skip): ").strip()

            if liked:
                feedback_map = {
                    "1": "great_pacing",
                    "2": "loved_characters",
                    "3": "good_mystery",
                    "4": "surprising_twist",
                    "5": "emotional_moments"
                }
                for num in liked.split(","):
                    num = num.strip()
                    if num in feedback_map:
                        feedback[feedback_map[num]] = True

        elif rating <= 2:
            print("\nWhat could be better?")
            print("1. Too slow")
            print("2. Not enough action")
            print("3. Characters felt off")
            print("4. Confusing plot")
            disliked = input("Enter numbers separated by commas (or skip): ").strip()

            if disliked:
                feedback_map = {
                    "1": "too_slow",
                    "2": "not_enough_action",
                    "3": "characters_felt_off",
                    "4": "confusing_plot"
                }
                for num in disliked.split(","):
                    num = num.strip()
                    if num in feedback_map:
                        feedback[feedback_map[num]] = True

        # Update bible with rating
        bible = update_story_history(
            bible=bible,
            story_summary=metadata['summary'],
            plot_type=metadata['plot_type'],
            rating=rating,
            feedback=feedback
        )

        print(f"\n✓ Rating recorded: {rating} stars")
        print(f"✓ Bible updated with preferences")

        # Save updated bible
        with open("test_bible_updated.json", "w") as f:
            json.dump(bible, f, indent=2)

        # STEP 6: Test premium tier
        print("\n" + "="*70)
        print("STEP 6: TEST PREMIUM TIER (Optional)")
        print("="*70)

        test_premium = input("\nGenerate a premium story (4500 words)? (y/n): ").strip().lower()

        if test_premium == 'y':
            print("\nGenerating premium story...")
            print("This will take ~3-4 minutes...\n")

            premium_result = await generate_standalone_story(
                story_bible=bible,
                user_tier="premium",
                dev_mode=True
            )

            if premium_result["success"]:
                premium_story = premium_result["story"]
                premium_meta = premium_result["metadata"]

                print(f"\n✓ Premium story generated!")
                print(f"\nTitle: {premium_story['title']}")
                print(f"Word count: {premium_story['word_count']} (target: ~4500)")
                print(f"Generation time: {premium_meta['generation_time_seconds']:.2f}s")

                # Save premium story
                with open("test_story_premium.txt", "w") as f:
                    f.write(f"{premium_story['title']}\n")
                    f.write(f"{'='*len(premium_story['title'])}\n\n")
                    f.write(premium_story['narrative'])

                print(f"\n✓ Premium story saved to: test_story_premium.txt")

        print("\n" + "="*70)
        print("TEST COMPLETE!")
        print("="*70)
        print("\nGenerated files:")
        print("  - test_bible_output.json (initial bible)")
        print("  - test_bible_updated.json (after rating)")
        print("  - test_story_output.txt (free tier story)")
        if test_premium == 'y':
            print("  - test_story_premium.txt (premium tier story)")

        print("\nNext steps:")
        print("  1. Read the generated stories")
        print("  2. Check the bible JSON to see AI expansion")
        print("  3. Run again to see preference learning")
        print("  4. Try different genres/settings")

    else:
        print(f"\n❌ Story generation failed:")
        print(f"  Error: {result.get('error', 'Unknown error')}")


async def test_cliffhanger_pattern():
    """Test the free tier cliffhanger pattern."""

    print("\n" + "="*70)
    print("TESTING CLIFFHANGER PATTERN (Free Tier)")
    print("="*70)

    # Create simple bible
    bible = {
        "genre": "scifi",
        "setting": {
            "name": "Test Station",
            "description": "A test setting",
            "key_locations": [],
            "atmosphere": "tense",
            "rules": "Sci-fi standard"
        },
        "protagonist": {
            "name": "Test Character",
            "role": "Security",
            "age_range": "adult",
            "key_traits": ["determined"],
            "defining_characteristic": "Quick thinking",
            "background": "Test",
            "motivation": "Solve mysteries",
            "voice": "analytical"
        },
        "supporting_characters": [],
        "tone": "tense",
        "themes": ["mystery"],
        "story_style": "Test stories",
        "story_history": {
            "total_stories": 0,
            "recent_summaries": [],
            "recent_plot_types": [],
            "used_cameos": [],
            "last_cliffhanger": None
        },
        "user_preferences": {
            "ratings": [],
            "liked_elements": [],
            "disliked_elements": [],
            "pacing_preference": "medium",
            "action_level": "medium",
            "emotional_depth": "medium"
        }
    }

    # Test pattern: Stories 1-4 complete, Story 5 cliffhanger
    for i in range(1, 6):
        bible["story_history"]["total_stories"] = i - 1

        from backend.storyteller.bible_enhancement import should_use_cliffhanger
        is_cliff = should_use_cliffhanger(bible, "free")

        print(f"Story {i}: {'CLIFFHANGER ✂️' if is_cliff else 'Complete ✓'}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "cliffhanger":
        asyncio.run(test_cliffhanger_pattern())
    else:
        asyncio.run(test_onboarding_and_first_story())
