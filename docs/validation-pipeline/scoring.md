# Scoring

## Live ranking (implemented)

Orchestrator task `continuous_roi_rank`:

- Combines last AGA feedback (`roi_top_ref`, `roi_top_score`, fleet health) with currency signal
- When `preferred_currency_path` is true, **hard-biases** toward `top_experiment` / `top_score` from CURRENCY_STATUS
- Stores the pick as a sequence tagged `roi:live_rank`
- Note field enforces draft-only, no force-merge, real-work preference

EverythingDB vector search returns cosine scores (0–1 range after L2 normalize) for retrieval ranking.

SelfImprover does not assign numeric quality scores; it uses binary accept/reject after AST comparison and tracks improvement count / failures.

## Metrics used as soft scores

- Orchestrator: cycles, improvements, serendipity captures, chaos runs, roi_ranks, currency_signals
- EverythingDB: llm_calls, cache_hits, sequences_added, embeddings_stored, vector_hits
- GitHubSeamless / free AI status tallies

These feed `evolution_summary()` and published evolution reports.

## Phase 2 / 3 direction

Unify evolution scoring, validation confidence, and ROI into a single consumable dashboard signal for agent proposals.
