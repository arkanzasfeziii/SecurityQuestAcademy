"""BashQuest wrapper — launches the standalone BashQuest game."""

import subprocess
import sys
from pathlib import Path

ORIGINAL = Path(__file__).parent.parent / "standalone" / "Bashquest.py"


def run() -> None:
    if not ORIGINAL.exists():
        print(f"[BashQuest] Game file not found at: {ORIGINAL}")
        sys.exit(1)
    subprocess.run([sys.executable, str(ORIGINAL)], check=False)
