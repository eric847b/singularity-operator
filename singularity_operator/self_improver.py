#!/usr/bin/env python3
"""SelfImprover v0.1 - Autonomous self-improvement module for Singularity Operator.

Enables the system to read its own code, propose improvements (LLM-ready), apply safely, and run cycles.
Stdlib only. Compact. Clear path to integrate free Groq/Cohere/etc for real proposals.

Core to your goals: self-improving code, PDCA, compact powerful implementations, auto-updates.

v0.1: Stub with full structure. Run demo to see cycle. Next iteration: Plug in LLM for actual diffs.
"""

import os
import difflib
from typing import Dict, Any, List, Optional


class SelfImprover:
    """Autonomous code self-improver.
    read -> propose (stub for LLM) -> apply (with backup) -> cycle.
    """

    def __init__(self, root_path: str = "."):
        self.root_path = root_path
        self.log: List[str] = []

    def read_code(self, relative_path: str) -> str:
        """Read a source file."""
        full_path = os.path.join(self.root_path, relative_path)
        with open(full_path, "r", encoding="utf-8") as f:
            return f.read()

    def propose_improvement(self, relative_path: str, goal: str = "make more compact, add better logging/error handling, improve metrics") -> Dict[str, Any]:
        """Propose improvement for a file.
        Stub: In full version, call free LLM API (e.g. Groq) with prompt like:
        f"You are an expert Python developer improving the Singularity Operator. Goal: {goal}\n\nCurrent code:\n{current_code}\n\nReturn ONLY a unified diff or the full improved code."
        Then parse the response into diff or new code.
        """
        try:
            current = self.read_code(relative_path)
        except FileNotFoundError:
            return {"error": f"File not found: {relative_path}"}

        # Stub suggestion (replace this block with real LLM call + parsing)
        suggestion = f"Add more self-documentation, metrics, and robustness for goal: {goal}"
        # Simple diff example (in real: use LLM output)
        improved_lines = current.splitlines(keepends=True) + [f"# Self-improver v0.1 applied: {suggestion}\n"]
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
            "note": "LLM integration pending - set GROQ_API_KEY and replace stub with API call for production-quality proposals"
        }

    def apply_improvement(self, improvement: Dict[str, Any], backup: bool = True) -> bool:
        """Apply the improvement safely (backup original). For stub: appends note. Real: apply patch or replace."""
        if "error" in improvement:
            self.log.append(improvement["error"])
            return False
        path = improvement["path"]
        full_path = os.path.join(self.root_path, path)
        try:
            if backup:
                backup_path = full_path + ".bak"
                with open(backup_path, "w", encoding="utf-8") as f:
                    f.write(self.read_code(path))
            # Stub apply: append note (real version would use patch or safe overwrite)
            with open(full_path, "a", encoding="utf-8") as f:
                f.write(f"\n\n# [SelfImprover v0.1] {improvement.get('suggestion', 'Improvement applied')}\n")
            self.log.append(f"Applied improvement to {path}")
            return True
        except Exception as e:
            self.log.append(f"Error applying to {path}: {str(e)}")
            return False

    def run_cycle(self, target_files: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """Run a full self-improvement cycle on target files."""
        if target_files is None:
            target_files = ["singularity_operator/everything_db.py"]
        results = []
        for f in target_files:
            imp = self.propose_improvement(f)
            applied = self.apply_improvement(imp)
            results.append({
                "file": f,
                "applied": applied,
                "suggestion": imp.get("suggestion", ""),
                "log_entry": self.log[-1] if self.log else ""
            })
        return results


if __name__ == "__main__":
    print("=== Singularity Operator - SelfImprover v0.1 Demo ===")
    improver = SelfImprover(".")
    print("SelfImprover initialized.")
    results = improver.run_cycle(["singularity_operator/everything_db.py"])
    print("Cycle results:", results)
    print("\nDemo complete. In real use: Set API key, replace stub propose with Groq call, run on push or schedule.")
    print("This module enables the operator to improve itself — key to singularity.")
