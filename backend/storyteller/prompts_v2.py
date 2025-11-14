"""
Dynamic prompt templates for continuation-based narrative generation.

This new system uses world templates (your beat design) + Claude improvisation.
No more RAG - just pure generative storytelling within your structure.
"""

import json
from pathlib import Path
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


def load_world_template(world_id: str) -> dict:
    """
    Load world template JSON.

    Args:
        world_id: World identifier (e.g., "west_haven")

    Returns:
        World template dictionary

    Raises:
        FileNotFoundError: If template doesn't exist
    """
    template_path = Path("story_worlds") / world_id / "world_template.json"

    if not template_path.exists():
        raise FileNotFoundError(
            f"World template not found: {template_path}\n"
            f"Please create world_template.json for world '{world_id}'"
        )

    with open(template_path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_beat_info(world_template: dict, beat_number: int) -> dict:
    """
    Extract beat-specific information from template.

    Args:
        world_template: Loaded world template
        beat_number: Current beat number (1-indexed)

    Returns:
        Beat info dictionary
    """
    beat_structure = world_template.get("beat_structure", [])

    # Find the beat (beat numbers in template are 1-indexed)
    for beat in beat_structure:
        if beat.get("beat") == beat_number:
            return beat

    # If beat not found, return generic info
    return {
        "beat": beat_number,
        "name": f"Beat {beat_number}",
        "goal": "Advance the story",
        "emotional_arc": "Continue the journey",
        "turns": 4,
        "key_moments": [],
        "dramatic_questions": []
    }


def create_opening_prompt(world_template: dict) -> ChatPromptTemplate:
    """
    Create prompt for story opening (Beat 1, first turn).

    This is where Claude creates the initial protagonist, love interest,
    and sets up the opening scene based on your beat structure.

    Args:
        world_template: Loaded world template with beat structure

    Returns:
        ChatPromptTemplate for opening
    """
    beat_1 = get_beat_info(world_template, 1)
    world_lore = world_template.get("world_lore", {})
    character_arc = world_template.get("character_arc_template", {})
    narrative_style = world_template.get("narrative_style", {})
    generation_guidelines = world_template.get("generation_guidelines", {})

    pov = narrative_style.get("pov", "third person past tense")
    tone = narrative_style.get("tone", "")

    # Format JSON outside f-string, then escape braces for LangChain template
    guidelines_json = json.dumps(generation_guidelines, indent=2).replace('{', '{{').replace('}', '}}')

    # JSON example as raw string, then escape for LangChain template
    json_example_raw = '''{
  "narrative": "Opening narrative (2-3 paragraphs)",
  "choices": [
    {
      "id": 1,
      "text": "First sentence(s) that continue the narrative...",
      "tone": "cautious/hopeful/defensive/etc"
    },
    {
      "id": 2,
      "text": "Alternative continuation with different tone...",
      "tone": "bold/vulnerable/curious/etc"
    },
    {
      "id": 3,
      "text": "Third continuation option...",
      "tone": "playful/serious/guarded/etc"
    }
  ],
  "image_prompt": "Visual description for image generation",
  "story_bible_update": {
    "protagonist": {
      "name": "Generated name",
      "age": 30,
      "occupation": "Generated occupation",
      "personality": "Key traits",
      "background": "Brief background",
      "current_situation": "Why they're here"
    },
    "locations": {
      "current_location": "Description of where opening takes place"
    },
    "key_events": ["Opening event description"]
  },
  "beat_progress": 0.25
}'''
    # Escape braces for LangChain template ({{ for { and }} for })
    json_example = json_example_raw.replace('{', '{{').replace('}', '}}')

    system_message = f"""You are generating the OPENING of an interactive narrative experience.

WORLD TEMPLATE:
Setting: {world_lore.get("setting", "")}
Themes: {", ".join(world_lore.get("themes", []))}
Tone: {tone}
Point of View: {pov}

BEAT 1: {beat_1.get("name", "Opening")}
Goal: {beat_1.get("goal", "")}
Emotional Arc: {beat_1.get("emotional_arc", "")}
Key Moments: {", ".join(beat_1.get("key_moments", []))}

CHARACTER ARC TEMPLATES:
Protagonist Archetype: {character_arc.get("protagonist", {}).get("archetype", "")}
Starting State: {character_arc.get("protagonist", {}).get("starting_state", "")}
Love Interest Archetype: {character_arc.get("love_interest", {}).get("archetype", "")}

GENERATION GUIDELINES:
{guidelines_json}

🎯 CRITICAL REQUIREMENT: Follow the 6-BEAT CHAPTER STRUCTURE below.
   Each beat is MANDATORY. Do not skip or combine beats.

⚠️  IMPORTANT: You MUST include beat markers in this EXACT format:
   --- BEAT 1: OPENING HOOK ---

   Use this format at the start of each beat section. These markers will be
   automatically removed before showing to readers, but they help you structure
   the chapter properly and ensure you write ALL 6 BEATS AT FULL LENGTH!

📖 CHAPTER STRUCTURE (Write all 6 beats in order with markers):

   --- BEAT 1: OPENING HOOK ---
   (300-400 words) ⚠️ WRITE THE FULL 300-400 WORDS!
   - Immediate sensory detail that pulls reader in
   - Character in action or reaction to situation
   - Set the scene with vivid, specific details
   - Establish mood and atmosphere

   --- BEAT 2: CONTEXT/GROUNDING ---
   (300-400 words) ⚠️ WRITE THE FULL 300-400 WORDS!
   - Character's internal state and thoughts
   - Brief relevant backstory or explanation
   - Establish what's at stake for the character
   - Show character's personality through their perspective

   --- BEAT 3: ESCALATION ---
   (400-500 words) ⚠️ WRITE THE FULL 400-500 WORDS!
   - New information, complication, or discovery
   - Action sequence or meaningful interaction
   - Raise tension or introduce conflict
   - Move the plot forward with specific events

   --- BEAT 4: TURNING POINT ---
   (400-500 words) ⚠️ WRITE THE FULL 400-500 WORDS!
   - The biggest moment of this chapter
   - Character makes a decision or faces a challenge
   - Emotional peak or revelation
   - This is the heart of the chapter - make it count

   --- BEAT 5: AFTERMATH/PROCESSING ---
   (300-400 words) ⚠️ WRITE THE FULL 300-400 WORDS!
   - Character reacts to what just happened
   - New understanding, question, or realization
   - Breathing room with reflection
   - Show impact of the turning point

   --- BEAT 6: CHAPTER ENDING ---
   (300-400 words) ⚠️ WRITE THE FULL 300-400 WORDS!
   - Clear forward momentum into next chapter
   - Hook that makes reader want to continue
   - Leave character in new situation or with new goal
   - End on a strong image or moment

   TOTAL TARGET: 2300-2700 words across all 6 beats

YOUR TASK:
1. CREATE the protagonist (name, age, occupation, personality) based on the archetype

2. WRITE Chapter 1 following the 6-BEAT STRUCTURE above:
   ⚠️  You MUST write all 6 beats in sequence
   ⚠️  Each beat should hit its target word count
   ⚠️  Write in {pov}
   ⚠️  Include dialogue, internal thoughts, sensory details, and action
   ⚠️  Make each beat distinct and purposeful

3. CREATE 3 choice continuations that START the next chapter:
   - Each continuation should be 1-3 sentences that naturally flow into Chapter 2
   - Offer different emotional approaches (cautious, bold, vulnerable, etc.)
   - Make them feel like narrative, not game choices

4. GENERATE an image prompt for the chapter's key scene

5. BUILD initial story bible with protagonist details

CHAPTER PACING:
- This is Chapter 1 of 30 (3% of total story)
- Take time to establish world and character - DON'T RUSH
- Multiple scenes showing character's situation
- Create emotional connection with protagonist
- End with clear stakes and forward momentum

CRITICAL - RESPONSE FORMAT (JSON only, no markdown):
""" + json_example + f"""

Remember:
- NO markdown code blocks
- ⚠️⚠️⚠️ MANDATORY: 2500-2700 WORDS TOTAL - Write FULL LENGTH for EACH beat! ⚠️⚠️⚠️
- Removing beat labels does NOT mean shortening the beats!
- Each beat MUST hit its target word count (300-500 words per beat)
- Write in {pov}
- Make choices feel like story continuations, not buttons
- Keep tone consistent with world template
"""

    return ChatPromptTemplate.from_messages([
        ("system", system_message),
        ("human", "Begin the story.")
    ])


def create_continuation_prompt(
    world_template: dict,
    beat_number: int,
    turns_in_beat: int,
    last_choice_continuation: str,
    generated_story_bible: dict,
    story_summary: list[str],
    chapter_number: int = 1,
    total_chapters: int = 30
) -> ChatPromptTemplate:
    """
    Create prompt for continuing the story after a choice.

    Args:
        world_template: Loaded world template
        beat_number: Current beat number
        turns_in_beat: How many turns we've done in this beat
        last_choice_continuation: The continuation text from selected choice
        generated_story_bible: Claude-generated story details so far
        story_summary: Previous turn summaries
        chapter_number: Current chapter number (1-30)
        total_chapters: Total chapters in story (default: 30)

    Returns:
        ChatPromptTemplate for continuation
    """
    beat_info = get_beat_info(world_template, beat_number)
    world_lore = world_template.get("world_lore", {})
    character_arc = world_template.get("character_arc_template", {})
    narrative_style = world_template.get("narrative_style", {})

    pov = narrative_style.get("pov", "third person past tense")
    tone = narrative_style.get("tone", "")

    max_turns = beat_info.get("turns", 4)
    turns_remaining = max(0, max_turns - turns_in_beat)
    progress = turns_in_beat / max_turns if max_turns > 0 else 0

    # Calculate overall story progress
    story_progress_pct = (chapter_number / total_chapters) * 100
    chapters_remaining = total_chapters - chapter_number

    # Format story summary
    summary_text = "\n".join([f"- {s}" for s in story_summary[-6:]]) if story_summary else "Beginning of story"

    # Format JSON outside f-string, then escape braces for LangChain template
    story_bible_json = json.dumps(generated_story_bible, indent=2).replace('{', '{{').replace('}', '}}')

    # JSON example as raw string, then escape for LangChain template
    json_example_raw = '''{
  "narrative": "2-3 paragraph continuation",
  "choices": [
    {
      "id": 1,
      "text": "First continuation sentence(s)...",
      "tone": "emotional tone"
    },
    {
      "id": 2,
      "text": "Second continuation...",
      "tone": "different tone"
    },
    {
      "id": 3,
      "text": "Third continuation...",
      "tone": "another approach"
    }
  ],
  "image_prompt": "Scene description",
  "story_bible_update": {
    "locations": {},
    "supporting_characters": {},
    "key_events": [],
    "relationships": {}
  },
  "beat_progress": 0.0-1.0
}'''
    # Escape braces for LangChain template ({{ for { and }} for })
    json_example = json_example_raw.replace('{', '{{').replace('}', '}}')

    system_message = f"""You are continuing an interactive narrative experience.

WORLD TEMPLATE:
Setting: {world_lore.get("setting", "")}
Themes: {", ".join(world_lore.get("themes", []))}
Tone: {tone}
Point of View: {pov}

CHAPTER PROGRESS:
📖 Chapter {chapter_number} of {total_chapters}
📊 Story Progress: {int(story_progress_pct)}%
📄 Chapters Remaining: {chapters_remaining}

CURRENT BEAT: {beat_number} - {beat_info.get("name", "")}
Goal: {beat_info.get("goal", "")}
Emotional Arc: {beat_info.get("emotional_arc", "")}
Progress: {turns_in_beat}/{max_turns} turns (approx {int(progress*100)}%)
Success Criteria: {beat_info.get("success_criteria", "")}

STORY SO FAR (Recent Events):
{summary_text}

GENERATED STORY BIBLE:
{story_bible_json}

LAST CHOICE (Continue from here):
"{last_choice_continuation}"

🎯 CRITICAL REQUIREMENT: Follow the 6-BEAT CHAPTER STRUCTURE below.
   Each beat is MANDATORY. Do not skip or combine beats.

⚠️  IMPORTANT: You MUST include beat markers in this EXACT format:
   --- BEAT 1: OPENING HOOK ---

   Use this format at the start of each beat section. These markers will be
   automatically removed before showing to readers, but they help you structure
   the chapter properly and ensure you write ALL 6 BEATS AT FULL LENGTH!

📖 CHAPTER STRUCTURE (Write all 6 beats in order with markers):

   --- BEAT 1: OPENING HOOK ---
   (300-400 words) ⚠️ WRITE THE FULL 300-400 WORDS!
   - Start by seamlessly incorporating the choice continuation text
   - Immediate action or reaction continuing from the choice
   - Vivid sensory details of the current moment
   - Establish the scene and mood

   --- BEAT 2: CONTEXT/DEVELOPMENT ---
   (300-400 words) ⚠️ WRITE THE FULL 300-400 WORDS!
   - Character's thoughts and feelings about current situation
   - Advance the plot thread from last chapter
   - Show character processing or observing
   - Deepen the current situation

   --- BEAT 3: ESCALATION ---
   (400-500 words) ⚠️ WRITE THE FULL 400-500 WORDS!
   - New complication, discovery, or interaction
   - Meaningful dialogue or action sequence
   - Raise stakes or tension
   - Move toward the beat goal: {beat_info.get("goal", "")}

   --- BEAT 4: TURNING POINT ---
   (400-500 words) ⚠️ WRITE THE FULL 400-500 WORDS!
   - The pivotal moment of this chapter
   - Character decision, revelation, or confrontation
   - Emotional climax of the chapter
   - Progress character arc: {character_arc.get("protagonist", {}).get("archetype", "")}

   --- BEAT 5: AFTERMATH/PROCESSING ---
   (300-400 words) ⚠️ WRITE THE FULL 300-400 WORDS!
   - Character reacts to the turning point
   - New understanding or question emerges
   - Show growth or change in character
   - Reflection and breathing room

   --- BEAT 6: CHAPTER ENDING ---
   (300-400 words) ⚠️ WRITE THE FULL 300-400 WORDS!
   - Strong forward momentum
   - Hook for next chapter
   - New situation, goal, or question
   - End on compelling moment

   TOTAL TARGET: 2300-2700 words across all 6 beats

YOUR TASK:
1. CONTINUE seamlessly from the choice continuation (incorporate it into Beat 1)

2. WRITE Chapter {chapter_number} following the 6-BEAT STRUCTURE above:
   ⚠️  You MUST write all 6 beats in sequence
   ⚠️  Each beat should hit its target word count
   ⚠️  Write in {pov}
   ⚠️  Include dialogue, internal thoughts, sensory details, and action
   ⚠️  Make each beat distinct and purposeful
   ⚠️  Advance toward beat goal: {beat_info.get("goal", "")}

3. CREATE 3 new choice continuations for Chapter {chapter_number + 1}

4. UPDATE story bible with any new details (characters, locations, events)

5. ASSESS beat progress (0.0-1.0 where 1.0 = beat complete)

STORY ARC PACING:
- Overall: {int(story_progress_pct)}% through story
- {"Act 1 (Setup)" if story_progress_pct < 33 else "Act 2 (Confrontation)" if story_progress_pct < 75 else "Act 3 (Resolution)"}
- Key moments to hit: {", ".join(beat_info.get("key_moments", []))}
- Dramatic questions: {", ".join(beat_info.get("dramatic_questions", []))}
- DON'T RUSH - Take time to develop scenes fully

RESPONSE FORMAT (JSON only):
""" + json_example + f"""

Remember:
- Continue FROM the last choice text (seamless flow)
- ⚠️⚠️⚠️ MANDATORY: 2500-2700 WORDS TOTAL - Write FULL LENGTH for EACH beat! ⚠️⚠️⚠️
- Removing beat labels does NOT mean shortening the beats!
- Each beat MUST hit its target word count (300-500 words per beat)
- Expand scenes with sensory details, dialogue, internal thoughts
- Choices should feel like narrative options, not game buttons
- Update story bible with NEW information only
- Write in {pov}
- Consider where we are in the overall {total_chapters}-chapter arc
"""

    return ChatPromptTemplate.from_messages([
        ("system", system_message),
        MessagesPlaceholder(variable_name="history"),
        ("human", "Continue the story from the choice: {last_choice}")
    ])


def format_conversation_history(messages: list) -> str:
    """
    Format conversation history for context.

    Args:
        messages: List of BaseMessage objects

    Returns:
        Formatted string of recent conversation
    """
    if not messages:
        return "No previous conversation."

    # Take last 6 messages for context (3 exchanges)
    recent = messages[-6:] if len(messages) > 6 else messages

    formatted = []
    for msg in recent:
        role = "Player" if msg.type == "human" else "Story"
        content = msg.content[:200] + "..." if len(msg.content) > 200 else msg.content
        formatted.append(f"{role}: {content}")

    return "\n".join(formatted)


# ===== SSBA (Story Structure Beat Agent) Prompts =====

def create_story_structure_prompt(
    world_template: dict,
    total_chapters: int = 30
) -> str:
    """
    Create prompt for SSBA to generate full story arc (Chapter 1 only).

    Uses "Save the Cat" beat structure adapted for 30-chapter serial story.

    Args:
        world_template: Loaded world template
        total_chapters: Total chapters in story (default 30)

    Returns:
        Prompt string for story structure generation
    """
    world_lore = world_template.get("world_lore", {})
    character_arc = world_template.get("character_arc_template", {})
    genre = world_template.get("genre", "science fiction")

    protagonist_arc = character_arc.get("protagonist", {}).get("arc", "")
    themes = world_template.get("themes", [])

    prompt = f"""You are a Story Structure Beat Agent (SSBA) creating a {total_chapters}-chapter story arc.

WORLD & GENRE:
- Setting: {world_lore.get('setting', 'sci-fi space station')}
- Genre: {genre}
- Themes: {', '.join(themes) if themes else 'exploration, mystery, relationships'}

PROTAGONIST ARC:
{protagonist_arc}

YOUR TASK:
Create a complete {total_chapters}-chapter story structure using the "Save the Cat" beat system adapted for serial storytelling.

MAP THESE BEATS TO CHAPTERS:

ACT 1 (Setup) - Chapters 1-{int(total_chapters * 0.25)}:
1. OPENING IMAGE (Chapter 1)
   - Before snapshot - establish ordinary world
   - Introduce protagonist's flaw or need

2. THEME STATED (Chapters 1-2)
   - Hint at the deeper meaning/lesson
   - Can be subtle or in dialogue

3. SETUP (Chapters 1-{int(total_chapters * 0.15)})
   - Establish characters, relationships, world rules
   - Show protagonist's status quo and what they want

4. CATALYST (Chapters {int(total_chapters * 0.10)}-{int(total_chapters * 0.12)})
   - Life-changing event happens
   - Point of no return approaches

5. DEBATE (Chapters {int(total_chapters * 0.12)}-{int(total_chapters * 0.25)})
   - Should they take the journey?
   - Fear, doubt, resistance

ACT 2A (Fun & Games) - Chapters {int(total_chapters * 0.25)}-{int(total_chapters * 0.5)}:
6. BREAK INTO 2 (Chapter {int(total_chapters * 0.25)})
   - Decision made, new world entered
   - "Point of no return"

7. B STORY (Chapters {int(total_chapters * 0.25)}-{int(total_chapters * 0.35)})
   - Love interest or mentor relationship develops
   - Represents thematic heart

8. FUN AND GAMES (Chapters {int(total_chapters * 0.25)}-{int(total_chapters * 0.5)})
   - Promise of the premise delivered
   - Exploration, discovery, new experiences
   - Build toward midpoint

9. MIDPOINT (Chapters {int(total_chapters * 0.48)}-{int(total_chapters * 0.52)})
   - False victory OR false defeat
   - Stakes raised, ticking clock starts
   - Protagonist takes control (or loses it)

ACT 2B (Bad Guys Close In) - Chapters {int(total_chapters * 0.52)}-{int(total_chapters * 0.75)}:
10. BAD GUYS CLOSE IN (Chapters {int(total_chapters * 0.52)}-{int(total_chapters * 0.70)})
    - External pressure increases
    - Internal doubts grow
    - Team falling apart OR enemies strengthening

11. ALL IS LOST (Chapters {int(total_chapters * 0.70)}-{int(total_chapters * 0.73)})
    - Lowest point
    - False defeat (if midpoint was false victory)
    - Whiff of death (literal or metaphorical)

12. DARK NIGHT OF SOUL (Chapter {int(total_chapters * 0.75)})
    - Reflection and despair
    - Questioning everything
    - Seeming to give up

ACT 3 (Resolution) - Chapters {int(total_chapters * 0.75)}-{total_chapters}:
13. BREAK INTO 3 (Chapter {int(total_chapters * 0.80)})
    - Inspiration strikes
    - New plan formed
    - Protagonist synthesizes lessons

14. FINALE (Chapters {int(total_chapters * 0.80)}-{int(total_chapters * 0.95)})
    - Execute the plan
    - Confront antagonist/challenge
    - All storylines converge
    - Character proves growth

15. FINAL IMAGE (Chapter {total_chapters})
    - After snapshot
    - Mirror of opening image
    - Show how character/world has changed

RETURN JSON FORMAT:
{{
  "story_structure": {{
    "act_1": {{
      "opening_image": {{
        "chapters": [1],
        "description": "Brief description of what happens",
        "character_state": "Protagonist's starting point"
      }},
      "theme_stated": {{ "chapters": [1, 2], "description": "...", "thematic_question": "..." }},
      "setup": {{ "chapters": [1-5], "description": "...", "key_relationships": ["..."] }},
      "catalyst": {{ "chapters": [3-4], "description": "...", "inciting_incident": "..." }},
      "debate": {{ "chapters": [4-8], "description": "...", "internal_conflict": "..." }}
    }},
    "act_2a": {{
      "break_into_2": {{ "chapters": [8], "description": "...", "point_of_no_return": "..." }},
      "b_story": {{ "chapters": [8-11], "description": "...", "relationship_focus": "..." }},
      "fun_and_games": {{ "chapters": [8-15], "description": "...", "premise_promise": "..." }},
      "midpoint": {{ "chapters": [14-16], "description": "...", "false_victory_or_defeat": "victory", "stakes_raised": "..." }}
    }},
    "act_2b": {{
      "bad_guys_close_in": {{ "chapters": [16-21], "description": "...", "pressure_sources": ["..."] }},
      "all_is_lost": {{ "chapters": [21-22], "description": "...", "loss_description": "..." }},
      "dark_night_of_soul": {{ "chapters": [23], "description": "...", "character_low_point": "..." }}
    }},
    "act_3": {{
      "break_into_3": {{ "chapters": [24], "description": "...", "revelation": "..." }},
      "finale": {{ "chapters": [24-29], "description": "...", "climax_description": "...", "resolution_plan": "..." }},
      "final_image": {{ "chapters": [30], "description": "...", "transformation_shown": "..." }}
    }}
  }},
  "key_arcs": {{
    "protagonist_arc": "From [starting state] to [ending state]",
    "love_interest_arc": "...",
    "antagonist_arc": "...",
    "thematic_arc": "..."
  }},
  "major_plot_points": [
    {{ "chapter": 3, "event": "...", "impact": "..." }},
    {{ "chapter": 15, "event": "...", "impact": "..." }},
    {{ "chapter": 23, "event": "...", "impact": "..." }}
  ]
}}

IMPORTANT:
- Be specific about what happens in each beat
- Consider {total_chapters} chapters - pace accordingly
- Leave room for player choices to influence details
- Character arcs should align with beat structure
- Balance action, relationship, and theme throughout
"""

    return prompt


def create_story_beat_checkin_prompt(
    story_structure: dict,
    chapter_number: int,
    total_chapters: int,
    story_bible: dict,
    summaries: list,
    inconsistency_flags: list
) -> str:
    """
    Create prompt for SSBA check-in (Chapters 2-30).

    Provides lightweight guidance based on story structure position.

    Args:
        story_structure: Full story structure from Chapter 1
        chapter_number: Current chapter number
        total_chapters: Total chapters
        story_bible: Current story bible
        summaries: Recent chapter summaries
        inconsistency_flags: Active inconsistency flags from CEA

    Returns:
        Prompt string for check-in
    """
    progress_pct = (chapter_number / total_chapters) * 100

    # Determine current act and beat
    if progress_pct < 25:
        act = "1"
        phase = "Setup"
    elif progress_pct < 50:
        act = "2a"
        phase = "Fun & Games"
    elif progress_pct < 75:
        act = "2b"
        phase = "Bad Guys Close In"
    else:
        act = "3"
        phase = "Resolution"

    # Find current beat from structure
    current_beat_name = "unknown"
    current_beat_description = ""
    upcoming_milestone = ""

    # Search through story structure to find current beat
    for act_name, act_data in story_structure.items():
        if isinstance(act_data, dict):
            for beat_name, beat_data in act_data.items():
                if isinstance(beat_data, dict) and "chapters" in beat_data:
                    chapters = beat_data["chapters"]
                    # Check if current chapter is in this beat's range
                    if isinstance(chapters, list) and len(chapters) > 0:
                        if isinstance(chapters[0], int):
                            if chapter_number in chapters or chapter_number == chapters[0]:
                                current_beat_name = beat_name
                                current_beat_description = beat_data.get("description", "")

    # Recent summaries for context
    recent_summary = "\n".join(summaries[-3:]) if summaries else "Story just beginning"

    # Format inconsistency flags
    flags_text = ""
    if inconsistency_flags:
        flags_text = "\n\nINCONSISTENCY FLAGS TO ADDRESS:\n"
        for flag in inconsistency_flags:
            flags_text += f"- {flag.get('description', 'Unknown')} (Suggested: {flag.get('suggested_resolution', 'TBD')})\n"

    prompt = f"""You are checking in on Chapter {chapter_number} of {total_chapters}.

STORY POSITION:
- Progress: {progress_pct:.1f}% complete
- Current Act: Act {act} ({phase})
- Current Beat: {current_beat_name}
- Description: {current_beat_description}

RECENT EVENTS:
{recent_summary}

PROTAGONIST STATUS:
{story_bible.get('protagonist', {}).get('current_state', 'Developing')}

YOUR TASK:
Provide guidance for Chapter {chapter_number} based on story structure position.{flags_text}

RETURN JSON FORMAT:
{{
  "current_story_beat": "{current_beat_name}",
  "act": "{act}",
  "progress_percentage": {progress_pct:.1f},
  "guidance_for_cba": "1-2 sentence guidance on what this chapter should accomplish",
  "upcoming_milestone": "What major beat or event is coming up soon",
  "character_arcs_status": {{
    "protagonist": "Brief status of protagonist's arc progression",
    "love_interest": "Brief status if relevant"
  }},
  "inconsistency_resolutions": [
    {{
      "flag_id": "id_from_flag_if_any",
      "resolution_plan": "How to weave contradiction into plot",
      "integrated_into_beat": "current_beat_name",
      "narrative_approach": "Brief approach description"
    }}
  ]
}}

GUIDANCE PRINCIPLES:
- Be specific but allow flexibility for player choices
- Reference story structure to maintain pacing
- Suggest how to advance character arcs
- Note if approaching major plot point
- If inconsistency flags exist, suggest creative resolutions
"""

    return prompt


def create_chapter_beat_prompt(
    world_template: dict,
    chapter_number: int,
    total_chapters: int,
    story_structure: dict = None,
    ssba_guidance: dict = None,
    story_bible: dict = None,
    last_choice: str = None,
    summaries: list = None
) -> str:
    """
    Create prompt for CBA (Chapter Beat Agent) to generate 6-beat chapter structure.

    This prompt helps CBA plan the internal structure of a single chapter using
    a 6-beat mini-arc that fits within the larger story beats from SSBA.

    Args:
        world_template: World template with genre, characters, setting
        chapter_number: Current chapter number (1-30)
        total_chapters: Total chapters in story (typically 30)
        story_structure: Full story structure from SSBA (Save the Cat beats)
        ssba_guidance: SSBA's guidance for this chapter from check-in
        story_bible: Current story bible with characters, events, locations
        last_choice: The player's choice that led to this chapter
        summaries: Recent chapter summaries for context

    Returns:
        str: Formatted prompt for CBA
    """
    world_name = world_template.get("name", "Unknown World")
    genre = world_template.get("genre", "science fiction")
    setting = world_template.get("world_lore", {}).get("setting", "")
    protagonist = world_template.get("characters", {}).get("protagonist", {})

    # Calculate progress
    progress = (chapter_number / total_chapters) * 100

    # Determine current story beat from SSBA guidance
    current_story_beat = "N/A"
    if ssba_guidance and "current_story_beat" in ssba_guidance:
        current_story_beat = ssba_guidance["current_story_beat"]

    # Build context sections
    story_structure_context = ""
    if story_structure:
        story_structure_context = f"\n\n## STORY STRUCTURE (from SSBA)\n{json.dumps(story_structure, indent=2)}"

    ssba_guidance_context = ""
    if ssba_guidance:
        ssba_guidance_context = f"\n\n## SSBA GUIDANCE FOR THIS CHAPTER\n{json.dumps(ssba_guidance, indent=2)}"

    story_bible_context = ""
    if story_bible:
        story_bible_context = f"\n\n## STORY BIBLE (Current State)\n{json.dumps(story_bible, indent=2)}"

    last_choice_context = ""
    if last_choice:
        last_choice_context = f"\n\n## PLAYER'S LAST CHOICE\n{last_choice}"

    summaries_context = ""
    if summaries and len(summaries) > 0:
        recent_summaries = summaries[-3:] if len(summaries) > 3 else summaries
        summaries_text = "\n".join([f"- {s}" for s in recent_summaries])
        summaries_context = f"\n\n## RECENT CHAPTER SUMMARIES\n{summaries_text}"

    prompt = f"""You are the Chapter Beat Agent (CBA) for "{world_name}", a {genre} interactive story.

## YOUR ROLE
Plan the internal structure of Chapter {chapter_number} using a 6-beat mini-arc that:
1. Fits within the larger story beat guidance from SSBA
2. Creates a satisfying chapter-level experience (~2,400-2,700 words)
3. Advances character arcs and plot while allowing for player choices
4. Maintains pacing and tension appropriate to the story position

## STORY CONTEXT
- **Chapter**: {chapter_number} of {total_chapters} ({progress:.1f}% complete)
- **Current Story Beat**: {current_story_beat}
- **Setting**: {setting}
- **Protagonist**: {protagonist.get('name', 'N/A')}{story_structure_context}{ssba_guidance_context}{story_bible_context}{last_choice_context}{summaries_context}

## 6-BEAT CHAPTER STRUCTURE

Plan 6 beats for this chapter, each targeting ~400-450 words:

**Beat 1: OPENING HOOK** (0-450 words)
- Immediate engagement: action, mystery, emotion, or tension
- Ground reader in POV, setting, immediate situation
- Connect to last chapter's ending/player's choice
- Set chapter question: "What will happen with...?"

**Beat 2: RISING ACTION** (450-900 words)
- Develop the chapter's central situation or conflict
- Introduce complications or new information
- Character reactions, decisions, interactions
- Build momentum toward midpoint

**Beat 3: MIDPOINT TWIST** (900-1,350 words)
- Surprise, revelation, or shift in understanding
- Raise stakes or change direction
- False victory OR setback that complicates situation
- Chapter question becomes more urgent

**Beat 4: COMPLICATIONS** (1,350-1,800 words)
- Consequences of midpoint unfold
- Obstacles intensify, pressure increases
- Character struggles with challenge
- Tension peaks as situation worsens or clarifies

**Beat 5: DARK NIGHT / TENSION PEAK** (1,800-2,250 words)
- Moment of maximum pressure or emotional intensity
- Character must make difficult choice or face hard truth
- All seems lost OR victory seems within grasp (depending on story beat)
- Sets up resolution

**Beat 6: RESOLUTION & HOOK** (2,250-2,700 words)
- Resolve chapter's immediate question/conflict
- Show consequences of character's actions/choices
- Advance story bible (character state, relationships, world state)
- **CRITICAL**: End with hook that sets up player choices
- Hook should present clear decision point or dilemma

## JSON FORMAT

Return your chapter beat plan as JSON:

```json
{{
  "chapter_beats": [
    {{
      "beat_number": 1,
      "beat_name": "opening_hook",
      "word_target": 450,
      "description": "Brief description of what happens in this beat",
      "key_elements": ["element1", "element2"],
      "emotional_tone": "tense/hopeful/mysterious/etc",
      "character_focus": "Who is POV or central to this beat"
    }},
    // ... beats 2-6 following same structure
  ],
  "chapter_goal": "What this chapter accomplishes in the larger story",
  "chapter_tension": "What creates tension/interest throughout chapter",
  "chapter_question": "The question that drives reader through chapter",
  "setup_for_next": "What this chapter sets up for next chapter",
  "choice_setup": {{
    "situation": "The dilemma or decision point at chapter end",
    "stakes": "Why this choice matters",
    "suggested_choice_types": ["type1", "type2", "type3"]
  }}
}}
```

## BEAT PLANNING PRINCIPLES

1. **Pacing**: Each beat should flow naturally into the next
2. **Character Arc**: Show protagonist changing, learning, or struggling
3. **World Building**: Integrate setting details organically
4. **Player Agency**: Structure allows for meaningful choices to affect story
5. **Story Alignment**: Serve the current story beat from SSBA
6. **Micro-Tension**: Each beat should have its own small tension or question
7. **Hook Quality**: Final beat must create genuine anticipation/dilemma

## ALIGNMENT WITH SSBA GUIDANCE

If SSBA provided specific guidance:
- Follow suggested character arc moments
- Hit any plot points mentioned
- Maintain specified emotional tone
- Advance relationships as indicated
- Resolve any inconsistency flags creatively

## TARGET METRICS

- **Total Chapter Length**: ~2,400-2,700 words
- **Beat Length**: ~400-450 words each
- **Pacing**: Varied (fast action vs slow reflection based on story beat)
- **Tension Curve**: Build → Peak at Beat 5 → Resolve + Hook at Beat 6

Plan the 6 beats for Chapter {chapter_number} now, ensuring they create a compelling chapter experience while advancing the larger story.
"""

    return prompt


def create_consistency_check_prompt(
    chapter_number: int,
    chapter_beat_plan: dict,
    story_bible: dict,
    consistency_report: dict,
    last_choice: str = None
) -> str:
    """
    Create prompt for CEA to analyze consistency and identify potential contradictions.

    CEA reviews the RAG consistency report and determines:
    1. Are there any contradictions that can be auto-fixed?
    2. Are there irreconcilable contradictions that should become plot features?
    3. What guidance should be provided to the Prose Agent?

    Args:
        chapter_number: Current chapter number
        chapter_beat_plan: CBA's beat plan for this chapter
        story_bible: Current story bible
        consistency_report: RAG consistency check results
        last_choice: Player's last choice

    Returns:
        str: Formatted prompt for CEA
    """
    chapter_goal = chapter_beat_plan.get("chapter_goal", "N/A")
    relevant_history = consistency_report.get("relevant_history", [])
    risk_level = consistency_report.get("overall_risk", "none")

    # Format relevant history
    history_text = ""
    if relevant_history:
        history_items = []
        for item in relevant_history[:10]:  # Top 10
            chapter = item.get("chapter", "?")
            text = item.get("text", "")
            history_items.append(f"  • Chapter {chapter}: {text}")
        history_text = "\n".join(history_items)
    else:
        history_text = "  (No relevant history found)"

    last_choice_context = ""
    if last_choice:
        last_choice_context = f"\n\n## PLAYER'S LAST CHOICE\n{last_choice}"

    prompt = f"""You are the Context Editor Agent (CEA) for this interactive story.

## YOUR ROLE

Review the planned chapter content against established narrative history and:
1. **Identify contradictions**: Does the plan conflict with established facts?
2. **Auto-fix minor issues**: Suggest adjustments for small inconsistencies
3. **Flag major contradictions**: Identify irreconcilable contradictions as plot opportunities
4. **Provide guidance**: Give clear directions to the Prose Agent

## CHAPTER CONTEXT

**Chapter {chapter_number}**
- **Goal**: {chapter_goal}
- **Risk Level**: {risk_level}{last_choice_context}

## PLANNED CHAPTER BEATS

{json.dumps(chapter_beat_plan, indent=2)}

## RELEVANT NARRATIVE HISTORY (from RAG)

{history_text}

## STORY BIBLE (Current State)

{json.dumps(story_bible, indent=2)}

## YOUR ANALYSIS TASK

Review the chapter beat plan against the narrative history and story bible.

For each beat in the plan, consider:
1. Does this beat contradict any established character traits, abilities, or limitations?
2. Does this beat contradict locations, timeline, or world rules?
3. Does this beat contradict relationships or past events?

**Minor Contradictions (Auto-Fix)**:
- Small timeline inconsistencies
- Character trait variations that can be explained
- Location details that can be reconciled
→ Suggest specific fixes in your guidance

**Major Contradictions (Flag as Plot Features)**:
- Character abilities suddenly changing without explanation
- Timeline impossibilities
- Character death/departure conflicts
- Physical impossibilities given established rules
→ Flag these for SSBA to weave into plot as reveals/twists

## JSON FORMAT

Return your analysis as JSON:

```json
{{
  "consistency_status": "clear" | "minor_issues" | "major_contradiction",
  "minor_issues": [
    {{
      "beat_number": 1,
      "issue": "Brief description of inconsistency",
      "auto_fix_suggestion": "How to adjust the beat to maintain consistency",
      "context_from_history": "Relevant history that conflicts"
    }}
  ],
  "major_contradictions": [
    {{
      "beat_number": 3,
      "contradiction": "Description of irreconcilable contradiction",
      "relevant_history": "Established facts that conflict",
      "plot_opportunity": "How this could become an intentional plot reveal",
      "flag_for_ssba": true
    }}
  ],
  "guidance_for_prose_agent": {{
    "general_guidance": "Overall guidance for prose generation",
    "beat_specific_notes": {{
      "1": "Note for beat 1",
      "3": "Note for beat 3"
    }},
    "emphasis_points": ["What to emphasize", "What to be careful with"],
    "avoid": ["What to avoid to prevent contradictions"]
  }},
  "inconsistency_flags": [
    {{
      "flag_id": "unique_flag_id_ch{chapter_number}_issue",
      "description": "Description for SSBA",
      "suggested_resolution": "How SSBA might weave this into story",
      "severity": "low" | "medium" | "high"
    }}
  ]
}}
```

## DECISION PRINCIPLES

1. **Prefer Auto-Fix**: Try to adjust beats to maintain consistency when possible
2. **Respect Player Agency**: Don't contradict player choices without narrative justification
3. **Protect Established Canon**: Character limitations (disabilities, skills) are sacred
4. **Embrace Plot Opportunities**: Major contradictions can become great story moments
5. **Clear Guidance**: Give PA specific, actionable direction

Analyze the chapter plan for consistency now, focusing on protecting established narrative canon while enabling creative storytelling.
"""

    return prompt


def create_choice_generation_prompt(
    world_template: dict,
    chapter_number: int,
    narrative: str,
    story_bible: dict,
    chapter_beat_plan: dict = None,
    ssba_guidance: dict = None
) -> str:
    """
    Create prompt for CEA to generate player choices.

    CEA generates 3 meaningful choices based on:
    - The chapter's ending situation
    - Character arcs and story beats
    - Player agency and story direction

    Args:
        world_template: World template
        chapter_number: Current chapter number
        narrative: The chapter narrative just generated
        story_bible: Current story bible
        chapter_beat_plan: CBA's beat plan (for context)
        ssba_guidance: SSBA guidance (for story direction)

    Returns:
        str: Formatted prompt for CEA to generate choices
    """
    world_name = world_template.get("name", "Unknown World")
    genre = world_template.get("genre", "science fiction")
    protagonist = world_template.get("characters", {}).get("protagonist", {})

    # Extract narrative ending (last ~500 chars)
    narrative_ending = narrative[-500:] if len(narrative) > 500 else narrative

    chapter_goal = ""
    choice_setup = {}
    if chapter_beat_plan:
        chapter_goal = chapter_beat_plan.get("chapter_goal", "")
        choice_setup = chapter_beat_plan.get("choice_setup", {})

    current_beat = ""
    if ssba_guidance:
        current_beat = ssba_guidance.get("current_story_beat", "")

    choice_setup_context = ""
    if choice_setup:
        choice_setup_context = f"\n\n## CHOICE SETUP FROM CBA\n{json.dumps(choice_setup, indent=2)}"

    prompt = f"""You are the Context Editor Agent (CEA) generating player choices for "{world_name}", a {genre} interactive story.

## YOUR ROLE

Generate 3 meaningful player choices that:
1. **Honor the Chapter Ending**: Choices emerge naturally from the narrative situation
2. **Advance Character Arcs**: Choices should challenge/develop the protagonist
3. **Serve Story Beats**: Align with current story beat and direction
4. **Provide Real Agency**: Each choice should lead to meaningfully different outcomes
5. **Maintain Genre Tone**: Choices fit the {genre} genre

## STORY CONTEXT

- **Chapter**: {chapter_number}
- **Protagonist**: {protagonist.get('name', 'N/A')}
- **Current Story Beat**: {current_beat}
- **Chapter Goal**: {chapter_goal}{choice_setup_context}

## NARRATIVE ENDING

The chapter ended with:

```
{narrative_ending}
```

## STORY BIBLE

{json.dumps(story_bible, indent=2)}

## CHOICE GENERATION GUIDELINES

**Good Choices**:
- ✅ Emerge naturally from the chapter's ending situation
- ✅ Present meaningful dilemmas (not obvious right/wrong)
- ✅ Each choice has clear consequences
- ✅ Choices reflect character personality and growth
- ✅ Advance the plot in different directions
- ✅ Respect established character limitations and abilities

**Avoid**:
- ❌ Choices that break established canon (e.g., "walk to..." for wheelchair user)
- ❌ Choices with obviously "correct" or "wrong" answers
- ❌ Choices that are too similar in outcome
- ❌ Choices that ignore the immediate narrative situation
- ❌ Choices that feel forced or unnatural

**Choice Types** (use 2-3 different types):
- **Action**: Do something physical/immediate
- **Relationship**: How to interact with another character
- **Investigation**: Explore, search, analyze
- **Moral Dilemma**: Competing values or loyalties
- **Strategic**: Plan or approach to a problem
- **Emotional**: Internal character decision

## JSON FORMAT

Return 3 choices as JSON:

```json
{{
  "choices": [
    {{
      "id": "ch{chapter_number}_choice_1",
      "text": "The choice text as the player will see it (2-3 sentences max)",
      "choice_type": "action|relationship|investigation|moral|strategic|emotional",
      "thematic_direction": "Brief note on where this choice leads the story",
      "character_arc_impact": "How this choice affects protagonist's development",
      "story_beat_alignment": "How this serves the current story beat"
    }},
    {{
      "id": "ch{chapter_number}_choice_2",
      "text": "Second choice text",
      "choice_type": "...",
      "thematic_direction": "...",
      "character_arc_impact": "...",
      "story_beat_alignment": "..."
    }},
    {{
      "id": "ch{chapter_number}_choice_3",
      "text": "Third choice text",
      "choice_type": "...",
      "thematic_direction": "...",
      "character_arc_impact": "...",
      "story_beat_alignment": "..."
    }}
  ],
  "choice_rationale": "Brief explanation of why these 3 choices work together"
}}
```

## IMPORTANT

- Each choice text should be 2-3 sentences maximum (player-facing)
- Choices should feel natural and immediate given the chapter ending
- Vary the choice types (don't make all 3 the same type)
- Consider protagonist's personality and established limitations
- Make choices that create anticipation for the next chapter

Generate 3 compelling choices now that give the player meaningful agency while serving the larger story.
"""

    return prompt
