"""Regression tests for show_level_info() crashing on a level missing
'category'. games/base.py already used level_data.get("category", "") —
all three standalone games used level_data["category"] directly, an
unhandled KeyError waiting to happen the moment a level is ever added
without that field. No current level is actually missing it (the
content-integrity suites already guard that), but the function itself
should be as defensive as its games/base.py counterpart."""

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

LEVEL_MISSING_CATEGORY = {
    "id": 1,
    "title": "Test",
    "points": 10,
    "description": "d",
    "challenge": "c",
}


def test_games_base_show_level_info_handles_missing_category(capsys):
    base.show_level_info(LEVEL_MISSING_CATEGORY, COLORS)
    out = capsys.readouterr().out
    assert "TEST" in out


@pytest.mark.parametrize("mod", [Cyberquest, Bashquest, Windowsquest], ids=lambda m: m.__name__)
def test_standalone_show_level_info_handles_missing_category(mod, capsys):
    level = dict(LEVEL_MISSING_CATEGORY)
    if mod is Windowsquest:
        level["shell"] = "cmd"
    mod.show_level_info(level)
    out = capsys.readouterr().out
    assert "TEST" in out
