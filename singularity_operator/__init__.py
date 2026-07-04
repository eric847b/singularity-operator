"""Singularity Operator v0.4.0 - All setpoints in a row: Orchestrator + GroqClient + BrowserAutomation + GitHubSeamless + UserscriptGenerator + EverythingDB (retry, difflib sim, L1/L2 demo, persist) + SelfImprover (real edits, PDCA rollback, metrics).

Full autonomous self-evolving system with GitHub integration, advanced userscripts, browser remote, multi-AI swarm, EverythingDB proposals, SelfImprover cycles with safe code surgery.

Highest ROI upgrades shipped: robust Groq loops, demonstrable transistor cache model, real autonomous code evolution with safety nets. Compact, zero bloat, PDCA everywhere. Perfection iteration continues.

User intent: Build the end-all-be-all self-improving AI. Eric (Mufnluvn) + Grok xAI"""

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
