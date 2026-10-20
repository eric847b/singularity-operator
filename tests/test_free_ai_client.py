"""Minimal tests for FreeAIClient status and version parity."""
from importlib.metadata import version

from singularity_operator import __version__
from singularity_operator.free_ai_client import FreeAIClient, get_free_ai


def test_free_ai_status_reports_current_package_version():
    status = FreeAIClient().get_status()
    assert status["version"] == __version__ == version("singularity-operator")


def test_status_shape_and_helpers():
    status = get_free_ai().get_status()
    assert "available" in status
    assert isinstance(status["available"], list)
    assert isinstance(status["tally"], dict)
    assert status.get("local_first") is True
    assert "keys_present" in status
    assert isinstance(status["keys_present"], dict)
