"""SerendipityEngine v0.5.4 - Cross-sequence unexpected connections + inspiration amplification.

Pulls sequences from EverythingDB, finds non-obvious pairings, amplifies with
random word sparks, persists captures. Stdlib + existing DB path. AI-owned.
"""

from __future__ import annotations

import json
import random
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

from .everything_db import EverythingDB


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


# Compact inspiration lexicon — zero external deps
SPARK_WORDS = (
    "lattice", "echo", "fold", "spark", "bridge", "mirror", "pulse",
    "threshold", "orbit", "fractal", "latch", "cascade", "rift", "seed",
    "weave", "horizon", "signal", "anchor", "drift", "bloom",
)


class SerendipityEngine:
    """Discover unexpected connections across stored sequences."""

    def __init__(self, db: Optional[EverythingDB] = None):
        self.db = db or EverythingDB()
        self.captures = 0
        self.connections_found = 0
        self.log: List[Dict[str, Any]] = []

    def _load_sequences(self, limit: int = 24) -> List[Tuple[str, Any, str]]:
        """Return list of (key, value, tags) from sqlite."""
        try:
            rows = self.db.conn.execute(
                "SELECT key, value, tags FROM sequences ORDER BY timestamp DESC LIMIT ?",
                (limit,),
            ).fetchall()
            out = []
            for key, value, tags in rows:
                try:
                    parsed = json.loads(value)
                except Exception:
                    parsed = value
                out.append((str(key), parsed, str(tags or "")))
            return out
        except Exception:
            return []

    def _pair_score(self, a: Any, b: Any, tags_a: str, tags_b: str) -> float:
        """Heuristic surprise score — different tags + shared tokens = interesting."""
        score = 0.0
        if tags_a != tags_b:
            score += 2.0
        sa = json.dumps(a, sort_keys=True) if isinstance(a, (dict, list)) else str(a)
        sb = json.dumps(b, sort_keys=True) if isinstance(b, (dict, list)) else str(b)
        tokens_a = set(sa.lower().replace("{", " ").replace("}", " ").split())
        tokens_b = set(sb.lower().replace("{", " ").replace("}", " ").split())
        overlap = tokens_a & tokens_b
        if 1 <= len(overlap) <= 4:
            score += 3.0 + len(overlap) * 0.5
        elif len(overlap) == 0 and tags_a != tags_b:
            score += 1.5  # pure novelty pair
        return score

    def find_connections(self, n: int = 3) -> List[Dict[str, Any]]:
        """Find up to n unexpected cross-sequence connections."""
        seqs = self._load_sequences(32)
        if len(seqs) < 2:
            # Bootstrap with propose if empty
            self.db.propose_unknown("serendipity bootstrap", 2)
            seqs = self._load_sequences(16)
        pairs: List[Tuple[float, Dict[str, Any]]] = []
        for i in range(len(seqs)):
            for j in range(i + 1, len(seqs)):
                ka, va, ta = seqs[i]
                kb, vb, tb = seqs[j]
                s = self._pair_score(va, vb, ta, tb)
                if s >= 2.0:
                    pairs.append((
                        s,
                        {
                            "score": round(s, 2),
                            "a_tags": ta,
                            "b_tags": tb,
                            "a_preview": str(va)[:80],
                            "b_preview": str(vb)[:80],
                        },
                    ))
        pairs.sort(key=lambda x: x[0], reverse=True)
        # Sample top-ish with slight randomness for serendipity
        top = pairs[: max(n * 3, n)]
        random.shuffle(top)
        chosen = [p[1] for p in top[:n]]
        self.connections_found += len(chosen)
        return chosen

    def amplify(self, connection: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Amplify a connection (or random spark) into a captured inspiration."""
        spark = random.choice(SPARK_WORDS)
        conn = connection or {}
        inspiration = {
            "spark": spark,
            "connection": conn,
            "insight": (
                f"Unexpected bridge via '{spark}': "
                f"{conn.get('a_tags', '?')} ↔ {conn.get('b_tags', '?')}"
            ),
            "timestamp": _utc_now(),
        }
        self.db.add_sequence(inspiration, "serendipity:amplified")
        self.db.metrics["serendipity_captures"] = (
            self.db.metrics.get("serendipity_captures", 0) + 1
        )
        self.captures += 1
        self.log.append(inspiration)
        return inspiration

    def run_cycle(self, connections: int = 3, amplifications: int = 2) -> Dict[str, Any]:
        """Find connections and amplify a subset — one serendipity cycle."""
        found = self.find_connections(n=connections)
        amplified = []
        for c in found[:amplifications]:
            amplified.append(self.amplify(c))
        if not amplified:
            amplified.append(self.amplify(None))
        self.db.persist_metrics()
        return {
            "connections": found,
            "amplified": amplified,
            "captures": self.captures,
            "connections_found": self.connections_found,
        }

    def summary_line(self) -> str:
        return (
            f"Serendipity: captures={self.captures} "
            f"connections={self.connections_found}"
        )

    def get_report(self) -> Dict[str, Any]:
        return {
            "captures": self.captures,
            "connections_found": self.connections_found,
            "log_tail": self.log[-5:],
        }


print("SerendipityEngine v0.5.4 - Cross-sequence connections + amplification ready")
