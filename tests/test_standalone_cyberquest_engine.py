"""Tests for standalone/Cyberquest.py's progress model, persistence, ranks, and achievements."""

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


def test_player_progress_defaults():
    p = Cyberquest.PlayerProgress()
    assert p.current_level == 1
    assert p.completed_levels == []
    assert p.total_points == 0
    assert p.achievements == []


def test_player_progress_to_dict_round_trip():
    p = Cyberquest.PlayerProgress()
    p.current_level = 5
    p.completed_levels = [1, 2, 3, 4]
    p.total_points = 40
    p.achievements = ["First Steps"]
    restored = Cyberquest.PlayerProgress.from_dict(p.to_dict())
    assert restored.current_level == 5
    assert restored.completed_levels == [1, 2, 3, 4]
    assert restored.total_points == 40
    assert restored.achievements == ["First Steps"]


def test_player_progress_from_empty_dict_uses_defaults():
    restored = Cyberquest.PlayerProgress.from_dict({})
    assert restored.current_level == 1
    assert restored.completed_levels == []


def test_save_and_load_round_trip(save_file):
    p = Cyberquest.PlayerProgress()
    p.current_level = 12
    p.total_points = 450
    Cyberquest.save_progress(p)
    restored = Cyberquest.load_progress()
    assert restored.current_level == 12
    assert restored.total_points == 450


def test_load_progress_missing_file_returns_defaults(save_file):
    restored = Cyberquest.load_progress()
    assert restored.current_level == 1


def test_load_progress_corrupt_file_returns_defaults(save_file, capsys):
    save_file.write_text("{ not valid json", encoding="utf-8")
    restored = Cyberquest.load_progress()
    assert restored.current_level == 1
    out = capsys.readouterr().out
    assert "Could not load save file" in out


def test_save_progress_swallows_write_errors(tmp_path, monkeypatch, capsys):
    unwritable = tmp_path / "save.json"
    unwritable.mkdir()
    monkeypatch.setattr(Cyberquest, "SAVE_FILE", unwritable)
    Cyberquest.save_progress(Cyberquest.PlayerProgress())
    out = capsys.readouterr().out
    assert "Error saving progress" in out


def test_get_rank_lowest():
    name, _ = Cyberquest.get_rank(1)
    assert name == Cyberquest.RANKS[0][1]


def test_get_rank_highest():
    name, _ = Cyberquest.get_rank(1000)
    assert name == Cyberquest.RANKS[-1][1]


def test_check_achievements_unlocks_at_threshold():
    p = Cyberquest.PlayerProgress()
    p.completed_levels = list(range(1, 6))
    Cyberquest.check_achievements(p)
    assert any("First Steps" in a for a in p.achievements)


def test_check_achievements_no_duplicate_unlock():
    p = Cyberquest.PlayerProgress()
    p.completed_levels = list(range(1, 6))
    Cyberquest.check_achievements(p)
    first_count = len(p.achievements)
    Cyberquest.check_achievements(p)
    assert len(p.achievements) == first_count


def test_check_achievements_below_threshold_unlocks_nothing():
    p = Cyberquest.PlayerProgress()
    p.completed_levels = [1, 2]
    Cyberquest.check_achievements(p)
    assert p.achievements == []
