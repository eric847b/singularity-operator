"""Minimal agent proposal workflow: propose → validate → store with provenance.

Zero-cost friendly: uses EverythingDB.propose_unknown + shared validation.
Accepted proposals become sequences with parent_key / derives_from links.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from .everything_db import EverythingDB
from .validation import ValidationResult, validate_sequence_payload, validate_python_evolution


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


class AgentProposalWorkflow:
    """Propose → validate → store pipeline for knowledge / code proposals."""

    def __init__(self, db: Optional[EverythingDB] = None):
        self.db = db or EverythingDB(enable_vectors=True)
        self.metrics = {
            "proposals_generated": 0,
            "proposals_accepted": 0,
            "proposals_rejected": 0,
        }

    def propose(
        self,
        domain: str = "singularity acceleration + currency experiment ranking",
        n: int = 3,
        parent_key: Optional[str] = None,
    ) -> List[Any]:
        """Generate candidate proposals (reuses EverythingDB.propose_unknown)."""
        seqs = self.db.propose_unknown(domain, n=n)
        self.metrics["proposals_generated"] += len(seqs)
        # re-store with explicit agent workflow provenance if parent given
        if parent_key:
            for seq in seqs:
                self.db.add_sequence(
                    seq,
                    tags=f"agent:proposed:{domain[:40]}",
                    parent_key=parent_key,
                    derives_from="agent_proposals.propose",
                )
        return seqs

    def validate_proposal(self, proposal: Any, *, as_code: bool = False, original_code: str = "") -> ValidationResult:
        """Validate a single proposal payload (structured or Python code)."""
        if as_code:
            src = proposal if isinstance(proposal, str) else str(proposal)
            return validate_python_evolution(original_code or "pass\n", src, require_change=bool(original_code))
        return validate_sequence_payload(proposal)

    def store_accepted(
        self,
        proposal: Any,
        *,
        parent_key: Optional[str] = None,
        tags: str = "agent:accepted",
        validation: Optional[ValidationResult] = None,
        meta: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Store an accepted proposal with provenance."""
        payload = {
            "proposal": proposal,
            "accepted_at": _utc_now(),
            "validation": validation.as_dict() if validation else None,
            "meta": meta or {},
        }
        key = self.db.add_sequence(
            payload,
            tags=tags,
            modality="code" if isinstance(proposal, str) and "def " in proposal else "text",
            parent_key=parent_key,
            derives_from="agent_proposals.store_accepted",
        )
        self.metrics["proposals_accepted"] += 1
        return key

    def run(
        self,
        domain: str = "singularity acceleration + currency experiment ranking",
        n: int = 3,
        parent_key: Optional[str] = None,
        as_code: bool = False,
        original_code: str = "",
    ) -> Dict[str, Any]:
        """Full pipeline: propose → validate each → store accepted with lineage."""
        candidates = self.propose(domain=domain, n=n, parent_key=None)
        accepted_keys: List[str] = []
        rejected: List[Dict[str, Any]] = []

        batch_parent = parent_key
        if batch_parent is None:
            # anchor batch so children share a common parent
            batch_parent = self.db.add_sequence(
                {"kind": "proposal_batch", "domain": domain, "n": n, "at": _utc_now()},
                tags="agent:batch",
                derives_from="agent_proposals.run",
            )

        for cand in candidates:
            vr = self.validate_proposal(cand, as_code=as_code, original_code=original_code)
            if vr.ok:
                key = self.store_accepted(
                    cand,
                    parent_key=batch_parent,
                    tags=f"agent:accepted:{domain[:32]}",
                    validation=vr,
                    meta={"domain": domain},
                )
                accepted_keys.append(key)
            else:
                self.metrics["proposals_rejected"] += 1
                rejected.append({"proposal_preview": str(cand)[:120], "reason": vr.reason})

        report = {
            "domain": domain,
            "batch_parent": batch_parent,
            "generated": len(candidates),
            "accepted": len(accepted_keys),
            "rejected": len(rejected),
            "accepted_keys": accepted_keys,
            "rejected_detail": rejected[:5],
            "metrics": self.metrics.copy(),
            "at": _utc_now(),
        }
        self.db.add_sequence(
            report,
            tags="agent:run_report",
            parent_key=batch_parent,
            derives_from="agent_proposals.run",
        )
        return report


def run_proposal_cycle(
    db: Optional[EverythingDB] = None,
    domain: str = "singularity acceleration + currency experiment ranking",
    n: int = 3,
    parent_key: Optional[str] = None,
) -> Dict[str, Any]:
    """Convenience entry point for Orchestrator / CLI."""
    wf = AgentProposalWorkflow(db=db)
    return wf.run(domain=domain, n=n, parent_key=parent_key)
