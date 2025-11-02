#!/usr/bin/env python3
"""
Manual test script for complete story flow.

This script tests the entire storytelling pipeline:
1. Initialize RAG
2. Create state machine
3. Generate opening narrative
4. Process player choice
5. Continue story

Usage:
    python scripts/test_story_flow.py [world_id]

Examples:
    python scripts/test_story_flow.py              # Uses default (tfogwf)
    python scripts/test_story_flow.py west_haven   # Tests West Haven story
    python scripts/test_story_flow.py tfogwf       # Tests TFOGWF story
"""

import sys
import asyncio
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.story_bible.rag import StoryWorldFactory
from backend.storyteller.graph import create_persistent_graph, run_story_turn
from backend.models.state import create_initial_state
from backend.config import config


async def test_complete_flow(world_id: str = "tfogwf"):
    """Test the complete storytelling flow."""

    print("=" * 70)
    print("STORYTELLER SYSTEM TEST")
    print("=" * 70)

    # Step 1: Initialize RAG
    print(f"\n[1/5] Initializing RAG for {world_id.upper()}...")
    try:
        bible_path = Path("bibles") / f"{world_id}.md"

        if not bible_path.exists():
            print(f"❌ Error: Bible not found at {bible_path}")
            return False

        rag = StoryWorldFactory.initialize_world(world_id, bible_path)
        stats = rag.get_collection_stats()

        print(f"✓ RAG initialized")
        print(f"  Documents indexed: {stats.get('document_count', 'unknown')}")
        print(f"  Search type: {stats.get('search_type', 'unknown')}")

    except Exception as e:
        print(f"❌ RAG initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return False

    # Step 2: Create state machine
    print("\n[2/5] Creating LangGraph state machine...")
    try:
        graph = create_persistent_graph("test_story.db")
        print("✓ State machine created")

    except Exception as e:
        print(f"❌ State machine creation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

    # Step 3: Create initial state
    print("\n[3/5] Creating initial story state...")
    try:
        initial_state = create_initial_state(
            user_id="test-user-123",
            world_id=world_id,
            credits=25
        )
        print("✓ Initial state created")
        print(f"  User: {initial_state['user_id']}")
        print(f"  World: {initial_state['world_id']}")
        print(f"  Beat: {initial_state['current_beat']}")
        print(f"  Credits: {initial_state['credits_remaining']}")

    except Exception as e:
        print(f"❌ State creation failed: {e}")
        return False

    # Step 4: Generate opening narrative
    print("\n[4/5] Generating opening narrative...")
    print("  (This may take 5-10 seconds...)")
    try:
        session_id = "test-session-001"

        final_state, outputs = await run_story_turn(
            graph=graph,
            user_input="Begin the story",
            session_id=session_id,
            current_state=initial_state
        )

        print("✓ Opening narrative generated")
        print("\n" + "=" * 70)
        print("NARRATIVE:")
        print("=" * 70)
        print(outputs["narrative"])
        print("\n" + "=" * 70)
        print("CHOICES:")
        print("=" * 70)
        for i, choice in enumerate(outputs["choices"], 1):
            print(f"{i}. {choice['text']}")
            print(f"   → {choice.get('consequence_hint', '')}")

        print("\n" + "=" * 70)
        print("METADATA:")
        print("=" * 70)
        print(f"Beat: {outputs['current_beat']}")
        print(f"Beat Complete: {outputs['beat_complete']}")
        print(f"Credits: {outputs['credits_remaining']}")
        if outputs.get('image_url'):
            print(f"Image: {outputs['image_url']}")
        if outputs.get('error'):
            print(f"⚠️  Error: {outputs['error']}")

    except Exception as e:
        print(f"❌ Narrative generation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

    # Step 5: Continue with a choice
    print("\n[5/5] Testing story continuation...")
    print("  Making choice 1...")
    print("  (This may take 5-10 seconds...)")
    try:
        # Simulate choosing first option
        choice_text = outputs["choices"][0]["text"] if outputs["choices"] else "Investigate"

        final_state, outputs = await run_story_turn(
            graph=graph,
            user_input=f"Player chose: {choice_text}",
            session_id=session_id,
            current_state=None  # Will load from checkpoint
        )

        print("✓ Story continued")
        print("\n" + "=" * 70)
        print("NARRATIVE (Continued):")
        print("=" * 70)
        print(outputs["narrative"])
        print("\n" + "=" * 70)
        print("NEW CHOICES:")
        print("=" * 70)
        for i, choice in enumerate(outputs["choices"], 1):
            print(f"{i}. {choice['text']}")

        print("\n" + "=" * 70)
        print(f"Beat: {outputs['current_beat']}")
        print(f"Credits: {outputs['credits_remaining']}")

    except Exception as e:
        print(f"❌ Story continuation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

    # Success!
    print("\n" + "=" * 70)
    print("✓ ALL TESTS PASSED!")
    print("=" * 70)
    print("\nThe storytelling system is working correctly.")
    print("You can now:")
    print("  1. Run the API: python backend/api/main.py")
    print("  2. Test endpoints with Postman or curl")
    print("  3. Build the frontend")

    return True


def main():
    """Main entry point."""
    # Check if OpenAI API key is set
    if config.OPENAI_API_KEY == "your-openai-api-key-here":
        print("=" * 70)
        print("❌ ERROR: OpenAI API key not set")
        print("=" * 70)
        print("\nPlease update your .env file with a valid OPENAI_API_KEY")
        print("Example:")
        print("  OPENAI_API_KEY=sk-...")
        print("\nThen run this script again.")
        sys.exit(1)

    # Get world_id from command line or use default
    world_id = sys.argv[1] if len(sys.argv) > 1 else "tfogwf"

    print(f"Testing world: {world_id}")
    print()

    # Run async test
    success = asyncio.run(test_complete_flow(world_id))

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
