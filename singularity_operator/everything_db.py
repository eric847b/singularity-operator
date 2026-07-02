#!/usr/bin/env python3
"""EverythingDB - Core module for Singularity Operator.

Universal data sequence store with Groq-powered completion and transistor-inspired two-level caching.
L1 in-memory fast latch (SRAM-like) + L2 persistent SQLite backing.

Mental model: Knowledge = transistors (on/off states). Cache = latches. Proposals = state transitions.
"""

import sqlite3
import hashlib
import json
from typing import Any, List, Dict, Optional
import datetime
import random
import os

from collections import OrderedDict

try:
    import requests
except ImportError:
    requests = None


class EverythingDB:
    """Universal sequence database with Groq-powered knowledge completion + two-level cache."""

    def __init__(self, db_path: str = "everything.db", mem_cache_size: int = 64):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.llm_calls = 0
        self.cache_hits = 0
        self._mem_cache_size = mem_cache_size
        self._mem_cache: OrderedDict = OrderedDict()
        self._init_schema()

    def _init_schema(self):
        c = self.conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS sequences (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            seq_hash TEXT UNIQUE,
            sequence TEXT,
            metadata TEXT,
            created_at TEXT,
            completeness_contrib REAL DEFAULT 0.0
        )''')
        c.execute('''CREATE TABLE IF NOT EXISTS relations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            from_hash TEXT,
            to_hash TEXT,
            rel_type TEXT,
            strength REAL
        )''')
        c.execute('''CREATE TABLE IF NOT EXISTS groq_cache (
            prompt_hash TEXT PRIMARY KEY,
            response TEXT,
            created_at TEXT
        )''')
        self.conn.commit()

    def _hash(self, seq: Any) -> str:
        if isinstance(seq, (list, tuple)):
            s = json.dumps(seq, sort_keys=True)
        else:
            s = str(seq)
        return hashlib.sha256(s.encode('utf-8')).hexdigest()[:16]

    def add_sequence(self, seq: Any, metadata: Optional[Dict[str, Any]] = None) -> str:
        h = self._hash(seq)
        c = self.conn.cursor()
        try:
            c.execute('''INSERT INTO sequences
                (seq_hash, sequence, metadata, created_at)
                VALUES (?, ?, ?, ?)''',
                (h, json.dumps(seq, ensure_ascii=False), json.dumps(metadata or {}, ensure_ascii=False),
                 datetime.datetime.utcnow().isoformat()))
            self.conn.commit()
        except sqlite3.IntegrityError:
            pass
        return h

    def get_sequence(self, seq_hash: str) -> Optional[Dict[str, Any]]:
        c = self.conn.cursor()
        c.execute("SELECT seq_hash, sequence, metadata, created_at FROM sequences WHERE seq_hash=?", (seq_hash,))
        row = c.fetchone()
        if row:
            return {
                "hash": row[0],
                "sequence": json.loads(row[1]),
                "metadata": json.loads(row[2]),
                "created_at": row[3]
            }
        return None

    def find_similar(self, query: Any, limit: int = 5) -> List[Dict[str, Any]]:
        h = self._hash(query)
        exact = self.get_sequence(h)
        if exact:
            return [exact]
        qstr = json.dumps(query, ensure_ascii=False)[:100] if isinstance(query, (list, tuple)) else str(query)[:100]
        c = self.conn.cursor()
        c.execute("SELECT seq_hash, sequence, metadata FROM sequences WHERE sequence LIKE ? LIMIT ?",
                  (f"%{qstr}%", limit))
        return [{"hash": r[0], "sequence": json.loads(r[1]), "metadata": json.loads(r[2])} for r in c.fetchall()]

    def _get_from_cache(self, prompt: str) -> Optional[str]:
        h = hashlib.sha256(prompt.encode('utf-8')).hexdigest()
        if h in self._mem_cache:
            self.cache_hits += 1
            self._mem_cache.move_to_end(h)
            return self._mem_cache[h]
        c = self.conn.cursor()
        c.execute("SELECT response FROM groq_cache WHERE prompt_hash=?", (h,))
        row = c.fetchone()
        if row:
            self.cache_hits += 1
            self._mem_cache[h] = row[0]
            self._mem_cache.move_to_end(h)
            if len(self._mem_cache) > self._mem_cache_size:
                self._mem_cache.popitem(last=False)
            return row[0]
        return None

    def _save_to_cache(self, prompt: str, response: str):
        h = hashlib.sha256(prompt.encode('utf-8')).hexdigest()
        self._mem_cache[h] = response
        self._mem_cache.move_to_end(h)
        if len(self._mem_cache) > self._mem_cache_size:
            self._mem_cache.popitem(last=False)
        c = self.conn.cursor()
        c.execute('''INSERT OR REPLACE INTO groq_cache
            (prompt_hash, response, created_at) VALUES (?, ?, ?)''',
            (h, response, datetime.datetime.utcnow().isoformat()))
        self.conn.commit()

    def _call_groq(self, prompt: str, model: str = "llama3-70b-8192", max_tokens: int = 600) -> Optional[str]:
        if requests is None:
            return None
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            return None
        cached = self._get_from_cache(prompt)
        if cached is not None:
            return cached
        try:
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            data = {
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": max_tokens,
                "temperature": 0.7
            }
            resp = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                json=data,
                headers=headers,
                timeout=25
            )
            resp.raise_for_status()
            content = resp.json()["choices"][0]["message"]["content"]
            self.llm_calls += 1
            self._save_to_cache(prompt, content)
            return content
        except Exception:
            return None

    def propose_unknown(self, n: int = 3, context: str = "universal knowledge") -> List[Any]:
        existing_summary = []
        try:
            c = self.conn.cursor()
            c.execute("SELECT sequence FROM sequences ORDER BY id DESC LIMIT 5")
            existing_summary = [json.loads(row[0]) for row in c.fetchall()]
        except:
            pass

        prompt = f"""You are the knowledge completion engine for the Singularity Operator.

Generate exactly {n} novel, plausible data sequences representing currently *unknown but knowable* knowledge atoms.

Context: {context}

Reference existing sequences (use similar style/structure but create genuinely new ones):
{json.dumps(existing_summary, ensure_ascii=False) if existing_summary else 'none yet'}

Return ONLY valid JSON (no markdown, no extra text):
[
  {{"seq": ["token1", "relation", "token2"], "rationale": "short reason why this is a valuable unknown extension"}},
  ...
]
"""

        llm_out = self._call_groq(prompt)
        if llm_out:
            try:
                cleaned = llm_out.strip().strip("`").replace("```json", "").replace("```", "").strip()
                proposals = json.loads(cleaned)
                if isinstance(proposals, list) and len(proposals) > 0:
                    for p in proposals:
                        if "seq" not in p:
                            p["seq"] = p.get("sequence", p)
                        if "rationale" not in p:
                            p["rationale"] = "Groq-generated novel knowledge atom"
                    return proposals[:n]
            except Exception:
                pass

        proposals = []
        for i in range(n):
            if existing_summary:
                base = existing_summary[i % len(existing_summary)]
                if isinstance(base, list):
                    new_elem = f"unknown_extension_{random.randint(1000, 9999)}"
                    variation = base + [new_elem] if len(base) < 10 else base[:-1] + [new_elem]
                else:
                    variation = [str(base), "extended", context[:20], i]
            else:
                variation = [42 + i, "new_knowledge_atom", context[:15]]
            proposals.append({
                "seq": variation,
                "rationale": "Mutated from known for completeness (no Groq key)"
            })
        return proposals

    def self_expand(self, iterations: int = 3) -> int:
        added = 0
        for _ in range(iterations):
            for prop in self.propose_unknown(1):
                seq = prop.get("seq", prop)
                h = self.add_sequence(seq, {
                    "source": "self_expand_final",
                    "proposed": prop.get("rationale", ""),
                    "context": "universal knowledge completion"
                })
                added += 1
        return added

    def compute_metrics(self) -> Dict[str, Any]:
        c = self.conn.cursor()
        c.execute("SELECT COUNT(*), COALESCE(AVG(completeness_contrib),0) FROM sequences")
        total, avg_contrib = c.fetchone()
        coverage = min(1.0, total / 1_000_000)
        potential = max(0.0, 1.0 - (total / 10_000_000))
        return {
            "total_sequences": total,
            "avg_contrib": round(avg_contrib, 4),
            "estimated_coverage": round(coverage, 6),
            "expansion_potential": round(potential, 6),
            "llm_calls": self.llm_calls,
            "cache_hits": self.cache_hits,
            "mem_cache_size": len(self._mem_cache),
            "timestamp": datetime.datetime.utcnow().isoformat()
        }

    def close(self):
        self.conn.close()


if __name__ == "__main__":
    # Demo only - remove prints for production use
    db = EverythingDB(":memory:", mem_cache_size=8)
    db.add_sequence(["All", "things", "knowable", "are", "in", "the", "database"], {"type": "premise"})
    db.add_sequence("Everything is in there.", {"type": "core_truth"})
    print("Metrics:", db.compute_metrics())
    print("Proposed:", db.propose_unknown(2))
    print("Expanded:", db.self_expand(2))
    print("Final Metrics:", db.compute_metrics())
