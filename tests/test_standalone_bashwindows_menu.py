"""Regression tests for the Jump to Level crash fix, shared by the
standalone BashQuest and WindowsQuest monoliths (same bug, same fix as
standalone/Cyberquest.py: main_menu() choice "3" used to call int() on the
user's answer with no try/except, so a non-numeric answer crashed the
whole game instead of just re-showing the menu)."""

import pytest

from standalone import Bashquest, Windowsquest

MODULES = [Bashquest, Windowsquest]


@pytest.fixture(autouse=True)
def _no_sleep(monkeypatch):
    for mod in MODULES:
        monkeypatch.setattr(mod.time, "sleep", lambda *_: None)


@pytest.fixture
def save_files(tmp_path, monkeypatch):
    paths = {}
    for mod in MODULES:
        path = tmp_path / f"{mod.__name__.rsplit('.', 1)[-1]}_save.json"
        monkeypatch.setattr(mod, "SAVE_FILE", path)
        paths[mod] = path
    return paths


@pytest.mark.parametrize("mod", MODULES, ids=lambda m: m.__name__)
def test_jump_with_non_numeric_input_does_not_crash(mod, save_files, monkeypatch, capsys):
    answers = iter(["3", "not-a-number", "6"])
    monkeypatch.setattr(mod.Prompt, "ask", lambda *a, **kw: next(answers))
    mod.main_menu()
    out = capsys.readouterr().out
    assert "Invalid level number" in out


@pytest.mark.parametrize("mod", MODULES, ids=lambda m: m.__name__)
def test_jump_to_valid_level_still_works(mod, save_files, monkeypatch):
    answers = iter(["3", "1", "6"])
    monkeypatch.setattr(mod.Prompt, "ask", lambda *a, **kw: next(answers))
    mod.main_menu()
    reloaded = mod.load_progress()
    assert reloaded.current_level == 1
