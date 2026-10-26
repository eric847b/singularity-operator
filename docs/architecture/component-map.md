# Component Map

| Component | Path | Responsibility |
|-----------|------|----------------|
| Entry / CLI | `singularity_operator.py`, `cli.py` | Launch and command surface |
| EverythingDB | `everything_db.py` | Knowledge store, sequences |
| SelfImprover | `self_improver.py` | Iterative code/docs improvement |
| Orchestrator | `orchestrator.py` | Task cycles, ROI ranking, signals |
| FreeAIClient | `free_ai_client.py` | Provider rotation, status |
| GitHubSeamless | `github_seamless.py` | Repo ops, AGA, currency, fleet |
| Chaos / Serendipity | `chaos_engine.py`, `serendipity_engine.py` | Controlled exploration |
| Browser / Userscript | `browser_automation.py`, `userscript_gen.py` | Automation surfaces |

Boundaries and contracts will be refined in Phase 1 (Foundation Stability).
