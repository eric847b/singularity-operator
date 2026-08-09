"""Singularity Operator v0.5.4 Launcher — full demo: propose, evolve, serendipity, chaos.
"""

import os
from datetime import datetime

from singularity_operator import (
    EverythingDB,
    SelfImprover,
    ChaosEngine,
    SerendipityEngine,
    SingularityOrchestrator,
)


def main():
    print("=== Singularity Operator v0.5.4 ===")
    print(f"Time: {datetime.now().isoformat()}")
    print(f"Groq key present: {bool(os.getenv('GROQ_API_KEY'))}")

    db = EverythingDB(":memory:", mem_cache_size=8)
    improver = SelfImprover(db=db)
    chaos = ChaosEngine(db=db)
    serendipity = SerendipityEngine(db=db)
    orch = SingularityOrchestrator(db=db)

    print("\n[1] Propose unknown sequences...")
    unknowns = db.propose_unknown("core self-improvement + singularity", 4)
    print("Proposed:", unknowns[:3])

    print("\n[2] Self-evolve sample code...")
    evolved = improver.evolve(
        "def core_v1(): return 'v1'  # TODO: self_improve",
        goal="compact + metrics + chaos-resilient + serendipity v0.5.4",
    )
    print("Evolved preview:", evolved[:280] + "...")

    print("\n[3] Serendipity cycle...")
    ser = serendipity.run_cycle(connections=3, amplifications=2)
    print("  ", serendipity.summary_line())
    for a in ser.get("amplified", [])[:2]:
        print("  insight:", a.get("insight", "")[:100])

    print("\n[4] Chaos battery...")
    battery = chaos.run_battery(n=3)
    for r in battery:
        print(f"  {r['experiment']}: ok={r['ok']} gain={r['gain']} score={r['score_after']}")
    print("  ", chaos.summary_line())

    print("\n[5] Orchestrated cycle...")
    cycle_results = orch.run_orchestrated_cycle()
    print("Cycle tasks:", [r.get("task") for r in cycle_results])
    print("Summary:", orch.evolution_summary())

    print("\n=== v0.5.4 complete. Serendipity + chaos + learning active. ===")


if __name__ == "__main__":
    main()
