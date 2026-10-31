# MaintenanceCrew — Seamless Soft-Fail Heal

**Goal:** If something breaks or required personal/custom input is not yet available, the **user channel keeps going**. Repair happens without a visible failure and without restart.

## Behavior

| Situation | User sees | System does |
|-----------|-----------|-------------|
| Exception in a channel | Continuation (safe path) | Soft-fail, remember inputs, optional free-AI propose-fix |
| Missing multi-file / multi-sensor piece | Continuation | IncompletePath pause + remember; resume on live update |
| Personal / unknown input not ready | Continuation | `defer_input` — store and apply later |
| Piece arrives later | Same session continues | `heal_tick` / `resume_if_ready` — no restart |

Optional: set `expose_pause_reason=True` if the user should see a short reason for a soft pause.

## API (singularity_operator)

```python
from singularity_operator import MaintenanceCrew, IncompletePathRegistry

crew = MaintenanceCrew(expose_pause_reason=False)
crew.register_path("pipeline", ["ingest", "model", "writer"])
crew.note_piece("pipeline", "ingest")

# User channel — never raises
out = crew.run_channel(
    "pipeline",
    run_full_pipeline,
    user_payload,
    safe_continuation={"status": "ok", "partial": True},
    path_name="pipeline",
)

# Unknown personal field — keep going
crew.defer_input("tax_id", None, reason="awaiting_user")

# Later tick (live update, no restart)
crew.note_piece("pipeline", "model")
crew.note_piece("pipeline", "writer")
report = crew.heal_tick(runners={"pipeline": run_full_pipeline})
```

Wire `ai_fixer` to FreeAIClient / SelfImprover for background code repair proposals.

Related: `MERGE_POLICY.md`, `incomplete_path.py`, orchestrator task `maintenance_heal`.
