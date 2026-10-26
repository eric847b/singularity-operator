# Dependency Inventory

## Runtime (from package layout + imports)

| Dependency | Role | Notes |
|------------|------|-------|
| Python stdlib | sqlite3, json, ast, datetime, math, re, collections, typing | Core EverythingDB + SelfImprover |
| Free AI rotator | `free_ai_client`, `groq_wrapper` / `call_ai` | Ollama → Pollinations → Groq/OpenRouter/Together free |
| Network (optional) | GitHub API via GitHubSeamless | Requires `GITHUB_TOKEN` / `GH_FULL_PAT` for live signals |

`requirements.txt` / `pyproject.toml` stay minimal; prefer zero paid APIs.

## Internal module graph (high level)

```
singularity_operator.py / cli
        │
        ▼
SingularityOrchestrator
   ├── EverythingDB
   ├── SelfImprover ──► EverythingDB, call_ai
   ├── GitHubSeamless
   ├── ChaosEngine ──► EverythingDB
   ├── SerendipityEngine ──► EverythingDB
   ├── BrowserAutomation
   ├── UserscriptGenerator
   └── free_ai_client
```

## External fleet targets (Orchestrator fleet_sync)

- `eric847b/autonomous-github-agent`
- `eric847b/AI-Collaboration-Hub`
- `eric847b/zero-cost-wealth-playbook-tool`

## CI / quality

GitHub Actions: quality-gate, version-consistency, auto-evolve, roi-status, failure-solver, release, dependency-review, dependabot.

## Gaps to close (Phase 1)

- Explicit lockfile / pinned free-tier client versions if any non-stdlib deps are introduced
- Automated generation of this inventory from imports (future)
