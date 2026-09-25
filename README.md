# story-universe-generator

Two-agent LLM pipeline built for a course exercise in December 2025. Agent 1 turns a short story idea into structured JSON (title, genre, logline, characters, setting, plot, themes) using the OpenAI Responses API with a JSON schema. Agent 2 renders that JSON as a self-contained HTML page, and `pipeline.py` chains the two.

The course supplied the scaffolding and the API-call limits in `config.py`. The system prompts and the pipeline function are mine. The original instructions are in `COURSE_INSTRUCTIONS.md`.

To run it, set `OPENAI_API_KEY` in your environment, then run `python pipeline.py`.
