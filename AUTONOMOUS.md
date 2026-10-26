# Autonomous mode (default)

**Operator constraint:** The owner has limited capacity and zero requirement to perform manual steps. All primary loops must run without human intervention.

## What is autonomous

| Capability | Mechanism |
|------------|-----------|
| Code/docs evolution | SelfImprover + free AI rotator + quality-gate |
| Knowledge + provenance | EverythingDB sequences, parent links, export_lineage |
| Agent proposals | AgentProposalWorkflow validate→store |
| Currency ranking | fetch_currency_signals → continuous_roi_rank → currency_next_action |
| Fleet visibility | hub-first fleet_sync + evolution reports |
| Schedule | `.github/workflows/auto-evolve.yml` every 6 hours + workflow_dispatch |

## What is not fabricated

- **Income:** No simulated ledger writes. Payment requires a real payer outside pure automation.
- **Force-merge / force-sale:** Draft-only notes; no force-merge; no marking experiments won without evidence.

## Design implication

Maximize **passive discoverability**, **agent-readable signals**, and **continuous zero-cost improvement**. Do not block on outreach, booking, or marketplace paste steps.

Related: `eric847b/zero-cost-wealth-playbook-tool` `AUTONOMOUS.md` + `OPERATOR_NEXT.md`.
