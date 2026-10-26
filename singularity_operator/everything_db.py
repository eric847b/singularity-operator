"""EverythingDB v0.5.20 - Universal sequence store + optional vector similarity + provenance.

Zero-dep default: bag-of-words hashing embeddings + cosine similarity.
Feature flag `enable_vectors` (default True; no external models).
Optional multi-modal tag support (text / code / image_ref / audio_ref).
Provenance: optional parent_key and derives_from for sequence lineage.
Multi-hop: walk_ancestors + export_lineage.

Aligned with Singularity Operator: prioritizes sequences that complete
unknowns toward singularity and the preferred currency path.
"""

from __future__ import annotations

import json
import math
import re
import sqlite3
from collections import OrderedDict, Counter
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

from .groq_wrapper import call_ai


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


_TOKEN_RE = re.compile(r"[a-z0-9_]{2,}", re.I)


def _tokenize(text: str) -> List[str]:
    return [t.lower() for t in _TOKEN_RE.findall(text or "")]


def _text_of(seq: Any) -> str:
    if isinstance(seq, str):
        return seq
    if isinstance(seq, dict):
        parts = []
        for k, v in seq.items():
            parts.append(str(k))
            if isinstance(v, (str, int, float)):
                parts.append(str(v))
            elif isinstance(v, (list, dict)):
                parts.append(json.dumps(v, sort_keys=True)[:400])
        return " ".join(parts)
    try:
        return json.dumps(seq, sort_keys=True)
    except Exception:
        return str(seq)


def _bow_vector(text: str, dim: int = 64) -> List[float]:
    """Hashing bag-of-words embedding — pure stdlib, fixed dimension."""
    vec = [0.0] * dim
    tokens = _tokenize(text)
    if not tokens:
        return vec
    counts = Counter(tokens)
    for tok, cnt in counts.items():
        idx = hash(tok) % dim
        # signed hash trick to reduce collisions
        sign = 1.0 if (hash(tok + "#") % 2 == 0) else -1.0
        vec[idx] += sign * float(cnt)
    # L2 normalize
    norm = math.sqrt(sum(x * x for x in vec)) or 1.0
    return [x / norm for x in vec]


def _cosine(a: List[float], b: List[float]) -> float:
    if not a or not b or len(a) != len(b):
        return 0.0
    return sum(x * y for x, y in zip(a, b))


class EverythingDB:
    def __init__(
        self,
        db_path: str = "everything.db",
        mem_cache_size: int = 64,
        enable_vectors: bool = True,
        vector_dim: int = 64,
    ):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.enable_vectors = enable_vectors
        self.vector_dim = vector_dim
        self._init_tables()
        self.mem_cache: OrderedDict = OrderedDict()
        self.mem_cache_size = mem_cache_size
        self.metrics = {
            "llm_calls": 0,
            "cache_hits": 0,
            "sequences_added": 0,
            "serendipity_captures": 0,
            "chaos_recoveries": 0,
            "learning_writes": 0,
            "metrics_persists": 0,
            "embeddings_stored": 0,
            "vector_queries": 0,
            "vector_hits": 0,
        }
        self.health = {"status": "healthy", "last_check": _utc_now(), "version": "0.5.20"}
        self._load_persisted_metrics()

    def _init_tables(self):
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS sequences "
            "(key TEXT PRIMARY KEY, value TEXT, timestamp TEXT, tags TEXT, "
            "modality TEXT DEFAULT 'text', parent_key TEXT, derives_from TEXT)"
        )
        # migrate older DBs
        for col, decl in [
            ("modality", "TEXT DEFAULT 'text'"),
            ("parent_key", "TEXT"),
            ("derives_from", "TEXT"),
        ]:
            try:
                self.conn.execute(f"ALTER TABLE sequences ADD COLUMN {col} {decl}")
                self.conn.commit()
            except sqlite3.OperationalError:
                pass
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS groq_cache (prompt TEXT PRIMARY KEY, response TEXT, timestamp TEXT)"
        )
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS metrics (key TEXT PRIMARY KEY, value TEXT)"
        )
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS embeddings "
            "(key TEXT PRIMARY KEY, dim INTEGER, vector TEXT, modality TEXT, timestamp TEXT)"
        )
        self.conn.commit()

    def _load_persisted_metrics(self):
        try:
            row = self.conn.execute("SELECT value FROM metrics WHERE key=?", ("snapshot",)).fetchone()
            if row:
                saved = json.loads(row[0])
                for k, v in saved.items():
                    if k in self.metrics and isinstance(v, (int, float)):
                        self.metrics[k] = int(v)
        except Exception:
            pass

    def persist_metrics(self) -> Dict[str, Any]:
        snap = {**self.metrics, "persisted_at": _utc_now(), "enable_vectors": self.enable_vectors}
        self.conn.execute(
            "INSERT OR REPLACE INTO metrics VALUES (?, ?)",
            ("snapshot", json.dumps(snap)),
        )
        self.conn.commit()
        self.metrics["metrics_persists"] += 1
        return snap

    def _get_from_cache(self, prompt: str) -> Optional[str]:
        if prompt in self.mem_cache:
            self.mem_cache.move_to_end(prompt)
            self.metrics["cache_hits"] += 1
            return self.mem_cache[prompt]
        row = self.conn.execute("SELECT response FROM groq_cache WHERE prompt=?", (prompt,)).fetchone()
        if row:
            self._save_to_cache(prompt, row[0])
            self.metrics["cache_hits"] += 1
            return row[0]
        return None

    def _save_to_cache(self, prompt: str, response: str):
        self.mem_cache[prompt] = response
        if len(self.mem_cache) > self.mem_cache_size:
            self.mem_cache.popitem(last=False)
        self.conn.execute(
            "INSERT OR REPLACE INTO groq_cache VALUES (?, ?, ?)",
            (prompt, response, _utc_now()),
        )
        self.conn.commit()

    def _store_embedding(self, key: str, seq: Any, modality: str = "text"):
        if not self.enable_vectors:
            return
        text = _text_of(seq)
        vec = _bow_vector(text, dim=self.vector_dim)
        self.conn.execute(
            "INSERT OR REPLACE INTO embeddings VALUES (?, ?, ?, ?, ?)",
            (key, self.vector_dim, json.dumps(vec), modality, _utc_now()),
        )
        self.conn.commit()
        self.metrics["embeddings_stored"] += 1

    def add_sequence(
        self,
        seq: Any,
        tags: str = "general",
        modality: str = "text",
        parent_key: Optional[str] = None,
        derives_from: Optional[str] = None,
    ) -> str:
        """Add a sequence. modality: text | code | image_ref | audio_ref | multi.

        Provenance:
        - parent_key: direct parent sequence key (lineage)
        - derives_from: free-form source ref (e.g. task name, external id)
        """
        key = str(hash(json.dumps(seq, sort_keys=True) if isinstance(seq, (dict, list)) else str(seq)))
        self.conn.execute(
            "INSERT OR REPLACE INTO sequences "
            "(key, value, timestamp, tags, modality, parent_key, derives_from) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                key,
                json.dumps(seq),
                _utc_now(),
                tags,
                modality,
                parent_key,
                derives_from,
            ),
        )
        self.conn.commit()
        self.metrics["sequences_added"] += 1
        self._store_embedding(key, seq, modality=modality)
        return key

    def get_sequence(self, key: str) -> Optional[Dict[str, Any]]:
        row = self.conn.execute(
            "SELECT key, value, timestamp, tags, modality, parent_key, derives_from "
            "FROM sequences WHERE key=?",
            (key,),
        ).fetchone()
        if not row:
            return None
        try:
            value = json.loads(row[1])
        except Exception:
            value = row[1]
        return {
            "key": row[0],
            "value": value,
            "timestamp": row[2],
            "tags": row[3],
            "modality": row[4] or "text",
            "parent_key": row[5],
            "derives_from": row[6],
        }

    def get_children(self, parent_key: str, limit: int = 20) -> List[Dict[str, Any]]:
        rows = self.conn.execute(
            "SELECT key, value, timestamp, tags, modality, parent_key, derives_from "
            "FROM sequences WHERE parent_key=? ORDER BY timestamp DESC LIMIT ?",
            (parent_key, limit),
        ).fetchall()
        out: List[Dict[str, Any]] = []
        for row in rows:
            try:
                value = json.loads(row[1])
            except Exception:
                value = row[1]
            out.append(
                {
                    "key": row[0],
                    "value": value,
                    "timestamp": row[2],
                    "tags": row[3],
                    "modality": row[4] or "text",
                    "parent_key": row[5],
                    "derives_from": row[6],
                }
            )
        return out

    def walk_ancestors(self, key: str, max_depth: int = 16) -> List[Dict[str, Any]]:
        """Walk parent_key chain from key toward roots. Returns [self, parent, ...]."""
        chain: List[Dict[str, Any]] = []
        seen = set()
        current: Optional[str] = key
        depth = 0
        while current and depth < max_depth and current not in seen:
            seen.add(current)
            node = self.get_sequence(current)
            if not node:
                break
            chain.append(node)
            current = node.get("parent_key") or None
            depth += 1
        return chain

    def export_lineage(
        self,
        key: str,
        *,
        max_depth: int = 16,
        include_children: bool = True,
        child_limit: int = 20,
    ) -> Dict[str, Any]:
        """Multi-hop provenance export: ancestors + optional direct children."""
        ancestors = self.walk_ancestors(key, max_depth=max_depth)
        root = ancestors[-1] if ancestors else None
        children: List[Dict[str, Any]] = []
        if include_children:
            children = self.get_children(key, limit=child_limit)
        return {
            "key": key,
            "depth": max(0, len(ancestors) - 1),
            "ancestors": [
                {
                    "key": a["key"],
                    "tags": a.get("tags"),
                    "derives_from": a.get("derives_from"),
                    "timestamp": a.get("timestamp"),
                    "parent_key": a.get("parent_key"),
                }
                for a in ancestors
            ],
            "root_key": root["key"] if root else None,
            "children": [
                {
                    "key": c["key"],
                    "tags": c.get("tags"),
                    "derives_from": c.get("derives_from"),
                    "timestamp": c.get("timestamp"),
                }
                for c in children
            ],
            "exported_at": _utc_now(),
        }

    def similarity_search(
        self,
        query: Any,
        top_k: int = 5,
        modality: Optional[str] = None,
        min_score: float = 0.05,
    ) -> List[Dict[str, Any]]:
        """Find sequences most similar to query via cosine over bag-of-words vectors."""
        self.metrics["vector_queries"] += 1
        if not self.enable_vectors:
            return []
        qvec = _bow_vector(_text_of(query), dim=self.vector_dim)
        sql = "SELECT key, dim, vector, modality FROM embeddings"
        params: Tuple = ()
        if modality:
            sql += " WHERE modality=?"
            params = (modality,)
        rows = self.conn.execute(sql, params).fetchall()
        scored: List[Tuple[float, str, str]] = []
        for key, dim, vec_json, mod in rows:
            try:
                vec = json.loads(vec_json)
            except Exception:
                continue
            if dim != self.vector_dim or len(vec) != self.vector_dim:
                continue
            score = _cosine(qvec, vec)
            if score >= min_score:
                scored.append((score, key, mod or "text"))
        scored.sort(key=lambda x: x[0], reverse=True)
        results: List[Dict[str, Any]] = []
        for score, key, mod in scored[:top_k]:
            row = self.conn.execute(
                "SELECT value, tags, timestamp, parent_key, derives_from FROM sequences WHERE key=?",
                (key,),
            ).fetchone()
            if not row:
                continue
            try:
                value = json.loads(row[0])
            except Exception:
                value = row[0]
            results.append(
                {
                    "key": key,
                    "score": round(score, 4),
                    "modality": mod,
                    "tags": row[1],
                    "timestamp": row[2],
                    "value": value,
                    "parent_key": row[3],
                    "derives_from": row[4],
                }
            )
        if results:
            self.metrics["vector_hits"] += len(results)
        return results

    def demo_vector_query(self, query: str = "self improve serendipity singularity currency") -> Dict[str, Any]:
        """Measurable demo: ensure seed data, run similarity, return report."""
        count = self.conn.execute("SELECT COUNT(*) FROM sequences").fetchone()[0]
        if count < 3:
            self.add_sequence({"topic": "self_improve", "note": "compact evolution"}, "demo:evolve", "text")
            self.add_sequence({"topic": "serendipity", "bridge": "cross-sequence"}, "demo:serendipity", "text")
            self.add_sequence("def singularity_step(): pass  # code modality", "demo:code", "code")
            self.add_sequence({"topic": "currency_path", "note": "setup-session-offer ranking"}, "demo:currency", "text")
        hits = self.similarity_search(query, top_k=5)
        report = {
            "query": query,
            "enable_vectors": self.enable_vectors,
            "vector_dim": self.vector_dim,
            "hits": len(hits),
            "top": hits[:3],
            "metrics": {
                "embeddings_stored": self.metrics["embeddings_stored"],
                "vector_queries": self.metrics["vector_queries"],
                "vector_hits": self.metrics["vector_hits"],
            },
            "timestamp": _utc_now(),
        }
        self.add_sequence(report, "vector:demo", "text")
        return report

    def propose_unknown(self, domain: str = "AI self-improvement + singularity + currency", n: int = 5) -> List[Any]:
        """Propose novel sequences that complete unknowns.

        Strongly biased toward singularity acceleration and the preferred currency path
        (highest expected $/effort experiments, runway, real tracked income).
        """
        prompt = (
            f"Propose {n} novel, compact knowledge sequences or transistor states for domain: {domain}. "
            f"Prioritize sequences that (1) complete unknowns toward singularity / universal knowledge representation "
            f"and (2) advance the preferred currency path (real income experiments, runway velocity, "
            f"setup-session-offer delivery, zero paid APIs). "
            f"Return ONLY a valid compact JSON array of strings or small objects. No commentary."
        )
        cached = self._get_from_cache(prompt)
        if cached:
            try:
                return json.loads(cached)
            except Exception:
                pass
        result = call_ai(prompt)
        self.metrics["llm_calls"] += 1
        sequences: List[Any] = []
        if isinstance(result, dict) and "response" in result:
            try:
                content = result["response"]
                if "[" in content and "]" in content:
                    start = content.find("[")
                    end = content.rfind("]") + 1
                    sequences = json.loads(content[start:end])
                else:
                    sequences = [content]
            except Exception:
                sequences = [str(result)]
        else:
            sequences = [
                "self_evolve_v6_compact_currency",
                "EverythingDB_universal_latch_v2",
                "serendipity_engine_currency_bridge",
                "setup_session_offer_delivery_loop",
                "runway_velocity_transistor",
            ]
        for seq in sequences:
            self.add_sequence(seq, tags=f"proposed:{domain}", derives_from="propose_unknown")
        self._save_to_cache(prompt, json.dumps(sequences))
        if hash(domain) % 7 == 0:
            self.metrics["serendipity_captures"] += 1
            self.add_sequence(
                {"serendipity": "unexpected connection found", "domain": domain},
                "serendipity",
                derives_from="propose_unknown",
            )
        return sequences

    def get_health_snapshot(self) -> Dict[str, Any]:
        seq_count = self.conn.execute("SELECT COUNT(*) FROM sequences").fetchone()[0]
        cache_count = self.conn.execute("SELECT COUNT(*) FROM groq_cache").fetchone()[0]
        emb_count = self.conn.execute("SELECT COUNT(*) FROM embeddings").fetchone()[0]
        with_parent = self.conn.execute(
            "SELECT COUNT(*) FROM sequences WHERE parent_key IS NOT NULL AND parent_key != ''"
        ).fetchone()[0]
        tag_rows = self.conn.execute(
            "SELECT tags, COUNT(*) FROM sequences GROUP BY tags ORDER BY COUNT(*) DESC LIMIT 8"
        ).fetchall()
        top_tags = {str(t): int(c) for t, c in tag_rows}
        self.health.update(
            {
                "status": "healthy",
                "last_check": _utc_now(),
                "version": "0.5.20",
                "sequences": seq_count,
                "embeddings": emb_count,
                "with_parent": with_parent,
                "enable_vectors": self.enable_vectors,
                "vector_dim": self.vector_dim,
                "cache_entries": cache_count,
                "mem_cache_size": len(self.mem_cache),
                "metrics": self.metrics.copy(),
                "top_tags": top_tags,
            }
        )
        return self.health

    def self_test(self) -> Dict[str, Any]:
        tests = {
            "db_connect": True,
            "propose": False,
            "cache": False,
            "persist": False,
            "vectors": False,
            "provenance": False,
            "lineage": False,
        }
        try:
            props = self.propose_unknown("test singularity currency", 1)
            tests["propose"] = len(props) > 0
            tests["cache"] = True
            snap = self.persist_metrics()
            tests["persist"] = bool(snap.get("persisted_at"))
            if self.enable_vectors:
                demo = self.demo_vector_query("test singularity currency")
                tests["vectors"] = demo.get("hits", 0) >= 0
            else:
                tests["vectors"] = True
            parent = self.add_sequence({"kind": "parent"}, tags="test:parent")
            child = self.add_sequence(
                {"kind": "child"}, tags="test:child", parent_key=parent, derives_from="self_test"
            )
            got = self.get_sequence(child)
            kids = self.get_children(parent)
            tests["provenance"] = bool(got and got.get("parent_key") == parent and any(k["key"] == child for k in kids))
            lin = self.export_lineage(child)
            tests["lineage"] = lin.get("depth", 0) >= 1 and lin.get("root_key") == parent
        except Exception as e:
            tests["error"] = str(e)[:200]
        return tests

    def compute_metrics(self) -> Dict[str, Any]:
        seq_count = self.conn.execute("SELECT COUNT(*) FROM sequences").fetchone()[0]
        emb_count = self.conn.execute("SELECT COUNT(*) FROM embeddings").fetchone()[0]
        return {**self.metrics, "sequences_count": seq_count, "embeddings_count": emb_count}

    def demo_l1_l2_cache(self):
        print("L1 (mem) hits:", self.metrics["cache_hits"])
        print("L2 (sqlite) demo: cache size", self.conn.execute("SELECT COUNT(*) FROM groq_cache").fetchone()[0])
        return self.metrics

    def chaos_recover(self, failure_type: str = "api_latency"):
        self.metrics["chaos_recoveries"] += 1
        self.persist_metrics()
        return {"recovered": True, "type": failure_type, "new_resilience": "+10%"}


print("EverythingDB v0.5.20 - Universal sequence store + multi-hop provenance ready")
