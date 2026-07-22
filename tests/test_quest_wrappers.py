"""Tests for the show_banner/simulate_boot/run wrapper functions shared by
CiscoQuest, CryptoQuest, ReverseQuest, and WebHackQuest — each delegates
actual gameplay to games.base.run_game(), already covered by test_run_game.py."""

import pytest

from games import ciscoquest, cryptoquest, reversequest, webhackquest

MODULES = [ciscoquest, cryptoquest, reversequest, webhackquest]


@pytest.fixture(autouse=True)
def _no_sleep(monkeypatch):
    monkeypatch.setattr("time.sleep", lambda *_: None)


@pytest.mark.parametrize("mod", MODULES, ids=lambda m: m.__name__)
def test_show_banner_prints_something(mod, capsys):
    mod.show_banner()
    out = capsys.readouterr().out
    assert out.strip() != ""


@pytest.mark.parametrize("mod", MODULES, ids=lambda m: m.__name__)
def test_simulate_boot_runs_without_error(mod, capsys):
    mod.simulate_boot()
    out = capsys.readouterr().out
    assert out.strip() != ""


def test_ciscoquest_run_calls_run_game_with_module_config(monkeypatch):
    calls = []
    monkeypatch.setattr(
        "games.base.run_game",
        lambda **kwargs: calls.append(kwargs),
    )
    ciscoquest.run()
    assert len(calls) == 1
    kwargs = calls[0]
    assert kwargs["levels"] is ciscoquest.LEVELS
    assert kwargs["ranks"] is ciscoquest.RANKS
    assert kwargs["colors"] is ciscoquest.COLORS
    assert kwargs["save_file"] == ciscoquest.SAVE_FILE
    assert kwargs["game_name"] == ciscoquest.GAME_NAME
    assert kwargs["engine"] == ciscoquest.ENGINE
    assert kwargs["achievement_thresholds"] is ciscoquest.ACHIEVEMENTS


@pytest.mark.parametrize("mod", [cryptoquest, reversequest, webhackquest], ids=lambda m: m.__name__)
def test_run_calls_run_game_with_module_config(mod, monkeypatch):
    calls = []
    monkeypatch.setattr(mod, "run_game", lambda **kwargs: calls.append(kwargs))
    mod.run()
    assert len(calls) == 1
    kwargs = calls[0]
    assert kwargs["levels"] is mod.LEVELS
    assert kwargs["ranks"] is mod.RANKS
    assert kwargs["colors"] is mod.COLORS
    assert kwargs["save_file"] == mod.SAVE_FILE
    assert kwargs["game_name"] == mod.GAME_NAME
    assert kwargs["engine"] == mod.ENGINE
    assert kwargs["achievement_thresholds"] is mod.ACHIEVEMENTS
