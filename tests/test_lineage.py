"""Multi-hop provenance / lineage export tests."""
import os
import tempfile

from singularity_operator.everything_db import EverythingDB


def test_walk_ancestors_and_export_lineage():
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        db = EverythingDB(db_path=path, enable_vectors=False)
        root = db.add_sequence({"k": "root"}, tags="t:root")
        mid = db.add_sequence({"k": "mid"}, tags="t:mid", parent_key=root, derives_from="mid")
        leaf = db.add_sequence({"k": "leaf"}, tags="t:leaf", parent_key=mid, derives_from="leaf")

        chain = db.walk_ancestors(leaf)
        assert len(chain) == 3
        assert chain[0]["key"] == leaf
        assert chain[-1]["key"] == root

        lin = db.export_lineage(leaf, include_children=True)
        assert lin["depth"] == 2
        assert lin["root_key"] == root
        assert any(a["key"] == mid for a in lin["ancestors"])

        # children of mid should include leaf
        kids = db.get_children(mid)
        assert any(c["key"] == leaf for c in kids)
    finally:
        try:
            os.unlink(path)
        except OSError:
            pass
