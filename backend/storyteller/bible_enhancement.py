"""
Story Bible Enhancement - AI expands minimal user input into rich story worlds.

Takes simple user input (genre + 1-2 sentences) and creates detailed story bible.
"""

import json
from typing import Dict, Any
from langchain_core.messages import HumanMessage
from langchain_anthropic import ChatAnthropic
from backend import config


async def enhance_story_bible(
    genre: str,
    user_setting: str,
    character_name: str = None,
    user_id: str = None
) -> Dict[str, Any]:
    """
    Take minimal user input and expand into a rich story bible.

    Args:
        genre: Genre selected by user (scifi, mystery, romance, etc.)
        user_setting: User's 1-2 sentence setting description
        character_name: Optional character name provided by user
        user_id: Optional user ID for personalization

    Returns:
        Enhanced story bible with full details
    """

    # Create enhancement prompt
    prompt = f"""You are a creative writing assistant helping to expand a story world.

The user wants {genre} stories and provided this setting:
"{user_setting}"

{f'They want the main character named: {character_name}' if character_name else 'Create an interesting protagonist name.'}

Your task: Expand this minimal input into a rich, detailed story bible that will enable consistent, engaging stories.

Return a JSON object with the following structure:

```json
{{
  "genre": "{genre}",
  "setting": {{
    "name": "Brief name for this world/setting",
    "description": "2-3 detailed paragraphs expanding on the user's setting. Add atmosphere, sensory details, key locations, tone. Make it vivid and specific.",
    "key_locations": [
      {{"name": "Location 1", "description": "Brief description"}},
      {{"name": "Location 2", "description": "Brief description"}}
    ],
    "atmosphere": "The overall mood and feel of this world",
    "rules": "Any important rules of this world (tech level, magic system, social norms, etc.)"
  }},
  "protagonist": {{
    "name": "{character_name if character_name else 'Choose an interesting name'}",
    "role": "Their job, position, or main identity",
    "age_range": "Approximate age (e.g., 'late 20s', 'middle-aged', 'young adult')",
    "key_traits": ["trait1", "trait2", "trait3"],
    "defining_characteristic": "One unique trait or limitation that makes them interesting (physical, emotional, or situational)",
    "background": "Brief backstory (2-3 sentences)",
    "motivation": "What drives them generally",
    "voice": "How they speak/think (cynical, optimistic, analytical, emotional, etc.)"
  }},
  "supporting_characters": [
    {{
      "name": "Character 2 name",
      "role": "Their role/job",
      "relationship_to_protagonist": "How they relate to the protagonist",
      "personality": "2-3 word personality descriptor",
      "purpose": "Their narrative purpose (mentor, foil, ally, comic relief, etc.)"
    }},
    {{
      "name": "Character 3 name",
      "role": "Their role/job",
      "relationship_to_protagonist": "How they relate to the protagonist",
      "personality": "2-3 word personality descriptor",
      "purpose": "Their narrative purpose"
    }}
  ],
  "tone": "The emotional tone of stories (tense, hopeful, mysterious, light, dark, heartwarming, etc.)",
  "themes": ["theme1", "theme2", "theme3"],
  "story_style": "Brief description of what makes these stories distinctive"
}}
```

Guidelines:
1. **Be specific**: "Space station" → "Deep Space Station Aurora, a crumbling research outpost on the edge of charted space"
2. **Add depth**: Give characters flaws, quirks, history
3. **Create contrast**: Support characters should complement/contrast with protagonist
4. **Establish tone**: Match the genre expectations
5. **Interesting limitation**: Give protagonist something that makes stories richer (disability, personality trait, situation)
6. **Internal consistency**: Everything should fit together logically

Make this feel like a real, lived-in world that can sustain many different stories.
"""

    try:
        # Initialize LLM
        llm = ChatAnthropic(
            model=config.MODEL_NAME,
            temperature=0.8,  # Creative expansion
            max_tokens=3000,
            anthropic_api_key=config.ANTHROPIC_API_KEY,
            timeout=45.0,
        )

        # Get enhancement
        response = await llm.ainvoke([HumanMessage(content=prompt)])
        response_text = response.content.strip()

        # Clean markdown if present
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0].strip()

        # Parse JSON
        enhanced_bible = json.loads(response_text)

        # Add metadata
        enhanced_bible["user_input"] = {
            "genre": genre,
            "setting": user_setting,
            "character_name": character_name
        }

        # Initialize tracking fields
        enhanced_bible["story_history"] = {
            "total_stories": 0,
            "recent_plot_types": [],
            "recent_summaries": [],
            "used_cameos": [],
            "last_cliffhanger": None
        }

        enhanced_bible["user_preferences"] = {
            "ratings": [],
            "liked_elements": [],
            "disliked_elements": [],
            "pacing_preference": "medium",
            "action_level": "medium",
            "emotional_depth": "medium"
        }

        return enhanced_bible

    except json.JSONDecodeError as e:
        print(f"Failed to parse enhanced bible JSON: {e}")
        print(f"Response: {response_text[:500]}")

        # Return minimal fallback
        return create_fallback_bible(genre, user_setting, character_name)

    except Exception as e:
        print(f"Error enhancing bible: {e}")
        import traceback
        traceback.print_exc()

        return create_fallback_bible(genre, user_setting, character_name)


def create_fallback_bible(genre: str, user_setting: str, character_name: str = None) -> Dict[str, Any]:
    """
    Create a minimal fallback bible if AI enhancement fails.
    """
    return {
        "genre": genre,
        "setting": {
            "name": "Your World",
            "description": user_setting,
            "key_locations": [],
            "atmosphere": genre,
            "rules": "Standard genre conventions"
        },
        "protagonist": {
            "name": character_name or "Alex",
            "role": "Protagonist",
            "age_range": "adult",
            "key_traits": ["determined", "curious", "resourceful"],
            "defining_characteristic": "Quick thinking",
            "background": "To be developed",
            "motivation": "Solve problems and help others",
            "voice": "thoughtful"
        },
        "supporting_characters": [],
        "tone": genre,
        "themes": [genre, "adventure", "discovery"],
        "story_style": f"{genre.capitalize()} stories in this world",
        "user_input": {
            "genre": genre,
            "setting": user_setting,
            "character_name": character_name
        },
        "story_history": {
            "total_stories": 0,
            "recent_plot_types": [],
            "recent_summaries": [],
            "used_cameos": [],
            "last_cliffhanger": None
        },
        "user_preferences": {
            "ratings": [],
            "liked_elements": [],
            "disliked_elements": [],
            "pacing_preference": "medium",
            "action_level": "medium",
            "emotional_depth": "medium"
        }
    }


def add_cameo_characters(bible: Dict[str, Any], cameos: list[Dict[str, str]]) -> Dict[str, Any]:
    """
    Add cameo characters to an existing bible.

    Args:
        bible: Existing story bible
        cameos: List of cameo character dicts with 'name' and 'description'

    Returns:
        Updated bible with cameos
    """
    if "cameo_characters" not in bible:
        bible["cameo_characters"] = []

    for cameo in cameos:
        bible["cameo_characters"].append({
            "name": cameo.get("name", "Unknown"),
            "description": cameo.get("description", ""),
            "frequency": cameo.get("frequency", "sometimes"),  # rarely, sometimes, often
            "appearances": 0  # Track how many times they've appeared
        })

    return bible


def update_story_history(
    bible: Dict[str, Any],
    story_summary: str,
    plot_type: str,
    rating: int = None,
    feedback: Dict[str, Any] = None
) -> Dict[str, Any]:
    """
    Update bible with new story history.

    Args:
        bible: Story bible to update
        story_summary: Brief summary of the story
        plot_type: Type of plot used
        rating: User rating (1-5)
        feedback: User feedback dict

    Returns:
        Updated bible
    """
    history = bible.get("story_history", {})

    # Increment total
    history["total_stories"] = history.get("total_stories", 0) + 1

    # Add to recent summaries (keep last 7)
    summaries = history.get("recent_summaries", [])
    summaries.append(story_summary)
    history["recent_summaries"] = summaries[-7:]

    # Track plot types (keep last 10)
    plots = history.get("recent_plot_types", [])
    plots.append(plot_type)
    history["recent_plot_types"] = plots[-10:]

    bible["story_history"] = history

    # Update preferences if rating provided
    if rating is not None:
        prefs = bible.get("user_preferences", {})
        ratings = prefs.get("ratings", [])
        ratings.append(rating)
        prefs["ratings"] = ratings[-20:]  # Keep last 20 ratings

        # Update preferences based on feedback
        if feedback and rating >= 4:
            # High rating - track what they liked
            liked = prefs.get("liked_elements", [])
            if "great_pacing" in feedback:
                liked.append("fast_pacing")
            if "loved_characters" in feedback:
                liked.append("character_focus")
            if "good_mystery" in feedback:
                liked.append("mystery_elements")
            if "surprising_twist" in feedback:
                liked.append("plot_twists")
            if "emotional_moments" in feedback:
                liked.append("emotional_depth")
            prefs["liked_elements"] = liked[-20:]

        elif feedback and rating <= 2:
            # Low rating - track what they disliked
            disliked = prefs.get("disliked_elements", [])
            if "too_slow" in feedback:
                disliked.append("slow_pacing")
                prefs["pacing_preference"] = "fast"
            if "not_enough_action" in feedback:
                disliked.append("low_action")
                prefs["action_level"] = "high"
            if "characters_felt_off" in feedback:
                disliked.append("character_inconsistency")
            prefs["disliked_elements"] = disliked[-20:]

        bible["user_preferences"] = prefs

    return bible


def should_use_cliffhanger(bible: Dict[str, Any], tier: str) -> bool:
    """
    Determine if this story should end on a cliffhanger (free tier only).

    Pattern: Stories 5, 11, 17, 23 (every 6 after first 4)

    Args:
        bible: Story bible with history
        tier: User tier (free, premium)

    Returns:
        True if should use cliffhanger
    """
    if tier != "free":
        return False

    story_count = bible.get("story_history", {}).get("total_stories", 0)

    # First 4 stories: always complete
    if story_count < 4:
        return False

    # Every 6th story after that: cliffhanger
    return (story_count - 4) % 6 == 0


def should_include_cameo(bible: Dict[str, Any]) -> Dict[str, Any]:
    """
    Decide if a cameo should appear and which one.

    Args:
        bible: Story bible with cameo characters

    Returns:
        Cameo character dict if should include, None otherwise
    """
    import random

    cameos = bible.get("cameo_characters", [])

    if not cameos:
        return None

    # Check each cameo's frequency
    for cameo in cameos:
        frequency = cameo.get("frequency", "sometimes")
        appearances = cameo.get("appearances", 0)

        # Frequency thresholds
        frequencies = {
            "rarely": 0.15,    # ~15% of stories
            "sometimes": 0.3,  # ~30% of stories
            "often": 0.6       # ~60% of stories
        }

        threshold = frequencies.get(frequency, 0.3)

        if random.random() < threshold:
            # Select this cameo
            cameo["appearances"] = appearances + 1
            return cameo

    return None
