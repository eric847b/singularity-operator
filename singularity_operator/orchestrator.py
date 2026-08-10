"""SingularityOrchestrator v0.5.10 - PDCA + AGA metrics feedback loop.

Coordinates EverythingDB, SelfImprover, Chaos, Serendipity, GitHubSeamless,
Browser, Userscript. Ingests autonomous-github-agent profile metrics into DB.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from .everything_db import EverythingDB
from .self_improver import SelfImprover
from .github_seamless import GitHubSeamless
from .chaos_engine import ChaosEngine
from .serendipity_engine import SerendipityEngine
from .browser_automation import BrowserAutomation
from .userscript_gen import UserscriptGenerator


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


class SingularityOrchestrator:
    def __init__(self, db: Optional[EverythingDB] = None):
        self.db = db or EverythingDB(enable_vectors=True)
        self.improver = SelfImprover(db=self.db)
        self.gh = GitHubSeamless()
        self.chaos = ChaosEngine(db=self.db)
        self.serendipity = SerendipityEngine(db=self.db)
        self.browser = BrowserAutomation(headless=True)
        self.userscript = UserscriptGenerator()
        self.cycle_count = 0
        self.metrics = {
            "cycles": 0,
            "improvements": 0,
            "serendipity": 0,
            "chaos_runs": 0,
            "fleet_syncs": 0,
            "evolution_reports": 0,
            "browser_tests": 0,
            "userscript_tests": 0,
            "vector_demos": 0,
            "aga_feedbacks": 0,
        }
        self.last_summary: str = ""
        self.last_aga: Optional[Dict[str, Any]] = None

    def run_orchestrated_cycle(self, tasks: List[str] = None) -> List[Dict[str, Any]]:
        if tasks is None:
            tasks = [
                "self_improve_core",
                "propose_unknown_sequences",
                "serendipity_cycle",
                "chaos_resilience_test",
                "browser_userscript_test",
                "vector_demo",
                "aga_feedback",
                "fleet_sync",
                "publish_evolution_report",
            ]
        results = []
        for task in tasks:
            self.cycle_count += 1
            if task == "self_improve_core":
                sample = "class CoreV1: pass  # TODO evolve"
                self.improver.evolve(
                    sample,
                    goal="compact + metrics + AGA feedback + multi-repo",
                )
                results.append(
                    {
                        "task": task,
                        "result": "evolved",
                        "improvements": self.improver.improvements_made,
                    }
                )
                self.metrics["improvements"] += 1
            elif task == "propose_unknown_sequences":
                seqs = self.db.propose_unknown("singularity acceleration", 3)
                results.append({"task": task, "sequences": seqs[:2]})
            elif task == "serendipity_cycle":
                ser = self.serendipity.run_cycle(connections=4, amplifications=3, deep=True)
                results.append(
                    {
                        "task": task,
                        "captures": ser["captures"],
                        "connections": ser["connections_found"],
                        "bridges": ser.get("bridges_persisted", 0),
                        "groq_insights": ser.get("groq_insights", 0),
                        "summary": self.serendipity.summary_line(),
                    }
                )
                self.metrics["serendipity"] += ser["captures"]
            elif task == "chaos_resilience_test":
                battery = self.chaos.run_battery(n=3)
                results.append(
                    {
                        "task": task,
                        "experiments": len(battery),
                        "resilience": self.chaos.resilience_score,
                        "summary": self.chaos.summary_line(),
                    }
                )
                self.metrics["chaos_runs"] += len(battery)
            elif task == "browser_userscript_test":
                smoke = self.browser.run_smoke_suite()
                us = self.userscript.run_self_evo_test()
                self.db.add_sequence(
                    {"browser_smoke": smoke, "userscript": us},
                    "self_evo:browser_userscript",
                )
                results.append(
                    {
                        "task": task,
                        "browser_pass_rate": smoke.get("pass_rate"),
                        "userscript_ok": (us.get("validation") or {}).get("ok"),
                    }
                )
                self.metrics["browser_tests"] += 1
                self.metrics["userscript_tests"] += 1
            elif task == "vector_demo":
                demo = self.db.demo_vector_query("self improve serendipity singularity evolution")
                results.append(
                    {
                        "task": task,
                        "hits": demo.get("hits"),
                        "vector_queries": self.db.metrics.get("vector_queries"),
                    }
                )
                self.metrics["vector_demos"] += 1
            elif task == "aga_feedback":
                ing = self.gh.ingest_aga_feedback(db=self.db)
                fb = ing.get("feedback") or {}
                self.last_aga = fb
                results.append(
                    {
                        "task": task,
                        "status": ing.get("status"),
                        "aga_runs": fb.get("runs"),
                        "roi_top_ref": fb.get("roi_top_ref"),
                        "roi_top_score": fb.get("roi_top_score"),
                        "fleet_health": fb.get("fleet_last_health"),
                        "stored_key": ing.get("stored_key"),
                    }
                )
                self.metrics["aga_feedbacks"] += 1
            elif task == "fleet_sync":
                summary = self.evolution_summary()
                sync = self.gh.sync_status(
                    summary,
                    target_repos=[
                        "eric847b/autonomous-github-agent",
                        "eric847b/AI-Collaboration-Hub",
                    ],
                )
                results.append(
                    {
                        "task": task,
                        "sync": sync.get("status"),
                        "targets": sync.get("targets"),
                    }
                )
                self.metrics["fleet_syncs"] += 1
            elif task == "publish_evolution_report":
                summary = self.evolution_summary()
                extra = {
                    "orchestrator_metrics": self.metrics.copy(),
                    "aga_feedback": self.last_aga,
                    "db_metrics": self.db.metrics.copy(),
                    "gh": self.gh.get_metrics(),
                }
                pub = self.gh.publish_evolution_report(summary, extra=extra)
                results.append(
                    {
                        "task": task,
                        "status": pub.get("status"),
                        "results": pub.get("results"),
                    }
                )
                self.metrics["evolution_reports"] += 1
            else:
                results.append({"task": task, "status": "noop"})
        self.metrics["cycles"] += 1
        self.db.add_sequence({"cycle": self.cycle_count, "metrics": self.metrics}, "orchestrator")
        self.db.persist_metrics()
        self.last_summary = self.evolution_summary()
        return results

    def evolution_summary(self) -> str:
        h = self.db.get_health_snapshot()
        aga = self.last_aga or {}
        aga_bit = ""
        if aga:
            aga_bit = (
                f"aga_runs={aga.get('runs', '?')} "
                f"roi={aga.get('roi_top_score', '?')}:{aga.get('roi_top_ref', '')} "
                f"fleet={aga.get('fleet_last_health', '?')} "
            )
        return (
            f"[{_utc_now()}] cycle={self.cycle_count} "
            f"improvements={self.improver.improvements_made} "
            f"seqs={h.get('sequences', 0)} "
            f"emb={h.get('embeddings', 0)} "
            f"llm={self.db.metrics.get('llm_calls', 0)} "
            f"vq={self.db.metrics.get('vector_queries', 0)} "
            f"chaos={self.chaos.experiments_run}/{self.chaos.resilience_score:.0f} "
            f"serendipity={self.serendipity.captures}/{self.serendipity.connections_found} "
            f"{aga_bit}"
            f"aga_ingests={self.gh.metrics.get('aga_ingests', 0)} "
            f"fleet_syncs={self.metrics.get('fleet_syncs', 0)} "
            f"evolution_reports={self.metrics.get('evolution_reports', 0)} "
            f"| {self.improver.learning_summary_line()} "
            f"| {self.chaos.summary_line()} "
            f"| {self.serendipity.summary_line()}"
        )

    def get_status(self) -> Dict[str, Any]:
        return {
            "version": "0.5.10",
            "cycles": self.cycle_count,
            "db_health": self.db.get_health_snapshot(),
            "aga_feedback": self.last_aga,
            "improver_report": self.improver.get_improvement_report(),
            "chaos_report": self.chaos.get_report(),
            "serendipity_report": self.serendipity.get_report(),
            "browser_metrics": self.browser.get_metrics(),
            "userscript_metrics": self.userscript.get_metrics(),
            "gh_metrics": self.gh.get_metrics(),
            "metrics": self.metrics,
            "last_summary": self.last_summary or self.evolution_summary(),
        }


print("SingularityOrchestrator v0.5.10 - AGA metrics feedback loop active")
