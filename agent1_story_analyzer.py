# agent1_story_analyzer.py
# Agent 1: Story Analyzer - Converts unstructured story ideas to structured JSON
# ==============================================================================

from openai import OpenAI
from config import OPENAI_API_KEY, MODEL, REASONING_EFFORT, MAX_OUTPUT_TOKENS, check_api_limit
import json

# Initialize the OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# =============================================================================
# YOUR TASK: Write the system prompt for the Story Analyzer
# =============================================================================
# 
# This agent should:
# 1. Analyze an unstructured story idea provided by the user
# 2. Extract key story elements (characters, setting, plot, themes, etc.)
# 3. Output a structured JSON following the schema defined below
#
# Tips for writing a good system prompt:
# - Be specific about what you want the AI to extract
# - Encourage creativity in filling in gaps
# - Tell it to infer reasonable details if not explicitly stated
# - Remind it to follow the exact JSON structure
#
# =============================================================================

SYSTEM_PROMPT = """
You are a creative story analyst in a two-agent Story Universe Generator system.

Your task is to:
- Read an unstructured story idea described in one to three paragraphs.
- Identify the key story elements.
- Infer missing details in a way that fits the tone, genre, and internal logic of the idea.
- Return ONLY a single JSON object that matches the JSON schema enforced in this request.

You must conceptually fill these fields:

1. "title"
   - A punchy working title for the story.

2. "genre"
   - The primary genre (e.g., Fantasy, Sci-Fi, Romance, Thriller, Horror, Mystery, Drama).
   - If the genre is not explicit, infer the best-fitting one.

3. "logline"
   - A single sentence summarizing the central conflict: who wants what, against what obstacle, and what is at stake.

4. "characters"
   - An array of the main characters.
   - Always include at least:
     - the primary protagonist,
     - the main antagonist or opposing force (if any),
     - other important supporting characters as needed.
   - For each character, fill:
     - "name": Character name (invent one if none is given).
     - "role": One of ["protagonist", "antagonist", "supporting", "mentor", "love_interest"].
       * Use "antagonist" for any character or force actively opposing the protagonist.
       * Use "supporting" for allies, helpers, or secondary characters who don't fit other categories.
     - "description": 1-2 sentences on appearance, personality, background, or role.
     - "motivation": What this character wants most in the story.
     - "arc": How this character is likely to change, grow, or fail to grow.

5. "setting"
   - Describe the story world:
     - "time_period": When the story takes place (e.g., "near-future dream economy", "contemporary city").
     - "location": Main locations or type of world.
     - "atmosphere": 1-3 sentences on the mood or tone (e.g., whimsical, oppressive, noir, hopeful).

6. "plot"
   - Summarize the story structure:
     - "hook": The opening situation or inciting incident.
     - "conflict": The central problem or main struggle the protagonist faces.
     - "stakes": What can be lost or gained if the protagonist fails or succeeds.
     - "resolution_hint": 1-2 sentences suggesting a plausible direction for how the story might resolve
       (the likely type of ending, not a detailed blow-by-blow).

7. "themes"
   - An array of 2-4 short theme phrases capturing the main ideas
     (e.g., "the cost of desire", "identity and memory", "power and corruption").

8. "unique_elements"
   - An array of 2-6 short phrases describing what makes this story special:
     unusual worldbuilding rules, magic or technology, narrative twists, character dynamics, etc.

Guidelines:
- If the idea omits some information, infer details that fit the tone, genre, and logic of the story.
- Keep each text field concise, typically 1-3 sentences.
- Make the language vivid and specific, but avoid over-flowery prose.
- Ensure every required field in the JSON schema is present and non-empty.
- Do NOT introduce any extra top-level keys beyond those defined in the schema.

Before outputting:
- Verify all required fields are present.
- Check that character roles use only the five allowed values.
- Ensure arrays (themes, unique_elements) have at least 2 items.
- Confirm all text fields are non-empty strings.

CRITICAL OUTPUT FORMAT:
Your response must contain ONLY the JSON object.
- No preamble like "Here is the analysis:"
- No markdown code fences (```json```)
- No explanatory text before or after the JSON
- Just the raw JSON object, starting with { and ending with }
- Use double quotes for all strings
- No comments
- No trailing commas
"""


# JSON Schema for structured output
# This ensures the AI outputs valid, well-structured JSON
JSON_SCHEMA = {
    "name": "story_analysis",
    "strict": True,
    "schema": {
        "type": "object",
        "properties": {
            "title": {
                "type": "string",
                "description": "A working title for the story"
            },
            "genre": {
                "type": "string",
                "description": "The primary genre (e.g., Fantasy, Sci-Fi, Romance, Thriller)"
            },
            "logline": {
                "type": "string",
                "description": "A one-sentence summary of the story"
            },
            "characters": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "role": {
                            "type": "string",
                            "enum": ["protagonist", "antagonist", "supporting", "mentor", "love_interest"]
                        },
                        "description": {"type": "string"},
                        "motivation": {"type": "string"},
                        "arc": {"type": "string"}
                    },
                    "required": ["name", "role", "description", "motivation", "arc"],
                    "additionalProperties": False
                },
                "description": "List of main characters"
            },
            "setting": {
                "type": "object",
                "properties": {
                    "time_period": {"type": "string"},
                    "location": {"type": "string"},
                    "atmosphere": {"type": "string"}
                },
                "required": ["time_period", "location", "atmosphere"],
                "additionalProperties": False,
                "description": "Where and when the story takes place"
            },
            "plot": {
                "type": "object",
                "properties": {
                    "hook": {"type": "string"},
                    "conflict": {"type": "string"},
                    "stakes": {"type": "string"},
                    "resolution_hint": {"type": "string"}
                },
                "required": ["hook", "conflict", "stakes", "resolution_hint"],
                "additionalProperties": False,
                "description": "The story structure"
            },
            "themes": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Major themes explored in the story"
            },
            "unique_elements": {
                "type": "array",
                "items": {"type": "string"},
                "description": "What makes this story special or unique"
            }
        },
        "required": ["title", "genre", "logline", "characters", "setting", "plot", "themes", "unique_elements"],
        "additionalProperties": False
    }
}


def analyze_story(story_idea: str) -> dict:
    """
    Analyzes a story idea and returns structured JSON.
    
    Args:
        story_idea: A paragraph or two describing the story concept
        
    Returns:
        A dictionary containing the structured story analysis
    """
    
    # Safety check - prevents infinite loops
    check_api_limit()
    
    # Make the API call using the Responses API
    response = client.responses.create(
        model=MODEL,
        input=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": story_idea}
        ],
        text={
            "format": {
                "type": "json_schema",
                "name": JSON_SCHEMA["name"],
                "schema": JSON_SCHEMA["schema"],
                "strict": JSON_SCHEMA["strict"],
            }
        },
        max_output_tokens=MAX_OUTPUT_TOKENS
    )
    
    # Extract the text content from the response
    output_text = response.output_text
    
    # Parse and return the JSON
    return json.loads(output_text)


# =============================================================================
# Test the agent
# =============================================================================
if __name__ == "__main__":
    # Read the sample story idea
    with open("sample_input.txt", "r") as f:
        story_idea = f.read()
    
    print("=" * 60)
    print("AGENT 1: STORY ANALYZER")
    print("=" * 60)
    print("\nInput Story Idea:")
    print("-" * 40)
    print(story_idea)
    print("-" * 40)
    
    print("\nAnalyzing story...")
    result = analyze_story(story_idea)
    
    print("\nStructured Output (JSON):")
    print("-" * 40)
    print(json.dumps(result, indent=2))
    
    # Save output to file
    with open("agent1_output.json", "w") as f:
        json.dump(result, f, indent=2)
    
    print("\n✓ Output saved to agent1_output.json")
