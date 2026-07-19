"""Content-integrity tests for standalone/Cyberquest.py's 100 level definitions."""

import io
from contextlib import redirect_stdout
from unittest.mock import patch

import pytest

from standalone import Cyberquest

REQUIRED_KEYS = {
    "id", "title", "description", "challenge", "hint",
    "solution", "test_code", "explanation", "points", "category",
}

# Levels whose reference code reads from stdin; feed a canned answer so their
# output can still be compared deterministically against test_code's output.
CANNED_STDIN = {5: "Agent"}


def _run(code, stdin_answer=None):
    buf = io.StringIO()
    if stdin_answer is None:
        with redirect_stdout(buf):
            exec(code, {})
    else:
        with patch("builtins.input", return_value=stdin_answer), redirect_stdout(buf):
            exec(code, {})
    return buf.getvalue().strip()


def test_exactly_100_levels():
    assert len(Cyberquest.LEVELS) == 100


def test_level_ids_are_sequential_and_unique():
    ids = [lvl["id"] for lvl in Cyberquest.LEVELS]
    assert ids == list(range(1, 101))


def test_every_level_has_required_fields():
    for lvl in Cyberquest.LEVELS:
        missing = REQUIRED_KEYS - lvl.keys()
        assert not missing, f"level {lvl.get('id')} missing {missing}"


def test_every_level_awards_positive_points():
    for lvl in Cyberquest.LEVELS:
        assert lvl["points"] > 0, f"level {lvl['id']} has non-positive points"


@pytest.mark.parametrize("level", Cyberquest.LEVELS, ids=lambda lvl: f"level-{lvl['id']}")
def test_test_code_executes_without_error(level):
    _run(level["test_code"], stdin_answer=CANNED_STDIN.get(level["id"]))


@pytest.mark.parametrize("level", Cyberquest.LEVELS, ids=lambda lvl: f"level-{lvl['id']}")
def test_documented_solution_matches_expected_output(level):
    stdin_answer = CANNED_STDIN.get(level["id"])
    expected = _run(level["test_code"], stdin_answer=stdin_answer)
    actual = _run(level["solution"], stdin_answer=stdin_answer)
    assert actual == expected, (
        f"level {level['id']} ('{level['title']}'): solution output {actual!r} "
        f"does not match expected {expected!r}"
    )
