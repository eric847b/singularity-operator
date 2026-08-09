"""Singularity Operator v0.5.3 - Ultimate self-improving AI system.
EverythingDB + SelfImprover + ChaosEngine + Multi-AI Orchestration + GitHubSeamless.

Core: Universal sequence completion for all knowable data. Self-evolution via AI.
Autonomous repo actions. Disciplined chaos for antifragility.

v0.5.3: Real chaos engineering experiments (inject/recover/measure resilience).
v0.5.2: Richer metrics, learning persist, evolution_summary for ROI status.
"""

from .everything_db import EverythingDB
from .self_improver import SelfImprover
from .groq_wrapper import call_ai, get_provider_status
from .github_seamless import GitHubSeamless
from .orchestrator import SingularityOrchestrator
from .chaos_engine import ChaosEngine

__version__ = "0.5.3"
__all__ = [
    "EverythingDB",
    "SelfImprover",
    "call_ai",
    "GitHubSeamless",
    "SingularityOrchestrator",
    "ChaosEngine",
]
