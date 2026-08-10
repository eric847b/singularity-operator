"""Singularity Operator v0.5.6 - Ultimate self-improving AI system.
EverythingDB + SelfImprover + ChaosEngine + SerendipityEngine + Orchestration + GitHubSeamless.

v0.5.6: Multi-repo fleet orchestration — status sync + catalyst propagation via GitHubSeamless.
v0.5.5: Deeper serendipity — richer scoring, Groq-assisted bridges, bridge persist.
v0.5.4: Cross-sequence connections + advancing auto-seed.
v0.5.3: Real chaos engineering experiments.
v0.5.2: Richer metrics, learning persist, evolution_summary.
"""

from .everything_db import EverythingDB
from .self_improver import SelfImprover
from .groq_wrapper import call_ai, get_provider_status
from .github_seamless import GitHubSeamless
from .orchestrator import SingularityOrchestrator
from .chaos_engine import ChaosEngine
from .serendipity_engine import SerendipityEngine

__version__ = "0.5.6"
__all__ = [
    "EverythingDB",
    "SelfImprover",
    "call_ai",
    "GitHubSeamless",
    "SingularityOrchestrator",
    "ChaosEngine",
    "SerendipityEngine",
]
