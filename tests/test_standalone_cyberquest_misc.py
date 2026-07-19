"""Tests for standalone/Cyberquest.py's remaining odds and ends: the get_rank
fallback, the boot animation, and the top-level main() entry point."""

import pytest

from standalone import Cyberquest


@pytest.fixture(autouse=True)
def _no_sleep(monkeypatch):
    monkeypatch.setattr(Cyberquest.time, "sleep", lambda *_: None)
    monkeypatch.setattr(Cyberquest.random, "uniform", lambda a, b: 0)


def test_get_rank_below_lowest_threshold_falls_back_to_rank_zero():
    name, desc = Cyberquest.get_rank(-1)
    assert name == Cyberquest.RANKS[0][1]
    assert desc == Cyberquest.RANKS[0][2]


def test_simulate_hacking_runs_without_error(capsys):
    Cyberquest.simulate_hacking()
    out = capsys.readouterr().out
    assert "System ready" in out


def test_main_happy_path_runs_boot_then_menu(monkeypatch):
    calls = []
    monkeypatch.setattr(Cyberquest, "simulate_hacking", lambda: calls.append("boot"))
    monkeypatch.setattr(Cyberquest, "main_menu", lambda: calls.append("menu"))
    Cyberquest.main()
    assert calls == ["boot", "menu"]


def test_main_keyboard_interrupt_is_caught(monkeypatch, capsys):
    monkeypatch.setattr(Cyberquest, "simulate_hacking", lambda: None)

    def _raise():
        raise KeyboardInterrupt

    monkeypatch.setattr(Cyberquest, "main_menu", _raise)
    Cyberquest.main()
    out = capsys.readouterr().out
    assert "interrupted" in out.lower()


def test_main_unexpected_error_is_caught(monkeypatch, capsys):
    monkeypatch.setattr(Cyberquest, "simulate_hacking", lambda: None)

    def _raise():
        raise RuntimeError("boom")

    monkeypatch.setattr(Cyberquest, "main_menu", _raise)
    Cyberquest.main()
    out = capsys.readouterr().out
    assert "An error occurred" in out
    assert "boom" in out
