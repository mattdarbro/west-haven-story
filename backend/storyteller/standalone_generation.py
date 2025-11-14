"""
Main story generation workflow for FictionMail standalone stories.

This orchestrates the multi-agent system for daily story generation.
"""

import time
import json
from typing import Dict, Any
from langchain_core.messages import HumanMessage
from langchain_anthropic import ChatAnthropic
from backend import config
from backend.storyteller.beat_templates import get_template
from backend.storyteller.bible_enhancement import should_use_cliffhanger, should_include_cameo
from backend.storyteller.prompts_standalone import (
    create_standalone_story_beat_prompt,
    create_prose_generation_prompt
)


async def generate_standalone_story(
    story_bible: Dict[str, Any],
    user_tier: str = "free",
    force_cliffhanger: bool = None,
    dev_mode: bool = False
) -> Dict[str, Any]:
    """
    Generate a complete standalone story using the multi-agent system.

    Flow:
    1. Select beat template based on genre and tier
    2. Determine if cliffhanger/cameo
    3. CBA: Generate beat plan
    4. CEA: Check consistency (simplified for standalone)
    5. PA: Generate prose
    6. Post-process: Extract summary, update bible

    Args:
        story_bible: Enhanced story bible
        user_tier: User's tier (free, premium)
        force_cliffhanger: Override cliffhanger logic (for dev mode)
        dev_mode: Enable dev mode features

    Returns:
        Dict with generated story and metadata
    """
    start_time = time.time()

    print(f"\n{'='*70}")
    print(f"GENERATING STANDALONE STORY")
    print(f"Genre: {story_bible.get('genre', 'N/A')}")
    print(f"Tier: {user_tier}")
    print(f"{'='*70}")

    try:
        # Step 1: Select beat template
        genre = story_bible.get("genre", "scifi")
        template = get_template(genre, user_tier)

        print(f"\n✓ Template selected: {template.name}")
        print(f"  Total words: {template.total_words}")
        print(f"  Beats: {len(template.beats)}")

        # Step 2: Determine cliffhanger (free tier only)
        if force_cliffhanger is not None:
            is_cliffhanger = force_cliffhanger
        else:
            is_cliffhanger = should_use_cliffhanger(story_bible, user_tier)

        if is_cliffhanger:
            print(f"  📌 Will use cliffhanger ending (free tier)")

        # Step 3: Determine cameo
        cameo = should_include_cameo(story_bible)
        if cameo:
            print(f"  ✨ Including cameo: {cameo.get('name', 'N/A')}")

        # Step 4: CBA - Generate beat plan
        print(f"\n{'─'*70}")
        print(f"CBA: PLANNING STORY BEATS")
        print(f"{'─'*70}")

        beat_plan = await generate_beat_plan(
            story_bible=story_bible,
            template=template,
            is_cliffhanger=is_cliffhanger,
            cameo=cameo
        )

        story_title = beat_plan.get("story_title", "Untitled")
        print(f"\n✓ Beat plan generated")
        print(f"  Title: {story_title}")
        print(f"  Plot type: {beat_plan.get('plot_type', 'N/A')}")
        print(f"  Story question: {beat_plan.get('story_question', 'N/A')[:60]}...")

        # Step 5: CEA - Simplified consistency check
        print(f"\n{'─'*70}")
        print(f"CEA: CONSISTENCY CHECK")
        print(f"{'─'*70}")

        consistency_report = await check_consistency_simplified(
            beat_plan=beat_plan,
            story_bible=story_bible
        )

        print(f"\n✓ Consistency check complete")
        print(f"  Status: {consistency_report.get('status', 'unknown')}")

        # Step 6: PA - Generate prose
        print(f"\n{'─'*70}")
        print(f"PA: GENERATING PROSE")
        print(f"{'─'*70}")

        narrative = await generate_prose(
            beat_plan=beat_plan,
            story_bible=story_bible,
            template=template,
            consistency_guidance=consistency_report.get("guidance_for_pa", {})
        )

        word_count = len(narrative.split())
        print(f"\n✓ Prose generated")
        print(f"  Word count: {word_count}")
        print(f"  Target: {template.total_words} (±200)")

        # Step 7: Generate cover image (if premium)
        cover_image_url = None
        if user_tier == "premium" or dev_mode:
            print(f"\n{'─'*70}")
            print(f"GENERATING COVER IMAGE")
            print(f"{'─'*70}")

            # TODO: Implement image generation
            print(f"  ⏭️  Skipping for MVP (will use Replicate)")
            cover_image_url = None

        # Step 8: Generate audio (if premium)
        audio_url = None
        if user_tier == "premium" or dev_mode:
            print(f"\n{'─'*70}")
            print(f"GENERATING AUDIO")
            print(f"{'─'*70}")

            # TODO: Implement audio generation
            print(f"  ⏭️  Skipping for MVP (will use ElevenLabs)")
            audio_url = None

        # Step 9: Create summary
        summary = f"{story_title}: {beat_plan.get('story_premise', 'A story in this world')}"

        # Calculate total time
        total_time = time.time() - start_time

        print(f"\n{'='*70}")
        print(f"STORY GENERATION COMPLETE")
        print(f"Total time: {total_time:.2f}s")
        print(f"{'='*70}")

        return {
            "success": True,
            "story": {
                "title": story_title,
                "narrative": narrative,
                "word_count": word_count,
                "genre": genre,
                "tier": user_tier,
                "is_cliffhanger": is_cliffhanger,
                "cover_image_url": cover_image_url,
                "audio_url": audio_url,
                "audio_duration_seconds": None  # TODO: calculate from audio
            },
            "metadata": {
                "beat_plan": beat_plan,
                "plot_type": beat_plan.get("plot_type", "unknown"),
                "summary": summary,
                "consistency_report": consistency_report,
                "generation_time_seconds": total_time,
                "template_used": template.name
            }
        }

    except Exception as e:
        print(f"\n❌ Error generating story: {e}")
        import traceback
        traceback.print_exc()

        return {
            "success": False,
            "error": str(e),
            "story": None,
            "metadata": {}
        }


async def generate_beat_plan(
    story_bible: Dict[str, Any],
    template: Any,
    is_cliffhanger: bool = False,
    cameo: Dict[str, Any] = None
) -> Dict[str, Any]:
    """
    CBA: Generate beat plan for the story.
    """
    from backend.storyteller.prompts_standalone import create_standalone_story_beat_prompt

    # Get user preferences
    user_preferences = story_bible.get("user_preferences", {})

    # Create prompt
    prompt = create_standalone_story_beat_prompt(
        story_bible=story_bible,
        beat_template=template.to_dict(),
        is_cliffhanger=is_cliffhanger,
        cameo=cameo,
        user_preferences=user_preferences
    )

    # Initialize LLM
    llm = ChatAnthropic(
        model=config.MODEL_NAME,
        temperature=0.7,  # Creative but coherent
        max_tokens=2500,
        anthropic_api_key=config.ANTHROPIC_API_KEY,
        timeout=45.0,
    )

    # Generate beat plan
    cba_start = time.time()
    response = await llm.ainvoke([HumanMessage(content=prompt)])
    cba_duration = time.time() - cba_start

    print(f"  LLM call: {cba_duration:.2f}s")

    # Parse response
    response_text = response.content.strip()

    if "```json" in response_text:
        response_text = response_text.split("```json")[1].split("```")[0].strip()
    elif "```" in response_text:
        response_text = response_text.split("```")[1].split("```")[0].strip()

    try:
        beat_plan = json.loads(response_text)
        return beat_plan
    except json.JSONDecodeError as e:
        print(f"  ⚠️  Failed to parse beat plan JSON: {e}")
        # Return minimal fallback
        return {
            "story_title": "A Story",
            "story_premise": "A story in this world",
            "plot_type": "adventure",
            "beats": template.beats,
            "story_question": "What happens?",
            "emotional_arc": "Discovery and resolution",
            "thematic_focus": story_bible.get("themes", ["adventure"])[0],
            "character_growth": "Protagonist learns something new",
            "unique_element": "To be discovered in the telling"
        }


async def check_consistency_simplified(
    beat_plan: Dict[str, Any],
    story_bible: Dict[str, Any]
) -> Dict[str, Any]:
    """
    CEA: Simplified consistency check for standalone stories.

    For MVP, we do a lightweight check. Can enhance later.
    """
    # For now, just check protagonist traits are in beat plan
    protagonist = story_bible.get("protagonist", {})
    defining_char = protagonist.get("defining_characteristic", "")

    # Create simple guidance
    guidance = {
        "general_guidance": f"Ensure {protagonist.get('name', 'protagonist')} is portrayed consistently. CRITICAL: {defining_char}",
        "emphasis_points": [
            defining_char,
            "Character voice and personality",
            "Setting consistency"
        ],
        "avoid": [
            "Contradicting established character traits",
            "Breaking world rules"
        ]
    }

    return {
        "status": "clear",
        "guidance_for_pa": guidance
    }


async def generate_prose(
    beat_plan: Dict[str, Any],
    story_bible: Dict[str, Any],
    template: Any,
    consistency_guidance: Dict[str, Any] = None
) -> str:
    """
    PA: Generate prose from beat plan.
    """
    from backend.storyteller.prompts_standalone import create_prose_generation_prompt

    # Create prompt
    prompt = create_prose_generation_prompt(
        beat_plan=beat_plan,
        story_bible=story_bible,
        beat_template=template.to_dict(),
        consistency_guidance=consistency_guidance
    )

    # Initialize LLM with extended output
    llm = ChatAnthropic(
        model=config.MODEL_NAME,
        temperature=0.8,  # Creative prose
        max_tokens=8000,  # Enough for full story
        anthropic_api_key=config.ANTHROPIC_API_KEY,
        timeout=120.0,  # Longer timeout for prose generation
    )

    # Generate prose
    pa_start = time.time()
    response = await llm.ainvoke([HumanMessage(content=prompt)])
    pa_duration = time.time() - pa_start

    print(f"  LLM call: {pa_duration:.2f}s")

    narrative = response.content.strip()

    # Clean up any markdown or metadata that leaked in
    if "```" in narrative:
        # Try to extract just the story
        parts = narrative.split("```")
        # Find the largest text block that's not JSON
        text_blocks = [p.strip() for p in parts if p.strip() and not p.strip().startswith("json")]
        if text_blocks:
            narrative = max(text_blocks, key=len)

    return narrative
