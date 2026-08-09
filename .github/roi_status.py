"""
Singularity Operator — fleet ROI status + auto-seed next evolution cycle.
v0.5.1 — Aligns with autonomous-github-agent ROI Catalyst pattern.
Living status issue (auto-updated). Seeds next high-ROI evolution task when ranked work is empty.
Draft/issue only. No force-merge. Stdlib + requests.
"""
from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests

HOST_REPO = os.getenv("GITHUB_REPOSITORY", "eric847b/singularity-operator")
STATUS_TITLE = "🚀 Singularity Operator ROI / Evolution Status (auto-updated)"
VERSION = "0.5.1"

CURRENCY_KW = ("revenue", "payment", "cash", "wallet", "monetize", "wealth", "profit")
CAPABILITY_KW = ("evolve", "self-improve", "everythingdb", "singularity", "unlock", "orchestrator", "serendipity")
CONFLICT_KW = ("blocker", "stuck", "deadlock", "conflict", "priority", "decision")


def _headers() -> dict:
    token = os.getenv("GH_FULL_PAT") or os.getenv("GITHUB_TOKEN")
    if not token:
        return {}
    return {"Authorization": f"token {token}", "Accept": "application/vnd.github+json"}


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _score_issue(issue: Dict[str, Any]) -> float:
    title = (issue.get("title") or "").lower()
    body = ((issue.get("body") or "")[:1500]).lower()
    labels = [str(l.get("name", "")).lower() for l in (issue.get("labels") or [])]
    blob = f"{title} {body} {' '.join(labels)}"
    score = 20.0
    if any(k in blob for k in CURRENCY_KW):
        score += 40.0
    if any(k in blob for k in CAPABILITY_KW):
        score += 30.0
    if any(k in blob for k in CONFLICT_KW):
        score += 25.0
    if "catalyst" in labels or "blocker" in labels:
        score += 15.0
    if int(issue.get("comments") or 0) == 0:
        score += 8.0
    return min(score, 100.0)


def fetch_open_work(per_page: int = 15) -> List[Dict[str, Any]]:
    headers = _headers()
    if not headers:
        return []
    try:
        resp = requests.get(
            f"https://api.github.com/repos/{HOST_REPO}/issues",
            headers=headers,
            params={"state": "open", "per_page": per_page, "sort": "updated", "direction": "desc"},
            timeout=20,
        )
        if resp.status_code != 200:
            return []
        items = [i for i in (resp.json() or []) if not i.get("pull_request")]
        work = []
        for issue in items:
            title = issue.get("title") or ""
            if title.startswith("🚀 Singularity Operator ROI") or "(auto-updated)" in title:
                continue
            labels = [str(l.get("name", "")).lower() for l in (issue.get("labels") or [])]
            if "fleet-status" in labels or "roi-catalyst" in labels:
                continue
            score = _score_issue(issue)
            work.append({
                "number": issue.get("number"),
                "title": title[:140],
                "html_url": issue.get("html_url"),
                "score": round(score, 1),
                "labels": labels,
            })
        work.sort(key=lambda x: x["score"], reverse=True)
        return work
    except Exception as e:
        print(f"[roi_status] fetch_open_work: {e}")
        return []


def find_status_issue(headers: dict) -> Optional[int]:
    try:
        resp = requests.get(
            f"https://api.github.com/repos/{HOST_REPO}/issues",
            headers=headers,
            params={"state": "open", "per_page": 30},
            timeout=20,
        )
        if resp.status_code != 200:
            return None
        for issue in resp.json() or []:
            if (issue.get("title") or "").startswith("🚀 Singularity Operator ROI"):
                return issue.get("number")
    except Exception:
        pass
    return None


def seed_evolution_issue(headers: dict) -> Optional[Dict[str, Any]]:
    """When no ranked work exists, seed one high-ROI evolution task."""
    title = "Evolution cycle: Expand EverythingDB metrics + SelfImprover learning loop"
    body = (
        "**Auto-seeded by ROI status v0.5.1** when open work queue was empty.\n\n"
        "### Goal\n"
        "Advance continuous unlimited upgrading without owner steps.\n\n"
        "### Suggested scope (AI-owned)\n"
        "1. Persist richer health_snapshot / metrics from EverythingDB and SelfImprover.\n"
        "2. After each auto-evolve run, write a one-line evolution summary into the ROI status issue.\n"
        "3. Prefer stdlib + existing Groq path. Draft-only / issue updates; no force-merge.\n\n"
        "Labels: catalyst, self-heal\n"
    )
    try:
        resp = requests.post(
            f"https://api.github.com/repos/{HOST_REPO}/issues",
            headers=headers,
            json={"title": title, "body": body, "labels": ["catalyst", "self-heal"]},
            timeout=20,
        )
        if resp.status_code in (200, 201):
            data = resp.json()
            return {"number": data.get("number"), "html_url": data.get("html_url"), "action": "seeded"}
    except Exception as e:
        print(f"[roi_status] seed: {e}")
    return None


def upsert_status(ranked: List[Dict[str, Any]], seeded: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    headers = _headers()
    if not headers:
        return {"error": "NO_TOKEN"}

    top = ranked[0] if ranked else None
    lines = [
        f"**Generated:** `{_utc_now_iso()}`  ",
        f"**Module:** Singularity ROI / Evolution Status v{VERSION}  ",
        f"**Work candidates scored:** {len(ranked)}  ",
        "",
        "### Root action (highest ROI)",
    ]
    if top:
        lines.append(
            f"- **[#{top['number']}]({top.get('html_url')})** — score **{top['score']}**  \n"
            f"  `{top['title']}`  \n"
            f"  labels: `{', '.join(top.get('labels') or [])}`"
        )
        lines.append("")
        lines.append("**Next prompt:**")
        lines.append(
            f"```\nExecute singularity-operator#{top['number']}: {top['title']}. "
            f"Do the toughest real work first (no simulation). Produce measurable progress "
            f"(code, metrics, or closed loop) and report the exact next prompt after that.\n```"
        )
    else:
        lines.append("- No scored open work above threshold.")
        if seeded:
            lines.append(f"- **Auto-seeded:** [#{seeded['number']}]({seeded.get('html_url')})")

    lines.extend(["", "### Top ranked work"])
    if ranked:
        for i, item in enumerate(ranked[:8], 1):
            lines.append(
                f"{i}. [#{item['number']}]({item.get('html_url')}) "
                f"score={item['score']} — {item['title'][:90]}"
            )
    else:
        lines.append("_None — seed will create next evolution cycle when empty._")

    lines.extend([
        "",
        "---",
        f"Auto-updated by **Singularity ROI Status v{VERSION}**. "
        "Scoring favors currency, capability unlock, conflict. "
        "Safe: issues + status only. No force-merge.",
    ])
    body = "\n".join(lines)

    existing = find_status_issue(headers)
    try:
        if existing:
            resp = requests.patch(
                f"https://api.github.com/repos/{HOST_REPO}/issues/{existing}",
                headers=headers,
                json={"body": body, "title": STATUS_TITLE},
                timeout=20,
            )
            if resp.status_code == 200:
                data = resp.json()
                return {"action": "updated", "number": data.get("number"), "html_url": data.get("html_url")}
            return {"error": f"patch:{resp.status_code}"}

        resp = requests.post(
            f"https://api.github.com/repos/{HOST_REPO}/issues",
            headers=headers,
            json={
                "title": STATUS_TITLE,
                "body": body,
                "labels": ["catalyst", "self-heal", "fleet-status"],
            },
            timeout=20,
        )
        if resp.status_code in (200, 201):
            data = resp.json()
            return {"action": "created", "number": data.get("number"), "html_url": data.get("html_url")}
        return {"error": f"create:{resp.status_code}", "detail": (resp.text or "")[:150]}
    except Exception as e:
        return {"error": str(e)[:150]}


def run() -> str:
    ranked = fetch_open_work()
    seeded = None
    if not ranked or (ranked and ranked[0]["score"] < 30):
        headers = _headers()
        if headers:
            seeded = seed_evolution_issue(headers)
            if seeded:
                ranked = fetch_open_work()  # refresh after seed

    result = upsert_status(ranked, seeded)
    artifact = {
        "generated_at": _utc_now_iso(),
        "version": VERSION,
        "work_candidates": len(ranked),
        "top": ranked[0] if ranked else None,
        "seeded": seeded,
        "status_issue": result,
    }
    Path("singularity-roi-status.json").write_text(json.dumps(artifact, indent=2) + "\n")
    summary = (
        f"roi_ok work={len(ranked)} "
        f"top=#{ranked[0]['number'] if ranked else 'none'} "
        f"score={ranked[0]['score'] if ranked else 0} "
        f"status={result.get('action')}:{result.get('number')} "
        f"seeded={seeded.get('number') if seeded else 'no'}"
    )
    print(f"[roi_status] {summary}")
    return summary


if __name__ == "__main__":
    print(run())
