"""SingularityOrchestrator v0.5.20 - Continuous ROI + currency next-action + hub-first fleet + agent proposals.

Currency path: fetch_currency_signals → continuous_roi_rank → currency_next_action
(concrete steps for top_experiment with provenance).
Fleet sync prioritizes AI-Collaboration-Hub as canonical entry.
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
from .free_ai_client import get_free_ai
from .agent_proposals import AgentProposalWorkflow
from .currency_action import plan_next_action, action_summary_line


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
        self.proposals = AgentProposalWorkflow(db=self.db)
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
            "roi_ranks": 0,
            "currency_signals": 0,
            "agent_proposals": 0,
            "currency_actions": 0,
        }
        self.last_summary: str = ""
        self.last_aga: Optional[Dict[str, Any]] = None
        self.last_roi_pick: Optional[Dict[str, Any]] = None
        self.last_roi_key: Optional[str] = None
        self.last_free_ai_status: Optional[Dict[str, Any]] = None
        self.last_currency: Optional[Dict[str, Any]] = None
        self.last_currency_key: Optional[str] = None
        self.last_proposal_report: Optional[Dict[str, Any]] = None
        self.last_currency_action: Optional[Dict[str, Any]] = None

    def run_orchestrated_cycle(self, tasks: List[str] = None) -> List[Dict[str, Any]]:
        if tasks is None:
            tasks = [
                "self_improve_core",
                "propose_unknown_sequences",
                "agent_propose",
                "serendipity_cycle",
                "chaos_resilience_test",
                "browser_userscript_test",
                "vector_demo",
                "aga_feedback",
                "currency_signal",
                "continuous_roi_rank",
                "currency_next_action",
                "free_ai_status",
                "fleet_sync",
                "publish_evolution_report",
            ]
        results = []
        for task in tasks:
            self.cycle_count += 1
            if task == "self_improve_core":
                sample = "class CoreV1: pass  # TODO evolve"
                before = self.improver.improvements_made
                evolved = self.improver.evolve(
                    sample,
                    goal="compact + continuous ROI ranking + currency experiment ranking + free AI context",
                )
                accepted = evolved.strip() != sample.strip()
                actual = self.improver.improvements_made - before
                results.append({
                    "task": task,
                    "result": "evolved" if accepted else "rejected",
                    "accepted": accepted,
                    "improvements": actual,
                })
                self.metrics["improvements"] += actual
            elif task == "propose_unknown_sequences":
                seqs = self.db.propose_unknown("singularity acceleration + currency experiment ranking", 3)
                results.append({"task": task, "sequences": seqs[:2]})
            elif task == "agent_propose":
                report = self.proposals.run(
                    domain="singularity acceleration + currency experiment ranking",
                    n=3,
                    parent_key=self.last_currency_key,
                )
                self.last_proposal_report = report
                results.append({
                    "task": task,
                    "generated": report.get("generated"),
                    "accepted": report.get("accepted"),
                    "rejected": report.get("rejected"),
                    "batch_parent": report.get("batch_parent"),
                })
                self.metrics["agent_proposals"] += int(report.get("accepted") or 0)
            elif task == "serendipity_cycle":
                ser = self.serendipity.run_cycle(connections=4, amplifications=3, deep=True)
                results.append({"task": task, "captures": ser["captures"], "connections": ser["connections_found"], "summary": self.serendipity.summary_line()})
                self.metrics["serendipity"] += ser["captures"]
            elif task == "chaos_resilience_test":
                battery = self.chaos.run_battery(n=3)
                results.append({"task": task, "experiments": len(battery), "resilience": self.chaos.resilience_score})
                self.metrics["chaos_runs"] += len(battery)
            elif task == "browser_userscript_test":
                smoke = self.browser.run_smoke_suite()
                us = self.userscript.run_self_evo_test()
                self.db.add_sequence(
                    {"browser_smoke": smoke, "userscript": us},
                    tags="self_evo:browser_userscript",
                    derives_from="browser_userscript_test",
                )
                results.append({"task": task, "browser_pass_rate": smoke.get("pass_rate"), "userscript_ok": (us.get("validation") or {}).get("ok")})
                self.metrics["browser_tests"] += 1
                self.metrics["userscript_tests"] += 1
            elif task == "vector_demo":
                demo = self.db.demo_vector_query("self improve serendipity singularity currency wealth experiment")
                results.append({"task": task, "hits": demo.get("hits")})
                self.metrics["vector_demos"] += 1
            elif task == "aga_feedback":
                ing = self.gh.ingest_aga_feedback(db=self.db)
                fb = ing.get("feedback") or {}
                self.last_aga = fb
                results.append({"task": task, "status": ing.get("status"), "roi_top_ref": fb.get("roi_top_ref"), "roi_top_score": fb.get("roi_top_score")})
                self.metrics["aga_feedbacks"] += 1
            elif task == "currency_signal":
                cur = self.gh.fetch_currency_signals()
                self.last_currency = cur
                key = self.db.add_sequence(
                    cur,
                    tags="currency:fleet_signal",
                    modality="text",
                    derives_from="currency_signal",
                )
                self.last_currency_key = key
                results.append({
                    "task": task,
                    "version": cur.get("version"),
                    "preferred": cur.get("preferred_currency_path"),
                    "top_experiment": cur.get("top_experiment"),
                    "top_score": cur.get("top_score"),
                    "capabilities": cur.get("capabilities"),
                    "status_file": cur.get("status_file_present"),
                    "stored_key": key,
                })
                self.metrics["currency_signals"] += 1
            elif task == "continuous_roi_rank":
                aga = self.last_aga or {}
                cur = self.last_currency or {}
                prefer_currency = bool(cur.get("preferred_currency_path"))
                top_exp = cur.get("top_experiment") or "setup-session-offer"
                top_score = cur.get("top_score")
                pick = {
                    "at": _utc_now(),
                    "source": "aga_profile+currency_experiment",
                    "roi_top_ref": aga.get("roi_top_ref"),
                    "roi_top_score": aga.get("roi_top_score"),
                    "fleet_health": aga.get("fleet_last_health"),
                    "currency_version": cur.get("version"),
                    "currency_preferred": prefer_currency,
                    "currency_status": cur.get("status"),
                    "currency_capabilities": cur.get("capabilities") or [],
                    "currency_status_file": cur.get("status_file_present"),
                    "top_experiment": top_exp,
                    "top_score": top_score,
                    "action": "rank_recorded",
                    "note": (
                        f"HARD BIAS to currency fleet top experiment '{top_exp}' "
                        f"(score={top_score}). Prefer real work that advances runway velocity, "
                        f"experiment delivery, quote, or public listing. Draft-only; no force-merge. "
                        f"Never mark won without real payment. Free AI context in CONTINUOUS_CONTEXT.md."
                        if prefer_currency
                        else "Execute highest-ROI open catalyst work from roi_top_ref; draft-only; no force-merge."
                    ),
                }
                key = self.db.add_sequence(
                    pick,
                    tags="roi:live_rank",
                    modality="text",
                    parent_key=self.last_currency_key,
                    derives_from="continuous_roi_rank",
                )
                self.last_roi_pick = pick
                self.last_roi_key = key
                results.append({
                    "task": task,
                    "roi_top_ref": pick.get("roi_top_ref"),
                    "roi_top_score": pick.get("roi_top_score"),
                    "currency_preferred": prefer_currency,
                    "top_experiment": top_exp,
                    "top_score": top_score,
                    "stored_key": key,
                    "parent_key": self.last_currency_key,
                })
                self.metrics["roi_ranks"] += 1
            elif task == "currency_next_action":
                action = plan_next_action(
                    currency_signal=self.last_currency,
                    roi_pick=self.last_roi_pick,
                )
                parent = self.last_roi_key or self.last_currency_key
                key = self.db.add_sequence(
                    action,
                    tags="currency:next_action",
                    modality="text",
                    parent_key=parent,
                    derives_from="currency_next_action",
                )
                self.last_currency_action = action
                results.append({
                    "task": task,
                    "experiment_id": action.get("experiment_id"),
                    "title": action.get("title"),
                    "expected_revenue": action.get("expected_revenue"),
                    "steps": len(action.get("steps") or []),
                    "stored_key": key,
                    "parent_key": parent,
                    "summary": action_summary_line(action),
                })
                self.metrics["currency_actions"] += 1
            elif task == "free_ai_status":
                status = get_free_ai().get_status()
                self.last_free_ai_status = status
                self.db.add_sequence(
                    status,
                    tags="free_ai:status",
                    modality="text",
                    derives_from="free_ai_status",
                )
                results.append({"task": task, "available": status.get("available"), "tally": status.get("tally")})
            elif task == "fleet_sync":
                summary = self.evolution_summary()
                if self.last_currency_action:
                    summary = summary + " | " + action_summary_line(self.last_currency_action)
                # Hub first as canonical platform entry, then specialized subsystems
                sync = self.gh.sync_status(
                    summary,
                    target_repos=[
                        "eric847b/AI-Collaboration-Hub",
                        "eric847b/autonomous-github-agent",
                        "eric847b/zero-cost-wealth-playbook-tool",
                    ],
                )
                results.append({"task": task, "sync": sync.get("status"), "hub_first": True})
                self.metrics["fleet_syncs"] += 1
            elif task == "publish_evolution_report":
                summary = self.evolution_summary()
                if self.last_currency_action:
                    summary = summary + " | " + action_summary_line(self.last_currency_action)
                extra = {
                    "orchestrator_metrics": self.metrics.copy(),
                    "aga_feedback": self.last_aga,
                    "roi_pick": self.last_roi_pick,
                    "currency": self.last_currency,
                    "currency_action": self.last_currency_action,
                    "free_ai": self.last_free_ai_status,
                    "proposal_report": self.last_proposal_report,
                    "gh": self.gh.get_metrics(),
                }
                pub = self.gh.publish_evolution_report(summary, extra=extra)
                results.append({"task": task, "status": pub.get("status")})
                self.metrics["evolution_reports"] += 1
            else:
                results.append({"task": task, "status": "noop"})
        self.metrics["cycles"] += 1
        self.db.add_sequence(
            {"cycle": self.cycle_count, "metrics": self.metrics},
            tags="orchestrator",
            derives_from="run_orchestrated_cycle",
        )
        self.db.persist_metrics()
        self.last_summary = self.evolution_summary()
        return results

    def evolution_summary(self) -> str:
        h = self.db.get_health_snapshot()
        aga = self.last_aga or {}
        pick = self.last_roi_pick or {}
        fa = self.last_free_ai_status or {}
        cur = self.last_currency or {}
        act = self.last_currency_action or {}
        aga_bit = ""
        if aga or pick:
            aga_bit = f"aga_runs={aga.get('runs', '?')} roi={pick.get('roi_top_score') or aga.get('roi_top_score', '?')}:{pick.get('roi_top_ref') or aga.get('roi_top_ref', '')} fleet={aga.get('fleet_last_health', '?')} "
        fa_bit = f"free_ai_avail={fa.get('available', [])} " if fa else ""
        cur_bit = (
            f"currency={cur.get('version', '?')} prefer={cur.get('preferred_currency_path', False)} "
            f"top_exp={cur.get('top_experiment', '?')} top_score={cur.get('top_score', '?')} "
            if cur else ""
        )
        act_bit = f"next={act.get('experiment_id', '?')} " if act else ""
        return (
            f"[{_utc_now()}] cycle={self.cycle_count} improvements={self.improver.improvements_made} "
            f"seqs={h.get('sequences', 0)} emb={h.get('embeddings', 0)} llm={self.db.metrics.get('llm_calls', 0)} "
            f"chaos={self.chaos.experiments_run}/{self.chaos.resilience_score:.0f} "
            f"serendipity={self.serendipity.captures}/{self.serendipity.connections_found} "
            f"{aga_bit}{fa_bit}{cur_bit}{act_bit}"
            f"roi_ranks={self.metrics.get('roi_ranks', 0)} currency_signals={self.metrics.get('currency_signals', 0)} "
            f"currency_actions={self.metrics.get('currency_actions', 0)} "
            f"agent_proposals={self.metrics.get('agent_proposals', 0)} "
            f"aga_ingests={self.gh.metrics.get('aga_ingests', 0)} fleet_syncs={self.metrics.get('fleet_syncs', 0)} | "
            f"{self.improver.learning_summary_line()} | {self.chaos.summary_line()} | {self.serendipity.summary_line()}"
        )

    def get_status(self) -> Dict[str, Any]:
        return {
            "version": "0.5.20",
            "cycles": self.cycle_count,
            "db_health": self.db.get_health_snapshot(),
            "aga_feedback": self.last_aga,
            "roi_pick": self.last_roi_pick,
            "currency": self.last_currency,
            "currency_action": self.last_currency_action,
            "free_ai_status": self.last_free_ai_status,
            "proposal_report": self.last_proposal_report,
            "metrics": self.metrics,
            "gh_metrics": self.gh.get_metrics(),
            "last_summary": self.last_summary or self.evolution_summary(),
        }


print("SingularityOrchestrator v0.5.20 - Currency next-action + hub-first fleet active")
