# Memory Storage

Primary implementation: `singularity_operator/everything_db.py` (`EverythingDB`).

## Backend

- **SQLite** file (default `everything.db`)
- Tables:
  - `sequences` — key (hash), value (JSON text), timestamp, tags, modality
  - `embeddings` — key, dim, vector (JSON), modality, timestamp
  - `groq_cache` — prompt → response cache (L2)
  - `metrics` — persisted snapshot key `snapshot`

## In-memory layer

- LRU-style `OrderedDict` mem_cache (default size 64) for prompt responses (L1)
- Metrics counters kept in process and periodically persisted

## Modalities

Supported / intended: `text` | `code` | `image_ref` | `audio_ref` | `multi` (default `text`).

## Write path

`add_sequence(seq, tags="general", modality="text")`:

1. Deterministic key from content hash
2. INSERT OR REPLACE into `sequences`
3. Optional bag-of-words embedding store when `enable_vectors=True`
4. Metrics: `sequences_added`, `embeddings_stored`

## Health & persistence

- `get_health_snapshot()` — sequence/embedding counts, top tags, metrics, version
- `persist_metrics()` — writes metrics snapshot to SQLite
- `compute_metrics()` — live + stored counts

Storage is intentionally zero-external-dep (stdlib + sqlite3) so the knowledge layer runs in free/constrained environments.
