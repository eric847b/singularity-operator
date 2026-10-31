# Autonomous mode (default)

**Operator constraint:** The owner has limited capacity and zero requirement to perform manual steps. All primary loops must run without human intervention.

## Cost policy

| Rule | Enforcement |
|------|-------------|
| **Free-only by default** | `FREE_ONLY=1` (default). FreeAIClient uses local + no-key + free-tier model IDs only |
| **No paid APIs unless self-funded** | `FREE_AI_ALLOW_PAID=1` required to relax; with zero income leave unset |
| **Never simulate income** | Ledger / experiment `won` only after real payment evidence |
| **GitHub Actions** | Use included minutes; no paid Actions runners required |

## Merge policy (trunk always shippable)

See **MERGE_POLICY.md**. Summary:

- Every PR must be mergeable to `main` without breaking the live path.
- Incomplete multi-file work is allowed only if incomplete pieces are **inert** (flag, stub, optional import).
- If runtime hits a dead end (only one of N required pieces present), use `incomplete_path.IncompletePath`: remember inputs, safe-default, pause for live update, resume when the missing piece lands.
- No force-merge / force-push. Prefer short-lived branches and early merge over long feature highways.

## What is autonomous

| Capability | Mechanism |
|------------|-----------|
| Code/docs evolution | SelfImprover + free AI rotator + quality-gate |
| Knowledge + provenance | EverythingDB sequences, parent links, export_lineage |
| Agent proposals | AgentProposalWorkflow validate→store |
| Currency ranking | fetch_currency_signals → continuous_roi_rank → currency_next_action |
| Incomplete / dead-end heal | IncompletePathRegistry + heal_tick |
| Fleet visibility | hub-first fleet_sync + evolution reports |
| Schedule | `.github/workflows/auto-evolve.yml` every 6 hours + workflow_dispatch |

## What is not fabricated

- **Income:** No simulated ledger writes
- **Force-merge / force-sale:** Draft-only notes; no force-merge
- **Paid spend:** Not initiated by the agent under default policy

Related: `eric847b/zero-cost-wealth-playbook-tool` AUTONOMOUS.md · `eric847b/autonomous-github-agent` AUTONOMOUS.md · **MERGE_POLICY.md**
