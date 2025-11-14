"""
Test CEA (Context Editor Agent) implementation.
Run with: python test_cea_manual.py
"""

import asyncio
import json
from backend.storyteller.prompts_v2 import (
    load_world_template,
    create_consistency_check_prompt,
    create_choice_generation_prompt
)


async def test_cea_prompts():
    """Test CEA prompt generation."""
    print("🧪 Testing CEA Prompts (Phase 4)")
    print("=" * 60)

    # Test 1: Load world template
    print("\n1. Loading world template...")
    try:
        world_template = load_world_template("tfogwf")
        print(f"   ✅ World template loaded: {world_template.get('name', 'Unknown')}")
    except Exception as e:
        print(f"   ❌ Failed to load template: {e}")
        return

    # Test 2: Create consistency check prompt
    print("\n2. Creating consistency check prompt...")
    try:
        # Mock chapter beat plan
        chapter_beat_plan = {
            "chapter_beats": [
                {
                    "beat_number": 1,
                    "beat_name": "opening_hook",
                    "word_target": 450,
                    "description": "Elena wheels through the station corridor",
                    "key_elements": ["Elena", "wheelchair", "station corridor"],
                    "emotional_tone": "tense",
                    "character_focus": "Elena Storm"
                }
            ],
            "chapter_goal": "Establish Elena's routine before the inciting incident",
            "chapter_tension": "Mysterious signal detected"
        }

        # Mock story bible
        story_bible = {
            "protagonist": {
                "name": "Elena Storm",
                "current_state": "Station security officer",
                "key_trait": "Uses wheelchair"
            }
        }

        # Mock consistency report from RAG
        consistency_report = {
            "checks_performed": ["Elena wheelchair", "station corridor"],
            "relevant_history": [
                {
                    "text": "Elena used a wheelchair after the accident in Chapter 3.",
                    "chapter": 3,
                    "distance": 0.15
                }
            ],
            "risk_flags": [],
            "overall_risk": "low",
            "total_checks": 2
        }

        prompt = create_consistency_check_prompt(
            chapter_number=5,
            chapter_beat_plan=chapter_beat_plan,
            story_bible=story_bible,
            consistency_report=consistency_report,
            last_choice="Investigate the mysterious signal"
        )

        print(f"   ✅ Consistency check prompt created ({len(prompt)} chars)")
        print(f"      Preview: {prompt[:200]}...")

        # Check for key elements
        assert "Context Editor Agent" in prompt
        assert "consistency" in prompt.lower()
        assert "Chapter 5" in prompt
        assert "Elena" in prompt
        assert "wheelchair" in prompt
        assert "JSON FORMAT" in prompt
        print(f"   ✅ All key consistency check elements present")
    except Exception as e:
        print(f"   ❌ Failed to create consistency check prompt: {e}")
        return

    # Test 3: Create choice generation prompt
    print("\n3. Creating choice generation prompt...")
    try:
        # Mock narrative ending
        narrative = """The emergency klaxons screamed through the corridors of Deep Space Station Aurora.

Elena Storm gripped the wheels of her chair, propelling herself forward with practiced speed. The mysterious signal was growing stronger, emanating from the abandoned section of the station.

She paused at the sealed bulkhead, her security override card in hand. Whatever was on the other side had been dormant for years. But now it was waking up.

The choice was hers."""

        prompt = create_choice_generation_prompt(
            world_template=world_template,
            chapter_number=1,
            narrative=narrative,
            story_bible=story_bible,
            chapter_beat_plan=chapter_beat_plan,
            ssba_guidance={"current_story_beat": "opening_image"}
        )

        print(f"   ✅ Choice generation prompt created ({len(prompt)} chars)")
        print(f"      Preview: {prompt[:200]}...")

        # Check for key elements
        assert "Context Editor Agent" in prompt
        assert "player choices" in prompt.lower()
        assert "Chapter 1" in prompt
        assert "The choice was hers" in prompt  # From narrative ending
        assert "JSON FORMAT" in prompt
        assert "choices" in prompt
        print(f"   ✅ All key choice generation elements present")
    except Exception as e:
        print(f"   ❌ Failed to create choice generation prompt: {e}")
        return

    # Test 4: Verify consistency check JSON format
    print("\n4. Verifying consistency check JSON format...")
    try:
        assert "consistency_status" in prompt or "consistency_status" in prompt
        assert "minor_issues" in prompt
        assert "major_contradictions" in prompt
        assert "guidance_for_prose_agent" in prompt
        assert "inconsistency_flags" in prompt
        print(f"   ✅ Consistency check JSON format specified")
    except Exception as e:
        print(f"   ❌ Failed JSON format verification: {e}")
        return

    # Test 5: Verify choice generation JSON format
    print("\n5. Verifying choice generation JSON format...")
    try:
        # Create a fresh choice prompt to check
        prompt = create_choice_generation_prompt(
            world_template=world_template,
            chapter_number=1,
            narrative=narrative,
            story_bible=story_bible
        )

        assert "choices" in prompt
        assert "choice_type" in prompt
        assert "thematic_direction" in prompt
        assert "character_arc_impact" in prompt
        assert "story_beat_alignment" in prompt
        assert "choice_rationale" in prompt
        print(f"   ✅ Choice generation JSON format specified")
    except Exception as e:
        print(f"   ❌ Failed choice format verification: {e}")
        return

    # Test 6: Verify CEA guidance principles
    print("\n6. Verifying CEA decision principles...")
    try:
        consistency_prompt = create_consistency_check_prompt(
            chapter_number=1,
            chapter_beat_plan=chapter_beat_plan,
            story_bible=story_bible,
            consistency_report=consistency_report
        )

        assert "Auto-Fix" in consistency_prompt or "auto-fix" in consistency_prompt.lower()
        assert "Player Agency" in consistency_prompt
        assert "Established Canon" in consistency_prompt or "canon" in consistency_prompt.lower()
        assert "Plot Opportunities" in consistency_prompt or "plot" in consistency_prompt.lower()
        print(f"   ✅ CEA decision principles present")
    except Exception as e:
        print(f"   ❌ Failed principles verification: {e}")
        return

    # Test 7: Verify choice quality guidelines
    print("\n7. Verifying choice quality guidelines...")
    try:
        choice_prompt = create_choice_generation_prompt(
            world_template=world_template,
            chapter_number=1,
            narrative=narrative,
            story_bible=story_bible
        )

        # Good choices guidelines
        assert "meaningful" in choice_prompt.lower()
        assert "dilemma" in choice_prompt.lower() or "consequences" in choice_prompt.lower()

        # Avoid guidelines
        assert "break established canon" in choice_prompt.lower() or "canon" in choice_prompt.lower()
        assert "wheelchair user" in choice_prompt.lower() or "limitations" in choice_prompt.lower()

        print(f"   ✅ Choice quality guidelines present")
    except Exception as e:
        print(f"   ❌ Failed guidelines verification: {e}")
        return

    print("\n" + "=" * 60)
    print("🎉 All CEA Prompt Tests Passed!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(test_cea_prompts())
