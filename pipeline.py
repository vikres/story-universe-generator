# pipeline.py
# Exercise III: Connect Agent 1 and Agent 2 into a complete pipeline
# ===================================================================

from openai import OpenAI
from config import OPENAI_API_KEY, MODEL, REASONING_EFFORT, MAX_OUTPUT_TOKENS, check_api_limit
import json

# Initialize the OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# =============================================================================
# IMPORT YOUR AGENTS
# =============================================================================
# 
# You need to import the functions from both agent files.
# The functions you need are:
# - analyze_story() from agent1_story_analyzer.py
# - generate_html() from agent2_html_generator.py
#
# Hint: Use "from <filename> import <function>"
# =============================================================================

# YOUR IMPORTS HERE
from agent1_story_analyzer import analyze_story
from agent2_html_generator import generate_html


# =============================================================================
# YOUR TASK: Complete the pipeline function
# =============================================================================
# 
# The pipeline should:
# 1. Take a story idea as input (string)
# 2. Call Agent 1 to convert it to structured JSON
# 3. Take that JSON output and pass it to Agent 2
# 4. Get the HTML output from Agent 2
# 5. Save the HTML to a file
# 6. Return the file path
#
# =============================================================================

def run_pipeline(story_idea: str, output_filename: str = "final_output.html") -> str:
    """
    Runs the complete Story Universe Generator pipeline.
    
    Args:
        story_idea: A paragraph or two describing the story concept
        output_filename: Name of the output HTML file (default: final_output.html)
        
    Returns:
        The path to the generated HTML file
    """
    
    print("=" * 60)
    print("STORY UNIVERSE GENERATOR PIPELINE")
    print("=" * 60)
    
    # =========================================================================
    # STEP 1: Run Agent 1 - Story Analyzer
    # =========================================================================
    # 
    # Call the analyze_story() function with the story_idea
    # Store the result (a dictionary) in a variable
    #
    # YOUR CODE HERE:
    print("\n[Step 1] Analyzing story idea...")
    story_json = analyze_story(story_idea)
    
    
    # =========================================================================
    # STEP 2: (Optional) Print or log the intermediate JSON
    # =========================================================================
    # 
    # This helps you debug and see what Agent 1 produced
    #
    # YOUR CODE HERE:
    print("\n[Step 1 Complete] Story Analysis:")
    print(json.dumps(story_json, indent=2))
    
    
    # =========================================================================
    # STEP 3: Run Agent 2 - HTML Generator
    # =========================================================================
    # 
    # Call the generate_html() function with the story_json from Step 1
    # Store the result (an HTML string) in a variable
    #
    # YOUR CODE HERE:
    print("\n[Step 2] Generating HTML Story Bible...")
    html_output = generate_html(story_json)
    
    
    # =========================================================================
    # STEP 4: Save the HTML to a file
    # =========================================================================
    # 
    # Write the HTML output to the specified filename
    #
    # YOUR CODE HERE:
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(html_output)
    
    
    # =========================================================================
    # STEP 5: Return the filename
    # =========================================================================
    # 
    # YOUR CODE HERE:
    print(f"\n[Complete] Story Bible saved to: {output_filename}")
    return output_filename
    

# =============================================================================
# Main execution
# =============================================================================
if __name__ == "__main__":
    # Read the sample story idea
    with open("sample_input.txt", "r") as f:
        story_idea = f.read()
    
    print("\nInput Story Idea:")
    print("-" * 40)
    print(story_idea)
    print("-" * 40)
    
    # Run the pipeline
    output_file = run_pipeline(story_idea)
    
    print("\n" + "=" * 60)
    print("SUCCESS!")
    print("=" * 60)
    print(f"\nYour Story Bible has been created: {output_file}")
    print("Open this file in a web browser to see the result!")
