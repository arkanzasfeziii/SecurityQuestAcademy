"""Tests for standalone/Cyberquest.py's main_menu() loop."""

import pytest

from standalone import Cyberquest


@pytest.fixture(autouse=True)
def _no_sleep(monkeypatch):
    monkeypatch.setattr(Cyberquest.time, "sleep", lambda *_: None)


@pytest.fixture
def save_file(tmp_path, monkeypatch):
    path = tmp_path / "save.json"
    monkeypatch.setattr(Cyberquest, "SAVE_FILE", path)
    return path


def _prompts(monkeypatch, *values):
    it = iter(values)
    monkeypatch.setattr(Cyberquest.Prompt, "ask", lambda *a, **kw: next(it))


def _confirms(monkeypatch, *values):
    it = iter(values)
    monkeypatch.setattr(Cyberquest.Confirm, "ask", lambda *a, **kw: next(it))


def _inputs(monkeypatch, value=""):
    monkeypatch.setattr("builtins.input", lambda *_: value)


def test_exit_immediately_does_not_touch_save_file(save_file, monkeypatch):
    _prompts(monkeypatch, "6")
    Cyberquest.main_menu()
    assert not save_file.exists()


def test_continue_completing_a_level_saves_progress(save_file, monkeypatch):
    monkeypatch.setattr(Cyberquest, "play_level", lambda level, progress: True)
    _prompts(monkeypatch, "1", "6")
    _confirms(monkeypatch, False)
    Cyberquest.main_menu()
    assert save_file.exists()
    reloaded = Cyberquest.load_progress()
    assert reloaded.current_level == 2


def test_continue_failed_level_declines_retry(save_file, monkeypatch):
    monkeypatch.setattr(Cyberquest, "play_level", lambda level, progress: False)
    _prompts(monkeypatch, "1", "6")
    _confirms(monkeypatch, False)
    Cyberquest.main_menu()
    reloaded = Cyberquest.load_progress()
    assert reloaded.current_level == 1


def test_continue_confirmed_advances_through_final_level_to_victory(save_file, monkeypatch, capsys):
    save_file.write_text(
        '{"current_level": 99, "completed_levels": [], "total_points": 0, '
        '"achievements": [], "start_date": "x", "last_played": "x"}',
        encoding="utf-8",
    )
    monkeypatch.setattr(Cyberquest, "play_level", lambda level, progress: True)
    _prompts(monkeypatch, "1", "6")
    _confirms(monkeypatch, True)
    _inputs(monkeypatch)
    Cyberquest.main_menu()
    out = capsys.readouterr().out
    assert "LEGENDARY HACKER" in out
    reloaded = Cyberquest.load_progress()
    assert reloaded.current_level == 101


def test_continue_failed_level_retries_when_confirmed(save_file, monkeypatch):
    monkeypatch.setattr(Cyberquest, "play_level", lambda level, progress: False)
    _prompts(monkeypatch, "1", "6")
    _confirms(monkeypatch, True, False)
    Cyberquest.main_menu()
    reloaded = Cyberquest.load_progress()
    assert reloaded.current_level == 1


def test_view_stats_then_exit(save_file, monkeypatch, capsys):
    _prompts(monkeypatch, "2", "6")
    _inputs(monkeypatch)
    Cyberquest.main_menu()
    out = capsys.readouterr().out
    assert "Your Stats" in out


def test_jump_to_valid_level_saves_progress(save_file, monkeypatch):
    _prompts(monkeypatch, "3", "1", "6")
    Cyberquest.main_menu()
    assert save_file.exists()
    reloaded = Cyberquest.load_progress()
    assert reloaded.current_level == 1


def test_jump_to_out_of_range_level_shows_error(save_file, monkeypatch, capsys):
    _prompts(monkeypatch, "3", "99", "6")
    Cyberquest.main_menu()
    out = capsys.readouterr().out
    assert "Invalid level number" in out


def test_jump_with_non_numeric_input_does_not_crash(save_file, monkeypatch, capsys):
    _prompts(monkeypatch, "3", "not-a-number", "6")
    Cyberquest.main_menu()
    out = capsys.readouterr().out
    assert "Invalid level number" in out


def test_achievements_empty_shows_placeholder(save_file, monkeypatch, capsys):
    _prompts(monkeypatch, "4", "6")
    _inputs(monkeypatch)
    Cyberquest.main_menu()
    out = capsys.readouterr().out
    assert "No achievements yet" in out


def test_achievements_lists_unlocked(save_file, monkeypatch, capsys):
    save_file.write_text(
        '{"current_level": 6, "completed_levels": [1,2,3,4,5], "total_points": 50, '
        '"achievements": ["First Steps"], "start_date": "x", "last_played": "x"}',
        encoding="utf-8",
    )
    _prompts(monkeypatch, "4", "6")
    _inputs(monkeypatch)
    Cyberquest.main_menu()
    out = capsys.readouterr().out
    assert "First Steps" in out


def test_reset_confirmed_clears_progress(save_file, monkeypatch, capsys):
    save_file.write_text(
        '{"current_level": 5, "completed_levels": [1,2,3,4], "total_points": 40, '
        '"achievements": [], "start_date": "x", "last_played": "x"}',
        encoding="utf-8",
    )
    _prompts(monkeypatch, "5", "6")
    _confirms(monkeypatch, True)
    Cyberquest.main_menu()
    out = capsys.readouterr().out
    assert "Progress reset" in out
    reloaded = Cyberquest.load_progress()
    assert reloaded.current_level == 1


def test_reset_declined_keeps_progress(save_file, monkeypatch):
    save_file.write_text(
        '{"current_level": 5, "completed_levels": [1,2,3,4], "total_points": 40, '
        '"achievements": [], "start_date": "x", "last_played": "x"}',
        encoding="utf-8",
    )
    _prompts(monkeypatch, "5", "6")
    _confirms(monkeypatch, False)
    Cyberquest.main_menu()
    reloaded = Cyberquest.load_progress()
    assert reloaded.current_level == 5
