"""Singularity Operator v0.3.0

Ultimate: EverythingDB + SelfImprover + Orchestrator + GroqWrapper + CLI.
All to next setpoint: Groq integration, CLI, packaging, userscript output, full autonomous orchestration.

Compact | Autonomous | PDCA | Max Benefit | Zero Cost
Mental model: Transistors (knowledge states) + latches (cache) + orchestrated flips (self-improvement)."""

__version__ = "0.3.0"
__author__ = "Eric (Mufnluvn) + Grok xAI"

try:
    from .everything_db import EverythingDB
    from .self_improver import SelfImprover
    from .orchestrator import SingularityOrchestrator
    from .groq_wrapper import GroqWrapper
except ImportError:
    from everything_db import EverythingDB
    from self_improver import SelfImprover
    from orchestrator import SingularityOrchestrator
    from groq_wrapper import GroqWrapper

__all__ = ["EverythingDB", "SelfImprover", "SingularityOrchestrator", "GroqWrapper"]
