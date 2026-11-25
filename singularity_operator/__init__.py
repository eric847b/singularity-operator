"""Singularity Operator v0.5.45 - Ultimate self-improving AI system.

v0.5.45: Currency action adds priority_mad (median absolute deviation) for robust dispersion of priority scores (#43). Version parity restored.
v0.5.44: Currency action adds days_since_signal + next_concrete_step + stale-signal confidence decay (#43). Version parity restored.
v0.5.43: Currency action adds priority_top_rest_ratio for sharper fleet selection metrics (#43). Version parity restored.
v0.5.42: Currency action adds priority_effective_n for sharper fleet selection metrics (#43). Version parity restored.
v0.5.41: Currency action adds priority_top_share for sharper fleet selection metrics (#43). Version parity restored.
v0.5.40: Currency action adds priority_hhi for sharper fleet selection metrics (#43). Version parity restored.
v0.5.39: Currency action adds priority_gini for sharper fleet selection metrics (#43). Version parity restored.
v0.5.38: Currency action adds priority_entropy for sharper fleet selection metrics (#43). Version parity restored.
v0.5.37: Currency action adds priority_kurtosis for sharper fleet selection metrics (#43). Version parity restored.
v0.5.36: Currency action adds priority_skewness for sharper fleet selection metrics (#43).
v0.5.35: Currency action adds priority_range + priority_cv for sharper fleet selection metrics (#43).
v0.5.34: Currency action adds priority_median + priority_iqr for sharper fleet selection metrics (#43).
v0.5.33: Currency action adds priority_std_dev for sharper fleet selection metrics (#43).
v0.5.32: Currency action adds priority_variance + selection_margin for sharper fleet selection metrics (#43).
v0.5.31: Currency action adds max_priority_score + top_avg_delta for sharper fleet selection metrics (#43).
v0.5.30: Currency action adds experiment_count + avg_priority_score for sharper fleet metrics (#43).
v0.5.29: Currency priority_score multiplies by confidence for live-signal weighting (#43).
v0.5.28: Currency action adds selection_reason + top_priority_score for sharper autonomous selection (#43).
v0.5.27: Currency ranked experiments add rank position + priority_score (roi_pe weighted by rank) for sharper autonomous selection (#43).
v0.5.26: FreeAIClient Together free-tier provider + provider_count status (#43).
v0.5.25: Currency ranked experiments by ROI-per-effort + confidence scoring for #43.
v0.5.24: Currency next-action adds computed roi_per_effort for ranking precision (#43).
v0.5.23: Currency action signal freshness + live confirmation provenance for #43.
v0.5.22: AGA usage/credits visibility + currency parity in orchestrator telemetry.
         MERGE_POLICY + IncompletePath + MaintenanceCrew + DynamicsCore
         (hard-fail resume, order variants, dynamics cache, resource morph).
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
from .incomplete_path import IncompletePath, IncompletePathRegistry
from .maintenance_crew import MaintenanceCrew, SoftEvent
from .dynamics_core import (
    DynamicsCore,
    DynamicsCache,
    DynamicStep,
    ProgressCheckpoint,
    ResourceProfile,
    STATE_ACTIVE,
    STATE_DEFERRED,
    STATE_INACTIVE,
)

__version__ = "0.5.45"
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
    "IncompletePath",
    "IncompletePathRegistry",
    "MaintenanceCrew",
    "SoftEvent",
    "DynamicsCore",
    "DynamicsCache",
    "DynamicStep",
    "ProgressCheckpoint",
    "ResourceProfile",
    "STATE_ACTIVE",
    "STATE_DEFERRED",
    "STATE_INACTIVE",
]
