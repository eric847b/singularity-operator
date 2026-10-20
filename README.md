# Singularity Operator v0.5.16

**Self-improving AI system** with EverythingDB, fleet orchestration, AGA metrics feedback, and **continuous upgrade from live ROI ranking** — powered by a zero-cost free AI rotator.

## Free AI Capacity

Continuous development loops use `singularity_operator/free_ai_client.py`:

| Priority | Provider        | Key required? | Notes                          |
|----------|-----------------|---------------|--------------------------------|
| 1        | Ollama (local)  | No            | Permanent free, your hardware  |
| 2        | Pollinations    | **No**        | Zero-key cloud free tier       |
| 3        | Groq free       | Optional      | Free tier with key             |
| 4        | OpenRouter free | Optional      | `:free` models                 |
| 5        | Together free   | Optional      | Free tier                      |

Seamless failover — work never pauses on rate limits or missing keys.  
`groq_wrapper.py` routes all intelligence through this pool. SelfImprover is free-AI primary.
`FreeAIClient.get_status()` now surfaces live available providers + tally for ROI / Orchestrator.

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
git tag v0.5.16
git push origin v0.5.16
```
GitHub Actions builds the EXE + packages and publishes the release automatically.

## What's New in v0.5.16
- Continuous upgrade cycle executed (ROI #33).
- FreeAIClient exposes `get_status()` (available providers, cooldown, tally, keys present) for live ROI and Orchestrator consumption.
- New cycle task `free_ai_status` records status into EverythingDB.
- Version metadata, launcher, SelfImprover, Orchestrator fully synchronized.
- Measurable free-AI primary progress + fleet-ready metrics surface.

## What's New in v0.5.15
- Continuous upgrade cycle executed (ROI #33).
- Launcher version fully synchronized with package.
- SelfImprover now free-AI primary (no hard provider lock) + provider logging.
- Orchestrator + metadata advanced to 0.5.15 for measurable progress.

## What's New in v0.5.14
- Free AI rotator (local + Pollinations no-key + free cloud tiers) integrated into continuous loops.
- `free_ai_client.py` + upgraded `groq_wrapper` for zero-cost continuous refinement.
- Auto-evolve workflow now exercises the expanded free capacity.

## Quick Start (from source)
```bash
pip install -e .
python singularity_operator.py
```

Requires `GITHUB_TOKEN` / `GH_FULL_PAT` for live AGA ingest and fleet actions.

## Architecture
EverythingDB · SelfImprover (free-AI primary) · Chaos · Serendipity · Browser · Userscript · GitHubSeamless (fleet + AGA feedback) · Orchestrator (incl. continuous_roi_rank + free_ai_status) · **FreeAIClient**

## Roadmap
- Next live-ranked catalyst work after empty queue / new seeds.
- Optional real embedding backend (feature-flagged).
- Keep release metadata synchronized automatically before every versioned release.
- Currency / wealth fleet signals from zero-cost-wealth-playbook-tool.

*Status: v0.5.16 continuous upgrade complete. Ready for next auto-evolve cycle.*
