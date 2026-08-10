"""Singularity Operator v0.5.7 - Ultimate self-improving AI system.
EverythingDB + SelfImprover + ChaosEngine + SerendipityEngine + Orchestration + GitHubSeamless.

v0.5.7: Auto-publish evolution_summary comments to ROI status issues (SO + AGA).
v0.5.6: Multi-repo fleet orchestration — status sync + catalyst propagation.
v0.5.5: Deeper serendipity — richer scoring, Groq-assisted bridges, bridge persist.
v0.5.4: Cross-sequence connections + advancing auto-seed.
v0.5.3: Real chaos engineering experiments.
"""

from .everything_db import EverythingDB
from .self_improver import SelfImprover
from .groq_wrapper import call_ai, get_provider_status
from .github_seamless import GitHubSeamless
from .orchestrator import SingularityOrchestrator
from .chaos_engine import ChaosEngine
from .serendipity_engine import SerendipityEngine

__version__ = "0.5.7"
__all__ = [
    "EverythingDB",
    "SelfImprover",
    "call_ai",
    "GitHubSeamless",
    "SingularityOrchestrator",
    "ChaosEngine",
    "SerendipityEngine",
]
