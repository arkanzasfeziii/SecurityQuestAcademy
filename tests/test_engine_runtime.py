"""Tests for the engine runtime: execution engines, persistence, achievements.

These cover the core game logic that the interactive UI relies on —
the Python/Bash execution engines, the save/load round-trip, and the
achievement unlock rules.
"""

import json
import shutil
import subprocess

import pytest

from games import base
from games.base import (
    PlayerProgress,
    check_achievements,
    eval_python_level,
    execute_bash,
    get_rank,
    load_progress,
    save_progress,
)

# Minimal colour map matching the keys the engine reads.
COLORS = {
    "primary": "cyan",
    "secondary": "blue",
    "success": "green",
    "info": "white",
    "warning": "yellow",
    "error": "red",
}


# ---------------------------------------------------------------------------
# Python execution engine
# ---------------------------------------------------------------------------

def test_eval_python_level_match():
    ok, user_out, expected_out = eval_python_level("print(2 + 2)", "print(4)")
    assert ok is True
    assert user_out == "4"
    assert expected_out == "4"


def test_eval_python_level_mismatch():
    ok, user_out, expected_out = eval_python_level("print(1)", "print(2)")
    assert ok is False
    assert user_out == "1"
    assert expected_out == "2"


def test_eval_python_level_syntax_error():
    ok, user_out, expected_out = eval_python_level("print(", "print(0)")
    assert ok is False
    assert user_out.startswith("ERROR:")
    assert expected_out == ""


def test_eval_python_level_runtime_error():
    ok, user_out, _ = eval_python_level("1 / 0", "print(0)")
    assert ok is False
    assert user_out.startswith("ERROR:")
    assert "division by zero" in user_out


# ---------------------------------------------------------------------------
# Bash execution engine (requires a bash interpreter)
# ---------------------------------------------------------------------------

def _bash_usable() -> bool:
    """Probe whether bash can actually run a sandboxed script here.

    Presence on PATH is not enough — on some Windows setups the only
    ``bash`` is WSL, which cannot resolve the Windows temp path the
    engine writes to. Skip rather than fail in those environments; the
    Linux CI runners exercise this path for real.
    """
    if shutil.which("bash") is None:
        return False
    try:
        ok, out = execute_bash("echo __sqa_probe__", expected_output="__sqa_probe__")
        return ok and out == "__sqa_probe__"
    except Exception:
        return False


requires_bash = pytest.mark.skipif(
    not _bash_usable(), reason="no working bash interpreter for sandboxed scripts"
)


@requires_bash
def test_execute_bash_expected_output_match():
    ok, output = execute_bash("echo hello", expected_output="hello")
    assert ok is True
    assert output == "hello"


@requires_bash
def test_execute_bash_expected_output_mismatch():
    ok, output = execute_bash("echo hello", expected_output="world")
    assert ok is False
    assert output == "hello"


@requires_bash
def test_execute_bash_return_code_only():
    ok, _ = execute_bash("true")
    assert ok is True


def test_execute_bash_timeout(monkeypatch):
    def _raise_timeout(*args, **kwargs):
        raise subprocess.TimeoutExpired(cmd="bash", timeout=5)

    monkeypatch.setattr(base.subprocess, "run", _raise_timeout)
    ok, output = execute_bash("sleep 999")
    assert ok is False
    assert output == "Command timed out"


def test_execute_bash_unexpected_error(monkeypatch):
    def _raise_oserror(*args, **kwargs):
        raise OSError("bash not found")

    monkeypatch.setattr(base.subprocess, "run", _raise_oserror)
    ok, output = execute_bash("echo hi")
    assert ok is False
    assert "bash not found" in output


# ---------------------------------------------------------------------------
# Persistence: save / load round-trip
# ---------------------------------------------------------------------------

def test_save_and_load_round_trip(tmp_path):
    save_file = tmp_path / "progress.json"
    original = PlayerProgress(
        current_level=12,
        completed_levels=[1, 2, 3],
        total_points=450,
        achievements=["First Blood"],
    )
    save_progress(original, save_file)

    restored = load_progress(save_file)
    assert restored.current_level == 12
    assert restored.completed_levels == [1, 2, 3]
    assert restored.total_points == 450
    assert restored.achievements == ["First Blood"]


def test_load_progress_missing_file(tmp_path):
    restored = load_progress(tmp_path / "does_not_exist.json")
    assert restored.current_level == 1
    assert restored.total_points == 0
    assert restored.completed_levels == []


def test_load_progress_corrupt_file(tmp_path):
    save_file = tmp_path / "progress.json"
    save_file.write_text("{ this is not valid json", encoding="utf-8")
    restored = load_progress(save_file)
    assert restored.current_level == 1
    assert restored.total_points == 0


def test_save_progress_writes_valid_json(tmp_path):
    save_file = tmp_path / "progress.json"
    save_progress(PlayerProgress(current_level=7, total_points=100), save_file)
    data = json.loads(save_file.read_text(encoding="utf-8"))
    assert data["current_level"] == 7
    assert data["total_points"] == 100


def test_save_progress_swallows_write_errors(tmp_path, capsys):
    unwritable_dir_as_file = tmp_path / "progress.json"
    unwritable_dir_as_file.mkdir()
    save_progress(PlayerProgress(), unwritable_dir_as_file)
    out = capsys.readouterr().out
    assert "Save error" in out


# ---------------------------------------------------------------------------
# Achievements
# ---------------------------------------------------------------------------

THRESHOLDS = [
    (1, "First Blood", "Complete your first level"),
    (3, "Getting Warm", "Complete three levels"),
    (5, "On Fire", "Complete five levels"),
]


def test_check_achievements_unlocks_reached(monkeypatch):
    monkeypatch.setattr("games.base.time.sleep", lambda *_: None)
    progress = PlayerProgress(completed_levels=[1, 2, 3])
    check_achievements(progress, COLORS, THRESHOLDS)
    assert "First Blood" in progress.achievements
    assert "Getting Warm" in progress.achievements
    assert "On Fire" not in progress.achievements


def test_check_achievements_no_duplicates(monkeypatch):
    monkeypatch.setattr("games.base.time.sleep", lambda *_: None)
    progress = PlayerProgress(completed_levels=[1, 2, 3], achievements=["First Blood"])
    check_achievements(progress, COLORS, THRESHOLDS)
    assert progress.achievements.count("First Blood") == 1
    assert "Getting Warm" in progress.achievements


def test_check_achievements_none_when_below_threshold(monkeypatch):
    monkeypatch.setattr("games.base.time.sleep", lambda *_: None)
    progress = PlayerProgress(completed_levels=[])
    check_achievements(progress, COLORS, THRESHOLDS)
    assert progress.achievements == []


# ---------------------------------------------------------------------------
# Rank edge case
# ---------------------------------------------------------------------------

def test_get_rank_below_first_threshold():
    ranks = [(1, "Noob", "Just started"), (10, "Hacker", "Getting there")]
    name, _ = get_rank(0, ranks)
    assert name == "Noob"
