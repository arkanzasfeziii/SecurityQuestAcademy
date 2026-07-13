"""Tests for the games/*.py thin wrappers that launch standalone games."""

import importlib

import pytest

WRAPPERS = [
    ("games.cyberquest", "CyberQuest"),
    ("games.bashquest", "BashQuest"),
    ("games.windowsquest", "WindowsQuest"),
]


class _FakePath:
    def __init__(self, exists, text):
        self._exists = exists
        self._text = text

    def exists(self):
        return self._exists

    def __str__(self):
        return self._text


@pytest.mark.parametrize("module_name,label", WRAPPERS)
def test_run_exits_when_game_file_missing(module_name, label, monkeypatch, capsys):
    mod = importlib.import_module(module_name)
    monkeypatch.setattr(mod, "ORIGINAL", _FakePath(False, "missing.py"))
    with pytest.raises(SystemExit) as exc:
        mod.run()
    assert exc.value.code == 1
    out = capsys.readouterr().out
    assert label in out
    assert "not found" in out


@pytest.mark.parametrize("module_name,label", WRAPPERS)
def test_run_launches_subprocess_when_game_file_present(module_name, label, monkeypatch):
    mod = importlib.import_module(module_name)
    monkeypatch.setattr(mod, "ORIGINAL", _FakePath(True, "game.py"))
    calls = []
    monkeypatch.setattr(mod.subprocess, "run", lambda *a, **kw: calls.append((a, kw)))
    mod.run()
    assert len(calls) == 1
    args, kwargs = calls[0]
    assert args[0] == [mod.sys.executable, "game.py"]
    assert kwargs == {"check": False}
