"""Tests for currency experiment next-action planner."""
from singularity_operator.currency_action import (
    EXPERIMENT_PLAYBOOK,
    plan_next_action,
    action_summary_line,
)


def test_plan_defaults_to_setup_session_offer():
    action = plan_next_action({})
    assert action["experiment_id"] == "setup-session-offer"
    assert action["expected_revenue"] == 149
    assert action["steps"]
    assert action["policy"]["never_mark_won_without_payment"] is True
    assert action["hub_handoff"]["canonical_entry"] == "eric847b/AI-Collaboration-Hub"


def test_plan_uses_top_experiment():
    action = plan_next_action({"top_experiment": "oss-inbound-help", "top_score": 49.5})
    assert action["experiment_id"] == "oss-inbound-help"
    assert action["expected_revenue"] == 99
    assert action["top_score"] == 49.5


def test_unknown_experiment_falls_back():
    action = plan_next_action({"top_experiment": "not-a-real-exp"})
    assert action["experiment_id"] == "setup-session-offer"


def test_summary_line():
    action = plan_next_action({"top_experiment": "template-pack-listing", "top_score": 39.5})
    line = action_summary_line(action)
    assert "template-pack-listing" in line
    assert "39.5" in line or "39.50" in line


def test_playbook_covers_live_ranked():
    for key in ("setup-session-offer", "oss-inbound-help", "template-pack-listing"):
        assert key in EXPERIMENT_PLAYBOOK
