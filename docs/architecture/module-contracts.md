# Module Contracts

Minimal contracts derived from current code. Callers should treat these surfaces as stable unless version is bumped.

## EverythingDB

- `__init__(db_path="everything.db", mem_cache_size=64, enable_vectors=True, vector_dim=64)`
- `add_sequence(seq, tags="general", modality="text") -> key: str`
- `similarity_search(query, top_k=5, modality=None, min_score=0.05) -> List[dict]`
- `propose_unknown(domain=..., n=5) -> List[Any]`
- `get_health_snapshot() -> dict`
- `persist_metrics() -> dict`
- `self_test() -> dict`

Side effects: SQLite writes, optional embedding writes, metrics mutation.

## SelfImprover

- `__init__(db_path=".", db=None)`
- `evolve(code_snippet: str, goal: str = ...) -> str`  # improved or original
- `get_improvement_report() -> dict`
- `learning_summary_line() -> str`

Contract: never returns invalid Python that fails `ast.parse` relative to acceptance path; on failure returns original.

## SingularityOrchestrator

- `__init__(db=None)` — owns EverythingDB, SelfImprover, GitHubSeamless, Chaos, Serendipity, Browser, Userscript
- `run_orchestrated_cycle(tasks: List[str] | None = None) -> List[dict]`
- `evolution_summary() -> str`
- `get_status() -> dict`

Default task list includes self_improve, propose_unknown, serendipity, chaos, browser/userscript, vector_demo, aga_feedback, currency_signal, continuous_roi_rank, free_ai_status, fleet_sync, publish_evolution_report.

## FreeAI / call_ai

Accessed via `free_ai_client.get_free_ai()` and `groq_wrapper.call_ai`. Primary path is free/local rotation; callers must tolerate empty or partial responses.

## GitHubSeamless (high-level)

- Currency signal fetch, AGA ingest, fleet sync, evolution report publish
- Used by Orchestrator; not a pure library — network and token dependent
