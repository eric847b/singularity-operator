"""groq_wrapper v0.6.0 - Multi-provider free AI router (local + Pollinations no-key + free tiers).
Real calls with requests. Health-aware, cost=0 focus, structured responses, seamless rotation.
Used by EverythingDB, SelfImprover, Orchestrator for all intelligence. Continuous refinement never pauses.
"""

from __future__ import annotations

import os
from typing import Any, Dict, Optional

from singularity_operator.free_ai_client import call_free_ai, get_free_ai

FREE_PROVIDERS = ["ollama", "pollinations", "groq", "openrouter", "together"]


def call_ai(prompt: str, provider: Optional[str] = None, max_retries: int = 2, **kwargs) -> Dict[str, Any]:
    """Universal free AI caller. Local-first + Pollinations no-key + free cloud tiers.
    Returns structured dict. Cost always 0 for free lanes.
    """
    # Prefer the unified free client (handles rotation, cooldowns, no-key lanes)
    result = call_free_ai(prompt, **kwargs)
    if "error" not in result:
        return result

    # Legacy fallback path if free client fully exhausted
    return {
        "error": result.get("error", "All free providers exhausted"),
        "providers_tried": result.get("providers_tried", FREE_PROVIDERS),
        "tally": result.get("tally", {}),
    }


def get_provider_status() -> Dict[str, Any]:
    client = get_free_ai()
    return {
        "groq_key_present": bool(os.getenv("GROQ_API_KEY")),
        "openrouter_key_present": bool(os.getenv("OPENROUTER_API_KEY")),
        "together_key_present": bool(os.getenv("TOGETHER_API_KEY")),
        "default": os.getenv("DEFAULT_AI_PROVIDER", "free-rotator"),
        "free_providers": FREE_PROVIDERS,
        "tally": client.tally,
        "pollinations_no_key": True,
        "local_first": True,
    }


print("groq_wrapper v0.6.0 - Free AI rotator (Pollinations no-key + local + free tiers) loaded")
