# Singularity Operator v0.5.48

**Self-improving AI system** with EverythingDB, fleet orchestration, AGA metrics feedback, **deep currency experiment ranking**, AGA usage/credits visibility, and continuous upgrade from live ROI ranking — powered by a zero-cost free AI rotator.

## Overview

Singularity Operator is an experimental autonomous knowledge, validation, and orchestration platform.

The project focuses on:

- Memory systems
- Agent collaboration
- Knowledge validation
- Architecture evolution
- Cross-system orchestration

The goal is practical autonomous system development through iterative evolution rather than speculative end-state intelligence claims.

See [ROADMAP.md](ROADMAP.md) and [docs/](docs/) for the phased plan, architecture, and documentation policy.

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

`GitHubSeamless.fetch_currency_signals()` pulls version + capabilities + **top_experiment / top_score / next_concrete_step** from `eric847b/zero-cost-wealth-playbook-tool` (CURRENCY_STATUS.md JSON).  
Orchestrator task `currency_signal` stores the signal; `continuous_roi_rank` **hard-biases** toward the highest expected $/effort open experiment when the signal is live.

v0.5.48 adds `priority_harmonic_mean` for robust multiplicative ranking insight on priority scores.

v0.5.47 adds `priority_geometric_mean` for multiplicative insight into priority score distribution.

v0.5.46 prefers the live `next_concrete_step` from the currency signal when present (playbook fallback otherwise).

v0.5.45 adds `priority_mad` (median absolute deviation) as a robust dispersion metric on priority scores.

v0.5.44 adds `days_since_signal`, confidence decay on stale signals, and `next_concrete_step` so fleet agents can act without parsing the full step list.

## Releases & Windows executable

Download the latest **Release** from the [Releases page](https://github.com/eric847b/singularity-operator/releases).

- **`singularity-operator.exe`** — single-file Windows launcher
- Wheel / sdist for `pip install`
- **`SHA256SUMS`** — verify downloaded release assets before use

The release workflow checks that `VERSION`, `pyproject.toml`, `singularity_operator/__init__.py`, the README heading, and the pushed tag all agree. Required builds fail closed; optional executable builds are not silently ignored.

After the v0.5.48 changes are merged, publish the matching tag:

```bash
git pull --ff-only origin main
git tag v0.5.48
git push origin v0.5.48
```

## What's New in v0.5.48
- Currency action adds `priority_harmonic_mean` for robust multiplicative ranking insight on priority scores (#43). Version parity restored.

## What's New in v0.5.47
- Currency action adds `priority_geometric_mean` for multiplicative ranking insight on priority scores (#43). Version parity restored.

## What's New in v0.5.46
- Prefer live currency signal `next_concrete_step` over playbook default for sharper fleet actionability (#43). Version parity restored.

## What's New in v0.5.45
- Currency action adds `priority_mad` (median absolute deviation) for robust dispersion of priority scores (#43). Version parity restored.

## What's New in v0.5.44
- Currency action adds `days_since_signal`, stale-signal confidence decay, and `next_concrete_step` for sharper actionable fleet selection (#43). Version parity restored.

## What's New in v0.5.43
- Currency action adds priority_top_rest_ratio for sharper fleet selection metrics (#43). Version parity restored.

## What's New in v0.5.42
- Currency action adds priority_effective_n for sharper fleet selection metrics (#43). Version parity restored.

## What's New in v0.5.41
- Currency action adds priority_top_share for sharper fleet selection metrics (#43). Version parity restored.

## What's New in v0.5.40
- Currency action adds priority_hhi for sharper fleet selection metrics (#43). Version parity restored.

## What's New in v0.5.39
- Currency action adds priority_gini for sharper fleet selection metrics (#43). Version parity restored.

## What's New in v0.5.38
- Currency action adds priority_entropy for sharper fleet selection metrics (#43). Version parity restored.

## What's New in v0.5.37
- Currency action adds priority_kurtosis for sharper fleet selection metrics (#43). Version parity restored.

## What's New in v0.5.36
- Currency action adds priority_skewness for sharper fleet selection metrics (#43).

## What's New in v0.5.35
- Currency action adds priority_range + priority_cv for sharper fleet selection metrics (#43).

## What's New in v0.5.34
- Currency action adds priority_median + priority_iqr for sharper fleet selection metrics (#43).

## What's New in v0.5.33
- Currency action adds priority_std_dev for sharper fleet selection metrics (#43).

## What's New in v0.5.32
- Currency action adds priority_variance + selection_margin for sharper fleet selection metrics (#43).

## What's New in v0.5.31
- Currency action adds max_priority_score + top_avg_delta for sharper fleet selection metrics (#43).

## What's New in v0.5.30
- Currency action adds experiment_count + avg_priority_score for sharper fleet metrics (#43).

## What's New in v0.5.29
- Currency priority_score now multiplies by confidence for sharper live ranking (#43).

## What's New in v0.5.28
- Currency action adds `selection_reason` + `top_priority_score` for sharper autonomous pick (#43).

## What's New in v0.5.27
- Currency ranked experiments add rank position + priority_score (roi_pe weighted by rank) for sharper autonomous selection (#43).

## What's New in v0.5.26
- FreeAIClient Together free-tier provider + provider_count status (#43).

## What's New in v0.5.25
- Currency ranked experiments by ROI-per-effort + confidence scoring for #43 continuous upgrade.

## What's New in v0.5.24
- Currency next-action adds computed `roi_per_effort` metric for ranking precision on #43.

## What's New in v0.5.23
- Currency next-action signal freshness + live confirmation provenance for #43.

## What's New in v0.5.22
- AGA usage/credits visibility + currency parity in orchestrator telemetry and evolution summaries.
- Full version surface parity (VERSION / pyproject / __init__ / README / orchestrator).

## What's New in v0.5.20
- Hardened release integrity checks across package metadata, runtime version, README, and Git tag.
- Release builds fail closed instead of silently ignoring a failed secondary executable build.
- Published SHA-256 checksums for release artifacts and narrowed workflow write permissions to the release job.

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

*Status: v0.5.48 version parity complete; publish tag after CI passes.*
