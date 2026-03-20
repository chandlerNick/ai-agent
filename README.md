# Simple "AI-Agent"

This follows the tutorial from boot.dev on how to build a simple agent using google's genai API.

It has the basic ability to edit code, execute files, and the like.

### Usage

1. Add a [Gemini API Key](https://aistudio.google.com/api-keys) to a `.env` file. Call it `GEMINI_API_KEY`.
2. Check out `main.py`.
3. Ensure [uv](https://docs.astral.sh/uv/getting-started/installation/) is installed and synced.
4. Run `uv run main.py`.