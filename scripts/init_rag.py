#!/usr/bin/env python3
"""
Initialize RAG system for a story world.

Usage:
    python scripts/init_rag.py tfogwf
"""

import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.story_bible.rag import StoryWorldFactory


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/init_rag.py <world_id>")
        print("\nAvailable worlds:")
        for world in StoryWorldFactory.list_worlds():
            print(f"  - {world}")
        sys.exit(1)

    world_id = sys.argv[1]
    bible_path = Path("bibles") / f"{world_id}.md"

    if not bible_path.exists():
        print(f"Error: Bible file not found: {bible_path}")
        sys.exit(1)

    print(f"Initializing RAG for world: {world_id}")
    print(f"Bible: {bible_path}")
    print("-" * 50)

    try:
        rag = StoryWorldFactory.initialize_world(world_id, bible_path)

        print("\nCollection Stats:")
        stats = rag.get_collection_stats()
        for key, value in stats.items():
            print(f"  {key}: {value}")

        print("\n" + "=" * 50)
        print("Testing retrieval...")
        print("=" * 50)

        # Test queries
        test_queries = [
            "Tell me about Elena Storm",
            "What is the Void Gate?",
            "What happened in Beat 1?",
        ]

        for query in test_queries:
            print(f"\nQuery: {query}")
            print("-" * 50)
            result = rag.retrieve(query, beat_number=1)
            print(result[:500] + "..." if len(result) > 500 else result)
            print()

        print("✓ RAG initialization successful!")

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
