"""Shared validation helpers for Singularity Operator.

Structural / change-detection validation used by SelfImprover and available
to Orchestrator and future agents. Keeps evolution safety invariants in one place.
"""

from __future__ import annotations

import ast
from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class ValidationResult:
    ok: bool
    reason: str
    candidate: Optional[str] = None
    detail: Optional[str] = None

    def as_dict(self) -> Dict[str, Any]:
        return {
            "ok": self.ok,
            "reason": self.reason,
            "candidate_preview": (self.candidate or "")[:200] if self.candidate else None,
            "detail": self.detail,
        }


def parse_python(source: str) -> ast.AST:
    """Parse source; raises SyntaxError on failure."""
    return ast.parse(source)


def is_valid_python(source: str) -> bool:
    try:
        parse_python(source)
        return True
    except SyntaxError:
        return False


def ast_equivalent(a: str, b: str) -> bool:
    """True if both parse and their ASTs are equal (whitespace-insensitive)."""
    try:
        ta = parse_python(a)
        tb = parse_python(b)
    except SyntaxError:
        return False
    return ast.dump(ta, include_attributes=False) == ast.dump(tb, include_attributes=False)


def validate_python_evolution(
    original: str,
    candidate: str,
    *,
    require_change: bool = True,
) -> ValidationResult:
    """Validate an evolved Python snippet against the original.

    Rules:
    - candidate must be non-empty
    - candidate must parse as Python
    - if require_change: candidate AST must differ from original AST
    - original is assumed valid; if original fails to parse, only candidate validity is checked
    """
    if not candidate or not str(candidate).strip():
        return ValidationResult(ok=False, reason="empty", candidate=candidate)

    cand = str(candidate).strip()
    try:
        parse_python(cand)
    except SyntaxError as e:
        return ValidationResult(
            ok=False,
            reason="syntax_error",
            candidate=cand,
            detail=str(e)[:200],
        )

    if require_change:
        try:
            if ast_equivalent(original, cand):
                return ValidationResult(ok=False, reason="no_change", candidate=cand)
        except SyntaxError:
            # original unparsable — allow candidate if it parses
            pass

    return ValidationResult(ok=True, reason="accepted", candidate=cand)


def validate_sequence_payload(value: Any) -> ValidationResult:
    """Lightweight structural check for knowledge units stored in EverythingDB."""
    if value is None:
        return ValidationResult(ok=False, reason="null_value")
    # Prefer JSON-serializable structures; strings and numbers are fine
    if isinstance(value, (str, int, float, bool)):
        return ValidationResult(ok=True, reason="scalar")
    if isinstance(value, (list, dict)):
        return ValidationResult(ok=True, reason="structured")
    return ValidationResult(ok=False, reason="unsupported_type", detail=type(value).__name__)
