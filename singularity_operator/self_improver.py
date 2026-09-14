"""SelfImprover v0.5.3 - AI-driven evolution with validation and persistence."""

from datetime import datetime, timezone
from typing import Any, Dict, Optional
import ast

from .groq_wrapper import call_ai
from .everything_db import EverythingDB


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


class SelfImprover:
    def __init__(self, db_path: str = ".", db: Optional[EverythingDB] = None):
        self.db = db or EverythingDB(db_path)
        self.improvements_made = 0
        self.failures = 0
        self.evolution_log: list = []

    def evolve(self, code_snippet: str, goal: str = "max compactness + self-evolve + resilience") -> str:
        prompt = f"""Analyze this code snippet and propose a compact improved version for goal: {goal}.
Focus on: efficiency, self-improvement hooks, error resilience, metrics. Return ONLY the improved Python code. Keep structure.

CODE:
{code_snippet[:1500]}
"""
        try:
            result = call_ai(prompt, provider="groq")
            resp = result.get("response", "") if isinstance(result, dict) else ""
            candidate = resp.strip()
            if not candidate or candidate == code_snippet.strip():
                self.evolution_log.append({"goal": goal, "timestamp": _utc_now(), "ok": False, "reason": "no_change"})
                return code_snippet
            ast.parse(candidate)
            ast.parse(code_snippet)
            improved = candidate
            self.improvements_made += 1
            entry = {"goal": goal, "timestamp": _utc_now(), "delta": len(improved) - len(code_snippet), "ok": True}
            self.evolution_log.append(entry)
            self.db.add_sequence({"evolution": goal, "improvement_preview": improved[:200], "delta": entry["delta"]}, "self_improver")
            self.db.metrics["learning_writes"] = self.db.metrics.get("learning_writes", 0) + 1
            print(f"SelfImprover v0.5.3: Applied evolution #{self.improvements_made} for {goal}")
            return improved
        except Exception as e:
            self.failures += 1
            self.evolution_log.append({"goal": goal, "timestamp": _utc_now(), "ok": False, "error": str(e)[:120]})
            print(f"SelfImprover v0.5.3: evolution rejected ({e}); keeping original")
            return code_snippet

    def get_improvement_report(self) -> Dict[str, Any]:
        return {"improvements_made": self.improvements_made, "failures": self.failures, "log": self.evolution_log[-5:], "db_metrics": self.db.compute_metrics()}

    def learning_summary_line(self) -> str:
        return f"SelfImprover: improvements={self.improvements_made} failures={self.failures} learning_writes={self.db.metrics.get('learning_writes', 0)}"


print("SelfImprover v0.5.3 - Validated AI evolution active")
