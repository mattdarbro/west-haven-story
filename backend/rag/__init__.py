"""
RAG (Retrieval-Augmented Generation) module for story consistency checking.

This module provides:
- Vector store operations (Chroma)
- Entity extraction from narrative text
- Consistency checking via similarity search
"""

from backend.rag.vector_store import VectorStore
from backend.rag.entity_extractor import EntityExtractor

__all__ = ["VectorStore", "EntityExtractor"]
