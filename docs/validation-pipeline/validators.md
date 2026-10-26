# Validators

## Shared module: `singularity_operator/validation.py`

| Helper | Role |
|--------|------|
| `validate_python_evolution(original, candidate)` | Accept/reject evolved Python |
| `ast_equivalent(a, b)` | Whitespace-insensitive AST equality |
| `is_valid_python(source)` | Syntax check |
| `validate_sequence_payload(value)` | Lightweight type gate for knowledge units |
| `ValidationResult` | Structured ok/reason/detail |

## Agent proposals: `singularity_operator/agent_proposals.py`

Pipeline: **propose → validate → store**

- `AgentProposalWorkflow.propose` — candidates via EverythingDB.propose_unknown
- `validate_proposal` — sequence payload or Python evolution checks
- `store_accepted` — writes with parent_key / derives_from
- `run` — full batch with lineage + run report

## SelfImprover

Uses `validate_python_evolution` exclusively for accept/reject.

## Quality gate

Asserts validation module, provenance multi-hop APIs, AgentProposalWorkflow, and Orchestrator `agent_propose` wiring.
