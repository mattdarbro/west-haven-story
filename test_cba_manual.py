"""
Test CBA (Chapter Beat Agent) implementation.
Run with: python test_cba_manual.py
"""

import asyncio
import json
from backend.storyteller.prompts_v2 import load_world_template, create_chapter_beat_prompt


async def test_cba_prompts():
    """Test CBA prompt generation."""
    print("🧪 Testing CBA Prompts (Phase 3)")
    print("=" * 60)

    # Test 1: Load world template
    print("\n1. Loading world template...")
    try:
        world_template = load_world_template("tfogwf")
        print(f"   ✅ World template loaded: {world_template.get('name', 'Unknown')}")
        print(f"      Genre: {world_template.get('genre', 'N/A')}")
    except Exception as e:
        print(f"   ❌ Failed to load template: {e}")
        return

    # Test 2: Create chapter beat prompt (Chapter 1)
    print("\n2. Creating chapter beat prompt for Chapter 1...")
    try:
        # Mock story structure from SSBA
        story_structure = {
            "act_1": {
                "opening_image": {
                    "chapters": [1],
                    "description": "Introduce Elena Storm's world before upheaval"
                },
                "theme_stated": {
                    "chapters": [1, 2],
                    "description": "Theme: Identity vs destiny"
                }
            }
        }

        # Mock SSBA guidance
        ssba_guidance = {
            "current_story_beat": "opening_image",
            "act": "1",
            "progress_percentage": 3.3,
            "guidance_for_cba": "Establish Elena's routine life before the catalyst",
            "character_arcs_status": {
                "protagonist": "Starting point - unaware of larger destiny"
            }
        }

        story_bible = {
            "protagonist": {
                "name": "Elena Storm",
                "current_state": "Station security officer, routine life"
            }
        }

        summaries = []
        last_choice = None

        prompt = create_chapter_beat_prompt(
            world_template=world_template,
            chapter_number=1,
            total_chapters=30,
            story_structure=story_structure,
            ssba_guidance=ssba_guidance,
            story_bible=story_bible,
            last_choice=last_choice,
            summaries=summaries
        )

        print(f"   ✅ Chapter 1 prompt created ({len(prompt)} chars)")
        print(f"      Preview: {prompt[:200]}...")

        # Check for key elements
        assert "Chapter 1" in prompt
        assert "6-beat mini-arc" in prompt or "6-BEAT" in prompt
        assert "OPENING HOOK" in prompt
        assert "MIDPOINT TWIST" in prompt
        assert "RESOLUTION & HOOK" in prompt
        assert "JSON FORMAT" in prompt
        assert "opening_image" in prompt
        print(f"   ✅ All key CBA elements present")
    except Exception as e:
        print(f"   ❌ Failed to create Chapter 1 prompt: {e}")
        return

    # Test 3: Create chapter beat prompt (Chapter 15)
    print("\n3. Creating chapter beat prompt for Chapter 15...")
    try:
        # Mock story structure for Act 2A
        story_structure = {
            "act_2a": {
                "fun_and_games": {
                    "chapters": [8, 9, 10, 11, 12, 13, 14],
                    "description": "Elena explores her abilities"
                },
                "midpoint": {
                    "chapters": [15, 16],
                    "description": "False victory turns to major setback"
                }
            }
        }

        ssba_guidance = {
            "current_story_beat": "midpoint",
            "act": "2A",
            "progress_percentage": 50.0,
            "guidance_for_cba": "Major turning point - false victory becomes a trap",
            "character_arcs_status": {
                "protagonist": "Confident, about to face major challenge"
            }
        }

        story_bible = {
            "protagonist": {
                "name": "Elena Storm",
                "current_state": "Mastering abilities, feeling confident"
            }
        }

        summaries = [
            "Elena discovered her connection to ancient technology.",
            "She began training with the artifact's powers.",
            "The crew planned to use Elena's abilities to solve the crisis."
        ]

        last_choice = "Trust the artifact and attempt full integration"

        prompt = create_chapter_beat_prompt(
            world_template=world_template,
            chapter_number=15,
            total_chapters=30,
            story_structure=story_structure,
            ssba_guidance=ssba_guidance,
            story_bible=story_bible,
            last_choice=last_choice,
            summaries=summaries
        )

        print(f"   ✅ Chapter 15 prompt created ({len(prompt)} chars)")
        print(f"      Preview: {prompt[:200]}...")

        # Check for key elements
        assert "Chapter 15" in prompt
        assert "50.0%" in prompt  # Progress percentage
        assert "midpoint" in prompt
        assert "Trust the artifact" in prompt  # Last choice
        assert len(summaries) > 0
        print(f"   ✅ All key context elements present")
    except Exception as e:
        print(f"   ❌ Failed to create Chapter 15 prompt: {e}")
        return

    # Test 4: Check prompt structure for all beats
    print("\n4. Verifying 6-beat structure definitions...")
    try:
        # Beat names to check
        required_beats = [
            "OPENING HOOK",
            "RISING ACTION",
            "MIDPOINT TWIST",
            "COMPLICATIONS",
            "DARK NIGHT",
            "RESOLUTION & HOOK"
        ]

        for beat_name in required_beats:
            assert beat_name in prompt, f"Missing beat: {beat_name}"
            print(f"   ✅ {beat_name} defined")

        # Check word targets
        assert "0-450" in prompt
        assert "450-900" in prompt
        assert "2,250-2,700" in prompt
        print(f"   ✅ Word targets specified for all beats")
    except Exception as e:
        print(f"   ❌ Failed beat structure verification: {e}")
        return

    # Test 5: Verify JSON format specification
    print("\n5. Verifying JSON format specification...")
    try:
        assert "chapter_beats" in prompt
        assert "beat_number" in prompt
        assert "beat_name" in prompt
        assert "word_target" in prompt
        assert "chapter_goal" in prompt
        assert "chapter_tension" in prompt
        assert "choice_setup" in prompt
        print(f"   ✅ JSON format fully specified")
    except Exception as e:
        print(f"   ❌ Failed JSON format verification: {e}")
        return

    print("\n" + "=" * 60)
    print("🎉 All CBA Prompt Tests Passed!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(test_cba_prompts())
