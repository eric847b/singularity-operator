# DynamicsCore — Reusable Dynamics, Hard-Fail Resume, Optimal Morph

## Idea

You do not need 50 programs that share the same software dynamics. Dynamics are **combinable primitives**. Topics and variables change; the dynamics reuse.

Each step is ternary: **inactive | active | deferred** — enough states to express missing inputs, hardware limits, and reorder without a new program per case.

## On hard fail

1. **Checkpoint** relative progress (step index, fraction, payload, config).
2. **Read** system messages / logs (optional `log_reader`).
3. **Morph** resource profile (tighten CPU/parallel, prefer cache).
4. **Retry** with a different step **order** (rotation / swap — bounded, not full n!).
5. Optional **AI fix** proposal from logs + error.
6. **Resume** from checkpoint — same relative progress, no full restart.

Successful compositions are **cached** so combining/expanding capabilities does not recompute the same mix.

## API

```python
from singularity_operator import DynamicsCore, ResourceProfile

core = DynamicsCore(resources=ResourceProfile(max_retries=3, allow_order_permute=True))
core.register("ingest", ingest_fn)
core.register("transform", transform_fn)
core.register("emit", emit_fn)

out = core.run_composition("job-1", ["ingest", "transform", "emit"], user_payload)
# on fail: auto checkpoint + log + reorder + tighten resources + retry
```

Related: `MaintenanceCrew` (seamless user channel), `IncompletePath` (partial pieces), `MERGE_POLICY.md`.
