"""Tests for the main menu and game launcher."""

import pytest

from securityquest import cli
from securityquest.config import GAMES


@pytest.fixture(autouse=True)
def _no_sleep(monkeypatch):
    monkeypatch.setattr(cli.time, "sleep", lambda *_: None)


def test_show_banner_prints_something(capsys):
    cli.show_banner()
    out = capsys.readouterr().out
    assert out.strip() != ""


def test_show_boot_runs_all_steps(capsys):
    cli.show_boot()
    out = capsys.readouterr().out
    assert "Academy ready!" in out


def test_show_menu_lists_all_games(capsys):
    cli.show_menu()
    out = capsys.readouterr().out
    for g in GAMES:
        # rich truncates long names in the narrow column; match a safe prefix
        assert g["name"][:5] in out


def test_launch_game_success(monkeypatch):
    calls = []

    class _FakeMod:
        @staticmethod
        def run():
            calls.append("ran")

    monkeypatch.setattr(cli.importlib, "import_module", lambda name: _FakeMod)
    cli.launch_game(GAMES[0])
    assert calls == ["ran"]


def test_launch_game_import_error_is_caught(monkeypatch, capsys):
    def _boom(name):
        raise ImportError("missing module")

    monkeypatch.setattr(cli.importlib, "import_module", _boom)
    cli.launch_game(GAMES[0])
    out = capsys.readouterr().out
    assert "Failed to load" in out


def test_launch_game_runtime_error_is_caught(monkeypatch, capsys):
    class _FakeMod:
        @staticmethod
        def run():
            raise RuntimeError("boom")

    monkeypatch.setattr(cli.importlib, "import_module", lambda name: _FakeMod)
    cli.launch_game(GAMES[0])
    out = capsys.readouterr().out
    assert "Error in" in out


def test_main_quits_on_q(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda *_: "Q")
    cli.main()
    out = capsys.readouterr().out
    assert "Goodbye" in out


def test_main_quits_on_eof(monkeypatch, capsys):
    def _raise_eof(*_):
        raise EOFError

    monkeypatch.setattr("builtins.input", _raise_eof)
    cli.main()
    out = capsys.readouterr().out
    assert "Goodbye" in out


def test_main_invalid_choice_then_quit(monkeypatch, capsys):
    answers = iter(["99", "Q"])
    monkeypatch.setattr("builtins.input", lambda *_: next(answers))
    cli.main()
    out = capsys.readouterr().out
    assert "Invalid choice" in out


def test_main_launches_selected_game_then_quits(monkeypatch, capsys):
    answers = iter(["1", "Q"])
    monkeypatch.setattr("builtins.input", lambda *_: next(answers))
    launched = []
    monkeypatch.setattr(cli, "launch_game", lambda game: launched.append(game["name"]))
    cli.main()
    assert launched == ["CyberQuest"]
