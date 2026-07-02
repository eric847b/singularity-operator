"""Singularity Operator v0.1.3 - Self-improving AI with Groq + FS cache for EverythingDB."""

__version__ = "0.1.3"
__author__ = "Eric (Mufnluvn) + Grok xAI"

from .everything_db import EverythingDB
from .self_improver import SelfImprover

__all__ = ["EverythingDB", "SelfImprover"]
