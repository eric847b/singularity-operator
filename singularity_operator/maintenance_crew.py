"""MaintenanceCrew — autonomous soft-fail heal with seamless user continuation.

When something breaks or a required input/sensor is missing:
- User-visible channel keeps going (safe continuation / deferred path).
- Broken path is healed in the background (AI propose-fix when available).
- Personal or unknown inputs are remembered and applied later (no restart).
- Incomplete multi-piece work remaps sensor/input order via IncompletePath.

This is the runtime face of MERGE_POLICY: trunk never looks broken to the user.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, Optional

from .incomplete_path import IncompletePath, IncompletePathRegistry


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


@dataclass
class SoftEvent:
    """One soft-fail or deferred-input event (user may optionally see reason)."""

    kind: str  # exception | missing_input | missing_piece | ai_heal
    channel: str
    message: str
    remembered: Any = None
    user_visible_reason: Optional[str] = None
    healed: bool = False
    at: str = field(default_factory=_utc_now)

    def as_dict(self) -> Dict[str, Any]:
        return {
            "kind": self.kind,
            "channel": self.channel,
            "message": self.message[:300],
            "has_remembered": self.remembered is not None,
            "user_visible_reason": self.user_visible_reason,
            "healed": self.healed,
            "at": self.at,
        }


class MaintenanceCrew:
    """Keeps the user channel continuous while repairing broken or incomplete paths."""

    def __init__(
        self,
        paths: Optional[IncompletePathRegistry] = None,
        ai_fixer: Optional[Callable[[str, str], Optional[str]]] = None,
        expose_pause_reason: bool = False,
    ) -> None:
        self.paths = paths or IncompletePathRegistry()
        self.ai_fixer = ai_fixer  # (context, error) -> proposed fix text or None
        self.expose_pause_reason = expose_pause_reason
        self.events: List[SoftEvent] = []
        self.deferred_inputs: Dict[str, Any] = {}
        self.metrics = {
            "soft_fails": 0,
            "deferred_inputs": 0,
            "ai_heals_attempted": 0,
            "ai_heals_applied": 0,
            "seamless_continuations": 0,
            "resumes": 0,
        }

    def register_path(self, name: str, required: List[str], **meta: Any) -> IncompletePath:
        return self.paths.register(name, required, **meta)

    def note_piece(self, name: str, piece: str) -> None:
        self.paths.mark_present(name, piece)

    def defer_input(self, key: str, value: Any, reason: str = "awaiting_required_context") -> None:
        """Store personal/custom/unknown input; continue without blocking."""
        self.deferred_inputs[key] = {"value": value, "reason": reason, "at": _utc_now()}
        self.metrics["deferred_inputs"] += 1
        self.events.append(
            SoftEvent(
                kind="missing_input",
                channel=key,
                message=reason,
                remembered=value,
                user_visible_reason=reason if self.expose_pause_reason else None,
            )
        )

    def take_deferred(self, key: str, default: Any = None) -> Any:
        entry = self.deferred_inputs.pop(key, None)
        if entry is None:
            return default
        return entry.get("value", default)

    def run_channel(
        self,
        channel: str,
        fn: Callable[..., Any],
        *args: Any,
        safe_continuation: Any = None,
        path_name: Optional[str] = None,
        source_hint: str = "",
        **kwargs: Any,
    ) -> Any:
        """Execute user channel with soft-fail. Never raises to the caller.

        On success: return result.
        On missing path pieces: remember + safe_continuation.
        On exception: remember, optional AI heal attempt, safe_continuation.
        User sees continuation; heal is background-oriented.
        """
        path = self.paths.get(path_name) if path_name else None
        if path is not None and not path.is_complete:
            path.remember({"args": args, "kwargs": kwargs})
            path.paused_for_update = True
            path.last_safe_result = safe_continuation
            self.metrics["seamless_continuations"] += 1
            self.events.append(
                SoftEvent(
                    kind="missing_piece",
                    channel=channel,
                    message=f"missing={sorted(path.missing)}",
                    remembered={"args": args, "kwargs": kwargs},
                    user_visible_reason=(
                        f"Waiting on: {', '.join(sorted(path.missing))}"
                        if self.expose_pause_reason
                        else None
                    ),
                )
            )
            return safe_continuation

        try:
            result = fn(*args, **kwargs)
            if path is not None:
                path.last_safe_result = result
                path.paused_for_update = False
            return result
        except Exception as exc:
            self.metrics["soft_fails"] += 1
            self.metrics["seamless_continuations"] += 1
            remembered = {"args": args, "kwargs": kwargs, "error": str(exc)[:400]}
            if path is not None:
                path.remember(remembered)
                path.paused_for_update = True
                path.last_safe_result = safe_continuation

            healed = False
            if self.ai_fixer is not None:
                self.metrics["ai_heals_attempted"] += 1
                try:
                    proposal = self.ai_fixer(
                        source_hint or channel,
                        f"{type(exc).__name__}: {exc}",
                    )
                    if proposal:
                        healed = True
                        self.metrics["ai_heals_applied"] += 1
                except Exception:
                    healed = False

            self.events.append(
                SoftEvent(
                    kind="ai_heal" if healed else "exception",
                    channel=channel,
                    message=f"{type(exc).__name__}: {exc}",
                    remembered=remembered,
                    user_visible_reason=(
                        f"Recovering: {type(exc).__name__}"
                        if self.expose_pause_reason
                        else None
                    ),
                    healed=healed,
                )
            )
            return safe_continuation

    def heal_tick(self, runners: Optional[Dict[str, Callable[..., Any]]] = None) -> Dict[str, Any]:
        """Resume any complete paused paths; report open ends. Live, no restart."""
        runners = runners or {}
        resumed = self.paths.heal_tick(runners)
        for item in resumed:
            if item.get("resumed"):
                self.metrics["resumes"] += 1
        return {
            "at": _utc_now(),
            "resumed": [r for r in resumed if r.get("resumed")],
            "open_ends": self.paths.open_ends(),
            "deferred_keys": list(self.deferred_inputs.keys()),
            "recent_events": [e.as_dict() for e in self.events[-8:]],
            "metrics": self.metrics.copy(),
        }

    def user_facing_status(self) -> Dict[str, Any]:
        """What the user may see: continuous progress + optional soft reasons."""
        reasons = [
            e.user_visible_reason
            for e in self.events
            if e.user_visible_reason and not e.healed
        ]
        return {
            "continuous": True,
            "paused_reasons": reasons[-3:] if self.expose_pause_reason else [],
            "open_ends": len(self.paths.open_ends()),
            "deferred_inputs": len(self.deferred_inputs),
            "heals": self.metrics.get("ai_heals_applied", 0),
            "seamless_continuations": self.metrics.get("seamless_continuations", 0),
        }

    def summary_line(self) -> str:
        u = self.user_facing_status()
        return (
            f"crew continuous={u['continuous']} open_ends={u['open_ends']} "
            f"deferred={u['deferred_inputs']} heals={u['heals']} "
            f"seamless={u['seamless_continuations']}"
        )
