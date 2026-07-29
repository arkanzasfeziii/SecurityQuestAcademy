"""Tests for `python -m securityquest` — securityquest/__main__.py runs
main() at import time, so it can't be safely imported in-process; drive it
as a real subprocess instead, the same way CI's build job verifies it."""

import subprocess
import sys

import pytest


@pytest.mark.timeout(30)
def test_module_entry_point_exits_cleanly_on_closed_stdin():
    result = subprocess.run(
        [sys.executable, "-m", "securityquest"],
        stdin=subprocess.DEVNULL,
        capture_output=True,
        text=True,
        timeout=20,
    )
    assert result.returncode == 0
    assert "Goodbye" in result.stdout
