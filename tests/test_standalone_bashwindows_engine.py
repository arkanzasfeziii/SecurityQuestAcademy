"""Tests for standalone BashQuest and WindowsQuest's progress model,
persistence, ranks, and achievements — the same pattern already covered
for standalone/Cyberquest.py, applied here since these two files had never
been tested beyond the Jump to Level crash fix and content-integrity."""

import pytest

from standalone import Bashquest, Windowsquest

MODULES = [Bashquest, Windowsquest]


@pytest.fixture(autouse=True)
def _no_sleep(monkeypatch):
    for mod in MODULES:
        monkeypatch.setattr(mod.time, "sleep", lambda *_: None)


@pytest.fixture
def save_file(tmp_path, monkeypatch, mod):
    path = tmp_path / "save.json"
    monkeypatch.setattr(mod, "SAVE_FILE", path)
    return path


def pytest_generate_tests(metafunc):
    if "mod" in metafunc.fixturenames:
        metafunc.parametrize("mod", MODULES, ids=lambda m: m.__name__)


def test_player_progress_defaults(mod):
    p = mod.PlayerProgress()
    assert p.current_level == 1
    assert p.completed_levels == []
    assert p.total_points == 0
    assert p.achievements == []


def test_player_progress_to_dict_round_trip(mod):
    p = mod.PlayerProgress()
    p.current_level = 5
    p.completed_levels = [1, 2, 3, 4]
    p.total_points = 40
    p.achievements = ["First Steps"]
    restored = mod.PlayerProgress.from_dict(p.to_dict())
    assert restored.current_level == 5
    assert restored.completed_levels == [1, 2, 3, 4]
    assert restored.total_points == 40
    assert restored.achievements == ["First Steps"]


def test_player_progress_from_empty_dict_uses_defaults(mod):
    restored = mod.PlayerProgress.from_dict({})
    assert restored.current_level == 1
    assert restored.completed_levels == []


def test_save_and_load_round_trip(mod, save_file):
    p = mod.PlayerProgress()
    p.current_level = 12
    p.total_points = 450
    mod.save_progress(p)
    restored = mod.load_progress()
    assert restored.current_level == 12
    assert restored.total_points == 450


def test_load_progress_missing_file_returns_defaults(mod, save_file):
    restored = mod.load_progress()
    assert restored.current_level == 1


def test_load_progress_corrupt_file_returns_defaults(mod, save_file, capsys):
    save_file.write_text("{ not valid json", encoding="utf-8")
    restored = mod.load_progress()
    assert restored.current_level == 1
    out = capsys.readouterr().out
    assert "Could not load save file" in out


def test_save_progress_swallows_write_errors(mod, tmp_path, monkeypatch, capsys):
    unwritable = tmp_path / "save.json"
    unwritable.mkdir()
    monkeypatch.setattr(mod, "SAVE_FILE", unwritable)
    mod.save_progress(mod.PlayerProgress())
    out = capsys.readouterr().out
    assert "Error saving progress" in out


def test_get_rank_lowest(mod):
    name, _ = mod.get_rank(0)
    assert name == mod.RANKS[0][1]


def test_get_rank_highest(mod):
    name, _ = mod.get_rank(1000)
    assert name == mod.RANKS[-1][1]


def test_check_achievements_unlocks_at_threshold(mod):
    p = mod.PlayerProgress()
    p.completed_levels = list(range(1, 6))
    mod.check_achievements(p)
    assert len(p.achievements) == 1


def test_check_achievements_no_duplicate_unlock(mod):
    p = mod.PlayerProgress()
    p.completed_levels = list(range(1, 6))
    mod.check_achievements(p)
    first_count = len(p.achievements)
    mod.check_achievements(p)
    assert len(p.achievements) == first_count


def test_check_achievements_below_threshold_unlocks_nothing(mod):
    p = mod.PlayerProgress()
    p.completed_levels = [1, 2]
    mod.check_achievements(p)
    assert p.achievements == []


def test_ranks_are_sequential_and_reachable(mod):
    thresholds = [r[0] for r in mod.RANKS]
    assert thresholds == sorted(thresholds)
    assert thresholds[0] == 0
    assert thresholds[-1] == 100
