# Continuous Free-AI Context & Roadmap

**Last updated:** 2026-10-15  
**Purpose:** Keep free AIs (local + Pollinations no-key + free tiers) fully context-aware and connected to everything they need while they add software and fix things continuously.

## Hard Constraint (2026-10-15)
Private repos consume limited GitHub Actions minutes (Free plan ~2,000 Linux minutes/month). Public repos on standard runners are **unlimited and free**.

**Consequence:** Fleet Maintenance and other scheduled workflows on the private `autonomous-github-agent` were disabled because usage exceeded available private quota. Do not re-enable heavy private schedules until the architecture is public-first or self-hosted.

## Fleet (always in scope)
- `eric847b/AI-Collaboration-Hub` — public — FreeAIRotator + suite (prefer for continuous work)
- `eric847b/singularity-operator` — public — FreeAIClient + Auto-Evolve (prefer for continuous work)
- `eric847b/autonomous-github-agent` — **private** — control plane / Catalyst (keep light; avoid frequent schedules)
- `eric847b/collabhub-modules` — public
- `eric847b/modular-hub-modernization` — public
- `eric847b/zero-cost-wealth-playbook-tool` — public

## Free AI Pool (never pause)
1. Local first (Ollama / LM Studio / LocalAI) — permanent free
2. Pollinations no-key (`text.pollinations.ai/openai`)
3. Free tiers: Groq, OpenRouter `:free`, Together, HF, Gemini (when keys present)

## Standing Prompt Patterns

### Pure "Your choice"
```
Your choice. Highest-return root action first. Improve zero-cost continuous development, free AI capacity, and software that fixes itself. Keep full context of the fleet. Respect private Actions minute limit — prefer public repos and local runners. Produce real measurable progress.
```

## Current High-ROI Themes (updated)
1. **Public-first continuous loops** — keep Auto-Evolve, ROI, quality gates, free-AI refinement on public repos only.
2. **Minimize private quota burn** — disable or heavily throttle scheduled workflows on autonomous-github-agent until self-hosted or public companion exists.
3. Expand free AI capacity and reliability.
4. Real measurable progress only (no simulated work).

## Recommended Architecture Adjustments
- Move status / digest / heartbeat reporting that does not need private secrets into a public companion or into singularity-operator / AI-Collaboration-Hub.
- Prefer `workflow_dispatch` over frequent cron on private repos.
- Consider self-hosted runners (free of GitHub minutes) for any remaining private continuous work.
- Keep singularity-operator + AI-Collaboration-Hub as the primary never-pausing engines.

## How free AIs stay connected
- Shared free provider pool across the core repos
- This file + evolution reports give persistent context
- Failover so work never stops on rate limits or missing keys

When prompted with "your choice", prioritize the highest-return root action that compounds continuous development **without burning private Actions minutes**.
