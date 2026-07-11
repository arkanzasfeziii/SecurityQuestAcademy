"""Tests for the interactive play_*_level orchestration functions.

These drive the Python/Cisco/Bash gameplay loops through Prompt.ask
mocking rather than exercising the underlying execution engines again
(those are already covered in test_engine_runtime.py).
"""

import pytest

from games.base import (
    PlayerProgress,
    _level_pass,
    play_bash_level,
    play_cisco_level,
    play_python_level,
)

COLORS = {
    "primary": "cyan",
    "secondary": "blue",
    "success": "green",
    "info": "white",
    "warning": "yellow",
    "error": "red",
}


@pytest.fixture(autouse=True)
def _no_sleep(monkeypatch):
    monkeypatch.setattr("games.base.time.sleep", lambda *_: None)


def _answers(monkeypatch, *values):
    it = iter(values)
    monkeypatch.setattr("games.base.Prompt.ask", lambda *a, **kw: next(it))


def _raise_interrupt(monkeypatch):
    def _ask(*a, **kw):
        raise KeyboardInterrupt
    monkeypatch.setattr("games.base.Prompt.ask", _ask)


# ---------------------------------------------------------------------------
# play_python_level
# ---------------------------------------------------------------------------

PY_LEVEL = {
    "id": 1, "title": "Add", "category": "basics", "points": 10,
    "description": "d", "challenge": "c", "hint": "print(2+2)",
    "explanation": "e", "test_code": "print(4)",
}


def test_play_python_level_success(monkeypatch):
    _answers(monkeypatch, "print(2 + 2)", "done")
    progress = PlayerProgress()
    assert play_python_level(PY_LEVEL, progress, COLORS) is True
    assert 1 in progress.completed_levels
    assert progress.total_points == 10


def test_play_python_level_hint_then_solve(monkeypatch):
    _answers(monkeypatch, "hint", "print(2 + 2)", "done")
    progress = PlayerProgress()
    assert play_python_level(PY_LEVEL, progress, COLORS) is True


def test_play_python_level_skip(monkeypatch):
    _answers(monkeypatch, "skip")
    progress = PlayerProgress()
    assert play_python_level(PY_LEVEL, progress, COLORS) is False
    assert progress.completed_levels == []


def test_play_python_level_no_code_entered(monkeypatch):
    _answers(monkeypatch, "done")
    progress = PlayerProgress()
    assert play_python_level(PY_LEVEL, progress, COLORS) is False


def test_play_python_level_code_error(monkeypatch):
    _answers(monkeypatch, "1 / 0", "done")
    progress = PlayerProgress()
    assert play_python_level(PY_LEVEL, progress, COLORS) is False
    assert progress.completed_levels == []


def test_play_python_level_wrong_output(monkeypatch):
    _answers(monkeypatch, "print(1)", "done")
    progress = PlayerProgress()
    assert play_python_level(PY_LEVEL, progress, COLORS) is False


def test_play_python_level_interrupted(monkeypatch):
    _raise_interrupt(monkeypatch)
    progress = PlayerProgress()
    assert play_python_level(PY_LEVEL, progress, COLORS) is False


# ---------------------------------------------------------------------------
# play_cisco_level
# ---------------------------------------------------------------------------

CISCO_LEVEL = {
    "id": 2, "title": "Save config", "category": "cisco", "points": 20,
    "description": "d", "challenge": "c", "hint": "copy run start",
    "explanation": "e", "solution": "copy running-config startup-config",
    "accepted": ["copy running-config startup-config", "copy run start"],
}


def test_play_cisco_level_correct(monkeypatch):
    _answers(monkeypatch, "copy run start")
    progress = PlayerProgress()
    assert play_cisco_level(CISCO_LEVEL, progress, COLORS) is True
    assert 2 in progress.completed_levels
    assert progress.total_points == 20


def test_play_cisco_level_hint_then_correct(monkeypatch):
    _answers(monkeypatch, "hint", "copy run start")
    progress = PlayerProgress()
    assert play_cisco_level(CISCO_LEVEL, progress, COLORS) is True


def test_play_cisco_level_skip(monkeypatch):
    _answers(monkeypatch, "skip")
    progress = PlayerProgress()
    assert play_cisco_level(CISCO_LEVEL, progress, COLORS) is False


def test_play_cisco_level_wrong_command(monkeypatch):
    _answers(monkeypatch, "show version")
    progress = PlayerProgress()
    assert play_cisco_level(CISCO_LEVEL, progress, COLORS) is False
    assert progress.completed_levels == []


def test_play_cisco_level_falls_back_to_solution_when_no_accepted(monkeypatch):
    level = {k: v for k, v in CISCO_LEVEL.items() if k != "accepted"}
    _answers(monkeypatch, "copy running-config startup-config")
    progress = PlayerProgress()
    assert play_cisco_level(level, progress, COLORS) is True


def test_play_cisco_level_interrupted(monkeypatch):
    _raise_interrupt(monkeypatch)
    progress = PlayerProgress()
    assert play_cisco_level(CISCO_LEVEL, progress, COLORS) is False


# ---------------------------------------------------------------------------
# play_bash_level (execute_bash is mocked so this doesn't need a real shell)
# ---------------------------------------------------------------------------

BASH_LEVEL = {
    "id": 3, "title": "Greet", "category": "bash", "points": 15,
    "description": "d", "challenge": "c", "hint": "echo hello",
    "explanation": "e", "expected_output": "hello",
}


def test_play_bash_level_success(monkeypatch):
    _answers(monkeypatch, "echo hello")
    monkeypatch.setattr("games.base.execute_bash", lambda *a, **kw: (True, "hello"))
    progress = PlayerProgress()
    assert play_bash_level(BASH_LEVEL, progress, COLORS) is True
    assert 3 in progress.completed_levels
    assert progress.total_points == 15


def test_play_bash_level_hint_then_solve(monkeypatch):
    _answers(monkeypatch, "hint", "echo hello")
    monkeypatch.setattr("games.base.execute_bash", lambda *a, **kw: (True, "hello"))
    progress = PlayerProgress()
    assert play_bash_level(BASH_LEVEL, progress, COLORS) is True


def test_play_bash_level_skip_never_executes(monkeypatch):
    _answers(monkeypatch, "skip")
    called = []
    monkeypatch.setattr("games.base.execute_bash", lambda *a, **kw: called.append(1) or (True, ""))
    progress = PlayerProgress()
    assert play_bash_level(BASH_LEVEL, progress, COLORS) is False
    assert called == []


def test_play_bash_level_wrong_output(monkeypatch):
    _answers(monkeypatch, "echo nope")
    monkeypatch.setattr("games.base.execute_bash", lambda *a, **kw: (False, "nope"))
    progress = PlayerProgress()
    assert play_bash_level(BASH_LEVEL, progress, COLORS) is False
    assert progress.completed_levels == []


def test_play_bash_level_interrupted(monkeypatch):
    _raise_interrupt(monkeypatch)
    progress = PlayerProgress()
    assert play_bash_level(BASH_LEVEL, progress, COLORS) is False


# ---------------------------------------------------------------------------
# _level_pass
# ---------------------------------------------------------------------------

def test_level_pass_awards_points_once():
    progress = PlayerProgress()
    _level_pass(PY_LEVEL, progress, COLORS)
    assert progress.completed_levels == [1]
    assert progress.total_points == 10


def test_level_pass_does_not_double_award():
    progress = PlayerProgress(completed_levels=[1], total_points=10)
    _level_pass(PY_LEVEL, progress, COLORS)
    assert progress.completed_levels == [1]
    assert progress.total_points == 10
