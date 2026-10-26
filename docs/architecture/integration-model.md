# Integration Model

## Ecosystem Positioning

Repositories in the ecosystem increasingly center on orchestration between projects rather than isolated features. Recommended posture:

- Treat **AI-Collaboration-Hub** (when present) as the canonical platform entry point.
- Position singularity-operator, nexus-related hubs, and third-door-style systems as specialized subsystems.

## Current Integration Points

- **Currency / wealth signals**: `GitHubSeamless.fetch_currency_signals()` → Orchestrator `currency_signal` / `continuous_roi_rank`
- **Fleet sync**: includes zero-cost-wealth-playbook-tool and related repos
- **GitHub Actions**: auto-evolve, quality-gate, roi-status, failure-solver, release integrity

## Target Shared Interfaces (Phase 4)

- Unified event bus
- Shared memory interfaces
- Cross-project observability / telemetry
