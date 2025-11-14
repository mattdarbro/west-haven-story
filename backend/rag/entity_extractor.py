"""
Entity extraction from narrative text.

Extracts:
- Characters mentioned
- Locations mentioned
- Key objects/items
- Important facts/events
- Themes/emotions
"""

from typing import List, Dict, Any
import re


class EntityExtractor:
    """Extract entities from narrative text for RAG indexing and querying."""

    @staticmethod
    def split_into_paragraphs(narrative: str) -> List[str]:
        """
        Split narrative into paragraph chunks.

        Args:
            narrative: Full narrative text

        Returns:
            List of paragraph strings
        """
        # Split on double newlines (paragraph breaks)
        paragraphs = re.split(r'\n\s*\n', narrative)

        # Clean up whitespace and filter empty paragraphs
        paragraphs = [p.strip() for p in paragraphs if p.strip()]

        return paragraphs

    @staticmethod
    def extract_entities_simple(text: str) -> Dict[str, List[str]]:
        """
        Simple entity extraction using pattern matching.

        This is a basic implementation. For production, consider using:
        - Spacy NER
        - LLM-based extraction
        - Custom trained models

        Args:
            text: Text to extract entities from

        Returns:
            Dict with entity types as keys and lists of entities as values
        """
        entities = {
            "characters": [],
            "locations": [],
            "objects": [],
            "themes": []
        }

        # Basic pattern matching for capitalized words (potential names/places)
        # This is simplified - real implementation should use NER or LLM
        capitalized_words = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text)

        # Remove common words that aren't entities
        common_words = {
            "The", "A", "An", "In", "On", "At", "To", "For", "Of", "With",
            "Chapter", "She", "He", "They", "It", "This", "That", "These", "Those"
        }

        potential_entities = [word for word in capitalized_words if word not in common_words]

        # For now, treat all as potential characters/locations
        # A real implementation would classify them properly
        entities["characters"] = list(set(potential_entities))

        return entities

    @staticmethod
    async def extract_entities_llm(text: str, llm) -> Dict[str, Any]:
        """
        Extract entities using an LLM (more accurate than pattern matching).

        Args:
            text: Text to extract entities from
            llm: ChatAnthropic instance

        Returns:
            Dict with extracted entities and metadata
        """
        from langchain_core.messages import HumanMessage
        import json

        prompt = f"""Extract key entities from this story text. Return a JSON object with:
- characters: List of character names mentioned
- locations: List of locations/places mentioned
- objects: List of significant objects/items mentioned
- themes: List of emotional themes or moods (e.g., "tension", "hope", "mystery")
- key_facts: List of important facts or events established

Story text:
{text}

Return ONLY valid JSON, no additional text:"""

        response = await llm.ainvoke([HumanMessage(content=prompt)])

        try:
            # Parse JSON response
            entities = json.loads(response.content.strip())
            return entities
        except json.JSONDecodeError:
            # Fallback to simple extraction if LLM doesn't return valid JSON
            print("⚠️  LLM entity extraction failed, falling back to simple extraction")
            return EntityExtractor.extract_entities_simple(text)

    @staticmethod
    def create_paragraph_metadata(
        paragraph: str,
        paragraph_number: int,
        chapter_number: int,
        entities: Dict[str, List[str]]
    ) -> Dict[str, Any]:
        """
        Create metadata for a paragraph chunk.

        Args:
            paragraph: Paragraph text
            paragraph_number: Index of paragraph in chapter
            chapter_number: Chapter number
            entities: Extracted entities

        Returns:
            Metadata dict for vector store
        """
        metadata = {
            "chapter_number": chapter_number,
            "paragraph_number": paragraph_number,
            "word_count": len(paragraph.split()),
            "characters": entities.get("characters", [])[:10],  # Limit to 10
            "locations": entities.get("locations", [])[:5],
            "themes": entities.get("themes", [])[:5]
        }

        return metadata
