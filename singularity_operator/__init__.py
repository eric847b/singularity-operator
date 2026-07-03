"""Singularity Operator v0.2.0

Ultimate self-improving AI: EverythingDB (sequences + Groq), SelfImprover (autonomous evolve), Orchestrator (swarm + userscript + hooks).

All next steps implemented from setpoint: tighter integration, full autonomous orchestration, userscript generation, metrics, swarm.

Mental model: Transistors (states), latches (cache), proposals (transitions), orchestrated flips for global perfection."""

__version__ = "0.2.0"
__author__ = "Eric (Mufnluvn) + Grok xAI"

try:
    from .everything_db import EverythingDB
    from .self_improver import SelfImprover
    from .orchestrator import SingularityOrchestrator
except ImportError:
    from everything_db import EverythingDB
    from self_improver import SelfImprover
    from orchestrator import SingularityOrchestrator

__all__ = ["EverythingDB", "SelfImprover", "SingularityOrchestrator"]
