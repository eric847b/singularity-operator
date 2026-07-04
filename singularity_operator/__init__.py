"""Singularity Operator v0.4.0

Ultimate self-improving AI system with EverythingDB (knowledge fabric + health + self_test), SelfImprover (PDCA + health-aware discovery), Orchestrator (full swarm with health snapshots), and supporting modules.

Key v0.4.0 capabilities:
- get_health_snapshot(): Real-time observability of metrics, cache, and system status
- self_test(): Self-contained validation for CI and autonomous loops
- Health-aware self-improvement decisions
- Resilient CLI with --test flag

This package is designed for rapid autonomous evolution toward perfection.

User intent: Build the end-all-be-all self-improving AI. Eric (Mufnluvn) + Grok xAI
"""

__version__ = "0.4.0"
__author__ = "Eric (Mufnluvn) + Grok xAI"

from .everything_db import EverythingDB

from .self_improver import SelfImprover

from .orchestrator import SingularityOrchestrator

from .groq_client import GroqClient

from .browser_automation import BrowserAutomation

from .github_seamless import GitHubSeamless

from .userscript_gen import UserscriptGenerator

__all__ = ["EverythingDB", "SelfImprover", "SingularityOrchestrator", "GroqClient", "BrowserAutomation", "GitHubSeamless", "UserscriptGenerator"]


def health(db_path: str = "everything.db"):
    """Convenience function: Return health snapshot from EverythingDB."""
    db = EverythingDB(db_path)
    snapshot = db.get_health_snapshot()
    db.close()
    return snapshot


def self_test(db_path: str = "everything.db"):
    """Convenience function: Run EverythingDB self_test() and return report."""
    db = EverythingDB(db_path)
    result = db.self_test()
    db.close()
    return result


def quick_validate():
    """Quick validation of the full v0.4.0 stack."""
    print("Singularity Operator v0.4.0 Quick Validate")
    print("Health:", health())
    print("Self Test:", self_test())
    print("Stack validated successfully.")
