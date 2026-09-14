# Singularity Operator v0.5.13

**Self-improving AI system** with EverythingDB, fleet orchestration, AGA metrics feedback, and **continuous upgrade from live ROI ranking**.

## Releases & Windows executable

Download the latest **Release** from the [Releases page](https://github.com/eric847b/singularity-operator/releases).

- **`singularity-operator.exe`** — single-file Windows launcher (no separate Python install)
- Wheel / sdist for `pip install`

Set environment variables as needed:
```bash
GROQ_API_KEY=...
GITHUB_TOKEN=...   # or GH_FULL_PAT
```

To cut a new release after packaging changes land:
```bash
git tag v0.5.13
git push origin v0.5.13
```
GitHub Actions builds the EXE + packages and publishes the release automatically.

## What's New in v0.5.13
- Version level advanced and synchronized across the canonical `VERSION` and Python package metadata.
- Release documentation advanced with the current executable/package release target.
- Continuous-upgrade architecture remains focused on measurable ROI and cross-repo fleet improvement.

## What's New in v0.5.12
- Fixed Dependabot parse failure on `release.yml` (inconsistent YAML indentation in multiline body block).
- Version strings synchronized across VERSION, pyproject.toml, launcher, and README.
- Release workflow is now fully Dependabot-compatible; next github-actions update should succeed.

## What's New in v0.5.11
- Orchestrator task `continuous_roi_rank` records AGA `roi_top_ref` / score into EverythingDB each cycle.
- **SO#9 closed** with real cross-repo currency work: OSS/Maintainer niche on `zero-cost-wealth-playbook-tool`.
- Ranking loop: ingest AGA → rank → prefer currency fleet path → measurable artifact.

## Quick Start (from source)
```bash
pip install -e .
python singularity_operator.py
```

Requires `GITHUB_TOKEN` / `GH_FULL_PAT` for live AGA ingest and fleet actions.

## Architecture
EverythingDB · SelfImprover · Chaos · Serendipity · Browser · Userscript · GitHubSeamless (fleet + AGA feedback) · Orchestrator (incl. continuous_roi_rank)

## Roadmap
- Next live-ranked catalyst work after empty queue / new seeds.
- Optional real embedding backend (feature-flagged).
- Keep release metadata synchronized automatically before every versioned release.

*Status: v0.5.13 continuous upgrade. Version metadata synchronized. Ready for release workflow/tag.*
