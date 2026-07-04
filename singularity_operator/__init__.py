"""Singularity Operator v0.3.0 - All setpoints in a row: Orchestrator + GroqClient + BrowserAutomation + GitHubSeamless + UserscriptGenerator.

Full autonomous self-evolving system with GitHub integration, advanced userscripts, browser remote, multi-AI swarm, EverythingDB proposals, SelfImprover cycles."""

__version__ = "0.3.0"
__author__ = "Eric (Mufnluvn) + Grok xAI"

from .everything_db import EverythingDB
from .self_improver import SelfImprover
from .orchestrator import SingularityOrchestrator
from .groq_client import GroqClient
from .browser_automation import BrowserAutomation
from .github_seamless import GitHubSeamless
from .userscript_gen import UserscriptGenerator

__all__ = ["EverythingDB", "SelfImprover", "SingularityOrchestrator", "GroqClient", "BrowserAutomation", "GitHubSeamless", "UserscriptGenerator"]"""