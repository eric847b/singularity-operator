"""Singularity Operator v0.3.0 - Multi-setpoint leap.

All setpoints in a row: GroqClient, BrowserAutomation, GitHubSeamless, AdvancedUserscriptGenerator + full integration in Orchestrator.

Autonomous, self-modifying, multi-AI, GitHub seamless, browser/remote control, userscript perfection."""

__version__ = "0.3.0"
__author__ = "Eric (Mufnluvn) + Grok xAI"

try:
    from .everything_db import EverythingDB
    from .self_improver import SelfImprover
    from .orchestrator import SingularityOrchestrator
    from .groq_client import GroqClient
    from .browser_automation import BrowserAutomation
    from .github_seamless import GitHubSeamless
    from .advanced_userscript import AdvancedUserscriptGenerator
except ImportError:
    from everything_db import EverythingDB
    from self_improver import SelfImprover
    from orchestrator import SingularityOrchestrator
    from groq_client import GroqClient
    from browser_automation import BrowserAutomation
    from github_seamless import GitHubSeamless
    from advanced_userscript import AdvancedUserscriptGenerator

__all__ = ["EverythingDB", "SelfImprover", "SingularityOrchestrator", "GroqClient", "BrowserAutomation", "GitHubSeamless", "AdvancedUserscriptGenerator"]
