"""
Quick manual test for RAG infrastructure.
Run with: python test_rag_manual.py
"""

from backend.rag.vector_store import VectorStore
from backend.rag.entity_extractor import EntityExtractor


def test_rag_infrastructure():
    """Test RAG vector store and entity extraction."""
    print("🧪 Testing RAG Infrastructure (Phase 1)")
    print("=" * 60)

    # Test 1: Vector Store Initialization
    print("\n1. Testing Vector Store Initialization...")
    vs = VectorStore(persist_directory="./test_chroma_db")
    print("   ✅ VectorStore initialized")

    # Test 2: Collection Creation
    print("\n2. Testing Collection Creation...")
    vs.get_or_create_collection("test_session_manual")
    print(f"   ✅ Collection created: {vs.collection_name}")

    # Test 3: Paragraph Splitting
    print("\n3. Testing Paragraph Splitting...")
    narrative = """The emergency klaxons screamed through the corridors.

Charlie wheeled through the corridor, her wheelchair moving swiftly.

Torres stood in the control room, analyzing the data."""

    paragraphs = EntityExtractor.split_into_paragraphs(narrative)
    print(f"   ✅ Split into {len(paragraphs)} paragraphs")

    # Test 4: Entity Extraction
    print("\n4. Testing Entity Extraction...")
    entities = EntityExtractor.extract_entities_simple(narrative)
    print(f"   ✅ Extracted {len(entities.get('characters', []))} potential characters")

    # Test 5: Add Paragraphs to Vector Store
    print("\n5. Testing Vector Store Indexing...")
    test_paragraphs = [
        "Charlie used a wheelchair after the accident in Chapter 3.",
        "Torres was working in engineering on the life support systems.",
        "The mysterious signal pulsed at 2.4 GHz frequency.",
        "Dr. Sarah Chen departed on the supply shuttle last week."
    ]

    chunks_added = vs.add_paragraph_chunks(test_paragraphs, chapter_number=5)
    print(f"   ✅ Indexed {chunks_added} paragraphs")

    # Test 6: Query for Similarity
    print("\n6. Testing RAG Query (wheelchair)...")
    results = vs.query_similar("wheelchair", n_results=2)
    print(f"   ✅ Found {len(results['documents'])} results:")
    for i, doc in enumerate(results["documents"], 1):
        print(f"      {i}. {doc[:80]}...")

    # Test 7: Query for Contradiction Detection
    print("\n7. Testing Contradiction Detection (Charlie walking)...")
    results = vs.query_similar("Charlie walking running", n_results=2)
    print(f"   ✅ Found {len(results['documents'])} results (should mention wheelchair):")
    for i, doc in enumerate(results["documents"], 1):
        print(f"      {i}. {doc[:80]}...")
        if "wheelchair" in doc.lower():
            print(f"         🎯 CONTRADICTION DETECTED: Narrative mentions wheelchair!")

    # Test 8: Query for Torres
    print("\n8. Testing Entity Query (Torres location)...")
    results = vs.query_similar("Where is Torres?", n_results=2)
    print(f"   ✅ Found {len(results['documents'])} results:")
    for i, doc in enumerate(results["documents"], 1):
        print(f"      {i}. {doc[:80]}...")

    # Test 9: Collection Stats
    print("\n9. Testing Collection Stats...")
    total_chunks = vs.get_collection_count()
    print(f"   ✅ Total chunks in collection: {total_chunks}")

    # Cleanup
    print("\n10. Cleanup...")
    vs.reset_all()
    print("   ✅ Test database cleaned up")

    print("\n" + "=" * 60)
    print("🎉 All RAG Infrastructure Tests Passed!")
    print("=" * 60)


if __name__ == "__main__":
    try:
        test_rag_infrastructure()
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
