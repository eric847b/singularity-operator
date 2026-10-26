# Validators

## Shared module: `singularity_operator/validation.py`

| Helper | Role |
|--------|------|
| `validate_python_evolution(original, candidate)` | Accept/reject evolved Python (non-empty, parses, optional AST change) |
| `ast_equivalent(a, b)` | Whitespace-insensitive AST equality |
| `is_valid_python(source)` | Syntax check |
| `validate_sequence_payload(value)` | Lightweight type gate for knowledge units |
| `ValidationResult` | Structured ok/reason/detail |

## SelfImprover

Uses `validate_python_evolution` exclusively for accept/reject. On failure keeps original and logs reason (`empty`, `no_change`, `syntax_error`). On success writes sequence with validation payload.

## Orchestrator

Does not force semantic validation on free-AI text; relies on draft-only ROI notes and structured storage with provenance links.

## Quality gate

`.github/workflows/quality-gate.yml` asserts:

- SelfImprover imports and calls shared validation
- validation.py defines core helpers
- EverythingDB exposes parent_key / derives_from / get_sequence / get_children
- Orchestrator links ROI rank to currency parent key

## Next

- Optional free-AI review step with policy gates
- CI-consumable pass/fail artifacts for agent proposals
