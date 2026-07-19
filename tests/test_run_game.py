"""Tests for the shared run_game() menu loop (continue/stats/jump/achievements/reset/exit)."""

import pytest

from games import base

COLORS = {
    "primary": "cyan",
    "secondary": "blue",
    "success": "green",
    "info": "white",
    "warning": "yellow",
    "error": "red",
}

RANKS = [(1, "Rookie", "Just starting out"), (10, "Veteran", "Seasoned hacker")]

ACHIEVEMENT_THRESHOLDS = [(1, "First Blood", "Complete your first level")]

LEVELS = [
    {
        "id": 1,
        "title": "One",
        "category": "basics",
        "points": 10,
        "description": "d",
        "challenge": "c",
        "hint": "h",
        "test_code": "pass",
    }
]


@pytest.fixture(autouse=True)
def _no_sleep(monkeypatch):
    monkeypatch.setattr(base.time, "sleep", lambda *_: None)


def _prompts(monkeypatch, *values):
    it = iter(values)
    monkeypatch.setattr(base.Prompt, "ask", lambda *a, **kw: next(it))


def _confirms(monkeypatch, *values):
    it = iter(values)
    monkeypatch.setattr(base.Confirm, "ask", lambda *a, **kw: next(it))


def _inputs(monkeypatch, value=""):
    monkeypatch.setattr("builtins.input", lambda *_: value)


def _run(save_file, engine="python", play_result=True, levels=LEVELS):
    base.run_game(
        levels=levels,
        ranks=RANKS,
        colors=COLORS,
        save_file=save_file,
        game_name="TestQuest",
        show_banner_fn=lambda: None,
        simulate_boot_fn=lambda: None,
        engine=engine,
        achievement_thresholds=ACHIEVEMENT_THRESHOLDS,
    )


def test_exit_immediately_does_not_touch_save_file(tmp_path, monkeypatch):
    save_file = tmp_path / "save.json"
    _prompts(monkeypatch, "6")
    _run(save_file)
    assert not save_file.exists()


def test_continue_completing_last_level_shows_victory(tmp_path, monkeypatch, capsys):
    save_file = tmp_path / "save.json"
    monkeypatch.setitem(base.ENGINE_MAP, "python", lambda level, progress, colors: True)
    _prompts(monkeypatch, "1", "6")
    _inputs(monkeypatch)
    _run(save_file)
    out = capsys.readouterr().out
    assert "COMPLETED ALL 100 LEVELS" in out
    assert save_file.exists()


def test_continue_failed_level_declines_retry(tmp_path, monkeypatch):
    save_file = tmp_path / "save.json"
    monkeypatch.setitem(base.ENGINE_MAP, "python", lambda level, progress, colors: False)
    _prompts(monkeypatch, "1", "6")
    _confirms(monkeypatch, False)
    _run(save_file)
    assert not save_file.exists()


def test_view_stats_then_exit(tmp_path, monkeypatch, capsys):
    save_file = tmp_path / "save.json"
    _prompts(monkeypatch, "2", "6")
    _inputs(monkeypatch)
    _run(save_file)
    out = capsys.readouterr().out
    assert "TestQuest" in out


def test_jump_to_valid_level_saves_progress(tmp_path, monkeypatch):
    save_file = tmp_path / "save.json"
    _prompts(monkeypatch, "3", "1", "6")
    _run(save_file)
    assert save_file.exists()


def test_jump_to_out_of_range_level_shows_error(tmp_path, monkeypatch, capsys):
    save_file = tmp_path / "save.json"
    _prompts(monkeypatch, "3", "99", "6")
    _run(save_file)
    out = capsys.readouterr().out
    assert "Out of range" in out


def test_jump_with_non_numeric_input_is_ignored(tmp_path, monkeypatch):
    save_file = tmp_path / "save.json"
    _prompts(monkeypatch, "3", "not-a-number", "6")
    _run(save_file)
    assert not save_file.exists()


def test_achievements_empty_shows_placeholder(tmp_path, monkeypatch, capsys):
    save_file = tmp_path / "save.json"
    _prompts(monkeypatch, "4", "6")
    _inputs(monkeypatch)
    _run(save_file)
    out = capsys.readouterr().out
    assert "No achievements yet" in out


def test_achievements_lists_unlocked(tmp_path, monkeypatch, capsys):
    save_file = tmp_path / "save.json"
    save_file.write_text(
        '{"current_level": 2, "completed_levels": [1], "total_points": 10, '
        '"achievements": ["First Blood"], "start_date": "x", "last_played": "x"}'
    )
    _prompts(monkeypatch, "4", "6")
    _inputs(monkeypatch)
    _run(save_file)
    out = capsys.readouterr().out
    assert "First Blood" in out


def test_reset_confirmed_clears_progress(tmp_path, monkeypatch, capsys):
    save_file = tmp_path / "save.json"
    save_file.write_text(
        '{"current_level": 5, "completed_levels": [1,2,3,4], "total_points": 40, '
        '"achievements": [], "start_date": "x", "last_played": "x"}'
    )
    _prompts(monkeypatch, "5", "6")
    _confirms(monkeypatch, True)
    _run(save_file)
    out = capsys.readouterr().out
    assert "Reset." in out
    reloaded = base.load_progress(save_file)
    assert reloaded.current_level == 1


def test_reset_declined_keeps_progress(tmp_path, monkeypatch):
    save_file = tmp_path / "save.json"
    save_file.write_text(
        '{"current_level": 5, "completed_levels": [1,2,3,4], "total_points": 40, '
        '"achievements": [], "start_date": "x", "last_played": "x"}'
    )
    _prompts(monkeypatch, "5", "6")
    _confirms(monkeypatch, False)
    _run(save_file)
    reloaded = base.load_progress(save_file)
    assert reloaded.current_level == 5


def test_boot_sequence_error_is_swallowed(tmp_path, monkeypatch):
    save_file = tmp_path / "save.json"
    _prompts(monkeypatch, "6")

    def _boom():
        raise RuntimeError("boot failed")

    base.run_game(
        levels=LEVELS,
        ranks=RANKS,
        colors=COLORS,
        save_file=save_file,
        game_name="TestQuest",
        show_banner_fn=lambda: None,
        simulate_boot_fn=_boom,
        engine="python",
        achievement_thresholds=ACHIEVEMENT_THRESHOLDS,
    )
    assert not save_file.exists()


def test_continue_declines_next_level_after_success(tmp_path, monkeypatch):
    save_file = tmp_path / "save.json"
    two_levels = LEVELS + [
        {
            "id": 2,
            "title": "Two",
            "category": "basics",
            "points": 10,
            "description": "d",
            "challenge": "c",
            "hint": "h",
            "test_code": "pass",
        }
    ]
    monkeypatch.setitem(base.ENGINE_MAP, "python", lambda level, progress, colors: True)
    _prompts(monkeypatch, "1", "6")
    _confirms(monkeypatch, False)
    _run(save_file, levels=two_levels)
    reloaded = base.load_progress(save_file)
    assert reloaded.current_level == 2
