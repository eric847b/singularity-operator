"""Tests for EverythingDB provenance (parent_key / derives_from)."""
import os
import tempfile

from singularity_operator.everything_db import EverythingDB


def test_parent_and_derives_from_roundtrip():
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        db = EverythingDB(db_path=path, enable_vectors=False)
        parent = db.add_sequence({"kind": "parent"}, tags="t:parent", derives_from="test")
        child = db.add_sequence(
            {"kind": "child"},
            tags="t:child",
            parent_key=parent,
            derives_from="test_child",
        )
        got = db.get_sequence(child)
        assert got is not None
        assert got["parent_key"] == parent
        assert got["derives_from"] == "test_child"
        kids = db.get_children(parent)
        assert any(k["key"] == child for k in kids)
        health = db.get_health_snapshot()
        assert health.get("with_parent", 0) >= 1
    finally:
        try:
            os.unlink(path)
        except OSError:
            pass


def test_self_test_includes_provenance():
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        db = EverythingDB(db_path=path, enable_vectors=False)
        # avoid network: propose_unknown may call AI; self_test still exercises provenance block
        result = db.self_test()
        assert "provenance" in result
        # provenance may depend on AI for propose; at minimum no crash
        assert result.get("db_connect") is True
    finally:
        try:
            os.unlink(path)
        except OSError:
            pass
