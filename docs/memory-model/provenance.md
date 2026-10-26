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
- `walk_ancestors(key, max_depth=16) -> list` — self → … → root
- `export_lineage(key, max_depth=16, include_children=True) -> dict` — multi-hop export
- Health snapshot includes `with_parent` count

### Orchestrator usage

- `currency_signal` stores the fleet signal and remembers `last_currency_key`
- `continuous_roi_rank` writes the ROI pick with `parent_key=last_currency_key`
- `agent_propose` runs AgentProposalWorkflow; accepted proposals parent to batch (and optionally currency)
- Cycle metrics and many task outputs set `derives_from` to the task name

### Agent proposals

`AgentProposalWorkflow.run` creates a batch parent, validates each candidate, stores accepted children with `parent_key=batch_parent`, and records a run report child.

## Still open

- Graph visualization / export formats beyond JSON dict
- Explicit `validation_status` column
- Downstream consumer registry
