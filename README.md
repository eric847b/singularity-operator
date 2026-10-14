# Singularity Operator v0.5.14

**Self-improving AI system** with EverythingDB, fleet orchestration, AGA metrics feedback, and **continuous upgrade from live ROI ranking** — now powered by a zero-cost free AI rotator.

## Free AI Capacity (2026-10-14)

Continuous development loops use `singularity_operator/free_ai_client.py`:

| Priority | Provider        | Key required? | Notes                          |
|----------|-----------------|---------------|--------------------------------|
| 1        | Ollama (local)  | No            | Permanent free, your hardware  |
| 2        | Pollinations    | **No**        | Zero-key cloud free tier       |
| 3        | Groq free       | Optional      | Free tier with key             |
| 4        | OpenRouter free | Optional      | `:free` models                 |
| 5        | Together free   | Optional      | Free tier                      |

Seamless failover — work never pauses on rate limits or missing keys.  
`groq_wrapper.py` v0.6.0 routes all intelligence through this pool.

## Releases & Windows executable

Download the latest **Release** from the [Releases page](https://github.com/eric847b/singularity-operator/releases).

- **`singularity-operator.exe`** — single-file Windows launcher (no separate Python install)
- Wheel / sdist for `pip install`

Set environment variables as needed:
```bash
GROQ_API_KEY=...
OPENROUTER_API_KEY=...   # optional free lanes
GITHUB_TOKEN=...         # or GH_FULL_PAT
```

To cut a new release after packaging changes land:
```bash
git tag v0.5.14
git push origin v0.5.14
```
GitHub Actions builds the EXE + packages and publishes the release automatically.

## What's New in v0.5.14
- Free AI rotator (local + Pollinations no-key + free cloud tiers) integrated into continuous loops.
- `free_ai_client.py` + upgraded `groq_wrapper` for zero-cost continuous refinement.
- Auto-evolve workflow now exercises the expanded free capacity.

## What's New in v0.5.13
- Version level advanced and synchronized across the canonical `VERSION` and Python package metadata.
- Release documentation advanced with the current executable/package release target.
- Continuous-upgrade architecture remains focused on measurable ROI and cross-repo fleet improvement.

## Quick Start (from source)
```bash
pip install -e .
python singularity_operator.py
```

Requires `GITHUB_TOKEN` / `GH_FULL_PAT` for live AGA ingest and fleet actions.

## Architecture
EverythingDB · SelfImprover · Chaos · Serendipity · Browser · Userscript · GitHubSeamless (fleet + AGA feedback) · Orchestrator (incl. continuous_roi_rank) · **FreeAIClient**

## Roadmap
- Next live-ranked catalyst work after empty queue / new seeds.
- Optional real embedding backend (feature-flagged).
- Keep release metadata synchronized automatically before every versioned release.

*Status: v0.5.14 continuous upgrade with free AI rotator. Ready for auto-evolve cycles.*
