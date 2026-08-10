"""Singularity Operator v0.5.8 Launcher — propose, evolve, serendipity, chaos, browser/userscript.
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
    print("=== Singularity Operator v0.5.8 ===")
    print(f"Time: {datetime.now().isoformat()}")
    print(f"Groq key present: {bool(os.getenv('GROQ_API_KEY'))}")

    db = EverythingDB(":memory:", mem_cache_size=8)
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
        goal="compact + metrics + browser/userscript self-evo v0.5.8",
    )
    print("Evolved preview:", evolved[:280] + "...")

    print("\n[3] Serendipity cycle...")
    ser = serendipity.run_cycle(connections=3, amplifications=2)
    print("  ", serendipity.summary_line())

    print("\n[4] Chaos battery...")
    battery = chaos.run_battery(n=3)
    print("  ", chaos.summary_line())

    print("\n[5] Browser smoke + userscript self-evo test...")
    smoke = browser.run_smoke_suite()
    print(f"  smoke pass_rate={smoke.get('pass_rate')} ok={smoke.get('ok')}/{smoke.get('total')}")
    us = usgen.run_self_evo_test()
    print(f"  userscript ok={us.get('validation', {}).get('ok')} bytes={us.get('validation', {}).get('bytes')}")
    db.add_sequence({"smoke": smoke, "userscript": us}, "self_evo:browser_userscript")

    print("\n[6] Orchestrated cycle...")
    cycle_results = orch.run_orchestrated_cycle()
    print("Cycle tasks:", [r.get("task") for r in cycle_results])
    print("Summary:", orch.evolution_summary())

    print("\n=== v0.5.8 complete. Browser/userscript self-evo active. ===")


if __name__ == "__main__":
    main()
