# Knowledge Indexing

Implementation lives in `EverythingDB` (same module as storage).

## Vector index (default on)

- Feature flag: `enable_vectors` (default `True`)
- Dimension: fixed `vector_dim=64`
- Embedding: pure-stdlib **hashing bag-of-words** with signed-hash trick + L2 normalize
- No external embedding models required

## Query

`similarity_search(query, top_k=5, modality=None, min_score=0.05)`:

1. Embed query with same BoW function
2. Scan embeddings table (optional modality filter)
3. Cosine similarity; return scored hits with value/tags/timestamp

Metrics: `vector_queries`, `vector_hits`.

## Demo / seed

`demo_vector_query()` ensures minimal seed sequences (self_improve, serendipity, code, currency_path) then runs a measurable search and stores the report sequence.

## Design notes

- Index is approximate and collision-tolerant by design (hashing BoW).
- Suitable for compact local operation and free-tier loops.
- Future upgrade path: optional higher-quality embeddings behind the same interface without breaking callers.
