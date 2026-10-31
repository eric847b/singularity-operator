# Merge Policy — Always Mergeable Trunk

**Status:** Fleet rule (2026-10-31)
**Applies to:** singularity-operator, AI-Collaboration-Hub, and all public fleet repos

## Rule

Every branch and every PR **must** be capable of landing on `main` (and ideally the release branch) without breaking the live path.

Incomplete work is allowed. Incomplete *execution* is not.

## Incomplete multi-file changes

When a change needs multiple files and only one lands:

| Case | Action |
|------|--------|
| Finished file has no runtime dependency on the missing one | Merge it. |
| Finished file would call missing code | Gate with a feature flag, optional import, or stub that returns a safe default. |
| Missing piece is discovered at runtime | Treat as a **dead end**: record the intended input, take the safe path, queue recovery (do not crash the trunk). |

Branches are short-lived increments, not long development highways. Prefer merge-early + inert incomplete over long-lived feature branches.

## Dead-end / open-ended recovery (programmed)

Use `singularity_operator.incomplete_path`:

1. **Register** required pieces and intended inputs when starting multi-part work.
2. **Check** before executing a path that depends on all pieces.
3. If incomplete → **safe default**, remember inputs, mark `paused_for_update`.
4. When the missing piece appears → **resume** with remembered inputs (live update on the fly).

This is the code-level expression of “dead end with a route to bypass the missing parts.”

## PR / agent checklist

- [ ] CI green (or only non-blocking skips)
- [ ] No force-merge / force-push
- [ ] Incomplete code is inert (flag, stub, or optional import)
- [ ] Multi-file features register an `IncompletePath` (or equivalent) when partial merge is possible
- [ ] Main remains shippable after merge

## VS Code

See AI-Collaboration-Hub `.vscode/settings.json` — policy reminder and GitHub PR extension recommended so incomplete work is visible before merge.

Related: `AUTONOMOUS.md`, `CONTINUOUS_CONTEXT.md`
