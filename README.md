# Singularity Operator v0.5.17

**Self-improving AI system** with EverythingDB, fleet orchestration, AGA metrics feedback, **currency fleet signal**, and continuous upgrade from live ROI ranking — powered by a zero-cost free AI rotator.

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
`FreeAIClient.get_status()` surfaces live available providers + tally for ROI / Orchestrator.

## Currency fleet signal

`GitHubSeamless.fetch_currency_signals()` pulls version + capabilities from `eric847b/zero-cost-wealth-playbook-tool` (tracker, runway, experiment rank/suggest, quote).  
Orchestrator task `currency_signal` stores the signal; `continuous_roi_rank` prefers the currency path when present.

## Releases & Windows executable

Download the latest **Release** from the [Releases page](https://github.com/eric847b/singularity-operator/releases).

- **`singularity-operator.exe`** — single-file Windows launcher
- Wheel / sdist for `pip install`

```bash
git tag v0.5.17
git push origin v0.5.17
```

## What's New in v0.5.17
- Currency fleet signal wired (#43): `fetch_currency_signals` + `currency_signal` cycle task.
- `continuous_roi_rank` records currency version/preference and prefers wealth path when signal is live.
- Fleet sync includes zero-cost-wealth-playbook-tool.

## What's New in v0.5.16
- FreeAIClient exposes `get_status()`; free_ai_status cycle task.
- Version metadata fully synchronized; continuous upgrade (#33).

## Quick Start
```bash
pip install -e .
python singularity_operator.py
```

Requires `GITHUB_TOKEN` / `GH_FULL_PAT` for live AGA ingest, currency signals, and fleet actions.

## Architecture
EverythingDB · SelfImprover (free-AI primary) · Chaos · Serendipity · Browser · Userscript · GitHubSeamless (AGA + **currency**) · Orchestrator (continuous_roi_rank + currency_signal) · FreeAIClient

*Status: v0.5.17 currency fleet signal live. Ready for next auto-evolve cycle.*
