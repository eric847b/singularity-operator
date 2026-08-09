"""Singularity Operator v0.5.3 Launcher - Resilient entry + full demo cycle incl. chaos battery.

Runs EverythingDB + SelfImprover + ChaosEngine + Orchestrator.
Use in CI (auto-evolve.yml) or locally with GROQ_API_KEY for full power.
"""

import os
from datetime import datetime

from singularity_operator import (
    EverythingDB,
    SelfImprover,
    ChaosEngine,
    call_ai,
    GitHubSeamless,
    SingularityOrchestrator,
)


def main():
    print("=== Singularity Operator v0.5.3 ===")
    print(f"Time: {datetime.now().isoformat()}")
    print(f"Groq key present: {bool(os.getenv('GROQ_API_KEY'))}")

    db = EverythingDB(":memory:", mem_cache_size=8)
    improver = SelfImprover(db=db)
    chaos = ChaosEngine(db=db)
    orch = SingularityOrchestrator(db=db)

    print("\n[1] Propose unknown sequences...")
    unknowns = db.propose_unknown("core self-improvement + singularity", 4)
    print("Proposed:", unknowns[:3])

    print("\n[2] Self-evolve sample code...")
    evolved = improver.evolve(
        "def core_v1(): return 'v1'  # TODO: self_improve",
        goal="compact + metrics + chaos-resilient v0.5.3",
    )
    print("Evolved snippet preview:", evolved[:280] + "...")

    print("\n[3] Chaos battery (3 experiments)...")
    battery = chaos.run_battery(n=3)
    for r in battery:
        print(f"  {r['experiment']}: ok={r['ok']} gain={r['gain']} score={r['score_after']}")
    print("  ", chaos.summary_line())

    print("\n[4] Orchestrated cycle...")
    cycle_results = orch.run_orchestrated_cycle()
    print("Cycle results:", cycle_results)

    print("\n[5] Health & metrics...")
    print("DB Health:", db.get_health_snapshot())
    print("Improver:", improver.get_improvement_report())
    print("Chaos:", chaos.get_report())
    print("Orchestrator:", orch.get_status())
    print("Summary line:", orch.evolution_summary())

    print("\n=== v0.5.3 cycle complete. Resilience measured. System stronger. ===")


if __name__ == "__main__":
    main()
