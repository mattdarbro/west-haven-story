"""
Vector store wrapper for Chroma DB.

Provides methods to:
- Initialize collection for a story session
- Add paragraph chunks with metadata
- Query for similar content
- Manage collection lifecycle
"""

import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any, Optional
import os


class VectorStore:
    """Wrapper for ChromaDB operations."""

    def __init__(self, persist_directory: str = "./chroma_db"):
        """
        Initialize ChromaDB client.

        Args:
            persist_directory: Directory to store Chroma data
        """
        # Create persist directory if it doesn't exist
        os.makedirs(persist_directory, exist_ok=True)

        # Initialize Chroma client with persistence
        self.client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )

        self.collection = None
        self.collection_name = None

    def get_or_create_collection(self, session_id: str) -> None:
        """
        Get or create a collection for a story session.

        Args:
            session_id: Unique session identifier
        """
        collection_name = f"story_{session_id}"
        self.collection_name = collection_name

        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"session_id": session_id}
        )

        print(f"✓ Vector store collection ready: {collection_name}")

    def add_paragraph_chunks(
        self,
        paragraphs: List[str],
        chapter_number: int,
        metadata_list: Optional[List[Dict[str, Any]]] = None
    ) -> int:
        """
        Add paragraph chunks to the vector store.

        Args:
            paragraphs: List of paragraph texts
            chapter_number: Current chapter number
            metadata_list: Optional list of metadata dicts (one per paragraph)

        Returns:
            Number of chunks added
        """
        if not self.collection:
            raise ValueError("Collection not initialized. Call get_or_create_collection() first.")

        if not paragraphs:
            return 0

        # Generate IDs for chunks
        ids = [f"ch{chapter_number}_p{i}" for i in range(len(paragraphs))]

        # Prepare metadata
        if metadata_list is None:
            metadata_list = [{"chapter_number": chapter_number} for _ in paragraphs]
        else:
            # Ensure chapter_number is in metadata
            for meta in metadata_list:
                meta["chapter_number"] = chapter_number

        # Add to collection
        self.collection.add(
            documents=paragraphs,
            metadatas=metadata_list,
            ids=ids
        )

        print(f"✓ Indexed {len(paragraphs)} paragraphs from Chapter {chapter_number}")
        return len(paragraphs)

    def query_similar(
        self,
        query_text: str,
        n_results: int = 5,
        where_filter: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Query for similar content in the vector store.

        Args:
            query_text: Text to search for
            n_results: Number of results to return
            where_filter: Optional metadata filter (e.g., {"chapter_number": {"$lt": 10}})

        Returns:
            Dict with 'documents', 'metadatas', 'distances', 'ids'
        """
        if not self.collection:
            raise ValueError("Collection not initialized. Call get_or_create_collection() first.")

        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_results,
            where=where_filter
        )

        # Flatten results (query_texts is a list, but we only query one)
        return {
            "documents": results["documents"][0] if results["documents"] else [],
            "metadatas": results["metadatas"][0] if results["metadatas"] else [],
            "distances": results["distances"][0] if results["distances"] else [],
            "ids": results["ids"][0] if results["ids"] else []
        }

    def get_collection_count(self) -> int:
        """Get total number of chunks in collection."""
        if not self.collection:
            return 0
        return self.collection.count()

    def delete_collection(self, session_id: str) -> None:
        """
        Delete a collection (e.g., when story session ends).

        Args:
            session_id: Session identifier
        """
        collection_name = f"story_{session_id}"
        try:
            self.client.delete_collection(name=collection_name)
            print(f"✓ Deleted vector store collection: {collection_name}")
        except ValueError:
            print(f"⚠️  Collection {collection_name} does not exist")

    def reset_all(self) -> None:
        """
        Reset all collections (use with caution - mainly for testing).
        """
        self.client.reset()
        print("⚠️  All vector store collections deleted")
