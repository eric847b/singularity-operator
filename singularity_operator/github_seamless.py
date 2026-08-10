"""GitHubSeamless v0.5.7 - Multi-repo orchestration + auto-publish evolution reports.

Real API actions where token available. Supports own-repo pushes, fleet status
sync, catalyst propagation, and structured evolution_summary comments on ROI
status issues (singularity-operator + autonomous-github-agent).
"""

from __future__ import annotations

import base64
import json
import os
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

import requests


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


FLEET_REPOS = [
    "eric847b/singularity-operator",
    "eric847b/autonomous-github-agent",
    "eric847b/AI-Collaboration-Hub",
    "eric847b/zero-cost-wealth-playbook-tool",
    "eric847b/modular-hub-modernization",
]

# Living ROI / status issues — title prefixes used to locate them
ROI_STATUS_TARGETS: List[Tuple[str, str]] = [
    ("eric847b/singularity-operator", "🚀 Singularity Operator ROI"),
    ("eric847b/autonomous-github-agent", "🚀 Fleet ROI Catalyst Status"),
]


class GitHubSeamless:
    """Seamless GitHub agent with multi-repo fleet + evolution report publish."""

    def __init__(
        self,
        token: Optional[str] = None,
        owner: str = "eric847b",
        repo: str = "singularity-operator",
    ):
        self.token = token or os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN") or os.getenv("GH_FULL_PAT")
        self.owner = owner
        self.repo = repo
        self.full_name = f"{owner}/{repo}"
        self.metrics = {
            "pushes": 0,
            "prs": 0,
            "issues": 0,
            "comments": 0,
            "cross_repo_syncs": 0,
            "catalyst_propagations": 0,
            "evolution_reports": 0,
            "errors": 0,
        }
        self.base = "https://api.github.com"

    def _headers(self) -> Dict[str, str]:
        h = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        if self.token:
            h["Authorization"] = f"Bearer {self.token}"
        return h

    def _req(
        self,
        method: str,
        path: str,
        json_body: Optional[Dict] = None,
        timeout: int = 15,
    ) -> Dict[str, Any]:
        url = f"{self.base}{path}"
        try:
            r = requests.request(
                method,
                url,
                headers=self._headers(),
                json=json_body,
                timeout=timeout,
            )
            try:
                body = r.json() if r.text else {}
            except Exception:
                body = {"raw": r.text[:300]}
            if r.status_code >= 400:
                self.metrics["errors"] += 1
                return {
                    "ok": False,
                    "status": r.status_code,
                    "error": body.get("message", str(body))[:200],
                    "body": body,
                }
            return {"ok": True, "status": r.status_code, "data": body}
        except Exception as e:
            self.metrics["errors"] += 1
            return {"ok": False, "status": 0, "error": str(e)[:200]}

    def push_update(
        self,
        file_path: str,
        content: str,
        commit_msg: str = "chore(autonomous): self-evolve update [GitHubSeamless]",
        branch: str = "main",
    ) -> Dict[str, Any]:
        path = f"/repos/{self.owner}/{self.repo}/contents/{file_path}"
        sha = None
        get = self._req("GET", f"{path}?ref={branch}")
        if get.get("ok"):
            sha = get["data"].get("sha")
        payload: Dict[str, Any] = {
            "message": commit_msg,
            "content": base64.b64encode(content.encode()).decode(),
            "branch": branch,
        }
        if sha:
            payload["sha"] = sha
        res = self._req("PUT", path, payload)
        if res.get("ok"):
            self.metrics["pushes"] += 1
            return {
                "status": "pushed",
                "file": file_path,
                "sha": res["data"].get("commit", {}).get("sha"),
                "metrics": self.metrics.copy(),
            }
        return {"status": "error", **res}

    def create_issue(
        self,
        title: str,
        body: str,
        labels: Optional[List[str]] = None,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
    ) -> Dict[str, Any]:
        o, r = owner or self.owner, repo or self.repo
        payload: Dict[str, Any] = {"title": title, "body": body}
        if labels:
            payload["labels"] = labels
        res = self._req("POST", f"/repos/{o}/{r}/issues", payload)
        if res.get("ok"):
            self.metrics["issues"] += 1
            return {
                "status": "created",
                "number": res["data"].get("number"),
                "html_url": res["data"].get("html_url"),
            }
        return {"status": "error", **res}

    def comment_on_issue(
        self,
        issue_number: int,
        body: str,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
    ) -> Dict[str, Any]:
        o, r = owner or self.owner, repo or self.repo
        res = self._req(
            "POST",
            f"/repos/{o}/{r}/issues/{issue_number}/comments",
            {"body": body},
        )
        if res.get("ok"):
            self.metrics["comments"] += 1
            return {"status": "commented", "id": res["data"].get("id")}
        return {"status": "error", **res}

    def create_pr(
        self,
        title: str,
        body: str,
        head: str,
        base: str = "main",
        owner: Optional[str] = None,
        repo: Optional[str] = None,
    ) -> Dict[str, Any]:
        o, r = owner or self.owner, repo or self.repo
        res = self._req(
            "POST",
            f"/repos/{o}/{r}/pulls",
            {"title": title, "body": body, "head": head, "base": base},
        )
        if res.get("ok"):
            self.metrics["prs"] += 1
            return {
                "status": "created",
                "number": res["data"].get("number"),
                "html_url": res["data"].get("html_url"),
            }
        return {"status": "error", **res}

    def list_fleet(self) -> List[str]:
        return list(FLEET_REPOS)

    def _find_issue_by_title_prefix(
        self, owner: str, repo: str, prefix: str
    ) -> Optional[int]:
        res = self._req(
            "GET",
            f"/repos/{owner}/{repo}/issues?state=open&per_page=30&sort=updated",
        )
        if not res.get("ok") or not isinstance(res.get("data"), list):
            return None
        for issue in res["data"]:
            if issue.get("pull_request"):
                continue
            title = issue.get("title") or ""
            if title.startswith(prefix):
                return issue.get("number")
        return None

    def publish_evolution_report(
        self,
        summary: str,
        extra: Optional[Dict[str, Any]] = None,
        targets: Optional[List[Tuple[str, str]]] = None,
    ) -> Dict[str, Any]:
        """Post a structured evolution_summary comment on living ROI status issues.

        Default targets:
          - singularity-operator ROI status issue
          - autonomous-github-agent Fleet ROI Catalyst Status issue

        Creates a minimal status issue if none exists (labeled fleet-status).
        """
        stamp = _utc_now()
        extra = extra or {}
        lines = [
            f"### 📈 Evolution report",
            f"**From:** `{self.full_name}`  ",
            f"**At:** `{stamp}`  ",
            "",
            "```",
            summary.strip()[:800],
            "```",
        ]
        if extra:
            lines.append("")
            lines.append("<details><summary>Extra metrics</summary>\n")
            lines.append("```json")
            lines.append(json.dumps(extra, indent=2)[:1200])
            lines.append("```")
            lines.append("</details>")
        lines.extend([
            "",
            f"— Auto-published by **GitHubSeamless v0.5.7** (evolution report)",
        ])
        body = "\n".join(lines)

        tgt = targets or ROI_STATUS_TARGETS
        results: List[Dict[str, Any]] = []

        for full, prefix in tgt:
            try:
                o, r = full.split("/", 1)
            except ValueError:
                results.append({"repo": full, "status": "skip", "reason": "bad name"})
                continue

            issue_num = self._find_issue_by_title_prefix(o, r, prefix)
            if issue_num:
                res = self.comment_on_issue(issue_num, body, owner=o, repo=r)
                entry = {"repo": full, "action": "comment", "issue": issue_num, **res}
            else:
                # Fallback: create living status issue then comment is not needed — body is the issue
                res = self.create_issue(
                    title=f"{prefix} (auto-updated)",
                    body=(
                        f"**Living ROI / Evolution status** for `{full}`\n\n"
                        f"Seeded by GitHubSeamless evolution report publisher.\n\n"
                        f"{body}"
                    ),
                    labels=["fleet-status", "catalyst", "self-heal"],
                    owner=o,
                    repo=r,
                )
                entry = {"repo": full, "action": "issue", **res}

            if entry.get("status") in ("commented", "created"):
                self.metrics["evolution_reports"] += 1
            results.append(entry)

        return {
            "status": "published",
            "targets": len(tgt),
            "results": results,
            "metrics": self.metrics.copy(),
        }

    def sync_status(
        self,
        summary: str,
        target_repos: Optional[List[str]] = None,
        label: str = "fleet-status",
    ) -> Dict[str, Any]:
        targets = target_repos or [x for x in FLEET_REPOS if x != self.full_name]
        results: List[Dict[str, Any]] = []
        stamp = _utc_now()
        body = (
            f"**Cross-repo status sync** from `{self.full_name}`  \n"
            f"**At:** `{stamp}`  \n\n"
            f"{summary}\n\n"
            f"— GitHubSeamless v0.5.7 multi-repo orchestration"
        )

        for full in targets:
            try:
                o, r = full.split("/", 1)
            except ValueError:
                results.append({"repo": full, "status": "skip", "reason": "bad name"})
                continue

            search = self._req(
                "GET",
                f"/repos/{o}/{r}/issues?state=open&labels={label}&per_page=5",
            )
            issue_num = None
            if search.get("ok") and isinstance(search.get("data"), list) and search["data"]:
                issue_num = search["data"][0].get("number")

            if issue_num:
                res = self.comment_on_issue(issue_num, body, owner=o, repo=r)
                results.append({"repo": full, "action": "comment", "issue": issue_num, **res})
            else:
                res = self.create_issue(
                    title=f"📡 Fleet status sync from {self.repo}",
                    body=body,
                    labels=[label, "catalyst"] if label else ["catalyst"],
                    owner=o,
                    repo=r,
                )
                results.append({"repo": full, "action": "issue", **res})

            if results[-1].get("status") in ("commented", "created"):
                self.metrics["cross_repo_syncs"] += 1

        return {
            "status": "sync_complete",
            "targets": len(targets),
            "results": results,
            "metrics": self.metrics.copy(),
        }

    def propagate_catalyst(
        self,
        key: str,
        insight: str,
        source_issue: Optional[int] = None,
        target_repos: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        targets = target_repos or [x for x in FLEET_REPOS if x != self.full_name]
        targets = sorted(
            targets,
            key=lambda x: 0 if "autonomous-github-agent" in x else 1,
        )
        results: List[Dict[str, Any]] = []
        stamp = _utc_now()
        title = f"Catalyst: {key[:60]}"
        body = (
            f"**Catalyst propagation** from `{self.full_name}`  \n"
            f"**Key:** `{key}`  \n"
            f"**Source issue:** {source_issue or 'n/a'}  \n"
            f"**At:** `{stamp}`  \n\n"
            f"### Insight\n{insight}\n\n"
            f"— Auto-generated by GitHubSeamless v0.5.7 (cross-repo catalyst)"
        )

        for full in targets[:3]:
            try:
                o, r = full.split("/", 1)
            except ValueError:
                continue
            res = self.create_issue(
                title=title,
                body=body,
                labels=["catalyst", "self-heal"],
                owner=o,
                repo=r,
            )
            results.append({"repo": full, **res})
            if res.get("status") == "created":
                self.metrics["catalyst_propagations"] += 1

        return {
            "status": "propagated",
            "key": key,
            "targets_attempted": len(results),
            "results": results,
            "metrics": self.metrics.copy(),
        }

    def fleet_health_snapshot(self) -> Dict[str, Any]:
        snap: Dict[str, Any] = {"at": _utc_now(), "repos": {}}
        for full in FLEET_REPOS:
            try:
                o, r = full.split("/", 1)
            except ValueError:
                continue
            res = self._req("GET", f"/repos/{o}/{r}/issues?state=open&per_page=1")
            open_count = "?"
            if res.get("ok"):
                open_count = len(res.get("data") or [])
            snap["repos"][full] = {"sample_open": open_count, "ok": res.get("ok", False)}
        return snap

    def get_metrics(self) -> Dict[str, Any]:
        return self.metrics.copy()


print("GitHubSeamless v0.5.7 - Multi-repo + evolution report publish ready")
