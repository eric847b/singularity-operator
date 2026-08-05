#!/usr/bin/env python3
"""Minimal entrypoint to run FailureSolver in singularity-operator / any repo."""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from failure_solver import get_failure_solver

def main():
    repo = os.getenv("GITHUB_REPOSITORY", "eric847b/singularity-operator")
    profile = {}
    def record(e, c=""):
        print(f"[ERROR:{c}] {e}")
    solver = get_failure_solver(repo, profile=profile, record_error=record)
    result = solver.run_proactive_pass(max_issues=3)
    print(result)
    print("Profile deltas:", {k: profile.get(k) for k in ("failures_triaged", "failure_solver_runs", "issues_created")})

if __name__ == "__main__":
    main()
