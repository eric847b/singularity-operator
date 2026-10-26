"""Agent proposal workflow tests (offline-friendly)."""
import os
import tempfile

from singularity_operator.agent_proposals import AgentProposalWorkflow
from singularity_operator.everything_db import EverythingDB
from singularity_operator.validation import validate_sequence_payload


def test_validate_and_store_without_network():
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        db = EverythingDB(db_path=path, enable_vectors=False)
        wf = AgentProposalWorkflow(db=db)

        # force offline path: inject candidates via store after manual validate
        cand = {"idea": "runway_velocity_transistor", "score": 1}
        vr = wf.validate_proposal(cand)
        assert vr.ok
        key = wf.store_accepted(cand, tags="agent:test", validation=vr)
        got = db.get_sequence(key)
        assert got is not None
        assert got.get("derives_from") == "agent_proposals.store_accepted"
        assert wf.metrics["proposals_accepted"] == 1
    finally:
        try:
            os.unlink(path)
        except OSError:
            pass


def test_run_pipeline_creates_batch_parent():
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        db = EverythingDB(db_path=path, enable_vectors=False)
        wf = AgentProposalWorkflow(db=db)
        # propose_unknown may hit network or fallback list — either is fine
        report = wf.run(domain="test domain", n=2)
        assert "batch_parent" in report
        assert report["generated"] >= 1
        assert report["accepted"] + report["rejected"] == report["generated"]
        parent = report["batch_parent"]
        kids = db.get_children(parent)
        # at least the run_report child
        assert len(kids) >= 1
    finally:
        try:
            os.unlink(path)
        except OSError:
            pass


def test_payload_validator_rejects_none():
    assert not validate_sequence_payload(None).ok
