"""
Unit tests for RAG system.
"""

import pytest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from backend.story_bible.rag import StoryBibleRAG, StoryWorldFactory
from backend.config import config


@pytest.fixture
def tfogwf_bible_path():
    """Path to TFOGWF story bible."""
    return Path("bibles/tfogwf.md")


@pytest.fixture
def rag_instance(tfogwf_bible_path):
    """Create a RAG instance for testing."""
    rag = StoryBibleRAG("tfogwf_test")

    if tfogwf_bible_path.exists():
        rag.load_and_index(tfogwf_bible_path)
    else:
        pytest.skip("TFOGWF bible not found")

    return rag


class TestStoryBibleRAG:
    """Tests for StoryBibleRAG class."""

    def test_initialization(self):
        """Test RAG initialization."""
        rag = StoryBibleRAG("test_world")
        assert rag.world_id == "test_world"
        assert rag.vectorstore is None

    def test_load_and_index(self, tfogwf_bible_path):
        """Test loading and indexing a story bible."""
        if not tfogwf_bible_path.exists():
            pytest.skip("TFOGWF bible not found")

        rag = StoryBibleRAG("tfogwf_test")
        rag.load_and_index(tfogwf_bible_path)

        assert rag.vectorstore is not None

        stats = rag.get_collection_stats()
        assert stats["world_id"] == "tfogwf_test"
        assert stats["document_count"] > 0

    def test_retrieval_quality(self, rag_instance):
        """Test that retrieval returns relevant results."""
        query = "Tell me about Elena Storm"
        results = rag_instance.retrieve(query, beat_number=1)

        assert len(results) > 0
        assert "Elena" in results or "protagonist" in results

    def test_beat_specific_retrieval(self, rag_instance):
        """Test beat-specific retrieval."""
        query = "What happens in Beat 1?"
        results = rag_instance.retrieve(query, beat_number=1)

        assert len(results) > 0
        assert "Beat 1" in results or "Awakening" in results

    def test_character_retrieval(self, rag_instance):
        """Test character information retrieval."""
        query = "Who is The Shadow?"
        results = rag_instance.retrieve(query)

        assert len(results) > 0
        assert "Shadow" in results


class TestStoryWorldFactory:
    """Tests for StoryWorldFactory."""

    def test_list_worlds(self):
        """Test listing available worlds."""
        worlds = StoryWorldFactory.list_worlds()
        assert isinstance(worlds, list)

        # Should include TFOGWF if bible exists
        if Path("bibles/tfogwf.md").exists():
            assert "tfogwf" in worlds

    def test_get_world_singleton(self):
        """Test that factory returns same instance."""
        world1 = StoryWorldFactory.get_world("test_singleton", auto_load=False)
        world2 = StoryWorldFactory.get_world("test_singleton", auto_load=False)

        assert world1 is world2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
