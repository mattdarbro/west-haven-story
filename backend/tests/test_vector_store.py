"""
Tests for new multi-agent RAG infrastructure (VectorStore + EntityExtractor).

Run with: python -m pytest backend/tests/test_vector_store.py -v
Or run manually: python backend/tests/test_vector_store.py
"""

import pytest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from backend.rag.vector_store import VectorStore
from backend.rag.entity_extractor import EntityExtractor


class TestVectorStore:
    """Tests for VectorStore class."""

    def test_initialization(self):
        """Test that vector store can be initialized."""
        vs = VectorStore(persist_directory="./test_chroma_db")
        assert vs is not None
        assert vs.client is not None

    def test_collection_creation(self):
        """Test creating a collection for a session."""
        vs = VectorStore(persist_directory="./test_chroma_db")
        vs.get_or_create_collection("test_session_123")

        assert vs.collection is not None
        assert vs.collection_name == "story_test_session_123"

    def test_add_and_query_paragraphs(self):
        """Test adding paragraphs and querying them."""
        vs = VectorStore(persist_directory="./test_chroma_db")
        vs.get_or_create_collection("test_session_456")

        # Add test paragraphs
        paragraphs = [
            "Charlie wheeled through the corridor, noticing the oxygen readings were fluctuating wildly.",
            "Lieutenant Torres stood in the control room, analyzing the mysterious signal from deep space.",
            "Dr. Sarah Chen had departed on the supply shuttle three days ago, leaving the station understaffed."
        ]

        metadata = [
            {"chapter_number": 1, "characters": ["Charlie"], "locations": ["corridor"]},
            {"chapter_number": 1, "characters": ["Torres"], "locations": ["control room"]},
            {"chapter_number": 1, "characters": ["Dr. Chen"], "locations": ["shuttle"]}
        ]

        chunks_added = vs.add_paragraph_chunks(paragraphs, chapter_number=1, metadata_list=metadata)
        assert chunks_added == 3

        # Query for Charlie
        results = vs.query_similar("Charlie wheelchair", n_results=2)
        assert len(results["documents"]) > 0
        assert "Charlie" in results["documents"][0]

        # Query for Torres
        results = vs.query_similar("Torres signal", n_results=2)
        assert len(results["documents"]) > 0
        assert "Torres" in results["documents"][0]

    def test_collection_count(self):
        """Test getting collection count."""
        vs = VectorStore(persist_directory="./test_chroma_db")
        vs.get_or_create_collection("test_session_count")

        # Initially empty
        assert vs.get_collection_count() == 0

        # Add some paragraphs
        paragraphs = ["Test paragraph 1.", "Test paragraph 2."]
        vs.add_paragraph_chunks(paragraphs, chapter_number=1)

        # Should have 2 chunks
        assert vs.get_collection_count() == 2


class TestEntityExtractor:
    """Tests for EntityExtractor class."""

    def test_paragraph_splitting(self):
        """Test splitting narrative into paragraphs."""
        narrative = """The emergency klaxons screamed through the corridors of Deep Space Station Aurora.

Charlie Chen gripped the wheels of her chair, propelling herself forward with practiced speed.

In the control room, Lieutenant Torres looked up from the console, his face grave."""

        paragraphs = EntityExtractor.split_into_paragraphs(narrative)

        assert len(paragraphs) == 3
        assert "klaxons" in paragraphs[0]
        assert "Charlie" in paragraphs[1]
        assert "Torres" in paragraphs[2]

    def test_entity_extraction_simple(self):
        """Test simple entity extraction."""
        text = "Charlie wheeled to the control room where Lieutenant Torres was waiting. The station's oxygen system was failing."

        entities = EntityExtractor.extract_entities_simple(text)

        assert "characters" in entities
        assert len(entities["characters"]) > 0

    def test_paragraph_metadata_creation(self):
        """Test creating metadata for paragraph chunks."""
        paragraph = "Charlie wheeled through the corridor."
        entities = {"characters": ["Charlie"], "locations": ["corridor"]}

        metadata = EntityExtractor.create_paragraph_metadata(
            paragraph=paragraph,
            paragraph_number=5,
            chapter_number=3,
            entities=entities
        )

        assert metadata["chapter_number"] == 3
        assert metadata["paragraph_number"] == 5
        assert "Charlie" in metadata["characters"]
        assert "corridor" in metadata["locations"]


# Cleanup
@pytest.fixture(autouse=True)
def cleanup():
    """Cleanup test database after each test."""
    yield
    # Reset test collections after each test
    try:
        vs = VectorStore(persist_directory="./test_chroma_db")
        vs.reset_all()
    except:
        pass  # Ignore cleanup errors


if __name__ == "__main__":
    # Run a quick manual test
    print("🧪 Running RAG infrastructure manual test...")
    print()

    vs = VectorStore(persist_directory="./test_chroma_db")
    vs.get_or_create_collection("manual_test")

    paragraphs = [
        "Charlie used a wheelchair after the accident in Chapter 3.",
        "Torres was working in engineering on the life support systems.",
        "The mysterious signal pulsed at 2.4 GHz frequency."
    ]

    print("Adding paragraphs to vector store...")
    vs.add_paragraph_chunks(paragraphs, chapter_number=5)

    # Query
    print("\nQuerying for 'wheelchair'...")
    results = vs.query_similar("wheelchair", n_results=2)
    print(f"Results:")
    for i, doc in enumerate(results["documents"], 1):
        print(f"  {i}. {doc}")

    # Query for contradiction checking
    print("\nQuerying for 'Charlie walking'...")
    results = vs.query_similar("Charlie walking running", n_results=2)
    print(f"Results (should find wheelchair contradiction):")
    for i, doc in enumerate(results["documents"], 1):
        print(f"  {i}. {doc}")

    # Cleanup
    vs.reset_all()
    print("\n✅ Manual test complete!")
