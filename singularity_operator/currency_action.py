"""Currency experiment next-action planner (autonomous-safe).

Turns top_experiment / top_score into a recorded next action with provenance.
Autonomous mode: records and publishes; does not require human outreach to run.
Never marks won without real payment — payment cannot be fabricated by the loop.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


EXPERIMENT_PLAYBOOK: Dict[str, Dict[str, Any]] = {
    "setup-session-offer": {
        "title": "Keep setup-session surface current; convert only on real inbound/payment",
        "expected_revenue": 149,
        "effort": 3,
        "steps": [
            "Autonomous: ensure offer/SOW/checklist templates remain accurate in wealth repo",
            "Autonomous: publish currency_next_action + digest signal for hub/agents",
            "Non-blocking optional: human capacity may book/deliver; not required for loop health",
            "Only after real payment: ledger write; never simulate income",
        ],
        "repo": "eric847b/zero-cost-wealth-playbook-tool",
        "artifacts": ["templates/setup_session_offer.md", "scripts/quote.py", "tracker.py"],
    },
    "oss-inbound-help": {
        "title": "Keep scoped OSS help offer ready for inbound threads",
        "expected_revenue": 99,
        "effort": 2,
        "steps": [
            "Autonomous: maintain templates/oss_inbound_help_offer.md accuracy",
            "Autonomous: surface experiment in ROI/fleet reports",
            "Convert only on real request + payment",
        ],
        "repo": "eric847b/zero-cost-wealth-playbook-tool",
        "artifacts": ["templates/oss_inbound_help_offer.md", "scripts/quote.py"],
    },
    "template-pack-listing": {
        "title": "Keep client pack + PUBLIC_LISTING release-ready",
        "expected_revenue": 79,
        "effort": 2,
        "steps": [
            "Autonomous: pack_client.py and PUBLIC_LISTING.md stay valid",
            "Autonomous: release workflow can attach zip on tag",
            "Marketplace paste is optional human capacity — not a loop dependency",
        ],
        "repo": "eric847b/zero-cost-wealth-playbook-tool",
        "artifacts": ["PUBLIC_LISTING.md", "scripts/pack_client.py"],
    },
}

DEFAULT_EXPERIMENT = "setup-session-offer"


def plan_next_action(
    currency_signal: Optional[Dict[str, Any]] = None,
    roi_pick: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Build a concrete next-action dict from currency + ROI context."""
    cur = currency_signal or {}
    roi = roi_pick or {}
    exp_id = (
        cur.get("top_experiment")
        or roi.get("top_experiment")
        or DEFAULT_EXPERIMENT
    )
    score = cur.get("top_score") if cur.get("top_score") is not None else roi.get("top_score")
    play = EXPERIMENT_PLAYBOOK.get(exp_id) or EXPERIMENT_PLAYBOOK[DEFAULT_EXPERIMENT]
    if exp_id not in EXPERIMENT_PLAYBOOK:
        exp_id = DEFAULT_EXPERIMENT

    # v0.5.23: signal freshness for live confirmation
    signal_at = cur.get("updated") or cur.get("at") or _utc_now()
    freshness_note = "live_signal_confirmed" if cur.get("ok") or cur.get("preferred_currency_path") else "fallback"

    # v0.5.24: computed ROI-per-effort for ranking precision
    exp_rev = play.get("expected_revenue") or 0
    effort = play.get("effort") or 1
    roi_per_effort = round(exp_rev / effort, 2) if effort else 0.0

    action = {
        "at": _utc_now(),
        "kind": "currency_next_action",
        "mode": "autonomous",
        "experiment_id": exp_id,
        "top_score": score,
        "title": play["title"],
        "expected_revenue": exp_rev,
        "effort": effort,
        "roi_per_effort": roi_per_effort,
        "steps": list(play.get("steps") or []),
        "repo": play.get("repo"),
        "artifacts": list(play.get("artifacts") or []),
        "currency_version": cur.get("version"),
        "preferred_currency_path": bool(cur.get("preferred_currency_path", True)),
        "roi_top_ref": roi.get("roi_top_ref"),
        "signal_freshness": freshness_note,
        "signal_at": signal_at,
        "policy": {
            "draft_only": True,
            "no_force_merge": True,
            "never_mark_won_without_payment": True,
            "zero_paid_apis": True,
            "no_human_required": True,
            "no_simulated_income": True,
        },
        "hub_handoff": {
            "canonical_entry": "eric847b/AI-Collaboration-Hub",
            "note": "Autonomous fleet signal; singularity-operator is specialized subsystem",
        },
        "status": "recorded",
    }
    return action


def action_summary_line(action: Dict[str, Any]) -> str:
    """Compact one-line summary that surfaces ROI-per-effort for ranking visibility."""
    return (
        f"next_action={action.get('experiment_id')} "
        f"mode={action.get('mode', 'autonomous')} "
        f"roi_pe={action.get('roi_per_effort', '?')} "
        f"score={action.get('top_score')} "
        f"rev={action.get('expected_revenue')} "
        f"effort={action.get('effort')} "
        f"fresh={action.get('signal_freshness', '?')} "
        f"title={str(action.get('title', ''))[:40]}"
    )
