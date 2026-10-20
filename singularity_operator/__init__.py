"""Singularity Operator v0.5.18 - Ultimate self-improving AI system.

v0.5.18: Deepen currency signal (#43) — fetch_currency_signals parses CURRENCY_STATUS.md JSON block from wealth repo.
v0.5.17: Currency fleet signal (#43) — GitHubSeamless.fetch_currency_signals + Orchestrator currency_signal task + continuous_roi_rank prefers wealth path.
v0.5.16: Continuous upgrade (#33) — FreeAIClient exposes get_status() + live provider tally; free-AI primary hardened.
v0.5.15: Continuous upgrade cycle — launcher synced, SelfImprover prefers free AI rotator.
v0.5.14: Free AI rotator fully integrated for zero-cost continuous refinement.
v0.5.11: Continuous upgrade from live ROI ranking (AGA roi_top_ref).
v0.5.10: AGA Actions → singularity-operator metrics feedback loop.
"""

from .everything_db import EverythingDB
from .self_improver import SelfImprover
from .groq_wrapper import call_ai, get_provider_status
from .free_ai_client import FreeAIClient, call_free_ai, get_free_ai
from .github_seamless import GitHubSeamless
from .orchestrator import SingularityOrchestrator
from .chaos_engine import ChaosEngine
from .serendipity_engine import SerendipityEngine
from .browser_automation import BrowserAutomation
from .userscript_gen import UserscriptGenerator

__version__ = "0.5.18"
__all__ = [
    "EverythingDB",
    "SelfImprover",
    "call_ai",
    "FreeAIClient",
    "call_free_ai",
    "get_free_ai",
    "get_provider_status",
    "GitHubSeamless",
    "SingularityOrchestrator",
    "ChaosEngine",
    "SerendipityEngine",
    "BrowserAutomation",
    "UserscriptGenerator",
]
