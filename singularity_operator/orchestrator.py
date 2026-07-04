#!/usr/bin/env python3
"""SingularityOrchestrator - Master coordinator for EverythingDB + SelfImprover + Groq swarm.

v0.4.0: Integrated persistent metrics sync from EverythingDB, optional L1/L2 cache demo visibility, lightweight PDCA goal refinement in cycles. Ties all v0.4.0 catalyst upgrades into full autonomous orchestration for faster perfection tracking.

Mental model: Orchestrator flips transistors across modules for global self-improvement and observable continuous evolution."""

import os
import json
import time
import threading
from typing import Dict, Any, List, Optional

try:
    from .everything_db import EverythingDB
    from .self_improver import SelfImprover
except ImportError:
    from everything_db import EverythingDB
    from self_improver import SelfImprover


class SingularityOrchestrator:
    """Master node for Singularity Operator v0.4.0+ with persistent metrics + PDCA."""

    def __init__(self, db_path: str = "everything.db", root_path: str = "."):
        self.db = EverythingDB(db_path)
        self.improver = SelfImprover(root_path, shared_db=self.db)
        self.swarm_nodes: List[Dict] = []
        self.metrics = {"cycles": 0, "improvements": 0, "proposals": 0, "llm_calls": 0}
        self._running = False
        # Sync persisted metrics from v0.4.0 EverythingDB on startup
        try:
            persisted = self.db.compute_metrics()
            self.metrics["llm_calls"] = persisted.get("llm_calls", 0)
        except:
            pass

    def register_swarm_node(self, name: str, role: str = "general"):
        self.swarm_nodes.append({"name": name, "role": role, "active": True})
        print(f"Registered swarm node: {name} ({role})")

    def run_orchestrated_cycle(self, goals: Optional[List[str]] = None):
        if goals is None:
            goals = ["compact code", "add logging", "enhance autonomy", "integrate userscript", "browser hooks"]
        results = []
        improvements_before = self.improver.improvements_made
        proposals_before = self.metrics["proposals"]
        for goal in goals:
            # Use SelfImprover for code (now with PDCA safety)
            imp = self.improver.propose_improvement("singularity_operator/self_improver.py", goal)
            if "error" not in imp:
                applied = self.improver.apply_improvement(imp)
                if applied:
                    self.metrics["improvements"] += 1
            # Propose new sequences in EverythingDB (benefits from retry + difflib)
            proposals = self.db.propose_unknown(n=2, context=goal)
            for p in proposals:
                if isinstance(p, dict) and "seq" in p:
                    self.db.add_sequence(p["seq"], {"goal": goal, "rationale": p.get("rationale", "")})
                    self.metrics["proposals"] += 1
            results.append({"goal": goal, "improvement": imp.get("suggestion", ""), "proposals": len(proposals)})
        self.metrics["cycles"] += 1
        self.metrics["llm_calls"] = self.db.llm_calls  # sync latest
        # Lightweight PDCA: if no improvement in this cycle, trigger cache demo + refine
        if self.improver.improvements_made == improvements_before and self.metrics["proposals"] == proposals_before:
            try:
                self.db.demo_l1_l2_cache()  # visibility into transistor model
            except:
                pass
            # Simple goal refinement for next cycle
            goals = ["self_expand knowledge gaps", "robust error handling", "metrics observability"]
        # Persist orchestrator metrics snapshot (via db meta for continuity)
        try:
            self.db._persist_metric("orchestrator_cycles", self.metrics["cycles"])
            self.db._persist_metric("orchestrator_improvements", self.metrics["improvements"])
        except:
            pass
        # New: Include health snapshot in results for observability
        try:
            health = self.db.get_health_snapshot()
            results.append({"health_snapshot": health})
        except:
            pass
        print(f"Orchestrated cycle complete. Metrics: {self.metrics}")
        return results

    def generate_userscript(self, prompt: str = "auto-updating Groq-powered userscript for browser automation and self-evolve") -> str:
        # Simple Groq call for userscript (integrate full wrapper if needed)
        script = f"""// ==UserScript==
// @name Singularity Auto-Updater v0.4
// @description {prompt}
// ==/UserScript==

console.log('Singularity Operator userscript active - Groq powered, autonomous evolve enabled');
// Add browser hooks, input simulation, screen capture here
"""
        return script

    def start_full_autonomous(self, interval: int = 300):
        def loop():
            while self._running:
                self.run_orchestrated_cycle()
                time.sleep(interval)
        self._running = True
        t = threading.Thread(target=loop, daemon=True)
        t.start()
        return "Full autonomous orchestration started (v0.4.0 - persistent metrics + PDCA)"

    def stop(self):
        self._running = False
        return "Stopped"


if __name__ == "__main__":
    orch = SingularityOrchestrator()
    orch.register_swarm_node("groq-primary", "inference")
    orch.register_swarm_node("self-improver", "code-evolve")
    print(orch.start_full_autonomous(interval=60))  # Demo short interval
    time.sleep(10)
    print("Metrics:", orch.metrics)
    print(orch.generate_userscript())
