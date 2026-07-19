"""Tests for standalone/Cyberquest.py's play_level() interactive loop."""

import pytest

from standalone import Cyberquest

LEVEL = {
    "id": 1,
    "title": "Add",
    "category": "basics",
    "points": 10,
    "description": "d",
    "challenge": "c",
    "hint": "print(2 + 2)",
    "explanation": "e",
    "test_code": "print(4)",
    "solution": "print(2 + 2)",
}


@pytest.fixture(autouse=True)
def _no_sleep(monkeypatch):
    monkeypatch.setattr(Cyberquest.time, "sleep", lambda *_: None)


def _answers(monkeypatch, *values):
    it = iter(values)
    monkeypatch.setattr(Cyberquest.Prompt, "ask", lambda *a, **kw: next(it))


def test_play_level_correct_code_completes(monkeypatch):
    _answers(monkeypatch, "print(2 + 2)", "done")
    progress = Cyberquest.PlayerProgress()
    assert Cyberquest.play_level(LEVEL, progress) is True
    assert 1 in progress.completed_levels
    assert progress.total_points == 10


def test_play_level_does_not_double_award_points(monkeypatch):
    _answers(monkeypatch, "print(2 + 2)", "done")
    progress = Cyberquest.PlayerProgress()
    progress.completed_levels = [1]
    progress.total_points = 10
    assert Cyberquest.play_level(LEVEL, progress) is True
    assert progress.total_points == 10
    assert progress.completed_levels == [1]


def test_play_level_hint_then_solve(monkeypatch):
    _answers(monkeypatch, "hint", "print(2 + 2)", "done")
    progress = Cyberquest.PlayerProgress()
    assert Cyberquest.play_level(LEVEL, progress) is True


def test_play_level_solution_request_is_refused(monkeypatch):
    _answers(monkeypatch, "solution", "print(2 + 2)", "done")
    progress = Cyberquest.PlayerProgress()
    assert Cyberquest.play_level(LEVEL, progress) is True


def test_play_level_skip_awards_nothing(monkeypatch):
    _answers(monkeypatch, "skip")
    progress = Cyberquest.PlayerProgress()
    assert Cyberquest.play_level(LEVEL, progress) is False
    assert progress.completed_levels == []


def test_play_level_no_code_entered(monkeypatch):
    _answers(monkeypatch, "done")
    progress = Cyberquest.PlayerProgress()
    assert Cyberquest.play_level(LEVEL, progress) is False


def test_play_level_wrong_output(monkeypatch):
    _answers(monkeypatch, "print(1)", "done")
    progress = Cyberquest.PlayerProgress()
    assert Cyberquest.play_level(LEVEL, progress) is False


def test_play_level_code_raises_exception(monkeypatch):
    _answers(monkeypatch, "1 / 0", "done")
    progress = Cyberquest.PlayerProgress()
    assert Cyberquest.play_level(LEVEL, progress) is False
    assert progress.completed_levels == []


def test_play_level_interrupted(monkeypatch):
    def _raise(*a, **kw):
        raise KeyboardInterrupt

    monkeypatch.setattr(Cyberquest.Prompt, "ask", _raise)
    progress = Cyberquest.PlayerProgress()
    assert Cyberquest.play_level(LEVEL, progress) is False
