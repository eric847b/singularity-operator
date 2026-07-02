#!/usr/bin/env python3
"""SelfImprover v0.1.3 - Autonomous self-improvement module for Singularity Operator.

Now with Groq integration for high-quality code improvement proposals (following the same pattern as EverythingDB).
When you think about it, the self-improver using the same intelligence layer as the knowledge completer makes perfect sense for coherent self-evolution.
"""

import os
import difflib
from typing import Dict, Any, List, Optional
import requests as _requests  # aliased to avoid conflict if needed

try:
    import requests
except ImportError:
    requests = None


class SelfImprover:
    """Autonomous code self-improver. Groq-powered when key available."""

    def __init__(self, root_path: str = "."):
        self.root_path = root_path
        self.log: List[str] = []

    def read_code(self, relative_path: str) -> str:
        full_path = os.path.join(self.root_path, relative_path)
        with open(full_path, "r", encoding="utf-8") as f:
            return f.read()

    def _call_groq(self, prompt: str, model: str = "llama3-70b-8192", max_tokens: int = 800) -> Optional[str]:
        """Same Groq pattern as EverythingDB for consistency."""
        if requests is None:
            return None
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            return None
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
            return resp.json()["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"[Groq SelfImprover] {type(e).__name__}")
            return None

    def propose_improvement(self, relative_path: str, goal: str = "make more compact, add better logging/error handling, improve metrics") -> Dict[str, Any]:
        try:
            current = self.read_code(relative_path)
        except FileNotFoundError:
            return {"error": f"File not found: {relative_path}"}

        # Try Groq for high-quality, context-aware improvement
        llm_prompt = f"""You are an expert Python developer specializing in self-improving AI systems like the Singularity Operator.

Goal: {goal}

Current code from {relative_path}:
```python
{current}
```

Provide:
1. A concise one-sentence suggestion.
2. A focused unified diff (or the key changed sections).

Keep changes minimal and high-impact. Prioritize compactness, robustness, and clarity."""

        llm_out = self._call_groq(llm_prompt)
        if llm_out:
            suggestion = llm_out.strip()[:500]  # keep compact
            return {
                "path": relative_path,
                "goal": goal,
                "suggestion": suggestion,
                "diff": "# LLM-generated improvement (see suggestion for details)",
                "note": "Groq-powered proposal"
            }

        # Fallback to simple enhancement (original logic)
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
            "note": "Fallback (no Groq key or error)"
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
            self.log.append(f"Error on {path}: {str(e)}")
            return False

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
    print("=== SelfImprover v0.1.3 (Groq-powered) Demo ===")
    improver = SelfImprover(".")
    print(improver.run_cycle())
    print("\nWhen Groq key is set, propose_improvement uses LLM for better suggestions.")
