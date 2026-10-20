# Singularity Operator v0.5.19

**Self-improving AI system** with EverythingDB, fleet orchestration, AGA metrics feedback, **deep currency experiment ranking**, and continuous upgrade from live ROI ranking — powered by a zero-cost free AI rotator.

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

## Currency fleet signal + experiment ranking

`GitHubSeamless.fetch_currency_signals()` pulls version + capabilities + **top_experiment / top_score** from `eric847b/zero-cost-wealth-playbook-tool` (CURRENCY_STATUS.md JSON).  
Orchestrator task `currency_signal` stores the signal; `continuous_roi_rank` **hard-biases** toward the highest expected $/effort open experiment when the signal is live.

## Releases & Windows executable

Download the latest **Release** from the [Releases page](https://github.com/eric847b/singularity-operator/releases).

- **`singularity-operator.exe`** — single-file Windows launcher
- Wheel / sdist for `pip install`

```bash
git tag v0.5.19
git push origin v0.5.19
```

## What's New in v0.5.19
- Deep currency experiment ranking (#43): `top_experiment` + `top_score` flow from CURRENCY_STATUS.md into `continuous_roi_rank`.
- Hard preference for highest expected-revenue/effort open experiment (currently setup-session-offer).
- Full version sync (VERSION / pyproject / __init__ / README / CONTINUOUS_CONTEXT / modules).

## What's New in v0.5.18
- Deepen currency signal (#43): parse full CURRENCY_STATUS.md JSON block.

## What's New in v0.5.17
- Currency fleet signal wired (#43): `fetch_currency_signals` + `currency_signal` cycle task.
- `continuous_roi_rank` records currency version/preference and prefers wealth path when signal is live.
- Fleet sync includes zero-cost-wealth-playbook-tool.

## Quick Start
```bash
pip install -e .
python singularity_operator.py
```

Requires `GITHUB_TOKEN` / `GH_FULL_PAT` for live AGA ingest, currency signals, and fleet actions.

## Architecture
EverythingDB · SelfImprover (free-AI primary) · Chaos · Serendipity · Browser · Userscript · GitHubSeamless (AGA + **currency + top experiment**) · Orchestrator (continuous_roi_rank + currency_signal) · FreeAIClient

*Status: v0.5.19 deep currency experiment ranking live. Ready for next auto-evolve cycle.*
