"""SingularityOrchestrator v0.5.2 - PDCA / self-evolve cycle orchestrator.

Coordinates EverythingDB, SelfImprover, GitHubSeamless for autonomous loops.
Supports multi-AI, serendipity injection, chaos experiments. Runs cycles toward singularity.
Emits one-line evolution_summary for ROI status issue after each cycle.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from .everything_db import EverythingDB
from .self_improver import SelfImprover
from .github_seamless import GitHubSeamless


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


class SingularityOrchestrator:
    def __init__(self, db: Optional[EverythingDB] = None):
        self.db = db or EverythingDB()
        self.improver = SelfImprover(db=self.db)
        self.gh = GitHubSeamless()
        self.cycle_count = 0
        self.metrics = {"cycles": 0, "improvements": 0, "serendipity": 0}
        self.last_summary: str = ""

    def run_orchestrated_cycle(self, tasks: List[str] = None) -> List[Dict[str, Any]]:
        if tasks is None:
            tasks = ["self_improve_core", "propose_unknown_sequences", "chaos_resilience_test"]
        results = []
        for task in tasks:
            self.cycle_count += 1
            if task == "self_improve_core":
                sample = "class CoreV1: pass  # TODO evolve"
                improved = self.improver.evolve(sample, goal="compact + self_evolve_v5 + metrics")
                results.append(
                    {"task": task, "result": "evolved", "improvements": self.improver.improvements_made}
                )
                self.metrics["improvements"] += 1
            elif task == "propose_unknown_sequences":
                seqs = self.db.propose_unknown("singularity acceleration", 3)
                results.append({"task": task, "sequences": seqs[:2]})
            elif task == "chaos_resilience_test":
                rec = self.db.chaos_recover("random_inspiration_noise")
                results.append({"task": task, "recovery": rec})
                self.metrics["serendipity"] += self.db.metrics.get("serendipity_captures", 0)
            else:
                results.append({"task": task, "status": "noop"})
        self.metrics["cycles"] += 1
        # Persist cycle summary + metrics
        self.db.add_sequence({"cycle": self.cycle_count, "metrics": self.metrics}, "orchestrator")
        self.db.persist_metrics()
        self.last_summary = self.evolution_summary()
        return results

    def evolution_summary(self) -> str:
        """One-line summary for ROI / living status issue (AI-owned continuous upgrade signal)."""
        h = self.db.get_health_snapshot()
        return (
            f"[{_utc_now()}] cycle={self.cycle_count} "
            f"improvements={self.improver.improvements_made} "
            f"seqs={h.get('sequences', 0)} "
            f"llm={self.db.metrics.get('llm_calls', 0)} "
            f"learning={self.db.metrics.get('learning_writes', 0)} "
            f"| {self.improver.learning_summary_line()}"
        )

    def get_status(self) -> Dict[str, Any]:
        return {
            "version": "0.5.2",
            "cycles": self.cycle_count,
            "db_health": self.db.get_health_snapshot(),
            "improver_report": self.improver.get_improvement_report(),
            "metrics": self.metrics,
            "last_summary": self.last_summary or self.evolution_summary(),
        }


print("SingularityOrchestrator v0.5.2 - Full autonomous cycles + evolution summary active")
