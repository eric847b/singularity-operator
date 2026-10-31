"""DynamicsCore — reusable code dynamics, hard-fail resume, order variants, resource morph.

Programs are compositions of a small set of dynamics (not 50 copies of the same
pattern). On hard fail: record relative progress, read logs/messages, change
config and/or step order, retry. Cache successful compositions. Optionally
reshape resource allocation and hardware constraint profile — live, no restart.

Binary/ternary idea: each dynamic step has states inactive | active | deferred
so incomplete work and sensors can reorder without unique programs per topic.
"""

from __future__ import annotations

import hashlib
import itertools
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable, Dict, Iterable, List, Optional, Sequence, Tuple

# Ternary step state: 0 inactive, 1 active, 2 deferred (awaiting input/resource)
STATE_INACTIVE = 0
STATE_ACTIVE = 1
STATE_DEFERRED = 2


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()[:16]


@dataclass
class ProgressCheckpoint:
    """Relative progress so hard-fail can resume without restarting from zero."""

    job_id: str
    step_index: int = 0
    step_name: str = ""
    fraction: float = 0.0  # 0..1 relative progress
    payload: Any = None
    config: Dict[str, Any] = field(default_factory=dict)
    log_tail: List[str] = field(default_factory=list)
    at: str = field(default_factory=_utc_now)

    def as_dict(self) -> Dict[str, Any]:
        return {
            "job_id": self.job_id,
            "step_index": self.step_index,
            "step_name": self.step_name,
            "fraction": self.fraction,
            "config": self.config,
            "log_tail": self.log_tail[-20:],
            "at": self.at,
        }


@dataclass
class ResourceProfile:
    """Hardware/resource constraints the runtime can reshape for optimal operation."""

    max_cpu_share: float = 1.0
    max_mem_mb: Optional[int] = None
    prefer_cache: bool = True
    max_parallel: int = 1
    allow_order_permute: bool = True
    max_retries: int = 3
    notes: str = ""

    def tighten(self) -> "ResourceProfile":
        return ResourceProfile(
            max_cpu_share=max(0.1, self.max_cpu_share * 0.7),
            max_mem_mb=self.max_mem_mb,
            prefer_cache=True,
            max_parallel=max(1, self.max_parallel // 2 or 1),
            allow_order_permute=self.allow_order_permute,
            max_retries=self.max_retries + 1,
            notes="tightened_after_fail",
        )

    def as_dict(self) -> Dict[str, Any]:
        return {
            "max_cpu_share": self.max_cpu_share,
            "max_mem_mb": self.max_mem_mb,
            "prefer_cache": self.prefer_cache,
            "max_parallel": self.max_parallel,
            "allow_order_permute": self.allow_order_permute,
            "max_retries": self.max_retries,
            "notes": self.notes,
        }


@dataclass
class DynamicStep:
    """One reusable dynamic — same code pattern, any topic via args."""

    name: str
    fn: Callable[..., Any]
    state: int = STATE_ACTIVE  # inactive | active | deferred

    def run(self, *args: Any, **kwargs: Any) -> Any:
        if self.state == STATE_INACTIVE:
            return None
        if self.state == STATE_DEFERRED:
            raise RuntimeError(f"deferred:{self.name}")
        return self.fn(*args, **kwargs)


class DynamicsCache:
    """Combine and expand capabilities by caching successful compositions."""

    def __init__(self) -> None:
        self._by_key: Dict[str, Dict[str, Any]] = {}
        self.hits = 0
        self.misses = 0

    @staticmethod
    def key(names: Sequence[str], config: Optional[Dict[str, Any]] = None) -> str:
        cfg = _digest(str(sorted((config or {}).items())))
        return _digest("|".join(names) + "#" + cfg)

    def get(self, names: Sequence[str], config: Optional[Dict[str, Any]] = None) -> Optional[Any]:
        k = self.key(names, config)
        if k in self._by_key:
            self.hits += 1
            return self._by_key[k].get("result")
        self.misses += 1
        return None

    def put(
        self,
        names: Sequence[str],
        result: Any,
        config: Optional[Dict[str, Any]] = None,
        meta: Optional[Dict[str, Any]] = None,
    ) -> str:
        k = self.key(names, config)
        self._by_key[k] = {
            "result": result,
            "names": list(names),
            "config": dict(config or {}),
            "meta": dict(meta or {}),
            "at": _utc_now(),
        }
        return k

    def stats(self) -> Dict[str, Any]:
        return {"entries": len(self._by_key), "hits": self.hits, "misses": self.misses}


class DynamicsCore:
    """Orchestrates reusable dynamics with hard-fail resume and variant trials."""

    def __init__(
        self,
        resources: Optional[ResourceProfile] = None,
        log_reader: Optional[Callable[[], List[str]]] = None,
        ai_fixer: Optional[Callable[[str, str], Optional[str]]] = None,
    ) -> None:
        self.resources = resources or ResourceProfile()
        self.cache = DynamicsCache()
        self.log_reader = log_reader  # optional: return recent system messages/logs
        self.ai_fixer = ai_fixer
        self.checkpoints: Dict[str, ProgressCheckpoint] = {}
        self.library: Dict[str, DynamicStep] = {}
        self.metrics = {
            "runs": 0,
            "hard_fails": 0,
            "resumes": 0,
            "order_trials": 0,
            "config_trials": 0,
            "cache_hits": 0,
            "ai_fix_attempts": 0,
        }

    def register(self, name: str, fn: Callable[..., Any], state: int = STATE_ACTIVE) -> None:
        self.library[name] = DynamicStep(name=name, fn=fn, state=state)

    def set_state(self, name: str, state: int) -> None:
        if name in self.library:
            self.library[name].state = state

    def _append_logs(self, cp: ProgressCheckpoint, extra: str = "") -> None:
        lines: List[str] = []
        if self.log_reader:
            try:
                lines = list(self.log_reader() or [])[-30:]
            except Exception as exc:
                lines = [f"log_reader_error:{exc}"]
        if extra:
            lines.append(extra)
        cp.log_tail = (cp.log_tail + lines)[-40:]

    def checkpoint(
        self,
        job_id: str,
        step_index: int,
        step_name: str,
        fraction: float,
        payload: Any = None,
        config: Optional[Dict[str, Any]] = None,
    ) -> ProgressCheckpoint:
        cp = ProgressCheckpoint(
            job_id=job_id,
            step_index=step_index,
            step_name=step_name,
            fraction=max(0.0, min(1.0, fraction)),
            payload=payload,
            config=dict(config or {}),
        )
        self._append_logs(cp)
        self.checkpoints[job_id] = cp
        return cp

    def get_checkpoint(self, job_id: str) -> Optional[ProgressCheckpoint]:
        return self.checkpoints.get(job_id)

    def _order_variants(self, names: Sequence[str]) -> List[Tuple[str, ...]]:
        base = tuple(names)
        if not self.resources.allow_order_permute or len(names) <= 1:
            return [base]
        # Cap permutations: first order + a few rotations/swaps (not full n!)
        variants: List[Tuple[str, ...]] = [base]
        n = len(names)
        for i in range(1, min(n, 4)):
            rot = tuple(names[i:] + names[:i])
            if rot not in variants:
                variants.append(rot)
        if n >= 2:
            swapped = list(names)
            swapped[0], swapped[1] = swapped[1], swapped[0]
            t = tuple(swapped)
            if t not in variants:
                variants.append(t)
        return variants

    def run_composition(
        self,
        job_id: str,
        step_names: Sequence[str],
        *args: Any,
        config: Optional[Dict[str, Any]] = None,
        resume: bool = True,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Run named dynamics as one composition; on hard fail resume + try variants."""
        self.metrics["runs"] += 1
        cfg = dict(config or {})
        names = list(step_names)

        if self.resources.prefer_cache:
            cached = self.cache.get(names, cfg)
            if cached is not None:
                self.metrics["cache_hits"] += 1
                return {"ok": True, "result": cached, "from_cache": True, "job_id": job_id}

        start_idx = 0
        payload = None
        if resume and job_id in self.checkpoints:
            cp = self.checkpoints[job_id]
            start_idx = cp.step_index
            payload = cp.payload
            cfg = {**cp.config, **cfg}
            self.metrics["resumes"] += 1

        last_error: Optional[str] = None
        attempts = 0
        order_list = self._order_variants(names)

        while attempts < self.resources.max_retries:
            attempts += 1
            order = order_list[min(attempts - 1, len(order_list) - 1)]
            if attempts > 1:
                self.metrics["order_trials"] += 1
                # Morph resources slightly under pressure
                self.resources = self.resources.tighten()
                self.metrics["config_trials"] += 1
                cfg["attempt"] = attempts
                cfg["resources"] = self.resources.as_dict()

            try:
                result = payload
                n_steps = max(1, len(order))
                for i, name in enumerate(order):
                    if i < start_idx and attempts == 1:
                        continue
                    step = self.library.get(name)
                    if step is None:
                        raise KeyError(f"unknown_dynamic:{name}")
                    result = step.run(*(args if result is None else (result,)), **kwargs)
                    frac = (i + 1) / n_steps
                    self.checkpoint(job_id, i + 1, name, frac, payload=result, config=cfg)

                self.cache.put(order, result, cfg, meta={"job_id": job_id})
                # Clear hard-fail progress on full success
                if job_id in self.checkpoints and self.checkpoints[job_id].fraction >= 1.0:
                    pass  # keep last successful checkpoint for audit
                return {
                    "ok": True,
                    "result": result,
                    "order": list(order),
                    "attempts": attempts,
                    "job_id": job_id,
                    "from_cache": False,
                    "resources": self.resources.as_dict(),
                }
            except Exception as exc:
                self.metrics["hard_fails"] += 1
                last_error = f"{type(exc).__name__}: {exc}"
                cp = self.checkpoints.get(job_id) or ProgressCheckpoint(job_id=job_id)
                self._append_logs(cp, extra=last_error)
                self.checkpoints[job_id] = cp

                if self.ai_fixer:
                    self.metrics["ai_fix_attempts"] += 1
                    try:
                        self.ai_fixer(
                            f"dynamics:{job_id}:{'|'.join(order)}",
                            last_error + "\n" + "\n".join(cp.log_tail[-10:]),
                        )
                    except Exception:
                        pass

                # Next loop: different order / tightened resources
                start_idx = cp.step_index  # resume relative progress

        return {
            "ok": False,
            "error": last_error,
            "attempts": attempts,
            "job_id": job_id,
            "checkpoint": self.checkpoints.get(job_id, ProgressCheckpoint(job_id=job_id)).as_dict(),
            "resources": self.resources.as_dict(),
            "cache": self.cache.stats(),
        }

    def summary_line(self) -> str:
        c = self.cache.stats()
        return (
            f"dynamics runs={self.metrics['runs']} hard_fails={self.metrics['hard_fails']} "
            f"resumes={self.metrics['resumes']} order_trials={self.metrics['order_trials']} "
            f"cache={c['hits']}/{c['entries']}"
        )
