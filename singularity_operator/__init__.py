"""Singularity Operator v0.5.20 - Ultimate self-improving AI system.

v0.5.20: Release integrity; shared validation; multi-hop provenance; AgentProposalWorkflow;
         currency_next_action (top_experiment → concrete steps); hub-first fleet_sync.
v0.5.19: Deep currency experiment ranking (#43).
v0.5.18: Deepen currency signal (#43).
v0.5.17: Currency fleet signal (#43).
v0.5.16: FreeAIClient get_status + live provider tally.
v0.5.15–v0.5.10: Free AI rotator, ROI ranking, AGA feedback loop.
"""

from .everything_db import EverythingDB
from .self_improver import SelfImprover
from .groq_wrapper import call_ai, get_provider_status
from .free_ai_client import FreeAIClient, call_free_ai, get_free_ai
from .github_seamless import GitHubSeamless
from .orchestrator import SingularityOrchestrator
from .chaos_engine import ChaosEngine
from .serendipity_engine import SerendipityEngine
from .browser_automation import BrowserAutomation
from .userscript_gen import UserscriptGenerator
from .validation import (
    ValidationResult,
    validate_python_evolution,
    validate_sequence_payload,
    is_valid_python,
)
from .agent_proposals import AgentProposalWorkflow, run_proposal_cycle
from .currency_action import plan_next_action, action_summary_line

__version__ = "0.5.20"
__all__ = [
    "EverythingDB",
    "SelfImprover",
    "call_ai",
    "FreeAIClient",
    "call_free_ai",
    "get_free_ai",
    "get_provider_status",
    "GitHubSeamless",
    "SingularityOrchestrator",
    "ChaosEngine",
    "SerendipityEngine",
    "BrowserAutomation",
    "UserscriptGenerator",
    "ValidationResult",
    "validate_python_evolution",
    "validate_sequence_payload",
    "is_valid_python",
    "AgentProposalWorkflow",
    "run_proposal_cycle",
    "plan_next_action",
    "action_summary_line",
]
