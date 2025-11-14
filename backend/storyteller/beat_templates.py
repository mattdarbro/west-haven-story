"""
Beat templates for different genres and story lengths.

Each template defines the structure for a complete standalone story.
"""

from typing import List, Dict, Any


class BeatTemplate:
    """A beat template defines the structure for a story."""

    def __init__(
        self,
        name: str,
        genre: str,
        total_words: int,
        beats: List[Dict[str, Any]],
        description: str = ""
    ):
        self.name = name
        self.genre = genre
        self.total_words = total_words
        self.beats = beats
        self.description = description

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "genre": self.genre,
            "total_words": self.total_words,
            "beats": self.beats,
            "description": self.description
        }


# ===== FREE TIER TEMPLATES (1500 words) =====

FREE_SCIFI_TEMPLATE = BeatTemplate(
    name="scifi_short",
    genre="sci-fi",
    total_words=1500,
    description="Concise sci-fi story with discovery and resolution",
    beats=[
        {
            "beat_number": 1,
            "beat_name": "opening_hook",
            "word_target": 400,
            "description": "Establish setting and protagonist, introduce intriguing element",
            "guidance": "Ground reader in sci-fi world. Present protagonist's normal. Hint at mystery/problem."
        },
        {
            "beat_number": 2,
            "beat_name": "discovery",
            "word_target": 450,
            "description": "Protagonist discovers or encounters the core mystery/problem",
            "guidance": "Raise stakes. Show protagonist's reaction. Complicate the situation."
        },
        {
            "beat_number": 3,
            "beat_name": "crisis",
            "word_target": 400,
            "description": "Problem intensifies, protagonist must make a choice",
            "guidance": "Peak tension. Protagonist faces decision or realization."
        },
        {
            "beat_number": 4,
            "beat_name": "resolution",
            "word_target": 250,
            "description": "Resolution of immediate problem, with emotional or thematic closure",
            "guidance": "Satisfy story question. Emotional landing. Hint at larger world continuing."
        }
    ]
)

FREE_MYSTERY_TEMPLATE = BeatTemplate(
    name="mystery_short",
    genre="mystery",
    total_words=1500,
    description="Quick mystery with clue discovery and solution",
    beats=[
        {
            "beat_number": 1,
            "beat_name": "incident",
            "word_target": 350,
            "description": "Present the mystery or crime",
            "guidance": "Establish what's wrong. Introduce detective/protagonist."
        },
        {
            "beat_number": 2,
            "beat_name": "investigation",
            "word_target": 500,
            "description": "Gather clues, interview, discover leads",
            "guidance": "Show protagonist's method. Plant clues for reader. Red herring optional."
        },
        {
            "beat_number": 3,
            "beat_name": "revelation",
            "word_target": 400,
            "description": "Key insight or breakthrough",
            "guidance": "Protagonist connects the dots. Aha moment."
        },
        {
            "beat_number": 4,
            "beat_name": "solution",
            "word_target": 250,
            "description": "Mystery solved, explanation",
            "guidance": "Reveal answer. Show protagonist's satisfaction or reflection."
        }
    ]
)

FREE_ROMANCE_TEMPLATE = BeatTemplate(
    name="romance_short",
    genre="romance",
    total_words=1500,
    description="Sweet romantic moment or connection",
    beats=[
        {
            "beat_number": 1,
            "beat_name": "setup",
            "word_target": 400,
            "description": "Introduce characters and situation",
            "guidance": "Show protagonist's emotional state. Set up meeting or interaction."
        },
        {
            "beat_number": 2,
            "beat_name": "connection",
            "word_target": 450,
            "description": "Romantic interaction or deepening bond",
            "guidance": "Chemistry, vulnerability, or shared moment. Show attraction/connection."
        },
        {
            "beat_number": 3,
            "beat_name": "complication",
            "word_target": 400,
            "description": "Obstacle or misunderstanding",
            "guidance": "Something threatens the connection. Internal or external conflict."
        },
        {
            "beat_number": 4,
            "beat_name": "resolution",
            "word_target": 250,
            "description": "Overcome obstacle, emotional payoff",
            "guidance": "Vulnerability wins. Sweet or hopeful ending. Connection strengthened."
        }
    ]
)


# ===== PREMIUM TIER TEMPLATES (4500 words) =====

PREMIUM_SCIFI_ADVENTURE = BeatTemplate(
    name="scifi_adventure_full",
    genre="sci-fi",
    total_words=4500,
    description="Full sci-fi adventure with world-building and action",
    beats=[
        {
            "beat_number": 1,
            "beat_name": "opening_hook",
            "word_target": 500,
            "description": "Establish world, protagonist, and normal",
            "guidance": "Rich world-building. Show protagonist's skills/personality. Hint at adventure to come."
        },
        {
            "beat_number": 2,
            "beat_name": "inciting_incident",
            "word_target": 500,
            "description": "Call to adventure or problem emerges",
            "guidance": "Disrupt the normal. Present the challenge. Show stakes."
        },
        {
            "beat_number": 3,
            "beat_name": "rising_action",
            "word_target": 500,
            "description": "Protagonist engages, complications arise",
            "guidance": "Active protagonist. Obstacles emerge. World expands."
        },
        {
            "beat_number": 4,
            "beat_name": "first_revelation",
            "word_target": 500,
            "description": "Discovery or twist that changes understanding",
            "guidance": "New information. Paradigm shift. Stakes raise."
        },
        {
            "beat_number": 5,
            "beat_name": "midpoint_crisis",
            "word_target": 600,
            "description": "Major setback or challenge",
            "guidance": "All seems lost OR false victory. Emotional low or high."
        },
        {
            "beat_number": 6,
            "beat_name": "renewed_push",
            "word_target": 600,
            "description": "Protagonist adapts, new approach",
            "guidance": "Character growth. New strategy. Building to climax."
        },
        {
            "beat_number": 7,
            "beat_name": "climax",
            "word_target": 500,
            "description": "Confrontation or final challenge",
            "guidance": "Peak action/tension. Protagonist uses what they've learned."
        },
        {
            "beat_number": 8,
            "beat_name": "resolution",
            "word_target": 500,
            "description": "Immediate aftermath and victory/outcome",
            "guidance": "Show results. Emotional payoff. Consequences."
        },
        {
            "beat_number": 9,
            "beat_name": "denouement",
            "word_target": 300,
            "description": "Return to new normal, reflection",
            "guidance": "Show growth. Thematic closure. World continues."
        }
    ]
)

PREMIUM_MYSTERY_NOIR = BeatTemplate(
    name="mystery_noir_full",
    genre="mystery",
    total_words=4500,
    description="Full noir mystery with investigation and twists",
    beats=[
        {
            "beat_number": 1,
            "beat_name": "setup",
            "word_target": 500,
            "description": "Introduce detective and world",
            "guidance": "Noir atmosphere. Show detective's life/personality."
        },
        {
            "beat_number": 2,
            "beat_name": "case_arrives",
            "word_target": 500,
            "description": "Crime or mystery presented",
            "guidance": "The hook. Why this case matters. Initial details."
        },
        {
            "beat_number": 3,
            "beat_name": "first_clues",
            "word_target": 500,
            "description": "Investigation begins, gather evidence",
            "guidance": "Detective method. Plant clues. Introduce suspects."
        },
        {
            "beat_number": 4,
            "beat_name": "red_herring",
            "word_target": 500,
            "description": "False lead or misdirection",
            "guidance": "Seems promising but wrong. Keep reader guessing."
        },
        {
            "beat_number": 5,
            "beat_name": "complication",
            "word_target": 600,
            "description": "New crime, threat, or setback",
            "guidance": "Stakes raise. Detective in danger or case gets personal."
        },
        {
            "beat_number": 6,
            "beat_name": "breakthrough",
            "word_target": 600,
            "description": "Key insight or evidence found",
            "guidance": "Pieces come together. Detective sees the pattern."
        },
        {
            "beat_number": 7,
            "beat_name": "confrontation",
            "word_target": 500,
            "description": "Confront culprit or reveal truth",
            "guidance": "Tension peaks. Truth comes out. Danger."
        },
        {
            "beat_number": 8,
            "beat_name": "resolution",
            "word_target": 500,
            "description": "Case closed, justice or consequence",
            "guidance": "Wrap up loose ends. Show outcome."
        },
        {
            "beat_number": 9,
            "beat_name": "reflection",
            "word_target": 300,
            "description": "Detective reflects, returns to life",
            "guidance": "Noir wisdom. Thematic landing. Bitter or sweet."
        }
    ]
)

PREMIUM_ROMANCE_FULL = BeatTemplate(
    name="romance_full",
    genre="romance",
    total_words=4500,
    description="Complete romantic arc with emotional depth",
    beats=[
        {
            "beat_number": 1,
            "beat_name": "introduction",
            "word_target": 500,
            "description": "Introduce protagonist and their world",
            "guidance": "Show protagonist's life, emotional state, desires."
        },
        {
            "beat_number": 2,
            "beat_name": "meet_cute",
            "word_target": 500,
            "description": "First meeting or meaningful interaction",
            "guidance": "Chemistry. Spark. Interesting dynamic."
        },
        {
            "beat_number": 3,
            "beat_name": "growing_connection",
            "word_target": 500,
            "description": "Spend time together, bond deepens",
            "guidance": "Vulnerability. Shared moments. Attraction builds."
        },
        {
            "beat_number": 4,
            "beat_name": "first_barrier",
            "word_target": 500,
            "description": "Internal resistance or external obstacle",
            "guidance": "Fear, past hurt, circumstances. Tension."
        },
        {
            "beat_number": 5,
            "beat_name": "turning_point",
            "word_target": 600,
            "description": "Breakthrough moment or confession",
            "guidance": "Emotional honesty. Risk taken. Relationship shifts."
        },
        {
            "beat_number": 6,
            "beat_name": "complication",
            "word_target": 600,
            "description": "Misunderstanding or serious obstacle",
            "guidance": "Something threatens to tear them apart. Dark night."
        },
        {
            "beat_number": 7,
            "beat_name": "realization",
            "word_target": 500,
            "description": "Character growth, understanding what matters",
            "guidance": "Internal change. Clarity about feelings."
        },
        {
            "beat_number": 8,
            "beat_name": "grand_gesture",
            "word_target": 500,
            "description": "One or both take decisive action",
            "guidance": "Vulnerability. Risk. Putting it all on the line."
        },
        {
            "beat_number": 9,
            "beat_name": "resolution",
            "word_target": 300,
            "description": "Together, emotional payoff",
            "guidance": "Satisfying ending. Hope or happiness. New beginning."
        }
    ]
)

PREMIUM_SITCOM_STYLE = BeatTemplate(
    name="sitcom_full",
    genre="sitcom",
    total_words=4500,
    description="Comedy with escalating chaos and warm resolution",
    beats=[
        {
            "beat_number": 1,
            "beat_name": "normal_day",
            "word_target": 500,
            "description": "Establish characters and normal situation",
            "guidance": "Show relationships. Light humor. Set baseline."
        },
        {
            "beat_number": 2,
            "beat_name": "disruption",
            "word_target": 500,
            "description": "Something goes wrong or unusual happens",
            "guidance": "Comic premise. Small problem that will escalate."
        },
        {
            "beat_number": 3,
            "beat_name": "attempted_fix",
            "word_target": 500,
            "description": "Try to solve it, makes it worse",
            "guidance": "Character flaws cause problems. Escalation."
        },
        {
            "beat_number": 4,
            "beat_name": "escalation",
            "word_target": 500,
            "description": "Problem grows, more chaos",
            "guidance": "Snowball effect. Multiple characters involved."
        },
        {
            "beat_number": 5,
            "beat_name": "peak_chaos",
            "word_target": 600,
            "description": "Everything falls apart hilariously",
            "guidance": "Maximum comedy. Multiple threads colliding."
        },
        {
            "beat_number": 6,
            "beat_name": "moment_of_truth",
            "word_target": 600,
            "description": "Honest moment amidst the chaos",
            "guidance": "Heart. Character insight. Why we care."
        },
        {
            "beat_number": 7,
            "beat_name": "resolution",
            "word_target": 500,
            "description": "Problem solved or accepted",
            "guidance": "Fix it together. Teamwork or acceptance."
        },
        {
            "beat_number": 8,
            "beat_name": "new_normal",
            "word_target": 500,
            "description": "Return to normalish, lessons learned",
            "guidance": "Back to baseline but slightly changed."
        },
        {
            "beat_number": 9,
            "beat_name": "tag",
            "word_target": 300,
            "description": "Callback joke or sweet moment",
            "guidance": "Button on the episode. Warm ending."
        }
    ]
)


# ===== TEMPLATE REGISTRY =====

TEMPLATES = {
    # Free tier (1500 words)
    "free_scifi": FREE_SCIFI_TEMPLATE,
    "free_mystery": FREE_MYSTERY_TEMPLATE,
    "free_romance": FREE_ROMANCE_TEMPLATE,

    # Premium tier (4500 words)
    "premium_scifi": PREMIUM_SCIFI_ADVENTURE,
    "premium_mystery": PREMIUM_MYSTERY_NOIR,
    "premium_romance": PREMIUM_ROMANCE_FULL,
    "premium_sitcom": PREMIUM_SITCOM_STYLE,
}


def get_template(genre: str, tier: str = "free") -> BeatTemplate:
    """
    Get the appropriate beat template based on genre and user tier.

    Args:
        genre: Genre of story (scifi, mystery, romance, sitcom, etc.)
        tier: User tier (free, premium)

    Returns:
        BeatTemplate for the story
    """
    # Normalize inputs
    genre = genre.lower().replace("-", "").replace("_", "")
    tier = tier.lower()

    # Map common variations
    genre_map = {
        "scifi": "scifi",
        "sciencefiction": "scifi",
        "mystery": "mystery",
        "detective": "mystery",
        "noir": "mystery",
        "romance": "romance",
        "love": "romance",
        "sitcom": "sitcom",
        "comedy": "sitcom",
    }

    normalized_genre = genre_map.get(genre, "scifi")

    # Build template key
    if tier == "premium":
        template_key = f"premium_{normalized_genre}"
    else:
        template_key = f"free_{normalized_genre}"

    # Get template or fall back to default
    template = TEMPLATES.get(template_key)

    if not template:
        # Fallback to free scifi if nothing matches
        template = TEMPLATES["free_scifi"]

    return template


def list_available_genres(tier: str = "free") -> List[str]:
    """
    List available genres for a given tier.

    Args:
        tier: User tier (free, premium)

    Returns:
        List of available genre names
    """
    if tier == "premium":
        return ["scifi", "mystery", "romance", "sitcom"]
    else:
        return ["scifi", "mystery", "romance"]
