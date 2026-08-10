"""Singularity Operator v0.5.9 Launcher — propose, evolve, vectors, serendipity, chaos, browser.
"""

import os
from datetime import datetime

from singularity_operator import (
    EverythingDB,
    SelfImprover,
    ChaosEngine,
    SerendipityEngine,
    SingularityOrchestrator,
    BrowserAutomation,
    UserscriptGenerator,
)


def main():
    print("=== Singularity Operator v0.5.9 ===")
    print(f"Time: {datetime.now().isoformat()}")
    print(f"Groq key present: {bool(os.getenv('GROQ_API_KEY'))}")

    db = EverythingDB(":memory:", mem_cache_size=8, enable_vectors=True)
    improver = SelfImprover(db=db)
    chaos = ChaosEngine(db=db)
    serendipity = SerendipityEngine(db=db)
    browser = BrowserAutomation()
    usgen = UserscriptGenerator()
    orch = SingularityOrchestrator(db=db)

    print("\n[1] Propose unknown sequences...")
    unknowns = db.propose_unknown("core self-improvement + singularity", 4)
    print("Proposed:", unknowns[:3])

    print("\n[2] Self-evolve sample code...")
    evolved = improver.evolve(
        "def core_v1(): return 'v1'  # TODO: self_improve",
        goal="compact + metrics + vectors v0.5.9",
    )
    print("Evolved preview:", evolved[:280] + "...")

    print("\n[3] Vector similarity demo...")
    demo = db.demo_vector_query("self improve serendipity singularity")
    print(f"  hits={demo.get('hits')} top_scores={[h.get('score') for h in demo.get('top', [])]}")
    print(f"  emb_stored={db.metrics.get('embeddings_stored')} vq={db.metrics.get('vector_queries')}")

    print("\n[4] Serendipity cycle...")
    serendipity.run_cycle(connections=3, amplifications=2)
    print("  ", serendipity.summary_line())

    print("\n[5] Chaos battery...")
    chaos.run_battery(n=3)
    print("  ", chaos.summary_line())

    print("\n[6] Browser smoke + userscript...")
    smoke = browser.run_smoke_suite()
    print(f"  smoke pass_rate={smoke.get('pass_rate')}")
    us = usgen.run_self_evo_test()
    print(f"  userscript ok={us.get('validation', {}).get('ok')}")

    print("\n[7] Orchestrated cycle...")
    cycle_results = orch.run_orchestrated_cycle()
    print("Cycle tasks:", [r.get("task") for r in cycle_results])
    print("Summary:", orch.evolution_summary())

    print("\n=== v0.5.9 complete. Vector similarity operational. ===")


if __name__ == "__main__":
    main()
