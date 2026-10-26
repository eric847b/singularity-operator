"""Tests for shared validation helpers."""
from singularity_operator.validation import (
    ast_equivalent,
    is_valid_python,
    validate_python_evolution,
    validate_sequence_payload,
)


def test_is_valid_python():
    assert is_valid_python("x = 1\n")
    assert not is_valid_python("def (")


def test_ast_equivalent_ignores_whitespace():
    a = "x=1"
    b = "x = 1\n"
    assert ast_equivalent(a, b)


def test_validate_rejects_empty_and_no_change():
    orig = "class A: pass\n"
    r1 = validate_python_evolution(orig, "")
    assert not r1.ok and r1.reason == "empty"
    r2 = validate_python_evolution(orig, "class A: pass\n")
    assert not r2.ok and r2.reason == "no_change"


def test_validate_accepts_real_change():
    orig = "class A: pass\n"
    cand = "class A:\n    def run(self):\n        return 1\n"
    r = validate_python_evolution(orig, cand)
    assert r.ok and r.reason == "accepted"


def test_validate_rejects_syntax_error():
    r = validate_python_evolution("x=1", "def (")
    assert not r.ok and r.reason == "syntax_error"


def test_sequence_payload():
    assert validate_sequence_payload({"a": 1}).ok
    assert validate_sequence_payload("ok").ok
    assert not validate_sequence_payload(None).ok
