# Singularity Operator v0.5.10

**Self-improving AI system** with EverythingDB (vectors), chaos, serendipity, multi-repo fleet orchestration, browser/userscript tests, and a **closed metrics feedback loop from autonomous-github-agent**.

## What's New in v0.5.10 (AGA → SO Feedback Loop)
- `GitHubSeamless.fetch_aga_profile()` reads `eric847b/autonomous-github-agent/.agent_profile.json`
- `fetch_aga_roi_signals()` pulls latest ROI/fleet status issue comments
- `ingest_aga_feedback(db=...)` stores compact metrics into EverythingDB (`aga:feedback`)
- Orchestrator task `aga_feedback` each cycle; surfaces `aga_runs`, `roi_top_ref`, `fleet_health` in `evolution_summary`

## Quick Start
```bash
git clone https://github.com/eric847b/singularity-operator.git
cd singularity-operator
pip install -e .
python singularity_operator.py
```

Requires `GITHUB_TOKEN` / `GH_FULL_PAT` for live AGA ingest and publish.

## Core Architecture
1. **EverythingDB** — Sequences + optional vectors + multi-modal tags.
2. **SelfImprover / Chaos / Serendipity** — Evolution + resilience + bridges.
3. **BrowserAutomation / UserscriptGenerator** — Live self-evo tests.
4. **GitHubSeamless** — Fleet sync, evolution report publish, **AGA feedback ingest**.
5. **Orchestrator** — PDCA including `aga_feedback` + `vector_demo` + publish.

## Roadmap (Next Highest-Return)
- Continuous upgrade cycles from live ROI ranking.
- Optional real embedding backend (feature-flagged).
- Deeper Playwright path in CI.

*Current status: v0.5.10 AGA metrics feedback loop operational.*
