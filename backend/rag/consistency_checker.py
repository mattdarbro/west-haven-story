"""
Consistency Checker for CEA (Context Editor Agent).

This module helps CEA detect potential contradictions by querying the RAG
vector store for relevant narrative history before prose generation.
"""

from typing import List, Dict, Any, Optional
from backend.rag.vector_store import VectorStore


class ConsistencyChecker:
    """
    Checks narrative consistency using RAG vector store.

    The consistency checker queries the story's vector store to find
    potentially contradictory information before generating new narrative.
    """

    def __init__(self, session_id: str, vector_store: Optional[VectorStore] = None):
        """
        Initialize consistency checker.

        Args:
            session_id: Story session ID
            vector_store: Optional pre-initialized VectorStore
        """
        self.session_id = session_id
        self.vector_store = vector_store or VectorStore()
        self.vector_store.get_or_create_collection(session_id)

    def check_character_consistency(
        self,
        character_name: str,
        proposed_action: str,
        n_results: int = 5
    ) -> Dict[str, Any]:
        """
        Check if a proposed character action contradicts established facts.

        Args:
            character_name: Name of character
            proposed_action: The action they're about to perform
            n_results: Number of similar chunks to retrieve

        Returns:
            Dict with:
                - relevant_history: List of relevant past mentions
                - potential_contradictions: List of potential issues
                - risk_level: "none", "low", "medium", "high"
        """
        query = f"{character_name} {proposed_action}"
        results = self.vector_store.query_similar(query, n_results=n_results)

        relevant_history = []
        potential_contradictions = []

        if results["documents"]:
            for doc, metadata in zip(results["documents"], results["metadatas"]):
                relevant_history.append({
                    "text": doc,
                    "chapter": metadata.get("chapter_number", "?"),
                    "distance": metadata.get("distance", 0)
                })

        # Simple heuristic for contradiction detection
        risk_level = "none"
        if len(relevant_history) > 0:
            risk_level = "low"  # Default if history exists

        return {
            "relevant_history": relevant_history,
            "potential_contradictions": potential_contradictions,
            "risk_level": risk_level,
            "query_used": query
        }

    def check_location_consistency(
        self,
        location: str,
        character_name: str = None,
        n_results: int = 5
    ) -> Dict[str, Any]:
        """
        Check location consistency for character/scene.

        Args:
            location: The location being used
            character_name: Optional character to check location for
            n_results: Number of similar chunks to retrieve

        Returns:
            Dict with relevant_history and risk assessment
        """
        if character_name:
            query = f"{character_name} at {location}"
        else:
            query = f"location {location}"

        results = self.vector_store.query_similar(query, n_results=n_results)

        relevant_history = []
        if results["documents"]:
            for doc, metadata in zip(results["documents"], results["metadatas"]):
                relevant_history.append({
                    "text": doc,
                    "chapter": metadata.get("chapter_number", "?"),
                    "distance": metadata.get("distance", 0)
                })

        return {
            "relevant_history": relevant_history,
            "risk_level": "low" if len(relevant_history) > 0 else "none",
            "query_used": query
        }

    def check_plot_element_consistency(
        self,
        plot_element: str,
        n_results: int = 5
    ) -> Dict[str, Any]:
        """
        Check consistency for plot elements (objects, events, facts).

        Args:
            plot_element: Description of plot element to check
            n_results: Number of similar chunks to retrieve

        Returns:
            Dict with relevant_history and risk assessment
        """
        results = self.vector_store.query_similar(plot_element, n_results=n_results)

        relevant_history = []
        if results["documents"]:
            for doc, metadata in zip(results["documents"], results["metadatas"]):
                relevant_history.append({
                    "text": doc,
                    "chapter": metadata.get("chapter_number", "?"),
                    "distance": metadata.get("distance", 0)
                })

        return {
            "relevant_history": relevant_history,
            "risk_level": "low" if len(relevant_history) > 0 else "none",
            "query_used": plot_element
        }

    def batch_consistency_check(
        self,
        checks: List[Dict[str, str]],
        n_results: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Perform multiple consistency checks at once.

        Args:
            checks: List of dicts with "type" and "query" keys
                Example: [
                    {"type": "character", "character": "Charlie", "action": "walking"},
                    {"type": "location", "location": "engineering bay"}
                ]
            n_results: Number of results per check

        Returns:
            List of check results
        """
        results = []

        for check in checks:
            check_type = check.get("type", "plot")

            if check_type == "character":
                result = self.check_character_consistency(
                    character_name=check.get("character", ""),
                    proposed_action=check.get("action", ""),
                    n_results=n_results
                )
            elif check_type == "location":
                result = self.check_location_consistency(
                    location=check.get("location", ""),
                    character_name=check.get("character"),
                    n_results=n_results
                )
            else:  # plot
                result = self.check_plot_element_consistency(
                    plot_element=check.get("query", ""),
                    n_results=n_results
                )

            results.append(result)

        return results

    def extract_key_entities_from_beat_plan(
        self,
        chapter_beat_plan: Dict[str, Any]
    ) -> List[str]:
        """
        Extract key entities from CBA's chapter beat plan for consistency checking.

        Args:
            chapter_beat_plan: CBA's beat plan with chapter_beats array

        Returns:
            List of entity queries to check
        """
        queries = []

        # Extract from beat descriptions
        beats = chapter_beat_plan.get("chapter_beats", [])
        for beat in beats:
            description = beat.get("description", "")
            key_elements = beat.get("key_elements", [])

            if description:
                queries.append(description)

            queries.extend(key_elements)

        # Add chapter goal and tension
        if "chapter_goal" in chapter_beat_plan:
            queries.append(chapter_beat_plan["chapter_goal"])

        if "chapter_tension" in chapter_beat_plan:
            queries.append(chapter_beat_plan["chapter_tension"])

        return queries[:10]  # Limit to top 10 most important

    def get_consistency_report(
        self,
        chapter_beat_plan: Dict[str, Any],
        story_bible: Dict[str, Any],
        max_queries: int = 5
    ) -> Dict[str, Any]:
        """
        Generate a comprehensive consistency report for CEA.

        Args:
            chapter_beat_plan: CBA's chapter beat plan
            story_bible: Current story bible
            max_queries: Maximum number of RAG queries to perform

        Returns:
            Consistency report with:
                - checks_performed: List of checks
                - relevant_history: Combined relevant narrative history
                - risk_flags: Any high-risk contradictions
                - overall_risk: "none", "low", "medium", "high"
        """
        # Extract key entities to check
        queries = self.extract_key_entities_from_beat_plan(chapter_beat_plan)[:max_queries]

        checks = [{"type": "plot", "query": q} for q in queries]
        check_results = self.batch_consistency_check(checks)

        # Aggregate results
        all_relevant_history = []
        risk_flags = []
        max_risk = "none"

        for result in check_results:
            all_relevant_history.extend(result.get("relevant_history", []))

            # Track highest risk level
            risk = result.get("risk_level", "none")
            if risk == "high":
                max_risk = "high"
            elif risk == "medium" and max_risk != "high":
                max_risk = "medium"
            elif risk == "low" and max_risk == "none":
                max_risk = "low"

        # Deduplicate history by text
        seen = set()
        unique_history = []
        for item in all_relevant_history:
            text = item["text"]
            if text not in seen:
                seen.add(text)
                unique_history.append(item)

        # Sort by chapter (most recent first)
        unique_history.sort(key=lambda x: x.get("chapter", 0), reverse=True)

        return {
            "checks_performed": [r.get("query_used", "") for r in check_results],
            "relevant_history": unique_history[:15],  # Top 15 most relevant
            "risk_flags": risk_flags,
            "overall_risk": max_risk,
            "total_checks": len(check_results)
        }
