# Trust Model

## Current posture

- Prefer **verifiable local state** (SQLite sequences, metrics, AST-checked evolutions) over opaque remote claims.
- Free-AI outputs are treated as proposals: accepted only after structural checks; originals retained on failure.
- Currency and ROI signals are ingested and ranked but explicitly **draft-only** — never force-merge and never mark "won" without real payment evidence.
- Fleet / AGA feedback is recorded with source refs for later audit.

## Principles going forward

1. Provenance-backed claims over anonymous ones
2. Explicit confidence / scoring where ranking occurs
3. Separation of experimental sequences vs validated knowledge
4. Human or policy gates for high-impact actions (repo writes that affect others, financial claims)

Trust is earned through measurable cycles (improvements accepted, chaos recoveries, green CI) rather than asserted intelligence claims.
