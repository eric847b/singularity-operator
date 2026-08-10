"""Singularity Operator v0.5.8 - Ultimate self-improving AI system.
EverythingDB + SelfImprover + ChaosEngine + SerendipityEngine + Orchestration +
GitHubSeamless + BrowserAutomation + UserscriptGenerator.

v0.5.8: Browser smoke + userscript generate/validate live self-evo test path.
v0.5.7: Auto-publish evolution_summary comments to ROI status issues.
v0.5.6: Multi-repo fleet orchestration.
v0.5.5: Deeper serendipity.
"""

from .everything_db import EverythingDB
from .self_improver import SelfImprover
from .groq_wrapper import call_ai, get_provider_status
from .github_seamless import GitHubSeamless
from .orchestrator import SingularityOrchestrator
from .chaos_engine import ChaosEngine
from .serendipity_engine import SerendipityEngine
from .browser_automation import BrowserAutomation
from .userscript_gen import UserscriptGenerator

__version__ = "0.5.8"
__all__ = [
    "EverythingDB",
    "SelfImprover",
    "call_ai",
    "GitHubSeamless",
    "SingularityOrchestrator",
    "ChaosEngine",
    "SerendipityEngine",
    "BrowserAutomation",
    "UserscriptGenerator",
]
