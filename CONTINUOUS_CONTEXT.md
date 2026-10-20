# Continuous Free-AI Context & Roadmap

**Last updated:** 2026-10-20  
**Purpose:** Keep free AIs (local + Pollinations no-key + free tiers) fully context-aware and connected to everything they need while they add software and fix things continuously.

## Hard Constraint (2026-10-15)
Private repos consume limited GitHub Actions minutes (Free plan ~2,000 Linux minutes/month). Public repos on standard runners are **unlimited and free**.

**Consequence:** Fleet Maintenance and other scheduled workflows on the private `autonomous-github-agent` were disabled because usage exceeded available private quota. Do not re-enable heavy private schedules until the architecture is public-first or self-hosted.

## Fleet (always in scope)
- `eric847b/AI-Collaboration-Hub` — public — FreeAIRotator + suite (prefer for continuous work)
- `eric847b/singularity-operator` — public — FreeAIClient + Auto-Evolve — **v0.5.19**
- `eric847b/autonomous-github-agent` — **private** — control plane / Catalyst (keep light; avoid frequent schedules)
- `eric847b/collabhub-modules` — public
- `eric847b/modular-hub-modernization` — public
- `eric847b/zero-cost-wealth-playbook-tool` — public — **v1.0.2** (currency path: tracker, runway, experiment rank/suggest, quote; top experiment: setup-session-offer)

## Free AI Pool (never pause)
1. Local first (Ollama / LM Studio / LocalAI) — permanent free
2. Pollinations no-key (`text.pollinations.ai/openai`)
3. Free tiers: Groq, OpenRouter `:free`, Together, HF, Gemini (when keys present)

## Standing Prompt Patterns

### Pure "Your choice" / "Continue"
```
Your choice. Highest-return root action first. Improve zero-cost continuous development, free AI capacity, currency/wealth path, and software that fixes itself. Keep full context of the fleet. Respect private Actions minute limit — prefer public repos and local runners. Produce real measurable progress.
```

## Current High-ROI Themes (updated 2026-10-20)
1. **Public-first continuous loops** — keep Auto-Evolve, ROI, quality gates, free-AI refinement on public repos only.
2. **Currency path first-class + experiment ranking** — zero-cost-wealth-playbook-tool signals (including top_experiment/top_score) are ingested via `fetch_currency_signals` and hard-biased inside `continuous_roi_rank` (v0.5.19).
3. **Minimize private quota burn** — disable or heavily throttle scheduled workflows on autonomous-github-agent until self-hosted or public companion exists.
4. Expand free AI capacity and reliability (FreeAIClient.get_status already live).
5. Real measurable progress only (no simulated work).

## Recent measurable progress
- singularity-operator **v0.5.19**: Deep currency experiment ranking (#43) — top_experiment + top_score flow into continuous_roi_rank; hard bias to highest expected $/effort open experiment.
- singularity-operator **v0.5.18**: Deepen currency signal (#43) — full CURRENCY_STATUS.md JSON parse.
- singularity-operator **v0.5.17**: Currency fleet signal wired (#43) — GitHubSeamless.fetch_currency_signals + currency_signal task + continuous_roi_rank preference.
- singularity-operator **v0.5.16**: FreeAIClient.get_status() + free_ai_status cycle task; tag + release published.
- zero-cost-wealth-playbook-tool v1.0.2: CURRENCY_STATUS.md live with ranked experiments.

## Recommended Architecture Adjustments
- Move status / digest / heartbeat reporting that does not need private secrets into a public companion or into singularity-operator / AI-Collaboration-Hub.
- Prefer `workflow_dispatch` over frequent cron on private repos.
- Keep singularity-operator + AI-Collaboration-Hub as the primary never-pausing engines.
- Next: act on top currency experiment (setup-session-offer) or expand free-AI self-improvement loops.

## How free AIs stay connected
- Shared free provider pool across the core repos
- This file + evolution reports give persistent context
- Failover so work never stops on rate limits or missing keys

When prompted with "your choice" or "continue", prioritize the highest-return root action that compounds continuous development **and currency path** without burning private Actions minutes.
