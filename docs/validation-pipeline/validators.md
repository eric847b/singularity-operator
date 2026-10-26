# Validators

There is no separate validator package yet. Validation is embedded in the evolution and orchestration paths.

## SelfImprover validation

`SelfImprover.evolve()`:

1. Calls free-AI rotator (`call_ai`)
2. Parses candidate with `ast.parse`
3. Rejects if AST dump is identical to original (no meaningful change)
4. On any parse / exception → keep original, increment failures, log reason
5. On accept → increment improvements, write sequence to EverythingDB under tag `self_improver`

This is structural + change-detection validation, not semantic proof.

## Orchestrator validation patterns

- Currency / ROI picks are stored as sequences with explicit tags; ranking is "draft-only; no force-merge"
- Browser smoke + userscript self-evo tests write pass/fail style results into the DB
- Chaos battery records resilience experiments
- Evolution reports publish summaries via GitHubSeamless (status recorded)

## Intended Phase 2 expansion

- Schema / structural validators for knowledge units
- Consistency checks against existing sequences
- Optional free-AI review step with explicit policy gates
- Clear pass/fail artifacts consumable by CI and the Orchestrator
