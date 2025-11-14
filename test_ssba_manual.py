"""
Test SSBA (Story Structure Beat Agent) implementation.
Run with: python test_ssba_manual.py
"""

import asyncio
import json
from backend.storyteller.prompts_v2 import load_world_template, create_story_structure_prompt, create_story_beat_checkin_prompt


async def test_ssba_prompts():
    """Test SSBA prompt generation."""
    print("🧪 Testing SSBA Prompts (Phase 2)")
    print("=" * 60)

    # Test 1: Load world template
    print("\n1. Loading world template...")
    try:
        world_template = load_world_template("tfogwf")
        print(f"   ✅ World template loaded: {world_template.get('name', 'Unknown')}")
        print(f"      Genre: {world_template.get('genre', 'N/A')}")
        print(f"      Setting: {world_template.get('world_lore', {}).get('setting', 'N/A')}")
    except Exception as e:
        print(f"   ❌ Failed to load template: {e}")
        return

    # Test 2: Create story structure prompt (Chapter 1)
    print("\n2. Creating story structure prompt...")
    try:
        prompt = create_story_structure_prompt(world_template, total_chapters=30)
        print(f"   ✅ Prompt created ({len(prompt)} chars)")
        print(f"      Preview: {prompt[:200]}...")

        # Check for key elements
        assert "Save the Cat" in prompt
        assert "ACT 1" in prompt
        assert "ACT 2A" in prompt
        assert "ACT 3" in prompt
        assert "OPENING IMAGE" in prompt
        assert "MIDPOINT" in prompt
        assert "JSON FORMAT" in prompt
        print(f"   ✅ All key beat structure elements present")
    except Exception as e:
        print(f"   ❌ Failed to create prompt: {e}")
        return

    # Test 3: Create check-in prompt (Chapter 15)
    print("\n3. Creating check-in prompt for Chapter 15...")
    try:
        # Mock story structure
        story_structure = {
            "act_2a": {
                "fun_and_games": {
                    "chapters": [8, 9, 10, 11, 12, 13, 14, 15],
                    "description": "Exploration and discovery phase"
                },
                "midpoint": {
                    "chapters": [14, 15, 16],
                    "description": "False victory, stakes raised"
                }
            }
        }

        story_bible = {
            "protagonist": {
                "name": "Elena Storm",
                "current_state": "Learning to trust the crew, discovering her abilities"
            }
        }

        summaries = [
            "Elena explored the mysterious signal source.",
            "She discovered ancient technology in the station core.",
            "A connection formed between Elena and the artifact."
        ]

        inconsistency_flags = []

        prompt = create_story_beat_checkin_prompt(
            story_structure=story_structure,
            chapter_number=15,
            total_chapters=30,
            story_bible=story_bible,
            summaries=summaries,
            inconsistency_flags=inconsistency_flags
        )

        print(f"   ✅ Check-in prompt created ({len(prompt)} chars)")
        print(f"      Preview: {prompt[:200]}...")

        # Check for key elements
        assert "Chapter 15" in prompt
        assert "50.0%" in prompt  # Progress percentage
        assert "JSON FORMAT" in prompt
        assert "Elena Storm" in prompt or "protagonist" in prompt
        print(f"   ✅ All key check-in elements present")
    except Exception as e:
        print(f"   ❌ Failed to create check-in prompt: {e}")
        return

    # Test 4: Check-in with inconsistency flags
    print("\n4. Creating check-in prompt with inconsistency flags...")
    try:
        inconsistency_flags = [
            {
                "flag_id": "elena_mobility_ch14",
                "description": "Player choice implied Elena walked independently, but Chapter 7 established mobility limitations",
                "suggested_resolution": "Reveal experimental treatment or modify scene"
            }
        ]

        prompt = create_story_beat_checkin_prompt(
            story_structure=story_structure,
            chapter_number=15,
            total_chapters=30,
            story_bible=story_bible,
            summaries=summaries,
            inconsistency_flags=inconsistency_flags
        )

        print(f"   ✅ Check-in prompt with flags created")
        assert "INCONSISTENCY FLAGS" in prompt
        assert "elena_mobility_ch14" in prompt
        print(f"   ✅ Inconsistency flag integrated into prompt")
    except Exception as e:
        print(f"   ❌ Failed to create prompt with flags: {e}")
        return

    print("\n" + "=" * 60)
    print("🎉 All SSBA Prompt Tests Passed!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(test_ssba_prompts())
