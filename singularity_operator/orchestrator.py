"""SingularityOrchestrator v0.5.8 - PDCA + chaos + serendipity + fleet + browser/userscript self-evo.

Coordinates EverythingDB, SelfImprover, ChaosEngine, SerendipityEngine, GitHubSeamless,
BrowserAutomation, UserscriptGenerator. Captures live smoke + userscript validation into DB
and publishes evolution_summary to ROI status issues.
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
        self.db = db or EverythingDB()
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
        }
        self.last_summary: str = ""

    def run_orchestrated_cycle(self, tasks: List[str] = None) -> List[Dict[str, Any]]:
        if tasks is None:
            tasks = [
                "self_improve_core",
                "propose_unknown_sequences",
                "serendipity_cycle",
                "chaos_resilience_test",
                "browser_userscript_test",
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
                    goal="compact + metrics + browser/userscript self-evo + multi-repo",
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
                # Live measurable path: HTTP smoke + userscript generate/validate
                smoke = self.browser.run_smoke_suite()
                us = self.userscript.run_self_evo_test()
                self.db.add_sequence(
                    {"browser_smoke": smoke, "userscript": us},
                    "self_evo:browser_userscript",
                )
                results.append(
                    {
                        "task": task,
                        "browser_ok": smoke.get("ok"),
                        "browser_pass_rate": smoke.get("pass_rate"),
                        "userscript_ok": (us.get("validation") or {}).get("ok"),
                        "browser_summary": self.browser.summary_line(),
                        "userscript_summary": self.userscript.summary_line(),
                    }
                )
                self.metrics["browser_tests"] += 1
                self.metrics["userscript_tests"] += 1
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
                        "gh_metrics": self.gh.get_metrics(),
                    }
                )
                self.metrics["fleet_syncs"] += 1
            elif task == "publish_evolution_report":
                summary = self.evolution_summary()
                extra = {
                    "orchestrator_metrics": self.metrics.copy(),
                    "serendipity": self.serendipity.get_report(),
                    "browser": self.browser.get_metrics(),
                    "userscript": self.userscript.get_metrics(),
                    "gh": self.gh.get_metrics(),
                }
                pub = self.gh.publish_evolution_report(summary, extra=extra)
                results.append(
                    {
                        "task": task,
                        "status": pub.get("status"),
                        "results": pub.get("results"),
                        "evolution_reports": self.gh.metrics.get("evolution_reports", 0),
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
        return (
            f"[{_utc_now()}] cycle={self.cycle_count} "
            f"improvements={self.improver.improvements_made} "
            f"seqs={h.get('sequences', 0)} "
            f"llm={self.db.metrics.get('llm_calls', 0)} "
            f"learning={self.db.metrics.get('learning_writes', 0)} "
            f"chaos={self.chaos.experiments_run}/{self.chaos.resilience_score:.0f} "
            f"serendipity={self.serendipity.captures}/{self.serendipity.connections_found}"
            f"/bridges={self.serendipity.bridges_persisted}"
            f"/groq={self.serendipity.groq_insights} "
            f"browser={self.browser.session_metrics.get('smoke_ok', 0)}/{self.browser.session_metrics.get('smoke_fail', 0)} "
            f"userscript={self.userscript.metrics.get('validated', 0)} "
            f"fleet_syncs={self.metrics.get('fleet_syncs', 0)} "
            f"evolution_reports={self.metrics.get('evolution_reports', 0)} "
            f"| {self.improver.learning_summary_line()} "
            f"| {self.chaos.summary_line()} "
            f"| {self.serendipity.summary_line()} "
            f"| {self.browser.summary_line()} "
            f"| {self.userscript.summary_line()}"
        )

    def get_status(self) -> Dict[str, Any]:
        return {
            "version": "0.5.8",
            "cycles": self.cycle_count,
            "db_health": self.db.get_health_snapshot(),
            "improver_report": self.improver.get_improvement_report(),
            "chaos_report": self.chaos.get_report(),
            "serendipity_report": self.serendipity.get_report(),
            "browser_metrics": self.browser.get_metrics(),
            "userscript_metrics": self.userscript.get_metrics(),
            "gh_metrics": self.gh.get_metrics(),
            "metrics": self.metrics,
            "last_summary": self.last_summary or self.evolution_summary(),
        }


print("SingularityOrchestrator v0.5.8 - Browser/userscript self-evo + fleet + publish")
