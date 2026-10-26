"""SelfImprover v0.5.20 - AI-driven evolution with free-AI primary path, shared validation and persistence."""

from datetime import datetime, timezone
from typing import Any, Dict, Optional

from .groq_wrapper import call_ai
from .everything_db import EverythingDB
from .validation import validate_python_evolution


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


class SelfImprover:
    def __init__(self, db_path: str = ".", db: Optional[EverythingDB] = None):
        self.db = db or EverythingDB(db_path)
        self.improvements_made = 0
        self.failures = 0
        self.evolution_log: list = []

    def evolve(self, code_snippet: str, goal: str = "max compactness + self-evolve + resilience + free AI") -> str:
        """
        Evolve a code snippet using free AI rotator first (local + Pollinations no-key + free tiers).
        Returns improved snippet or original if no meaningful change. Logs + persists to EverythingDB.
        Uses shared validation.validate_python_evolution for accept/reject.
        """
        prompt = f"""Analyze this code snippet and propose a compact improved version for goal: {goal}.
Focus on: efficiency, self-improvement hooks, error resilience, metrics, free-AI readiness. Return ONLY the improved Python code. Keep structure.

CODE:
{code_snippet[:1500]}
"""
        try:
            # Free AI rotator is primary (no hard provider lock)
            result = call_ai(prompt)
            resp = result.get("response", "") if isinstance(result, dict) else ""
            candidate = resp.strip()
            vr = validate_python_evolution(code_snippet, candidate, require_change=True)
            if not vr.ok:
                self.evolution_log.append(
                    {
                        "goal": goal,
                        "timestamp": _utc_now(),
                        "ok": False,
                        "reason": vr.reason,
                        "provider": result.get("provider") if isinstance(result, dict) else None,
                        "detail": vr.detail,
                    }
                )
                return code_snippet

            improved = vr.candidate or candidate
            self.improvements_made += 1
            entry = {
                "goal": goal,
                "timestamp": _utc_now(),
                "delta": len(improved) - len(code_snippet),
                "ok": True,
                "provider": result.get("provider") if isinstance(result, dict) else None,
                "validation": vr.reason,
            }
            self.evolution_log.append(entry)
            self.db.add_sequence(
                {
                    "evolution": goal,
                    "improvement_preview": improved[:200],
                    "delta": entry["delta"],
                    "provider": entry.get("provider"),
                    "validation": vr.as_dict(),
                },
                tags="self_improver",
                derives_from="self_improver.evolve",
            )
            self.db.metrics["learning_writes"] = self.db.metrics.get("learning_writes", 0) + 1
            print(f"SelfImprover v0.5.20: Applied evolution #{self.improvements_made} via {entry.get('provider')} for {goal}")
            return improved
        except Exception as e:
            self.failures += 1
            self.evolution_log.append({"goal": goal, "timestamp": _utc_now(), "ok": False, "error": str(e)[:120]})
            print(f"SelfImprover v0.5.20: evolution rejected ({e}); keeping original")
            return code_snippet

    def get_improvement_report(self) -> Dict[str, Any]:
        return {
            "improvements_made": self.improvements_made,
            "failures": self.failures,
            "log": self.evolution_log[-5:],
            "db_metrics": self.db.compute_metrics(),
        }

    def learning_summary_line(self) -> str:
        return f"SelfImprover: improvements={self.improvements_made} failures={self.failures} learning_writes={self.db.metrics.get('learning_writes', 0)}"


print("SelfImprover v0.5.20 - Free-AI primary + shared validation active")
