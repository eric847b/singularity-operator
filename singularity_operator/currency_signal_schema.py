"""Shared currency fleet signal schema (parity with AGA roi_catalyst).

Core keys must match autonomous-github-agent ROI Catalyst CURRENCY_CORE_KEYS
and GitHubSeamless.fetch_currency_signals output.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, Iterable, Optional

CORE_KEYS = (
    "ok",
    "source",
    "at",
    "version",
    "preferred_currency_path",
    "status",
    "top_experiment",
    "top_score",
    "capabilities",
    "roi_note",
    "status_file_present",
    "mode",
)

DEFAULT_SOURCE = "eric847b/zero-cost-wealth-playbook-tool"


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def normalize_currency_signal(raw: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Return a dict with shared core keys filled; never invents payment."""
    r = raw or {}
    caps = r.get("capabilities") or []
    if not isinstance(caps, list):
        caps = list(caps) if isinstance(caps, Iterable) else []
    return {
        "ok": bool(r.get("ok")),
        "source": r.get("source") or DEFAULT_SOURCE,
        "at": r.get("at") or _utc_now(),
        "version": r.get("version"),
        "preferred_currency_path": bool(r.get("preferred_currency_path", False)),
        "status": r.get("status") or "unknown",
        "top_experiment": r.get("top_experiment"),
        "top_score": r.get("top_score"),
        "capabilities": list(caps),
        "roi_note": (r.get("roi_note") or "")[:240],
        "status_file_present": bool(r.get("status_file_present")),
        "mode": r.get("mode") or "autonomous",
    }


def extract_from_aga_profile(profile: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Build signal from AGA .agent_profile.json currency fields when present."""
    p = profile or {}
    if p.get("currency_signal") and isinstance(p["currency_signal"], dict):
        return normalize_currency_signal(p["currency_signal"])
    if p.get("currency_top_experiment") is not None or p.get("currency_version"):
        return normalize_currency_signal(
            {
                "ok": True,
                "version": p.get("currency_version"),
                "top_experiment": p.get("currency_top_experiment"),
                "top_score": p.get("currency_top_score"),
                "preferred_currency_path": bool(p.get("currency_preferred", True)),
                "status": "from_aga_profile",
                "mode": "autonomous",
            }
        )
    return normalize_currency_signal({"ok": False})
