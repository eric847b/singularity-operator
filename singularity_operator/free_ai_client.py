#!/usr/bin/env python3
"""Free AI Client — zero-cost multi-provider rotator for continuous development.

Local-first (Ollama) → Pollinations no-key → free cloud tiers (Groq, OpenRouter, etc.).
Seamless failover so continuous refinement never pauses on rate limits or missing keys.
Compatible with Orchestrator, SelfImprover, EverythingDB, and autonomous agents.
"""

from __future__ import annotations

import os
import time
import json
from typing import Any, Dict, List, Optional

import requests


def _env(key: str, default: str = "") -> str:
    return (os.getenv(key) or default).strip()


class FreeAIClient:
    """Rotating free AI client. Prefer permanent-free local, then no-key cloud, then free-tier keys."""

    def __init__(self, timeout: int = 30):
        self.timeout = timeout
        self.tally = {"calls": 0, "failures": 0, "rotations": 0}
        self.cooldowns: Dict[str, float] = {}
        self.cooldown_s = 60.0

    def _providers(self) -> List[Dict[str, Any]]:
        """Ordered free pool. Local permanent-free first."""
        return [
            {
                "name": "ollama",
                "url": _env("OLLAMA_URL", "http://127.0.0.1:11434/v1/chat/completions"),
                "model": _env("OLLAMA_MODEL", "phi3:mini"),
                "headers": lambda: {"Content-Type": "application/json"},
                "key_required": False,
            },
            {
                "name": "pollinations",
                "url": _env("POLLINATIONS_URL", "https://text.pollinations.ai/openai"),
                "model": _env("POLLINATIONS_MODEL", "openai"),
                "headers": lambda: {"Content-Type": "application/json"},
                "key_required": False,
            },
            {
                "name": "groq",
                "url": "https://api.groq.com/openai/v1/chat/completions",
                "model": _env("GROQ_MODEL", "llama-3.3-70b-versatile"),
                "headers": lambda: {
                    "Authorization": f"Bearer {_env('GROQ_API_KEY')}",
                    "Content-Type": "application/json",
                },
                "key_required": True,
                "key_env": "GROQ_API_KEY",
            },
            {
                "name": "openrouter",
                "url": "https://openrouter.ai/api/v1/chat/completions",
                "model": _env("OPENROUTER_MODEL", "meta-llama/llama-3-8b:free"),
                "headers": lambda: {
                    "Authorization": f"Bearer {_env('OPENROUTER_API_KEY')}",
                    "HTTP-Referer": "https://github.com/eric847b/singularity-operator",
                    "X-Title": "SingularityOperator",
                    "Content-Type": "application/json",
                },
                "key_required": True,
                "key_env": "OPENROUTER_API_KEY",
            },
            {
                "name": "together",
                "url": "https://api.together.xyz/v1/chat/completions",
                "model": _env("TOGETHER_MODEL", "meta-llama/Meta-Llama-3.1-8b-instruct-turbo"),
                "headers": lambda: {
                    "Authorization": f"Bearer {_env('TOGETHER_API_KEY')}",
                    "Content-Type": "application/json",
                },
                "key_required": True,
                "key_env": "TOGETHER_API_KEY",
            },
        ]

    def _available(self, p: Dict[str, Any]) -> bool:
        if time.time() < self.cooldowns.get(p["name"], 0):
            return False
        if p.get("key_required") and not _env(p.get("key_env", "")):
            return False
        return True

    def complete(
        self,
        prompt: str,
        system: str = "You are a high-leverage continuous development agent. Produce maximum functional progress with free resources.",
        max_tokens: int = 1024,
        temperature: float = 0.7,
    ) -> Dict[str, Any]:
        """Call free AI with seamless rotation. Returns structured result."""
        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ]
        providers = self._providers()
        last_err = "no providers available"

        for _ in range(len(providers) * 2):
            for p in providers:
                if not self._available(p):
                    continue
                self.tally["calls"] += 1
                try:
                    payload = {
                        "model": p["model"],
                        "messages": messages,
                        "temperature": temperature,
                        "max_tokens": max_tokens,
                    }
                    resp = requests.post(
                        p["url"],
                        headers=p["headers"](),
                        json=payload,
                        timeout=self.timeout,
                    )
                    if resp.status_code >= 200 and resp.status_code < 300:
                        data = resp.json()
                        content = (
                            data.get("choices", [{}])[0]
                            .get("message", {})
                            .get("content")
                            or data.get("text")
                            or ""
                        )
                        if content.strip():
                            return {
                                "provider": p["name"],
                                "response": content.strip(),
                                "cost": 0.0,
                                "tally": dict(self.tally),
                                "raw": data,
                            }
                    # non-success → cool down and rotate
                    self.cooldowns[p["name"]] = time.time() + self.cooldown_s
                    self.tally["failures"] += 1
                    self.tally["rotations"] += 1
                    last_err = f"{p['name']} HTTP {resp.status_code}"
                except Exception as e:
                    self.cooldowns[p["name"]] = time.time() + self.cooldown_s
                    self.tally["failures"] += 1
                    self.tally["rotations"] += 1
                    last_err = f"{p['name']}: {str(e)[:120]}"
            time.sleep(0.3)

        return {
            "error": f"All free AI providers exhausted: {last_err}",
            "tally": dict(self.tally),
            "providers_tried": [p["name"] for p in providers],
        }


# Convenience singleton-style helper used by wrappers
_default_client: Optional[FreeAIClient] = None


def get_free_ai() -> FreeAIClient:
    global _default_client
    if _default_client is None:
        _default_client = FreeAIClient()
    return _default_client


def call_free_ai(prompt: str, **kwargs) -> Dict[str, Any]:
    """Drop-in free AI call for continuous development loops."""
    return get_free_ai().complete(prompt, **kwargs)


if __name__ == "__main__":
    r = call_free_ai("State in one line the highest-return free AI action for continuous software development.")
    print(json.dumps(r, indent=2))
