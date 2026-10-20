from importlib.metadata import version

from singularity_operator import __version__
from singularity_operator.free_ai_client import FreeAIClient


def test_free_ai_status_reports_current_package_version():
    status = FreeAIClient().get_status()
    assert status["version"] == __version__ == version("singularity-operator")
