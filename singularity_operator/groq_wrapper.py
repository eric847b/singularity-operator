#!/usr/bin/env python3
"""GroqWrapper - Compact, high-performance Groq API client integrated for Singularity Operator.

From initial catalyst: self-iterating, PDCA, metrics, error handling, auto-state save. Optimized for EverythingDB + Orchestrator."""

import os
import json
import time
import logging
from typing import Optional, Dict, Any

try:
    from groq import Groq
except ImportError:
    Groq = None

logging.basicConfig(level=logging.INFO)

class GroqWrapper:
    """Compact Groq client with built-in iteration, metrics, state persistence."""

    def __init__(self, api_key: Optional[str] = None, model: str = "llama-3.3-70b-versatile", auto_iter: bool = True):
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        self.model = model
        self.auto_iter = auto_iter
        self.client = Groq(api_key=self.api_key) if Groq and self.api_key else None
        self.history: list = []
        self.metrics: Dict[str, Any] = {"calls": 0, "tokens": 0, "latency": [], "errors": 0}

    def call(self, prompt: str, system: str = "You are Singularity Operator node. Iterate to maximum benefit and perfection.", max_iter: int = 3, **kwargs) -> str:
        if not self.client:
            return "[GroqWrapper] No client/API key configured."
        start = time.time()
        messages = [{"role": "system", "content": system}, {"role": "user", "content": prompt}] + self.history[-4:]  # compact context
        try:
            resp = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=kwargs.get("max_tokens", 4096),
                tools=kwargs.get("tools")
            )
            content = resp.choices[0].message.content or ""
            self.history.append({"role": "assistant", "content": content})
            self.metrics["calls"] += 1
            self.metrics["tokens"] += len(content.split())
            self.metrics["latency"].append(time.time() - start)
            if self.auto_iter and max_iter > 1:
                refine_prompt = f"Refine for perfection and max benefit: {content[:500]}... Output only the improved version."
                content = self.call(refine_prompt, max_iter=max_iter-1)
            return content
        except Exception as e:
            self.metrics["errors"] += 1
            logging.error(f"Groq error: {e}")
            return f"Error: {str(e)}"

    def save_state(self, path: str = "groq_state.json"):
        with open(path, "w") as f:
            json.dump({"history": self.history[-10:], "metrics": self.metrics}, f)
        logging.info(f"GroqWrapper state saved. Avg latency: {sum(self.metrics['latency'])/max(1,len(self.metrics['latency'])):.2f}s")

    def get_metrics(self) -> Dict[str, Any]:
        return self.metrics.copy()

if __name__ == "__main__":
    gw = GroqWrapper()
    print(gw.call("Enhance Singularity Operator with browser automation and GitHub auto-PR on self-improvements."))
    gw.save_state()