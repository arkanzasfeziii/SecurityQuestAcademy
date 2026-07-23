"""Tests for standalone BashQuest and WindowsQuest's boot animations and
the exception/timeout branches of their real command-execution engines.
subprocess is mocked so these run everywhere, independent of bash/cmd
availability — the happy-path execution against real solutions is covered
in test_standalone_bashwindows_levels.py."""

import subprocess

import pytest

from standalone import Bashquest, Windowsquest


@pytest.fixture(autouse=True)
def _no_sleep_no_jitter(monkeypatch):
    for mod in (Bashquest, Windowsquest):
        monkeypatch.setattr(mod.time, "sleep", lambda *_: None)
        monkeypatch.setattr(mod.random, "uniform", lambda a, b: 0)


def test_bashquest_simulate_terminal_boot_runs_without_error(capsys):
    Bashquest.simulate_terminal_boot()
    out = capsys.readouterr().out
    assert "System ready" in out


def test_windowsquest_simulate_windows_boot_runs_without_error(capsys):
    Windowsquest.simulate_windows_boot()
    out = capsys.readouterr().out
    assert "System ready" in out


def test_bashquest_execute_bash_command_timeout(monkeypatch):
    def _raise(*a, **kw):
        raise subprocess.TimeoutExpired(cmd="bash", timeout=5)

    monkeypatch.setattr(Bashquest.subprocess, "run", _raise)
    ok, output = Bashquest.execute_bash_command("sleep 999")
    assert ok is False
    assert "timed out" in output


def test_bashquest_execute_bash_command_unexpected_error(monkeypatch):
    def _raise(*a, **kw):
        raise OSError("bash not found")

    monkeypatch.setattr(Bashquest.subprocess, "run", _raise)
    ok, output = Bashquest.execute_bash_command("echo hi")
    assert ok is False
    assert "bash not found" in output


def test_bashquest_execute_bash_command_return_code_only_success(monkeypatch):
    class _FakeResult:
        returncode = 0
        stdout = "done"

    monkeypatch.setattr(Bashquest.subprocess, "run", lambda *a, **kw: _FakeResult())
    ok, output = Bashquest.execute_bash_command("true")
    assert ok is True
    assert output == "done"


def test_windowsquest_execute_windows_command_timeout(monkeypatch):
    def _raise(*a, **kw):
        raise subprocess.TimeoutExpired(cmd="cmd", timeout=10)

    monkeypatch.setattr(Windowsquest.subprocess, "run", _raise)
    ok, output = Windowsquest.execute_windows_command("ping -t localhost", "cmd")
    assert ok is False
    assert "timed out" in output


def test_windowsquest_execute_windows_command_cmd_not_found(monkeypatch):
    def _raise(*a, **kw):
        raise FileNotFoundError

    monkeypatch.setattr(Windowsquest.subprocess, "run", _raise)
    ok, output = Windowsquest.execute_windows_command("dir", "cmd")
    assert ok is False
    assert "CMD not available" in output


def test_windowsquest_execute_windows_command_powershell_not_found(monkeypatch):
    def _raise(*a, **kw):
        raise FileNotFoundError

    monkeypatch.setattr(Windowsquest.subprocess, "run", _raise)
    ok, output = Windowsquest.execute_windows_command("Get-Item .", "powershell")
    assert ok is False
    assert "PowerShell not found" in output


def test_windowsquest_execute_windows_command_unexpected_error(monkeypatch):
    def _raise(*a, **kw):
        raise OSError("boom")

    monkeypatch.setattr(Windowsquest.subprocess, "run", _raise)
    ok, output = Windowsquest.execute_windows_command("dir", "cmd")
    assert ok is False
    assert "boom" in output
