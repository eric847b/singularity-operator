"""Currency experiment next-action planner (autonomous-safe).

Turns top_experiment / top_score into a recorded next action with provenance.
Autonomous mode: records and publishes; does not require human outreach to run.
Never marks won without real payment — payment cannot be fabricated by the loop.

v0.5.45: priority_mad (median absolute deviation) for robust dispersion of priority scores.
v0.5.44: days_since_signal + next_concrete_step + stale-signal confidence decay.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import statistics
import math


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _parse_signal_date(raw: Any) -> Optional[datetime]:
    """Best-effort parse of signal updated/at fields into aware UTC datetime."""
    if not raw:
        return None
    if isinstance(raw, datetime):
        return raw if raw.tzinfo else raw.replace(tzinfo=timezone.utc)
    s = str(raw).strip()
    if not s:
        return None
    # Common forms: 2026-11-19, 2026-11-19T12:00:00Z, ISO with offset
    for fmt in (
        "%Y-%m-%dT%H:%M:%S.%fZ",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%dT%H:%M:%S.%f%z",
        "%Y-%m-%d",
    ):
        try:
            dt = datetime.strptime(s.replace("+00:00", "Z").rstrip("Z") + ("Z" if "T" in s and not s.endswith("Z") and "+" not in s[-6:] else ""), fmt) if False else None
        except Exception:
            dt = None
        try:
            cleaned = s.replace("Z", "+00:00") if s.endswith("Z") else s
            if "T" in cleaned:
                dt = datetime.fromisoformat(cleaned)
            else:
                dt = datetime.strptime(cleaned[:10], "%Y-%m-%d").replace(tzinfo=timezone.utc)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt
        except Exception:
            continue
    return None


def _days_since(signal_at: Any) -> Optional[float]:
    dt = _parse_signal_date(signal_at)
    if not dt:
        return None
    now = datetime.now(timezone.utc)
    delta = now - dt
    return round(delta.total_seconds() / 86400.0, 2)


EXPERIMENT_PLAYBOOK: Dict[str, Dict[str, Any]] = {
    "setup-session-offer": {
        "title": "Keep setup-session surface current; convert only on real inbound/payment",
        "expected_revenue": 149,
        "effort": 3,
        "steps": [
            "Autonomous: ensure offer/SOW/checklist templates remain accurate in wealth repo",
            "Autonomous: publish currency_next_action + freshness signal for hub/agents",
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


def _compute_roi_pe(play: Dict[str, Any]) -> float:
    exp_rev = play.get("expected_revenue") or 0
    effort = play.get("effort") or 1
    return round(exp_rev / effort, 2) if effort else 0.0


def _ranked_experiments(confidence: float = 0.7) -> List[Dict[str, Any]]:
    """v0.5.29+: rank by ROI-per-effort; priority_score = (roi_pe / rank) * confidence."""
    ranked = []
    for eid, play in EXPERIMENT_PLAYBOOK.items():
        ranked.append({
            "experiment_id": eid,
            "roi_per_effort": _compute_roi_pe(play),
            "expected_revenue": play.get("expected_revenue") or 0,
            "effort": play.get("effort") or 1,
            "title": play.get("title", "")[:60],
        })
    ranked.sort(key=lambda x: x["roi_per_effort"], reverse=True)
    for i, item in enumerate(ranked):
        item["rank"] = i + 1
        base_priority = item["roi_per_effort"] / (i + 1)
        item["priority_score"] = round(base_priority * confidence, 2)
    return ranked


def _first_autonomous_step(steps: List[str]) -> str:
    for s in steps or []:
        if isinstance(s, str) and s.strip().lower().startswith("autonomous"):
            return s.strip()
    if steps:
        return str(steps[0]).strip()
    return ""


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

    signal_at = cur.get("updated") or cur.get("at") or _utc_now()
    freshness_note = "live_signal_confirmed" if cur.get("ok") or cur.get("preferred_currency_path") else "fallback"
    days_since = _days_since(signal_at)

    roi_per_effort = _compute_roi_pe(play)

    confidence = 0.7
    if freshness_note == "live_signal_confirmed":
        confidence += 0.2
    if score and score >= 80:
        confidence += 0.1
    # v0.5.44: decay confidence when the currency signal is stale
    if days_since is not None:
        if days_since > 14:
            confidence -= 0.25
        elif days_since > 7:
            confidence -= 0.15
        elif days_since > 5:
            confidence -= 0.08
    confidence = max(0.35, min(round(confidence, 2), 1.0))

    ranked = _ranked_experiments(confidence)

    top_by_priority = ranked[0]["experiment_id"] if ranked else DEFAULT_EXPERIMENT
    selection_reason = "explicit_signal" if (cur.get("top_experiment") or roi.get("top_experiment")) else "priority_rank"
    if not cur.get("top_experiment") and not roi.get("top_experiment"):
        exp_id = top_by_priority
        play = EXPERIMENT_PLAYBOOK[exp_id]
        roi_per_effort = _compute_roi_pe(play)
        selection_reason = "priority_rank"

    top_priority_score = ranked[0]["priority_score"] if ranked else 0.0
    experiment_count = len(ranked)
    avg_priority_score = round(sum(item["priority_score"] for item in ranked) / experiment_count, 2) if experiment_count else 0.0
    max_priority_score = max((item["priority_score"] for item in ranked), default=0.0)
    top_avg_delta = round(top_priority_score - avg_priority_score, 2)
    scores = [item["priority_score"] for item in ranked]
    priority_variance = round(statistics.variance(scores), 2) if len(scores) > 1 else 0.0
    selection_margin = round(top_priority_score - (ranked[1]["priority_score"] if len(ranked) > 1 else 0.0), 2)
    priority_std_dev = round(statistics.stdev(scores), 2) if len(scores) > 1 else 0.0
    sorted_scores = sorted(scores)
    n = len(sorted_scores)
    priority_median = round(statistics.median(scores), 2) if n else 0.0
    if n >= 4:
        q1 = statistics.median(sorted_scores[:n//2])
        q3 = statistics.median(sorted_scores[(n+1)//2:])
        priority_iqr = round(q3 - q1, 2)
    else:
        priority_iqr = 0.0
    min_priority_score = min(scores) if scores else 0.0
    priority_range = round(max_priority_score - min_priority_score, 2)
    priority_cv = round(priority_std_dev / avg_priority_score, 3) if avg_priority_score > 0 else 0.0
    if n > 2 and priority_std_dev > 0:
        mean = avg_priority_score
        cubed_devs = sum((s - mean) ** 3 for s in scores)
        priority_skewness = round((cubed_devs / n) / (priority_std_dev ** 3), 3)
    else:
        priority_skewness = 0.0
    if n > 3 and priority_std_dev > 0:
        mean = avg_priority_score
        fourth_devs = sum((s - mean) ** 4 for s in scores)
        priority_kurtosis = round((fourth_devs / n) / (priority_std_dev ** 4) - 3, 3)
    else:
        priority_kurtosis = 0.0
    priority_entropy = 0.0
    if n > 0 and sum(scores) > 0:
        total = sum(scores)
        probs = [s / total for s in scores if s > 0]
        if probs:
            entropy = -sum(p * math.log2(p) for p in probs)
            priority_entropy = round(entropy, 3)
    priority_gini = 0.0
    if n > 1 and sum(scores) > 0:
        sorted_scores_g = sorted(scores)
        cumsum = 0.0
        for i, s in enumerate(sorted_scores_g):
            cumsum += (i + 1) * s
        total = sum(sorted_scores_g)
        priority_gini = round((2 * cumsum) / (n * total) - (n + 1) / n, 3)
    priority_hhi = 0.0
    if n > 0 and sum(scores) > 0:
        total = sum(scores)
        shares = [s / total for s in scores]
        priority_hhi = round(sum(s * s for s in shares), 3)
    priority_top_share = 0.0
    if n > 0 and sum(scores) > 0:
        total = sum(scores)
        priority_top_share = round(top_priority_score / total, 3)
    priority_effective_n = round(1.0 / priority_hhi, 2) if priority_hhi > 0 else float(n)
    priority_top_rest_ratio = 0.0
    if n > 1 and sum(scores) > top_priority_score:
        rest_sum = sum(scores) - top_priority_score
        priority_top_rest_ratio = round(top_priority_score / rest_sum, 3) if rest_sum > 0 else float("inf")
    # v0.5.45: robust dispersion via median absolute deviation
    priority_mad = 0.0
    if n > 0:
        med = priority_median
        abs_devs = [abs(s - med) for s in scores]
        priority_mad = round(statistics.median(abs_devs), 3) if abs_devs else 0.0

    steps = list(play.get("steps") or [])
    next_concrete_step = _first_autonomous_step(steps)

    action = {
        "at": _utc_now(),
        "kind": "currency_next_action",
        "mode": "autonomous",
        "experiment_id": exp_id,
        "top_score": score,
        "title": play["title"],
        "expected_revenue": play.get("expected_revenue") or 0,
        "effort": play.get("effort") or 1,
        "roi_per_effort": roi_per_effort,
        "ranked_experiments": ranked,
        "confidence": confidence,
        "selection_reason": selection_reason,
        "top_priority_score": top_priority_score,
        "max_priority_score": max_priority_score,
        "experiment_count": experiment_count,
        "avg_priority_score": avg_priority_score,
        "top_avg_delta": top_avg_delta,
        "priority_variance": priority_variance,
        "selection_margin": selection_margin,
        "priority_std_dev": priority_std_dev,
        "priority_median": priority_median,
        "priority_iqr": priority_iqr,
        "priority_range": priority_range,
        "priority_cv": priority_cv,
        "priority_skewness": priority_skewness,
        "priority_kurtosis": priority_kurtosis,
        "priority_entropy": priority_entropy,
        "priority_gini": priority_gini,
        "priority_hhi": priority_hhi,
        "priority_top_share": priority_top_share,
        "priority_effective_n": priority_effective_n,
        "priority_top_rest_ratio": priority_top_rest_ratio,
        "priority_mad": priority_mad,
        "days_since_signal": days_since,
        "next_concrete_step": next_concrete_step,
        "steps": steps,
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
    return (
        f"next_action={action.get('experiment_id')} "
        f"mode={action.get('mode', 'autonomous')} "
        f"title={action.get('title', '')[:50]} "
        f"score={action.get('top_score')} "
        f"roi_pe={action.get('roi_per_effort', '?')} "
        f"conf={action.get('confidence', '?')} "
        f"fresh={action.get('signal_freshness', '?')} "
        f"days={action.get('days_since_signal', '?')} "
        f"step={str(action.get('next_concrete_step', ''))[:40]} "
        f"reason={action.get('selection_reason', '?')} "
        f"count={action.get('experiment_count', '?')} "
        f"avg_pri={action.get('avg_priority_score', '?')} "
        f"max_pri={action.get('max_priority_score', '?')} "
        f"delta={action.get('top_avg_delta', '?')} "
        f"var={action.get('priority_variance', '?')} "
        f"margin={action.get('selection_margin', '?')} "
        f"std={action.get('priority_std_dev', '?')} "
        f"med={action.get('priority_median', '?')} "
        f"iqr={action.get('priority_iqr', '?')} "
        f"range={action.get('priority_range', '?')} "
        f"cv={action.get('priority_cv', '?')} "
        f"skew={action.get('priority_skewness', '?')} "
        f"kurt={action.get('priority_kurtosis', '?')} "
        f"ent={action.get('priority_entropy', '?')} "
        f"gini={action.get('priority_gini', '?')} "
        f"hhi={action.get('priority_hhi', '?')} "
        f"top_share={action.get('priority_top_share', '?')} "
        f"eff_n={action.get('priority_effective_n', '?')} "
        f"top_rest={action.get('priority_top_rest_ratio', '?')} "
        f"mad={action.get('priority_mad', '?')}"
    )
