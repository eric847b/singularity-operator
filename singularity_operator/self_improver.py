#!/usr/bin/env python3
"""SelfImprover - Autonomous self-improvement module for Singularity Operator.

Full autonomous mode: Groq-powered, cached, self-discovering, self-improving, self-monitoring with PDCA.
Can run independently (needs no one). Shares cache with EverythingDB when provided.

Mental model: Self-improver = reconfigurable logic array that flips and rewires transistors (code atoms) in the codebase autonomously.

v0.4.0: Real targeted code edits (parseable OLD->NEW markers), PDCA syntax verification + auto-rollback on failure, improvements_made tracking, health-aware discovery, health logging in autonomous_loop, adaptive expansion, and now uses overall_health_score for smarter balancing between code improvement and knowledge expansion. Zero-cost upgrade to actual self-coding capability with observability.
"""

import os
import difflib
import threading
import time
from typing import Dict, Any, List, Optional
import datetime
import ast  # for safe syntax validation

try:
    import requests
except ImportError:
    requests = None


class SelfImprover:
    """Autonomous code self-improver with Groq + shared caching + self-discovery + PDCA safety."""

    def __init__(self, root_path: str = ".", shared_db=None):
        self.root_path = root_path
        self.log: List[str] = []
        self.cache_hits = 0
        self.improvements_made = 0
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

    def propose_improvement(self, relative_path: str, goal: str = "make more compact, add better logging/error handling, improve metrics, add PDCA verification") -> Dict[str, Any]:
        try:
            current = self.read_code(relative_path)
        except FileNotFoundError:
            return {"error": f"File not found: {relative_path}"}

        llm_prompt = f"""You are an expert Python developer specializing in self-improving AI systems (Singularity Operator).

Goal: {goal}

Current code (keep changes minimal, focused, compact):
```python
{current[:3000]}  # truncated for context
```

Return ONLY a concise suggestion. If suggesting code change, use this exact parseable format for safe apply:
SUGGESTION: <one line summary>
>>>OLD:
<exact old snippet to replace, 1-5 lines>
>>>NEW:
<new improved snippet>
>>>END

Otherwise just give the suggestion text."""

        llm_out = self._call_groq(llm_prompt)
        if llm_out:
            return {
                "path": relative_path,
                "goal": goal,
                "suggestion": llm_out.strip()[:800],
                "raw": llm_out,
                "note": "Groq-powered + cached + structured edit ready"
            }

        # Fallback: simple improvement comment (preserves old behavior)
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
            "note": "Fallback (no Groq)"
        }

    def apply_improvement(self, improvement: Dict[str, Any], backup: bool = True) -> bool:
        """Applies improvement. Supports structured >>>OLD / >>>NEW edits for real code changes. Always runs PDCA Check (compile) + Act (rollback on fail). Zero bloat, maximum safety for autonomous self-evolution."""
        if "error" in improvement:
            self.log.append(improvement["error"])
            return False
        path = improvement["path"]
        full_path = os.path.join(self.root_path, path)
        try:
            original = self.read_code(path)
            if backup:
                with open(full_path + ".bak", "w", encoding="utf-8") as f:
                    f.write(original)

            applied = False
            suggestion_text = improvement.get("suggestion", "")
            raw = improvement.get("raw", suggestion_text)

            # Try structured edit if markers present
            if ">>>OLD:" in raw and ">>>NEW:" in raw:
                try:
                    old_part = raw.split(">>>OLD:")[1].split(">>>NEW:")[0].strip()
                    new_part = raw.split(">>>NEW:")[1].split(">>>END")[0].strip() if ">>>END" in raw else raw.split(">>>NEW:")[1].strip()
                    if old_part and new_part and old_part in original:
                        new_code = original.replace(old_part, new_part, 1)
                        with open(full_path, "w", encoding="utf-8") as f:
                            f.write(new_code)
                        applied = True
                        self.log.append(f"Real edit applied to {path} via structured markers")
                except Exception as parse_e:
                    self.log.append(f"Parse edit failed: {parse_e}")

            if not applied:
                # Fallback: append comment (safe, non-breaking)
                with open(full_path, "a", encoding="utf-8") as f:
                    f.write(f"\n\n# [SelfImprover v0.4.0] {suggestion_text[:200]}\n")
                applied = True
                self.log.append(f"Comment appended to {path}")

            if applied:
                # PDCA Check phase: syntax validation
                try:
                    with open(full_path, "r", encoding="utf-8") as f:
                        new_content = f.read()
                    ast.parse(new_content)  # raises SyntaxError if bad
                    self.improvements_made += 1
                    self.log.append(f"PDCA Check PASSED for {path}")
                    return True
                except SyntaxError as se:
                    # Act: rollback
                    if backup and os.path.exists(full_path + ".bak"):
                        with open(full_path, "w", encoding="utf-8") as f:
                            f.write(original)
                    self.log.append(f"PDCA Check FAILED (SyntaxError) - ROLLED BACK {path}: {se}")
                    return False
            return applied
        except Exception as e:
            self.log.append(str(e))
            return False

    def self_discover(self) -> Dict[str, Any]:
        """Autonomous discovery: Analyzes state and proposes next high-ROI improvement or sequence. Now factors in health snapshot from shared_db when available for smarter decisions."""
        health = None
        if self._shared_db and hasattr(self._shared_db, 'get_health_snapshot'):
            try:
                health = self._shared_db.get_health_snapshot()
            except:
                pass

        if health and health.get('status') == 'needs_expansion':
            return {
                "type": "sequence_proposal",
                "context": "knowledge base needs expansion per health snapshot",
                "n": 5
            }
        if len(self.log) > 5 or self.improvements_made > 2:
            return {
                "type": "code_improvement",
                "target": "singularity_operator/self_improver.py",
                "goal": "Further enhance autonomous monitoring, PDCA robustness, and integration with health snapshots"
            }
        return {
            "type": "sequence_proposal",
                "context": "universal knowledge gaps in current self-improvement state",
                "n": 3
            }

    def autonomous_loop(self, interval: int = 300, max_cycles: int = None):
        self._running = True
        cycle = 0
        while self._running:
            if max_cycles and cycle >= max_cycles:
                break
            try:
                health = None
                if self._shared_db and hasattr(self._shared_db, 'get_health_snapshot'):
                    try:
                        health = self._shared_db.get_health_snapshot()
                        score = health.get('overall_health_score', 50)
                        self.log.append(f"Cycle {cycle} health: {health.get('status')} | score: {score} | sequences: {health['metrics']['total_sequences']} | potential: {health['metrics']['expansion_potential']}")

                        # Adaptive behavior based on overall_health_score
                        if score < 40 and hasattr(self._shared_db, 'self_expand'):
                            try:
                                added = self._shared_db.self_expand(3)  # more aggressive expansion if health low
                                self.log.append(f"Adaptive: low health score ({score}), triggered aggressive self_expand, added {added} sequences")
                            except:
                                pass
                        elif score > 70:
                            # If healthy, focus more on code improvements
                            self.log.append("Adaptive: high health score, prioritizing code improvements")
                    except:
                        pass

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
        if self._thread and self._thread.is_alive():
            return "Already running"
        self._thread = threading.Thread(target=self.autonomous_loop, args=(interval,), daemon=True)
        self._thread.start()
        return "Autonomous mode started (needs no one) - v0.4.0 PDCA + health logging + score-based adaptive expansion"

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
            results.append({"file": f, "applied": applied, "suggestion": imp.get("suggestion", ""), "improvements_made": self.improvements_made, "log_entry": self.log[-1] if self.log else ""})
        return results


if __name__ == "__main__":
    improver = SelfImprover(".")
    print("SelfImprover v0.4.0 PDCA demo starting...")
    # Demo a single improvement cycle on itself (safe)
    res = improver.run_cycle(["singularity_operator/self_improver.py"])
    print("Cycle result:", res)
    print("Improvements made:", improver.improvements_made)
    print("Log sample:", improver.log[-3:] if improver.log else "None")
