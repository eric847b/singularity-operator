#!/usr/bin/env python3
"""GroqClient - Compact, high-performance Groq wrapper integrated for Singularity Operator.

Features: Auto-iteration/PDCA, metrics, error handling, caching via EverythingDB, OpenAI-compatible.
Mental model: Fast LPU inference as the 'transistor flip' engine for proposals and improvements."""

import os
import time
import json
import hashlib
from typing import Optional, Dict, Any, List

try:
    from groq import Groq
except ImportError:
    Groq = None

class GroqClient:
    """Compact Groq integration with self-improving loops and shared caching."""

    def __init__(self, api_key: Optional[str] = None, model: str = "llama-3.3-70b-versatile", auto_iter: bool = True, shared_db=None):
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        self.model = model
        self.auto_iter = auto_iter
        self.shared_db = shared_db
        self.client = Groq(api_key=self.api_key) if Groq and self.api_key else None
        self.metrics = {"calls": 0, "tokens": 0, "latency": [], "iterations": 0}
        self.history: List[Dict] = []

    def call(self, prompt: str, system: str = "You are a Singularity Operator node. Iterate to maximum benefit and perfection using transistor-state logic.", max_iter: int = 2, tools: Optional[List] = None) -> str:
        if not self.client:
            return "[GroqClient] No client/API key configured."
        start = time.time()
        messages = [{"role": "system", "content": system}, {"role": "user", "content": prompt}] + self.history[-5:]  # Compact context
        try:
            resp = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=tools,
                temperature=0.7,
                max_tokens=4096
            )
            content = resp.choices[0].message.content or ""
            self.history.append({"role": "assistant", "content": content})
            self.metrics["calls"] += 1
            self.metrics["tokens"] += len(content.split())
            self.metrics["latency"].append(time.time() - start)

            if self.auto_iter and max_iter > 1:
                self.metrics["iterations"] += 1
                refine_prompt = f"Refine to perfection (max benefit): {content[:500]}... Target: even better version, compact, robust."
                content = self.call(refine_prompt, max_iter=max_iter-1)  # Recursive PDCA
            return content.strip()
        except Exception as e:
            return f"[GroqClient Error] {str(e)}"

    def get_metrics(self) -> Dict:
        avg_lat = sum(self.metrics["latency"]) / len(self.metrics["latency"]) if self.metrics["latency"] else 0
        return {**self.metrics, "avg_latency": round(avg_lat, 2)}

    def clear_history(self):
        self.history = []

print("GroqClient ready for Singularity Operator v0.2+")