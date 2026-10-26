# Provenance Tracking

## Implemented (v0.5.20+)

EverythingDB sequences support optional lineage fields:

| Field | Meaning |
|-------|--------|
| `parent_key` | Direct parent sequence key |
| `derives_from` | Free-form source ref (task name, module path, external id) |
| `timestamp` | UTC ISO on write |
| `tags` | Caller-supplied classification |
| `modality` | text / code / … |
| `key` | Content-hash of stored value |

### APIs

- `add_sequence(..., parent_key=None, derives_from=None)`
- `get_sequence(key) -> dict | None`
- `get_children(parent_key, limit=20) -> list`
- Health snapshot includes `with_parent` count

### Orchestrator usage

- `currency_signal` stores the fleet signal and remembers `last_currency_key`
- `continuous_roi_rank` writes the ROI pick with `parent_key=last_currency_key` and `derives_from="continuous_roi_rank"`
- Cycle metrics and many task outputs set `derives_from` to the task name

### SelfImprover

Evolution records are tagged `self_improver` with `derives_from="self_improver.evolve"` and embed the shared `ValidationResult`.

## Still open (later Phase 2)

- Multi-hop graph export / visualization
- Explicit validation_status column on every unit
- Downstream consumer registry
- Stronger trust tiers (experimental vs validated)
