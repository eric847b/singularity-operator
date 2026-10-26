# Currency signal schema (AGA ↔ SO parity)

Both **autonomous-github-agent** (`roi_catalyst.fetch_currency_signal`) and **singularity-operator** (`GitHubSeamless.fetch_currency_signals` + `currency_signal_schema.normalize_currency_signal`) share this core:

| Key | Type | Notes |
|-----|------|--------|
| ok | bool | Parse success |
| source | str | Default `eric847b/zero-cost-wealth-playbook-tool` |
| at | ISO-8601 | Emit time |
| version | str\|null | Wealth VERSION / status block |
| preferred_currency_path | bool | Hard-bias flag |
| status | str | healthy / unknown / … |
| top_experiment | str\|null | e.g. setup-session-offer |
| top_score | number\|null | Rank score |
| capabilities | list[str] | tracker, runway, … |
| roi_note | str | ≤240 chars |
| status_file_present | bool | CURRENCY_STATUS.md found |
| mode | str | `autonomous` |

**Policy:** never simulate income; no human required for signal loop health.

SO also may attach `open_issues_sample` / `open_titles` as SO-only extensions.
