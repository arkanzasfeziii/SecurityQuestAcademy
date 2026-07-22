"""Regression tests for a launch-crashing bug: CiscoQuest, CryptoQuest,
ReverseQuest, and WebHackQuest each define their own RANKS/ACHIEVEMENTS/
COLORS and hand them to the shared games.base engine. Nothing previously
exercised those real module-level values against the real engine functions
(test_run_game.py uses a synthetic fixture; test_quest_wrappers.py mocks
run_game entirely), so CryptoQuest/ReverseQuest/WebHackQuest crashed via
get_rank() the instant their main menu tried to render — before a player
could see anything — and WebHackQuest's COLORS was additionally missing
keys games.base reads throughout. These tests drive the real engine
functions with each game's own real data so this can't regress silently."""

import pytest

from games import base, ciscoquest, cryptoquest, reversequest, webhackquest

MODULES = [ciscoquest, cryptoquest, reversequest, webhackquest]

REQUIRED_COLOR_KEYS = {"primary", "secondary", "success", "error", "warning", "info", "hacker"}


@pytest.fixture(autouse=True)
def _no_sleep(monkeypatch):
    monkeypatch.setattr(base.time, "sleep", lambda *_: None)


@pytest.mark.parametrize("mod", MODULES, ids=lambda m: m.__name__)
def test_ranks_are_valid_three_tuples_get_rank_can_use(mod):
    for min_level, name, description in mod.RANKS:
        assert isinstance(min_level, int)
        assert isinstance(name, str) and name
        assert isinstance(description, str) and description
    for level in (0, 1, 25, 50, 99, 100):
        name, description = base.get_rank(level, mod.RANKS)
        assert name and description


@pytest.mark.parametrize("mod", MODULES, ids=lambda m: m.__name__)
def test_achievements_are_valid_three_tuples_check_achievements_can_use(mod):
    for threshold, name, description in mod.ACHIEVEMENTS:
        assert isinstance(threshold, int)
        assert isinstance(name, str) and name
        assert isinstance(description, str) and description
    progress = base.PlayerProgress(completed_levels=list(range(1, 101)))
    base.check_achievements(progress, mod.COLORS, mod.ACHIEVEMENTS)
    assert len(progress.achievements) == len(mod.ACHIEVEMENTS)


@pytest.mark.parametrize("mod", MODULES, ids=lambda m: m.__name__)
def test_colors_has_every_key_the_engine_reads(mod):
    missing = REQUIRED_COLOR_KEYS - mod.COLORS.keys()
    assert not missing, f"{mod.__name__} COLORS missing {missing}"


@pytest.mark.parametrize("mod", MODULES, ids=lambda m: m.__name__)
def test_show_stats_renders_with_real_module_config(mod, capsys):
    progress = base.PlayerProgress(current_level=10, completed_levels=list(range(1, 6)))
    base.show_stats(progress, mod.RANKS, mod.COLORS, mod.GAME_NAME)
    out = capsys.readouterr().out
    assert mod.GAME_NAME in out
