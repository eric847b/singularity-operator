# Provenance Tracking

Current (implemented) provenance is lightweight and operational rather than full cryptographic audit.

## What is recorded today

| Field | Source |
|-------|--------|
| Timestamp | UTC ISO on every sequence / embedding / cache write |
| Tags | Caller-supplied (e.g. `proposed:…`, `currency:fleet_signal`, `roi:live_rank`, `self_improver`) |
| Modality | text / code / … |
| Key | Content-hash of the stored value |
| Metrics counters | llm_calls, learning_writes, serendipity_captures, etc. |

Orchestrator and SelfImprover write structured sequences that embed:

- Provider used for an evolution
- ROI pick + currency top_experiment / top_score
- AGA feedback refs
- Free-AI status snapshots

## Gaps (Phase 2 targets)

- Explicit parent / derives-from links between sequences
- Validation status and scorer identity on each unit
- Downstream consumer list
- Stronger trust tiers (experimental vs validated)

Until those land, treat tags + timestamps + stored structured payloads as the provenance trail.
