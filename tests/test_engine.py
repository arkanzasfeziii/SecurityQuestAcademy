"""Tests for the game engine base module."""

from games.base import PlayerProgress, get_rank, match_cisco_command


def test_player_progress_defaults():
    p = PlayerProgress()
    assert p.current_level == 1
    assert p.completed_levels == []
    assert p.total_points == 0


def test_player_progress_to_dict():
    p = PlayerProgress(current_level=5, total_points=100)
    d = p.to_dict()
    assert d["current_level"] == 5
    assert d["total_points"] == 100
    assert "start_date" in d


def test_player_progress_from_dict():
    data = {"current_level": 10, "total_points": 500,
            "completed_levels": [1, 2, 3], "achievements": ["First Blood"]}
    p = PlayerProgress.from_dict(data)
    assert p.current_level == 10
    assert p.total_points == 500
    assert len(p.completed_levels) == 3


def test_player_progress_from_empty_dict():
    p = PlayerProgress.from_dict({})
    assert p.current_level == 1
    assert p.total_points == 0


def test_get_rank():
    ranks = [(1, "Noob", "Just started"), (10, "Hacker", "Getting there"),
             (50, "Elite", "Almost done")]
    name, desc = get_rank(15, ranks)
    assert name == "Hacker"


def test_get_rank_highest():
    ranks = [(1, "Noob", "Just started"), (10, "Hacker", "Getting there"),
             (50, "Elite", "Almost done")]
    name, desc = get_rank(99, ranks)
    assert name == "Elite"


def test_match_cisco_command_exact():
    assert match_cisco_command("show ip route", ["show ip route"])


def test_match_cisco_command_case_insensitive():
    assert match_cisco_command("SHOW IP ROUTE", ["show ip route"])


def test_match_cisco_command_extra_spaces():
    assert match_cisco_command("show  ip   route", ["show ip route"])


def test_match_cisco_command_no_match():
    assert not match_cisco_command("show version", ["show ip route"])


def test_match_cisco_command_abbreviation():
    assert match_cisco_command("conf t", ["conf t", "configure terminal"])
