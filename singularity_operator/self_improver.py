#!/usr/bin/env python3
"""SelfImprover - Autonomous self-improvement module for Singularity Operator.

Full autonomous mode: Groq-powered, cached, self-discovering, self-improving, self-monitoring.
Can run independently (needs no one). Shares cache with EverythingDB when provided.

Mental model: Self-improver = reconfigurable logic that flips transistors in the codebase autonomously.
"""

import os
import difflib
import threading
import time
from typing import Dict, Any, List, Optional
import datetime

try:
    import requests
except ImportError:
    requests = None


class SelfImprover:
    """Autonomous code self-improver with Groq + shared caching + self-discovery."""

    def __init__(self, root_path: str = ".", shared_db=None):
        self.root_path = root_path
        self.log: List[str] = []
        self.cache_hits = 0
        self._shared_db = shared_db
        self._running = False
        self._thread = None

    def read_code(self, relative_path: str) -> str:
        full_path = os.path.join(self.root_path, relative_path)
        with open(full_path, "r", encoding="utf-8") as f:
            return f.read()

    def _get_from_cache(self, prompt: str) -> Optional[str]:
        if self._shared_db and hasattr(self._shared_db, '_get_from_cache'):
            return self._shared_db._get_from_cache(prompt)
        if not hasattr(self, '_mem_cache'):
            self._mem_cache = {}
        h = str(hash(prompt))
        if h in self._mem_cache:
            self.cache_hits += 1
            return self._mem_cache[h]
        return None

    def _save_to_cache(self, prompt: str, response: str):
        if self._shared_db and hasattr(self._shared_db, '_save_to_cache'):
            self._shared_db._save_to_cache(prompt, response)
            return
        if not hasattr(self, '_mem_cache'):
            self._mem_cache = {}
        h = str(hash(prompt))
        self._mem_cache[h] = response

    def _call_groq(self, prompt: str, model: str = "llama3-70b-8192", max_tokens: int = 800) -> Optional[str]:
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
                "temperature": 0.6
            }
            resp = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                json=data,
                headers=headers,
                timeout=30
            )
            resp.raise_for_status()
            content = resp.json()["choices"][0]["message"]["content"]
            self._save_to_cache(prompt, content)
            return content
        except Exception:
            return None

    def propose_improvement(self, relative_path: str, goal: str = "make more compact, add better logging/error handling, improve metrics") -> Dict[str, Any]:
        try:
            current = self.read_code(relative_path)
        except FileNotFoundError:
            return {"error": f"File not found: {relative_path}"}

        llm_prompt = f"""You are an expert Python developer for self-improving AI systems.

Goal: {goal}

Current code:
```python
{current}
```

Provide a concise suggestion and focused changes."""

        llm_out = self._call_groq(llm_prompt)
        if llm_out:
            return {
                "path": relative_path,
                "goal": goal,
                "suggestion": llm_out.strip()[:600],
                "diff": "# LLM + cached improvement",
                "note": "Groq-powered + cached"
            }

        suggestion = f"Add more self-documentation, metrics, and robustness for goal: {goal}"
        improved_lines = current.splitlines(keepends=True) + [f"# Self-improver applied: {suggestion}\n"]
        diff = difflib.unified_diff(
            current.splitlines(keepends=True),
            improved_lines,
            fromfile=relative_path,
            tofile=relative_path + " (improved)"
        )
        return {
            "path": relative_path,
            "goal": goal,
            "suggestion": suggestion,
            "diff": "".join(diff),
            "note": "Fallback"
        }

    def apply_improvement(self, improvement: Dict[str, Any], backup: bool = True) -> bool:
        if "error" in improvement:
            self.log.append(improvement["error"])
            return False
        path = improvement["path"]
        full_path = os.path.join(self.root_path, path)
        try:
            if backup:
                with open(full_path + ".bak", "w", encoding="utf-8") as f:
                    f.write(self.read_code(path))
            with open(full_path, "a", encoding="utf-8") as f:
                f.write(f"\n\n# [SelfImprover] {improvement.get('suggestion', 'Improvement applied')}\n")
            self.log.append(f"Applied to {path}")
            return True
        except Exception as e:
            self.log.append(str(e))
            return False

    def self_discover(self) -> Dict[str, Any]:
        """Autonomous discovery: Analyzes current state and proposes the next high-ROI improvement or sequence."""
        # Simple discovery based on log and metrics
        if len(self.log) > 5:
            return {
                "type": "code_improvement",
                "target": "self_improver.py",
                "goal": "Add more autonomous monitoring and self-optimization"
            }
        return {
            "type": "sequence_proposal",
            "context": "universal knowledge gaps in current state",
            "n": 3
        }

    def autonomous_loop(self, interval: int = 300, max_cycles: int = None):
        """Run autonomous self-improvement and discovery loop. Can be started in background."""
        self._running = True
        cycle = 0
        while self._running:
            if max_cycles and cycle >= max_cycles:
                break
            try:
                discovery = self.self_discover()
                if discovery["type"] == "code_improvement":
                    imp = self.propose_improvement(discovery.get("target", "singularity_operator/self_improver.py"), discovery.get("goal", ""))
                    if "error" not in imp:
                        self.apply_improvement(imp)
                self.log.append(f"Autonomous cycle {cycle} completed at {datetime.datetime.utcnow()}")
            except Exception as e:
                self.log.append(f"Autonomous error: {str(e)}")
            cycle += 1
            time.sleep(interval)

    def start_autonomous(self, interval: int = 300):
        """Start the autonomous loop in a background thread (needs no one)."""
        if self._thread and self._thread.is_alive():
            return "Already running"
        self._thread = threading.Thread(target=self.autonomous_loop, args=(interval,), daemon=True)
        self._thread.start()
        return "Autonomous mode started (needs no one)"

    def stop_autonomous(self):
        self._running = False
        return "Autonomous mode stopped"

    def run_cycle(self, target_files: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        if target_files is None:
            target_files = ["singularity_operator/everything_db.py"]
        results = []
        for f in target_files:
            imp = self.propose_improvement(f)
            applied = self.apply_improvement(imp)
            results.append({"file": f, "applied": applied, "suggestion": imp.get("suggestion", ""), "log_entry": self.log[-1] if self.log else ""})
        return results


if __name__ == "__main__":
    improver = SelfImprover(".")
    print("Starting autonomous mode...")
    print(improver.start_autonomous(interval=60))  # Short interval for demo
    time.sleep(5)
    print("Stopping...")
    print(improver.stop_autonomous())
    print("Log:", improver.log[-5:] if improver.log else "No logs yet")
