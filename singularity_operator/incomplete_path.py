"""Incomplete-path recovery: multi-file / multi-component work that may land partially.

When only some required pieces exist, remember intended inputs, take a safe path,
and resume when the missing software (or signal) arrives. Supports the fleet
MERGE_POLICY: every PR mergeable to main; incomplete work must be inert.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Set


@dataclass
class IncompletePath:
    """Tracks a multi-piece unit of work that may be only partially present."""

    name: str
    required: Set[str]
    present: Set[str] = field(default_factory=set)
    remembered_input: Optional[Any] = None
    paused_for_update: bool = False
    last_safe_result: Any = None
    meta: Dict[str, Any] = field(default_factory=dict)

    def mark_present(self, piece: str) -> None:
        self.present.add(piece)
        if self.is_complete:
            self.paused_for_update = False

    @property
    def missing(self) -> Set[str]:
        return set(self.required) - set(self.present)

    @property
    def is_complete(self) -> bool:
        return self.required <= self.present

    def remember(self, payload: Any) -> None:
        self.remembered_input = payload

    def safe_execute(
        self,
        fn: Callable[..., Any],
        *args: Any,
        safe_default: Any = None,
        **kwargs: Any,
    ) -> Any:
        """Run fn only if complete; else remember args and return safe_default."""
        if args or kwargs:
            self.remember({"args": args, "kwargs": kwargs})
        if not self.is_complete:
            self.paused_for_update = True
            self.last_safe_result = safe_default
            return safe_default
        result = fn(*args, **kwargs)
        self.last_safe_result = result
        self.paused_for_update = False
        return result

    def resume_if_ready(self, fn: Callable[..., Any], safe_default: Any = None) -> Any:
        """If complete and we remembered input, re-run with that input."""
        if not self.is_complete:
            self.paused_for_update = True
            return self.last_safe_result if self.last_safe_result is not None else safe_default
        payload = self.remembered_input or {}
        if isinstance(payload, dict) and ("args" in payload or "kwargs" in payload):
            args = tuple(payload.get("args") or ())
            kwargs = dict(payload.get("kwargs") or {})
            return self.safe_execute(fn, *args, safe_default=safe_default, **kwargs)
        return self.safe_execute(fn, payload, safe_default=safe_default)

    def as_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "required": sorted(self.required),
            "present": sorted(self.present),
            "missing": sorted(self.missing),
            "complete": self.is_complete,
            "paused_for_update": self.paused_for_update,
            "has_remembered_input": self.remembered_input is not None,
            "meta": self.meta,
        }


class IncompletePathRegistry:
    """Named registry so orchestrators can heal dead ends across ticks."""

    def __init__(self) -> None:
        self._paths: Dict[str, IncompletePath] = {}

    def register(self, name: str, required: List[str], **meta: Any) -> IncompletePath:
        path = IncompletePath(name=name, required=set(required), meta=dict(meta))
        self._paths[name] = path
        return path

    def get(self, name: str) -> Optional[IncompletePath]:
        return self._paths.get(name)

    def mark_present(self, name: str, piece: str) -> Optional[IncompletePath]:
        path = self._paths.get(name)
        if path:
            path.mark_present(piece)
        return path

    def open_ends(self) -> List[Dict[str, Any]]:
        return [p.as_dict() for p in self._paths.values() if not p.is_complete]

    def heal_tick(self, runners: Dict[str, Callable[..., Any]]) -> List[Dict[str, Any]]:
        """Attempt resume for any path that became complete; return status list."""
        out: List[Dict[str, Any]] = []
        for name, path in self._paths.items():
            if path.is_complete and path.paused_for_update and name in runners:
                result = path.resume_if_ready(runners[name])
                out.append({"name": name, "resumed": True, "result_preview": str(result)[:120]})
            else:
                out.append(path.as_dict())
        return out
