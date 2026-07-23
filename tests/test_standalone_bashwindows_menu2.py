"""Tests for standalone BashQuest and WindowsQuest's main_menu() loop
(view stats / achievements / reset / victory screen), beyond the Jump to
Level crash-fix tests already in test_standalone_bashwindows_menu.py.
The real shell execution is mocked so these run everywhere."""

import pytest

from standalone import Bashquest, Windowsquest

MODULES = [Bashquest, Windowsquest]


@pytest.fixture(autouse=True)
def _no_sleep(monkeypatch):
    for mod in MODULES:
        monkeypatch.setattr(mod.time, "sleep", lambda *_: None)


def pytest_generate_tests(metafunc):
    if "mod" in metafunc.fixturenames:
        metafunc.parametrize("mod", MODULES, ids=lambda m: m.__name__)


@pytest.fixture
def save_file(tmp_path, monkeypatch, mod):
    path = tmp_path / "save.json"
    monkeypatch.setattr(mod, "SAVE_FILE", path)
    return path


def _prompts(monkeypatch, mod, *values):
    it = iter(values)
    monkeypatch.setattr(mod.Prompt, "ask", lambda *a, **kw: next(it))


def _confirms(monkeypatch, mod, *values):
    it = iter(values)
    monkeypatch.setattr(mod.Confirm, "ask", lambda *a, **kw: next(it))


def _inputs(monkeypatch, value=""):
    monkeypatch.setattr("builtins.input", lambda *_: value)


def _exec_name(mod):
    return "execute_bash_command" if mod is Bashquest else "execute_windows_command"


def test_view_stats_then_exit(mod, save_file, monkeypatch, capsys):
    _prompts(monkeypatch, mod, "2", "6")
    _inputs(monkeypatch)
    mod.main_menu()
    out = capsys.readouterr().out
    assert "Your Stats" in out


def test_achievements_empty_shows_placeholder(mod, save_file, monkeypatch, capsys):
    _prompts(monkeypatch, mod, "4", "6")
    _inputs(monkeypatch)
    mod.main_menu()
    out = capsys.readouterr().out
    assert "No achievements yet" in out


def test_achievements_lists_unlocked(mod, save_file, monkeypatch, capsys):
    save_file.write_text(
        '{"current_level": 6, "completed_levels": [1,2,3,4,5], "total_points": 50, '
        '"achievements": ["First Steps"], "start_date": "x", "last_played": "x"}',
        encoding="utf-8",
    )
    _prompts(monkeypatch, mod, "4", "6")
    _inputs(monkeypatch)
    mod.main_menu()
    out = capsys.readouterr().out
    assert "First Steps" in out


def test_reset_confirmed_clears_progress(mod, save_file, monkeypatch, capsys):
    save_file.write_text(
        '{"current_level": 5, "completed_levels": [1,2,3,4], "total_points": 40, '
        '"achievements": [], "start_date": "x", "last_played": "x"}',
        encoding="utf-8",
    )
    _prompts(monkeypatch, mod, "5", "6")
    _confirms(monkeypatch, mod, True)
    mod.main_menu()
    out = capsys.readouterr().out
    assert "Progress reset" in out
    reloaded = mod.load_progress()
    assert reloaded.current_level == 1


def test_reset_declined_keeps_progress(mod, save_file, monkeypatch):
    save_file.write_text(
        '{"current_level": 5, "completed_levels": [1,2,3,4], "total_points": 40, '
        '"achievements": [], "start_date": "x", "last_played": "x"}',
        encoding="utf-8",
    )
    _prompts(monkeypatch, mod, "5", "6")
    _confirms(monkeypatch, mod, False)
    mod.main_menu()
    reloaded = mod.load_progress()
    assert reloaded.current_level == 5


def test_continue_failed_level_returns_to_menu_without_retry_prompt(mod, save_file, monkeypatch):
    # play_level itself owns the retry loop (recursive on Confirm "Try again?");
    # main_menu just breaks back to the menu on a False return, no menu-level prompt.
    monkeypatch.setattr(mod, _exec_name(mod), lambda *a, **kw: (False, "nope"))
    _prompts(monkeypatch, mod, "1", "echo nope", "6")
    _confirms(monkeypatch, mod, False)
    mod.main_menu()
    reloaded = mod.load_progress()
    assert reloaded.current_level == 1


def test_continue_completing_final_level_shows_victory(mod, save_file, monkeypatch, capsys):
    save_file.write_text(
        '{"current_level": 100, "completed_levels": [], "total_points": 0, '
        '"achievements": [], "start_date": "x", "last_played": "x"}',
        encoding="utf-8",
    )
    monkeypatch.setattr(mod, _exec_name(mod), lambda *a, **kw: (True, "ok"))
    _prompts(monkeypatch, mod, "1", "some-command", "6")
    _inputs(monkeypatch)
    mod.main_menu()
    out = capsys.readouterr().out
    assert "GRANDMASTER" in out
    reloaded = mod.load_progress()
    assert reloaded.current_level == 101


def test_jump_to_out_of_range_level_shows_error(mod, save_file, monkeypatch, capsys):
    _prompts(monkeypatch, mod, "3", "99", "6")
    mod.main_menu()
    out = capsys.readouterr().out
    assert "Invalid level number" in out


def _boot_fn_name(mod):
    return "simulate_terminal_boot" if mod is Bashquest else "simulate_windows_boot"


def test_main_happy_path_runs_boot_then_menu(mod, monkeypatch):
    calls = []
    # WindowsQuest.main() warns and asks to continue when not actually on
    # Windows (e.g. this suite running under CI's Linux runners) before it
    # ever reaches boot/menu — force the "continue anyway" path so this test
    # is deterministic regardless of which OS runs it.
    monkeypatch.setattr(mod.Confirm, "ask", lambda *a, **kw: True)
    monkeypatch.setattr(mod, _boot_fn_name(mod), lambda: calls.append("boot"))
    monkeypatch.setattr(mod, "main_menu", lambda: calls.append("menu"))
    mod.main()
    assert calls == ["boot", "menu"]


def test_main_keyboard_interrupt_is_caught(mod, monkeypatch, capsys):
    monkeypatch.setattr(mod.Confirm, "ask", lambda *a, **kw: True)
    monkeypatch.setattr(mod, _boot_fn_name(mod), lambda: None)

    def _raise():
        raise KeyboardInterrupt

    monkeypatch.setattr(mod, "main_menu", _raise)
    mod.main()
    out = capsys.readouterr().out
    assert out.strip() != ""


def test_main_unexpected_error_is_caught(mod, monkeypatch, capsys):
    monkeypatch.setattr(mod.Confirm, "ask", lambda *a, **kw: True)
    monkeypatch.setattr(mod, _boot_fn_name(mod), lambda: None)

    def _raise():
        raise RuntimeError("boom")

    monkeypatch.setattr(mod, "main_menu", _raise)
    mod.main()
    out = capsys.readouterr().out
    assert "boom" in out
