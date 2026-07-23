"""Tests for standalone BashQuest and WindowsQuest's play_level() interactive
loop. The actual shell execution (execute_bash_command / execute_windows_command)
is mocked so these run everywhere, independent of bash/cmd availability —
content correctness of the real solutions is covered separately in
test_standalone_bashwindows_levels.py via real execution."""

import pytest

from standalone import Bashquest, Windowsquest

BASH_LEVEL = {
    "id": 1, "title": "Echo", "category": "basics", "points": 10,
    "description": "d", "challenge": "c", "hint": "echo hello",
    "explanation": "e", "expected_output": "hello",
}

WINDOWS_LEVEL = {
    "id": 1, "title": "Echo", "category": "basics", "points": 10,
    "description": "d", "challenge": "c", "hint": "echo hello",
    "explanation": "e", "expected_output": "hello", "shell": "cmd",
}

CASES = [
    (Bashquest, BASH_LEVEL, "execute_bash_command"),
    (Windowsquest, WINDOWS_LEVEL, "execute_windows_command"),
]


@pytest.fixture(autouse=True)
def _no_sleep(monkeypatch):
    for mod, _, _ in CASES:
        monkeypatch.setattr(mod.time, "sleep", lambda *_: None)


def _mock_exec(monkeypatch, mod, exec_name, result):
    monkeypatch.setattr(mod, exec_name, lambda *a, **kw: result)


def _answers(monkeypatch, mod, *values):
    it = iter(values)
    monkeypatch.setattr(mod.Prompt, "ask", lambda *a, **kw: next(it))


@pytest.mark.parametrize("mod,level,exec_name", CASES, ids=lambda x: getattr(x, "__name__", x))
def test_play_level_success_awards_points(mod, level, exec_name, monkeypatch):
    _mock_exec(monkeypatch, mod, exec_name, (True, "hello"))
    _answers(monkeypatch, mod, "echo hello")
    progress = mod.PlayerProgress()
    assert mod.play_level(level, progress) is True
    assert 1 in progress.completed_levels
    assert progress.total_points == 10


@pytest.mark.parametrize("mod,level,exec_name", CASES, ids=lambda x: getattr(x, "__name__", x))
def test_play_level_does_not_double_award(mod, level, exec_name, monkeypatch):
    _mock_exec(monkeypatch, mod, exec_name, (True, "hello"))
    _answers(monkeypatch, mod, "echo hello")
    progress = mod.PlayerProgress()
    progress.completed_levels = [1]
    progress.total_points = 10
    assert mod.play_level(level, progress) is True
    assert progress.total_points == 10


@pytest.mark.parametrize("mod,level,exec_name", CASES, ids=lambda x: getattr(x, "__name__", x))
def test_play_level_hint_then_solve(mod, level, exec_name, monkeypatch):
    _mock_exec(monkeypatch, mod, exec_name, (True, "hello"))
    _answers(monkeypatch, mod, "hint", "echo hello")
    progress = mod.PlayerProgress()
    assert mod.play_level(level, progress) is True


@pytest.mark.parametrize("mod,level,exec_name", CASES, ids=lambda x: getattr(x, "__name__", x))
def test_play_level_solution_request_does_not_submit(mod, level, exec_name, monkeypatch):
    _mock_exec(monkeypatch, mod, exec_name, (True, "hello"))
    _answers(monkeypatch, mod, "solution", "echo hello")
    progress = mod.PlayerProgress()
    assert mod.play_level(level, progress) is True


@pytest.mark.parametrize("mod,level,exec_name", CASES, ids=lambda x: getattr(x, "__name__", x))
def test_play_level_blank_input_is_rejected(mod, level, exec_name, monkeypatch):
    _mock_exec(monkeypatch, mod, exec_name, (True, "hello"))
    _answers(monkeypatch, mod, "   ", "echo hello")
    progress = mod.PlayerProgress()
    assert mod.play_level(level, progress) is True


@pytest.mark.parametrize("mod,level,exec_name", CASES, ids=lambda x: getattr(x, "__name__", x))
def test_play_level_skip_awards_nothing(mod, level, exec_name, monkeypatch):
    _answers(monkeypatch, mod, "skip")
    progress = mod.PlayerProgress()
    assert mod.play_level(level, progress) is False
    assert progress.completed_levels == []


@pytest.mark.parametrize("mod,level,exec_name", CASES, ids=lambda x: getattr(x, "__name__", x))
def test_play_level_wrong_output_declines_retry(mod, level, exec_name, monkeypatch):
    _mock_exec(monkeypatch, mod, exec_name, (False, "nope"))
    _answers(monkeypatch, mod, "echo nope")
    monkeypatch.setattr(mod.Confirm, "ask", lambda *a, **kw: False)
    progress = mod.PlayerProgress()
    assert mod.play_level(level, progress) is False
    assert progress.completed_levels == []


@pytest.mark.parametrize("mod,level,exec_name", CASES, ids=lambda x: getattr(x, "__name__", x))
def test_play_level_wrong_output_then_retry_succeeds(mod, level, exec_name, monkeypatch):
    results = iter([(False, "nope"), (True, "hello")])
    monkeypatch.setattr(mod, exec_name, lambda *a, **kw: next(results))
    _answers(monkeypatch, mod, "echo nope", "echo hello")
    monkeypatch.setattr(mod.Confirm, "ask", lambda *a, **kw: True)
    progress = mod.PlayerProgress()
    assert mod.play_level(level, progress) is True
    assert 1 in progress.completed_levels


def test_windowsquest_short_output_has_no_misleading_ellipsis(monkeypatch, capsys):
    _mock_exec(monkeypatch, Windowsquest, "execute_windows_command", (True, "hello"))
    _answers(monkeypatch, Windowsquest, "echo hello")
    progress = Windowsquest.PlayerProgress()
    Windowsquest.play_level(WINDOWS_LEVEL, progress)
    out = capsys.readouterr().out
    assert "hello..." not in out
    assert "hello" in out


@pytest.mark.parametrize("mod,level,exec_name", CASES, ids=lambda x: getattr(x, "__name__", x))
def test_play_level_interrupted(mod, level, exec_name, monkeypatch):
    def _raise(*a, **kw):
        raise KeyboardInterrupt

    monkeypatch.setattr(mod.Prompt, "ask", _raise)
    progress = mod.PlayerProgress()
    assert mod.play_level(level, progress) is False
