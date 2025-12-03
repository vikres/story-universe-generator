# config.py
# Configuration file for the Story Universe Generator
# =====================================================
import os

# API key (read from the environment)
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")  # class key removed; set OPENAI_API_KEY in your environment

# Model Configuration
# We use gpt-4.1-nano for fast, cost-effective responses
MODEL = "gpt-4.1-nano"

# Reasoning effort: "low" for minimal reasoning (faster, cheaper)
REASONING_EFFORT = "low"

# Maximum tokens for output
MAX_OUTPUT_TOKENS = 4096

# =============================================================================
# SAFETY LIMITS - DO NOT MODIFY
# =============================================================================
# These limits prevent accidental infinite loops and excessive API usage

# Maximum API calls allowed per script execution
MAX_API_CALLS = 10

# Global counter for API calls (do not modify)
_api_call_count = 0

def check_api_limit():
    """
    Call this before each API request to enforce the limit.
    Raises an exception if the limit is exceeded.
    """
    global _api_call_count
    _api_call_count += 1
    
    if _api_call_count > MAX_API_CALLS:
        raise RuntimeError(
            f"\n{'='*60}\n"
            f"⚠️  SAFETY LIMIT REACHED: Maximum {MAX_API_CALLS} API calls exceeded!\n"
            f"{'='*60}\n"
            f"This limit exists to prevent infinite loops and excessive charges.\n"
            f"If you need more calls, restart your Python script.\n"
            f"{'='*60}"
        )
    
    print(f"[API Call {_api_call_count}/{MAX_API_CALLS}]")

def reset_api_counter():
    """Reset the API call counter (use only for testing)."""
    global _api_call_count
    _api_call_count = 0
