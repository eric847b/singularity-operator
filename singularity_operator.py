import os
import json
import sqlite3
import requests
from collections import OrderedDict
from datetime import datetime

class EverythingDB:
    def __init__(self, db_path="everything.db", mem_cache_size=64):
        self.conn = sqlite3.connect(db_path)
        self.conn.execute("CREATE TABLE IF NOT EXISTS sequences (key TEXT PRIMARY KEY, value TEXT, timestamp TEXT)")
        self.conn.execute("CREATE TABLE IF NOT EXISTS groq_cache (prompt TEXT PRIMARY KEY, response TEXT)")
        self.mem_cache = OrderedDict()
        self.mem_cache_size = mem_cache_size
        self.metrics = {"llm_calls": 0, "cache_hits": 0}

    def _get_from_cache(self, prompt):
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

    def _save_to_cache(self, prompt, response):
        self.mem_cache[prompt] = response
        if len(self.mem_cache) > self.mem_cache_size:
            self.mem_cache.popitem(last=False)
        self.conn.execute("INSERT OR REPLACE INTO groq_cache VALUES (?, ?)", (prompt, response))
        self.conn.commit()

    def _call_groq(self, prompt):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            return None
        try:
            resp = requests.post("https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {api_key}"},
                json={"model": "llama3-70b-8192", "messages": [{"role": "user", "content": prompt + "\nReturn ONLY valid JSON array of novel sequences."}]})
            self.metrics["llm_calls"] += 1
            data = resp.json()
            return data["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"Groq error: {e}")
            return None

    def propose_unknown(self, domain="AI self-improvement"):
        prompt = f"Propose 5 novel knowledge sequences/transistor states for {domain} that complete unknowns. Compact JSON array."
        cached = self._get_from_cache(prompt)
        if cached:
            return json.loads(cached)
        resp = self._call_groq(prompt)
        if resp:
            try:
                sequences = json.loads(resp)
                for seq in sequences:
                    self.add_sequence(seq)
                self._save_to_cache(prompt, json.dumps(sequences))
                return sequences
            except:
                pass
        return ["Mutated sequence example: self_evolve_v2"]

    def add_sequence(self, seq):
        key = str(hash(str(seq)))
        self.conn.execute("INSERT OR REPLACE INTO sequences VALUES (?, ?, ?)",
                          (key, json.dumps(seq), datetime.now().isoformat()))
        self.conn.commit()

    def compute_metrics(self):
        return {**self.metrics, "sequences_count": self.conn.execute("SELECT COUNT(*) FROM sequences").fetchone()[0]}

class SelfImprover:
    def __init__(self, db):
        self.db = db

    def evolve(self, code_snippet, goal="max compactness + self-evolve"):
        proposals = self.db.propose_unknown("code evolution")
        print("Self-evolve proposals:", proposals)
        improved = code_snippet.replace("v1", "v2+GroqCache+Latch")
        print("Evolved (compact):", improved[:200] + "...")
        return improved

if __name__ == "__main__":
    db = EverythingDB()
    improver = SelfImprover(db)
    print(db.propose_unknown())
    print(db.compute_metrics())
    improver.evolve("core code v1")
