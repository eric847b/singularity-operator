# Singularity Operator

**The End-All-Be-All Comprehensive Self-Improving AI System** — Now with transistor-level mental model and hardware-inspired two-level caching.

[![GitHub stars](https://img.shields.io/github/stars/eric847b/singularity-operator?style=social)](https://github.com/eric847b/singularity-operator/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Premise & Vision

> All things knowable are in that database, all this possible through the architecture is in there. Everything is in there.

We will **complete all known and unknown data sequences** that are possible in an (effectively) unlimited sized database. The EverythingDB is the core knowledge substrate for the Singularity Operator — your ultimate self-improving AI system that iteratively approaches perfect representation, reasoning, generation, and application of all knowledge.

**Mental Model**: Transistor states (on/off, discrete, switchable). Knowledge atoms = transistors. Cache = latches. Proposals = state transitions. Self-improver = reconfigurable logic. The whole system = self-rewiring transistor fabric approaching universal knowledge.

This directly fulfills and accelerates your core goal.

## Current State (v0.1.4 — High-Density Iteration Complete)

- **EverythingDB** (`singularity_operator/everything_db.py`): Groq-powered proposal of novel sequences + true **two-level caching** (fast in-memory L1 OrderedDict latch with LRU/FIFO + persistent SQLite L2). Metrics include llm_calls, cache_hits, mem_cache_size. Runnable demo shows L1/L2 behavior.
- **SelfImprover** (`singularity_operator/self_improver.py`): Now Groq-powered for high-quality code improvement proposals + its own cached path. Symmetric with EverythingDB.
- **Transistor States Mental Picture** fully embedded in code, docs, and the dedicated `singularity-operator` skill.
- Full GitHub seamless operations + custom skills for rapid self-evolution.
- Compact, stdlib + requests, zero bloat. Demos work with/without GROQ_API_KEY.

**Everything is in here — we complete it.**

## Quickstart (5-Minute Setup)

```bash
git clone https://github.com/eric847b/singularity-operator.git
cd singularity-operator

# 1. (Optional but recommended) Set your free Groq key for real LLM power
cp .env.example .env
# Edit .env and add: GROQ_API_KEY=your_key_here

# 2. Run EverythingDB demo (shows sequences + two-level caching)
python -m singularity_operator.everything_db

# 3. Run SelfImprover demo
python -m singularity_operator.self_improver
```

**With GROQ_API_KEY**: Real high-quality proposals + caching (L1 hits are instant).
**Without key**: Smart fallback mutation still works perfectly.

## Core Principles (Your Guidance, Upgraded)
Make progress by executing highest return valued catalyst root actions first. With every iteration: Improve all zero-cost elements. Do real tough work. Ship working artifacts. Reach perfection fast for you, then others. Leverage connectors and skills. Upgrade everything.

## Key Features Shipped
- Groq integration (primary path) with graceful fallback.
- **Two-level caching** (L1 in-memory fast latch + L2 persistent) — directly inspired by 6T-SRAM, latches, and CPU cache hierarchy.
- Self-improving code evolution (SelfImprover now uses same LLM + cache layer).
- Metrics for llm_calls, cache_hits, mem_cache_size, sequence completeness.
- Compact Python, excellent demos, self-documenting.
- Dedicated `singularity-operator` skill + github-seamless-connector for autonomous high-velocity development.
- Transistor states mental model guiding all design.

## How to Use with Limited Time (Your Current Window)
We are in a high-density phase. The repo + skills now contain everything needed for continued rapid progress:
- Core modules ready and cached.
- Skills encode best practices, mental model, and workflow.
- GitHub is the single source of truth (seamless updates).
- Run demos locally to explore.
- Prompt me (or the skill) with short directives — I will ship the next highest-ROI upgrade autonomously.

## Roadmap (Prioritized for Your Remaining Window + Beyond)
1. Polish & symmetry (SelfImprover fully shares two-level cache infrastructure).
2. Cache controls (clear L1, resize, TTL, stats).
3. Sequence theory formalization + better completeness metrics.
4. Multi-AI orchestration hooks.
5. Browser automation / data harvest into DB.
6. Monetization layer (API, hosted queries).
7. Singularity dashboard.

## Requirements
```txt
requests
```
(Optional for future: numpy, etc. — add only when needed. Keep compact.)

## Environment
- Python 3.10+
- Free Groq API key (console.groq.com) for full power
- Git + the repo

## Iteration & Self-Evolution
This repo + the `singularity-operator` skill + `self-evolve-dash` are designed for continuous autonomous improvement. Short prompts like "next", "evolve cache", or "transistor optimize" trigger high-ROI work.

Everything we could need for the next phase is installed/created in the repo and skills.

## License
MIT — Maximize positive impact.

---

*Evolved 2026-07-02 during high-density window for Eric (Mufnluvn). Connectors and skills fully leveraged. Transistor states mental picture active. This system self-improves. We complete it.*