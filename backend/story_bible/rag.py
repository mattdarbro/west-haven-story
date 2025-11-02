"""
RAG (Retrieval-Augmented Generation) system for story bible context.

This module implements the core RAG pipeline using ChromaDB for vector storage
and OpenAI embeddings. It enables consistent storytelling by retrieving relevant
lore, characters, and locations from the story bible.
"""

from pathlib import Path
from typing import Optional
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStoreRetriever

from backend.config import config


class StoryBibleRAG:
    """
    RAG system for story bible retrieval.

    Loads markdown story bibles, chunks them semantically by headers,
    embeds them, and provides context-aware retrieval for narrative generation.
    """

    def __init__(self, world_id: str):
        """
        Initialize RAG system for a specific story world.

        Args:
            world_id: Identifier for the story world (e.g., "tfogwf")
        """
        self.world_id = world_id
        self.embeddings = OpenAIEmbeddings(
            model=config.EMBEDDING_MODEL,
            openai_api_key=config.OPENAI_API_KEY
        )

        # Configure markdown splitter to preserve structure
        self.splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=[
                ("#", "section"),      # Top-level sections (Metadata, Characters, etc.)
                ("##", "category"),    # Categories (Character: Elena, Location: Citadel)
                ("###", "entity")      # Specific entities (traits, relationships)
            ],
            strip_headers=False  # Keep headers for context
        )

        self.vectorstore: Optional[Chroma] = None
        self._collection_name = f"{world_id}_bible"

    def load_and_index(self, bible_path: str | Path) -> None:
        """
        Load story bible from markdown file and create vector index.

        Args:
            bible_path: Path to the story bible markdown file

        Raises:
            FileNotFoundError: If bible file doesn't exist
            ValueError: If bible content is empty
        """
        bible_path = Path(bible_path)

        if not bible_path.exists():
            raise FileNotFoundError(f"Story bible not found: {bible_path}")

        # Load and split markdown by headers
        markdown_text = bible_path.read_text(encoding="utf-8")

        if not markdown_text.strip():
            raise ValueError(f"Story bible is empty: {bible_path}")

        docs = self.splitter.split_text(markdown_text)

        if not docs:
            raise ValueError(f"No documents extracted from bible: {bible_path}")

        # Enrich documents with metadata
        for doc in docs:
            doc.metadata.update({
                "world_id": self.world_id,
                "source": "story_bible",
                "bible_path": str(bible_path)
            })

            # Add section info to page_content for better retrieval
            section_info = []
            if "section" in doc.metadata:
                section_info.append(f"Section: {doc.metadata['section']}")
            if "category" in doc.metadata:
                section_info.append(f"Category: {doc.metadata['category']}")
            if "entity" in doc.metadata:
                section_info.append(f"Entity: {doc.metadata['entity']}")

            if section_info:
                doc.page_content = "\n".join(section_info) + "\n\n" + doc.page_content

        # Create vector store with persistence
        persist_dir = Path(config.chroma_persist_directory) / self.world_id
        persist_dir.mkdir(parents=True, exist_ok=True)

        self.vectorstore = Chroma.from_documents(
            documents=docs,
            embedding=self.embeddings,
            collection_name=self._collection_name,
            persist_directory=str(persist_dir)
        )

        print(f"✓ Indexed {len(docs)} document chunks for world '{self.world_id}'")

    def load_existing_index(self) -> None:
        """
        Load previously created vector index from disk.

        Raises:
            FileNotFoundError: If no index exists for this world
        """
        persist_dir = Path(config.chroma_persist_directory) / self.world_id

        if not persist_dir.exists():
            raise FileNotFoundError(
                f"No existing index found for world '{self.world_id}'. "
                f"Call load_and_index() first."
            )

        self.vectorstore = Chroma(
            collection_name=self._collection_name,
            embedding_function=self.embeddings,
            persist_directory=str(persist_dir)
        )

        print(f"✓ Loaded existing index for world '{self.world_id}'")

    def get_retriever(
        self,
        beat_number: Optional[int] = None,
        search_type: Optional[str] = None
    ) -> VectorStoreRetriever:
        """
        Get a configured retriever for context-aware queries.

        Args:
            beat_number: Current story beat (for beat-specific filtering)
            search_type: Override default search type ("mmr" or "similarity")

        Returns:
            Configured retriever ready for queries

        Raises:
            ValueError: If vectorstore hasn't been loaded
        """
        if self.vectorstore is None:
            raise ValueError(
                "Vectorstore not initialized. Call load_and_index() or load_existing_index() first."
            )

        search_type = search_type or config.RAG_SEARCH_TYPE

        # Build metadata filter
        metadata_filter = {"world_id": self.world_id}

        # Note: Beat-specific filtering could be added here if beats are tagged in bible
        # if beat_number:
        #     metadata_filter["beat"] = beat_number

        return self.vectorstore.as_retriever(
            search_type=search_type,
            search_kwargs={
                "k": config.RAG_RETRIEVAL_K,
                "fetch_k": config.RAG_FETCH_K,
                "filter": metadata_filter
            }
        )

    async def aretrieve(
        self,
        query: str,
        beat_number: Optional[int] = None
    ) -> str:
        """
        Asynchronously retrieve relevant context for a query.

        Args:
            query: Search query (typically current user input or beat context)
            beat_number: Current story beat for context-aware retrieval

        Returns:
            Formatted context string ready for LLM prompt
        """
        retriever = self.get_retriever(beat_number=beat_number)
        docs = await retriever.ainvoke(query)

        if not docs:
            return "No relevant context found in story bible."

        # Format documents with section headers
        formatted_chunks = []
        for doc in docs:
            header_info = []
            if "section" in doc.metadata:
                header_info.append(doc.metadata["section"])
            if "category" in doc.metadata:
                header_info.append(doc.metadata["category"])

            header = " > ".join(header_info) if header_info else "Context"
            formatted_chunks.append(f"[{header}]\n{doc.page_content}")

        return "\n\n---\n\n".join(formatted_chunks)

    def retrieve(
        self,
        query: str,
        beat_number: Optional[int] = None
    ) -> str:
        """
        Synchronously retrieve relevant context for a query.

        Args:
            query: Search query
            beat_number: Current story beat

        Returns:
            Formatted context string
        """
        retriever = self.get_retriever(beat_number=beat_number)
        docs = retriever.invoke(query)

        if not docs:
            return "No relevant context found in story bible."

        # Format documents
        formatted_chunks = []
        for doc in docs:
            header_info = []
            if "section" in doc.metadata:
                header_info.append(doc.metadata["section"])
            if "category" in doc.metadata:
                header_info.append(doc.metadata["category"])

            header = " > ".join(header_info) if header_info else "Context"
            formatted_chunks.append(f"[{header}]\n{doc.page_content}")

        return "\n\n---\n\n".join(formatted_chunks)

    def get_collection_stats(self) -> dict:
        """
        Get statistics about the indexed collection.

        Returns:
            Dictionary with collection metrics
        """
        if self.vectorstore is None:
            return {"error": "Vectorstore not initialized"}

        collection = self.vectorstore._collection
        return {
            "world_id": self.world_id,
            "collection_name": self._collection_name,
            "document_count": collection.count(),
            "embedding_model": config.EMBEDDING_MODEL,
            "search_type": config.RAG_SEARCH_TYPE,
            "retrieval_k": config.RAG_RETRIEVAL_K
        }


# ===== Factory Pattern for Multi-World Support =====

class StoryWorldFactory:
    """
    Factory for managing multiple story worlds.

    Ensures only one RAG instance per world (singleton pattern per world).
    """

    _worlds: dict[str, StoryBibleRAG] = {}

    @classmethod
    def get_world(cls, world_id: str, auto_load: bool = True) -> StoryBibleRAG:
        """
        Get or create RAG instance for a story world.

        Args:
            world_id: World identifier
            auto_load: If True, attempt to load existing index

        Returns:
            RAG instance for the world
        """
        if world_id not in cls._worlds:
            rag = StoryBibleRAG(world_id)

            if auto_load:
                try:
                    rag.load_existing_index()
                except FileNotFoundError:
                    # Index doesn't exist yet - will need to call load_and_index()
                    print(f"No existing index for '{world_id}' - needs initialization")

            cls._worlds[world_id] = rag

        return cls._worlds[world_id]

    @classmethod
    def list_worlds(cls) -> list[str]:
        """
        List all available story worlds based on bible files.

        Returns:
            List of world IDs (bible filenames without extension)
        """
        bibles_dir = Path("bibles")
        if not bibles_dir.exists():
            return []

        return [
            bible.stem for bible in bibles_dir.glob("*.md")
            if bible.stem != "template"  # Exclude template file
        ]

    @classmethod
    def initialize_world(cls, world_id: str, bible_path: Optional[Path] = None) -> StoryBibleRAG:
        """
        Initialize a new world by indexing its bible.

        Args:
            world_id: World identifier
            bible_path: Path to bible file (defaults to bibles/{world_id}.md)

        Returns:
            Initialized RAG instance
        """
        if bible_path is None:
            bible_path = Path("bibles") / f"{world_id}.md"

        rag = StoryBibleRAG(world_id)
        rag.load_and_index(bible_path)
        cls._worlds[world_id] = rag

        return rag
