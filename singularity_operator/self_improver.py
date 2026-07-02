#!/usr/bin/env python3
"""SelfImprover v0.1 - Autonomous self-improvement module for Singularity Operator.

v0.1.2 note: Groq integration pattern now demonstrated in EverythingDB._call_groq.
Reuse the same _call_groq helper or copy the pattern here for code improvement proposals.
"""

import os
import difflib
from typing import Dict, Any, List, Optional


class SelfImprover:
    """Autonomous code self-improver. LLM-ready (see EverythingDB for Groq example)."""

    def __init__(self, root_path: str = "."):
        self.root_path = root_path
        self.log: List[str] = []

    def read_code(self, relative_path: str) -> str:
        full_path = os.path.join(self.root_path, relative_path)
        with open(full_path, "r", encoding="utf-8") as f:
            return f.read()

    def propose_improvement(self, relative_path: str, goal: str = "make more compact, add better logging/error handling, improve metrics") -> Dict[str, Any]:
        try:
            current = self.read_code(relative_path)
        except FileNotFoundError:
            return {"error": f"File not found: {relative_path}"}

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
            "note": "LLM integration pattern available in EverythingDB._call_groq - plug Groq here for real code diffs"
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
    print("=== SelfImprover v0.1.2 Demo ===")
    improver = SelfImprover(".")
    print(improver.run_cycle())
