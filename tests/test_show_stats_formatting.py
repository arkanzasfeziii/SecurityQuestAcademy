"""Regression tests for show_stats() rendering Total Points with thousands
separators. games/base.py already formatted it as f"{points:,}" — all
three standalone games used plain str(points) instead, so a player past
~1,000 points (every level list here totals over 20,000) saw an unbroken
run of digits in one place and a comma-grouped number in the other."""

import pytest

from games import base
from standalone import Bashquest, Cyberquest, Windowsquest

COLORS = {
    "primary": "cyan",
    "secondary": "blue",
    "success": "green",
    "info": "white",
    "warning": "yellow",
    "hacker": "bright_green",
}

RANKS = [(1, "Rookie", "Just starting out")]


def test_games_base_show_stats_formats_points_with_commas(capsys):
    progress = base.PlayerProgress(total_points=21990)
    base.show_stats(progress, RANKS, COLORS, "Stats")
    out = capsys.readouterr().out
    assert "21,990" in out


@pytest.mark.parametrize("mod", [Cyberquest, Bashquest, Windowsquest], ids=lambda m: m.__name__)
def test_standalone_show_stats_formats_points_with_commas(mod, capsys):
    progress = mod.PlayerProgress()
    progress.total_points = 21990
    mod.show_stats(progress)
    out = capsys.readouterr().out
    assert "21,990" in out
