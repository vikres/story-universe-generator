# Story Universe Generator

## Setup Instructions

### 1. Install Python Requirements

Make sure you have Python 3.9+ installed. Then install the OpenAI library:

```bash
pip install openai
```

### 2. API Key

Set the `OPENAI_API_KEY` environment variable. (The shared class key that was here has been removed.)

> **Note:** This is a shared class API key. A safety limit of **10 API calls per script run** is enforced to prevent accidental infinite loops. If you hit the limit, simply restart your script.

### 3. Test Your Setup

Run this command to verify everything is working:

```bash
python -c "from openai import OpenAI; print('OpenAI library installed successfully!')"
```

---

## How to Complete the Exercises

### Exercise II: Building the Agents

#### Agent 1: Story Analyzer
1. Open `agent1_story_analyzer.py`
2. Find the `SYSTEM_PROMPT` variable (around line 25)
3. Write your system prompt instructions
4. Test by running: `python agent1_story_analyzer.py`
5. Check the output in `agent1_output.json`

#### Agent 2: HTML Generator
1. Open `agent2_html_generator.py`
2. Find the `SYSTEM_PROMPT` variable (around line 25)
3. Write your system prompt instructions
4. Test by running: `python agent2_html_generator.py`
5. Check the output in `agent2_output.html` (open in browser)

### Exercise III: Connecting the Pipeline

1. Open `pipeline.py`
2. Add the import statements at the top
3. Complete the `run_pipeline()` function
4. Test by running: `python pipeline.py`
5. Check the output in `final_output.html`

---

## File Structure

```
story_universe_generator/
├── config.py                 # API configuration (add your key here)
├── agent1_story_analyzer.py  # Exercise II - Part 1
├── agent2_html_generator.py  # Exercise II - Part 2
├── pipeline.py               # Exercise III
├── sample_input.txt          # Sample story idea for testing
└── README.md                 # This file
```

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'openai'"
Run: `pip install openai`

### "AuthenticationError" or "Invalid API Key"
Check that your API key in `config.py` is correct and has no extra spaces.

### "RateLimitError"
Wait a minute and try again. You may have hit the API rate limit.

### "SAFETY LIMIT REACHED" error
This means you've made 10 API calls in one script run. This is normal! Just restart your Python script to reset the counter. This limit protects against infinite loops.

### "The model does not exist"
Make sure you're using `gpt-4.1-nano` (or `gpt-4o-mini` as a fallback).

### JSON parsing errors in Agent 1
Check that your system prompt asks for JSON output and follows the schema.

### HTML looks broken
Make sure Agent 2's system prompt asks for complete, self-contained HTML with embedded CSS.

---

## Tips for Writing Good System Prompts

1. **Be Specific**: Tell the AI exactly what you want it to do
2. **Give Examples**: Show the format you expect
3. **Set Constraints**: Mention any rules or limitations
4. **Encourage Creativity**: For creative tasks, tell it to be imaginative
5. **Iterate**: Test and refine your prompts based on the output

---

## Need Help?

- Use ChatGPT or Claude to help you understand the code
- Search the OpenAI documentation: https://platform.openai.com/docs
- Message the instructor on Teams for conceptual questions

Good luck and have fun! 🚀
