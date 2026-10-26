"""Currency experiment next-action planner.

Turns top_experiment / top_score from the wealth fleet signal into a concrete,
provenance-linked next action. Draft-only: never marks won without real payment.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


# Concrete next steps keyed by experiment id from CURRENCY_STATUS / income_experiments
EXPERIMENT_PLAYBOOK: Dict[str, Dict[str, Any]] = {
    "setup-session-offer": {
        "title": "Book or deliver one real setup session",
        "expected_revenue": 149,
        "effort": 3,
        "steps": [
            "Open templates/setup_session_offer.md and confirm CTA + price still accurate",
            "Share offer link or SOW with one real prospect (not simulated)",
            "On paid delivery only: log income in tracker.py ledger; mark experiment won",
            "Update runway via runway.py after ledger write",
        ],
        "repo": "eric847b/zero-cost-wealth-playbook-tool",
        "artifacts": ["templates/setup_session_offer.md", "scripts/quote.py", "tracker.py"],
    },
    "oss-inbound-help": {
        "title": "Convert one GitHub issue/reply into a paid help offer",
        "expected_revenue": 99,
        "effort": 2,
        "steps": [
            "Pick one open inbound issue or reply in fleet/public repos",
            "Reply with scoped paid help offer ($99) + clear deliverable",
            "On acceptance + payment: log ledger; only then mark won",
        ],
        "repo": "eric847b/zero-cost-wealth-playbook-tool",
        "artifacts": ["scripts/quote.py", "tracker.py"],
    },
    "template-pack-listing": {
        "title": "Publish template pack listing and sell one pack",
        "expected_revenue": 79,
        "effort": 2,
        "steps": [
            "Paste PUBLIC_LISTING.md blurb to Gumroad/Lemon free-tier product",
            "Attach pack ZIP from scripts/pack_client.py output",
            "On first sale: log ledger; mark won only after payment confirmed",
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

    action = {
        "at": _utc_now(),
        "kind": "currency_next_action",
        "experiment_id": exp_id,
        "top_score": score,
        "title": play["title"],
        "expected_revenue": play.get("expected_revenue"),
        "effort": play.get("effort"),
        "steps": list(play.get("steps") or []),
        "repo": play.get("repo"),
        "artifacts": list(play.get("artifacts") or []),
        "currency_version": cur.get("version"),
        "preferred_currency_path": bool(cur.get("preferred_currency_path", True)),
        "roi_top_ref": roi.get("roi_top_ref"),
        "policy": {
            "draft_only": True,
            "no_force_merge": True,
            "never_mark_won_without_payment": True,
            "zero_paid_apis": True,
        },
        "hub_handoff": {
            "canonical_entry": "eric847b/AI-Collaboration-Hub",
            "note": "Surface this action in hub fleet status; singularity-operator remains specialized subsystem",
        },
        "status": "ready",
    }
    return action


def action_summary_line(action: Dict[str, Any]) -> str:
    return (
        f"next_action={action.get('experiment_id')} "
        f"title={action.get('title', '')[:60]} "
        f"score={action.get('top_score')} "
        f"rev={action.get('expected_revenue')}"
    )
