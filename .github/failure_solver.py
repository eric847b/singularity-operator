"""
Proactive Runtime Failure Solver for Autonomous GitHub Agent.
Detects, classifies, and remediates (or proposes) runtime failures of all common types.
v3.4.0 — highest-ROI self-healing catalyst.
"""

from __future__ import annotations

import json
import os
import re
import base64
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import requests

# Patterns that indicate specific failure classes (ordered by specificity)
FAILURE_PATTERNS: List[Tuple[str, str, float]] = [
    # (regex, class_name, base_score)
    (r"ModuleNotFoundError|No module named|ImportError", "missing_dependency", 90.0),
    (r"pip install.*failed|Could not find a version that satisfies", "pip_resolution", 85.0),
    (r"Timeout|timed out|Read timed out|ConnectTimeout", "timeout", 80.0),
    (r"Permission denied|EACCES|Access is denied", "permission", 75.0),
    (r"FileNotFoundError|No such file or directory|ENOENT", "missing_file", 78.0),
    (r"SyntaxError|IndentationError|TabError", "syntax", 70.0),
    (r"KeyError|AttributeError|TypeError|ValueError|NameError", "python_runtime", 65.0),
    (r"rate.?limit|429|Too Many Requests|secondary rate limit", "rate_limit", 82.0),
    (r"GITHUB_TOKEN|GH_FULL_PAT|authentication failed|401 Unauthorized|403 Forbidden", "auth", 88.0),
    (r"git.*failed|fatal:|error: failed to push|rejected", "git", 72.0),
    (r"out of memory|OOM|Killed|MemoryError", "oom", 85.0),
    (r"disk space|No space left on device|ENOSPC", "disk", 90.0),
    (r"YAML|yaml\.load|ScannerError|ParserError", "yaml", 68.0),
    (r"Action failed|Process completed with exit code [1-9]", "generic_exit", 55.0),
    (r"Connection refused|Connection reset|Network is unreachable", "network", 77.0),
]

COMMON_REMEDIATIONS: Dict[str, Dict[str, Any]] = {
    "missing_dependency": {
        "description": "Add missing package to requirements.txt and ensure install step runs",
        "safe_actions": ["update_requirements", "create_issue"],
        "example_fix": "Ensure the package is listed in requirements.txt and the Install dependencies step runs before the agent.",
    },
    "pip_resolution": {
        "description": "Pin compatible versions or clear cache",
        "safe_actions": ["update_requirements", "create_issue"],
        "example_fix": "Tighten version ranges or add --no-cache-dir to pip install.",
    },
    "timeout": {
        "description": "Increase timeouts or add retries with exponential backoff",
        "safe_actions": ["edit_timeouts", "create_issue"],
        "example_fix": "Raise requests timeout and wrap external calls in retry logic.",
    },
    "permission": {
        "description": "Check token scopes and file permissions",
        "safe_actions": ["create_issue"],
        "example_fix": "Verify GH_FULL_PAT has repo + workflow scopes; avoid writing outside allowed paths.",
    },
    "missing_file": {
        "description": "Guard path existence or create placeholder",
        "safe_actions": ["create_issue", "add_guard"],
        "example_fix": "Add Path.exists() checks before open(); create empty profile if absent.",
    },
    "syntax": {
        "description": "Fix syntax error in source",
        "safe_actions": ["create_issue"],
        "example_fix": "Correct the reported line; prefer black/ruff in CI.",
    },
    "python_runtime": {
        "description": "Defensive coding around the failing attribute/key",
        "safe_actions": ["create_issue"],
        "example_fix": "Use .get() with defaults; guard None; add type checks.",
    },
    "rate_limit": {
        "description": "Backoff + respect Retry-After; reduce concurrent calls",
        "safe_actions": ["add_backoff", "create_issue"],
        "example_fix": "Sleep on 429; use secondary rate-limit headers; cache results.",
    },
    "auth": {
        "description": "Token missing, expired, or insufficient scope",
        "safe_actions": ["create_issue"],
        "example_fix": "Confirm secrets.GH_FULL_PAT is set and has required scopes; fall back to GITHUB_TOKEN gracefully.",
    },
    "git": {
        "description": "Git state conflict or push rejection",
        "safe_actions": ["create_issue"],
        "example_fix": "Fetch before push; use unique branch names; avoid force-push to protected branches.",
    },
    "oom": {
        "description": "Process killed by OOM",
        "safe_actions": ["create_issue"],
        "example_fix": "Reduce memory footprint; process data in streams; increase runner resources if possible.",
    },
    "disk": {
        "description": "Disk full",
        "safe_actions": ["create_issue"],
        "example_fix": "Clean caches, artifacts, and large logs early in the job.",
    },
    "yaml": {
        "description": "Invalid YAML in workflow or config",
        "safe_actions": ["create_issue"],
        "example_fix": "Validate YAML with yamllint; fix indentation/anchors.",
    },
    "network": {
        "description": "Transient network failure",
        "safe_actions": ["add_retry", "create_issue"],
        "example_fix": "Retry with backoff on connection errors.",
    },
    "generic_exit": {
        "description": "Non-zero exit without specific pattern",
        "safe_actions": ["create_issue"],
        "example_fix": "Inspect full logs; add more structured error reporting.",
    },
}


class FailureSolver:
    """Detects recent workflow failures and proposes or applies safe remediations."""

    def __init__(self, repo_name: str, profile: Optional[Dict] = None, record_error=None):
        self.repo_name = repo_name
        self.profile = profile if profile is not None else {}
        self.record_error = record_error or (lambda e, c="": None)
        self.token = os.getenv("GH_FULL_PAT") or os.getenv("GITHUB_TOKEN")
        self.headers = {}
        if self.token:
            self.headers = {
                "Authorization": f"token {self.token}",
                "Accept": "application/vnd.github+json",
            }

    def _gh_get(self, url: str, params: Optional[Dict] = None) -> Tuple[int, Any]:
        if not self.headers:
            return 0, None
        try:
            resp = requests.get(url, headers=self.headers, params=params or {}, timeout=25)
            if resp.status_code == 200:
                return 200, resp.json()
            return resp.status_code, None
        except Exception as e:
            self.record_error(e, "failure_solver_get")
            return 0, None

    def list_recent_failed_runs(self, max_runs: int = 15) -> List[Dict]:
        """Return recent failed or cancelled workflow runs."""
        url = f"https://api.github.com/repos/{self.repo_name}/actions/runs"
        status, data = self._gh_get(url, {"per_page": max_runs, "status": "completed"})
        if status != 200 or not data:
            return []
        failed = []
        for run in data.get("workflow_runs") or []:
            conclusion = (run.get("conclusion") or "").lower()
            if conclusion in ("failure", "timed_out", "cancelled", "startup_failure"):
                failed.append({
                    "id": run.get("id"),
                    "name": run.get("name"),
                    "conclusion": conclusion,
                    "html_url": run.get("html_url"),
                    "created_at": run.get("created_at"),
                    "head_branch": run.get("head_branch"),
                    "head_sha": run.get("head_sha"),
                    "event": run.get("event"),
                    "run_attempt": run.get("run_attempt", 1),
                })
        return failed

    def get_run_jobs(self, run_id: int) -> List[Dict]:
        url = f"https://api.github.com/repos/{self.repo_name}/actions/runs/{run_id}/jobs"
        status, data = self._gh_get(url, {"per_page": 20})
        if status != 200 or not data:
            return []
        return data.get("jobs") or []

    def classify_log_snippet(self, text: str) -> List[Dict]:
        """Return list of matched failure classes with scores."""
        if not text:
            return []
        matches = []
        lower = text
        for pattern, cls, score in FAILURE_PATTERNS:
            if re.search(pattern, lower, re.IGNORECASE | re.DOTALL):
                m = re.search(pattern, lower, re.IGNORECASE | re.DOTALL)
                start = max(0, m.start() - 80)
                end = min(len(lower), m.end() + 120)
                context = lower[start:end].replace("\n", " ")[:200]
                matches.append({
                    "class": cls,
                    "score": score,
                    "context": context,
                    "remediation": COMMON_REMEDIATIONS.get(cls, {}),
                })
        best: Dict[str, Dict] = {}
        for m in matches:
            c = m["class"]
            if c not in best or m["score"] > best[c]["score"]:
                best[c] = m
        return sorted(best.values(), key=lambda x: x["score"], reverse=True)

    def analyze_run(self, run: Dict) -> Dict:
        """Full analysis of one failed run: jobs + classification."""
        jobs = self.get_run_jobs(run["id"])
        classifications = []
        failing_steps = []
        for job in jobs:
            if (job.get("conclusion") or "").lower() not in ("failure", "timed_out", "cancelled"):
                continue
            for step in job.get("steps") or []:
                if (step.get("conclusion") or "").lower() in ("failure", "timed_out"):
                    failing_steps.append({
                        "job": job.get("name"),
                        "step": step.get("name"),
                        "conclusion": step.get("conclusion"),
                        "number": step.get("number"),
                    })
            proxy_text = " ".join([
                run.get("name") or "",
                job.get("name") or "",
                " ".join(s.get("name") or "" for s in job.get("steps") or []),
            ])
            classifications.extend(self.classify_log_snippet(proxy_text))

        if run.get("conclusion") == "timed_out":
            classifications.append({
                "class": "timeout",
                "score": 85.0,
                "context": "run conclusion timed_out",
                "remediation": COMMON_REMEDIATIONS["timeout"],
            })

        seen = set()
        unique_cls = []
        for c in sorted(classifications, key=lambda x: x["score"], reverse=True):
            if c["class"] not in seen:
                seen.add(c["class"])
                unique_cls.append(c)

        return {
            "run": run,
            "failing_steps": failing_steps,
            "classifications": unique_cls[:5],
            "top_class": unique_cls[0]["class"] if unique_cls else "unknown",
            "top_score": unique_cls[0]["score"] if unique_cls else 40.0,
        }

    def scan_and_prioritize(self, max_runs: int = 10) -> List[Dict]:
        """Return prioritized list of failure analyses (highest ROI first)."""
        failed = self.list_recent_failed_runs(max_runs=max_runs)
        analyses = []
        for run in failed:
            try:
                analyses.append(self.analyze_run(run))
            except Exception as e:
                self.record_error(e, "analyze_run")
        analyses.sort(key=lambda a: a.get("top_score", 0), reverse=True)
        return analyses

    def create_remediation_issue(self, analysis: Dict) -> Optional[Dict]:
        """Create a high-signal issue for a failure (safe, always draft-level)."""
        if not self.headers:
            return None
        run = analysis.get("run") or {}
        top = analysis.get("classifications") or [{}]
        cls = top[0].get("class", "unknown") if top else "unknown"
        rem = top[0].get("remediation") or {} if top else {}
        title = f"🛠️ Runtime failure: {cls} — {run.get('name', 'workflow')} #{run.get('id')}"
        body_lines = [
            f"**Run:** [{run.get('name')}]({run.get('html_url')})",
            f"**Conclusion:** `{run.get('conclusion')}`",
            f"**Branch:** `{run.get('head_branch')}`",
            f"**Detected class:** `{cls}` (score {analysis.get('top_score', 0):.0f})",
            "",
            "### Suggested remediation",
            rem.get("description", "Investigate logs and apply defensive fixes."),
            "",
            f"**Example fix direction:** {rem.get('example_fix', 'Add guards and improve error reporting.')}",
            "",
            "### Failing steps",
        ]
        for s in analysis.get("failing_steps") or []:
            body_lines.append(f"- Job `{s.get('job')}` / Step `{s.get('step')}` → `{s.get('conclusion')}`")
        if not analysis.get("failing_steps"):
            body_lines.append("- (no step details available)")
        body_lines.extend([
            "",
            "---",
            "Auto-created by **FailureSolver v3.4.0** (proactive runtime failure catalyst).",
            "Highest-ROI self-healing path. Safe: issue only, no destructive actions.",
        ])
        body = "\n".join(body_lines)
        try:
            url = f"https://api.github.com/repos/{self.repo_name}/issues"
            resp = requests.post(
                url,
                headers=self.headers,
                json={
                    "title": title[:200],
                    "body": body,
                    "labels": ["runtime-failure", "self-heal", "catalyst", cls],
                },
                timeout=20,
            )
            if resp.status_code in (200, 201):
                data = resp.json()
                self.profile["failures_triaged"] = self.profile.get("failures_triaged", 0) + 1
                self.profile["issues_created"] = self.profile.get("issues_created", 0) + 1
                return {"number": data.get("number"), "html_url": data.get("html_url"), "class": cls}
            return {"error": f"API {resp.status_code}", "detail": resp.text[:200]}
        except Exception as e:
            self.record_error(e, "create_remediation_issue")
            return None

    def run_proactive_pass(self, max_issues: int = 3) -> str:
        """
        Highest-ROI entry point:
        scan recent failures → prioritize → create remediation issues for top ones.
        Returns human-readable summary.
        """
        if not self.token:
            return "NO_TOKEN"
        analyses = self.scan_and_prioritize(max_runs=12)
        if not analyses:
            return "NO_RECENT_FAILURES"
        created = []
        for a in analyses[:max_issues]:
            if a.get("top_score", 0) < 50:
                continue
            result = self.create_remediation_issue(a)
            if result and result.get("number"):
                created.append(f"#{result['number']} ({result.get('class')})")
        self.profile["failure_solver_runs"] = self.profile.get("failure_solver_runs", 0) + 1
        if created:
            return f"Created {len(created)} remediation issues: {', '.join(created)}"
        return f"Scanned {len(analyses)} failures; no new high-signal issues created (may already exist)"


def get_failure_solver(repo_name: str, profile: Optional[Dict] = None, record_error=None) -> FailureSolver:
    return FailureSolver(repo_name, profile=profile, record_error=record_error)


if __name__ == "__main__":
    repo = os.getenv("GITHUB_REPOSITORY", "eric847b/singularity-operator")
    solver = FailureSolver(repo)
    print(json.dumps({
        "recent_failed": len(solver.list_recent_failed_runs()),
        "status": "ready",
    }, indent=2))
