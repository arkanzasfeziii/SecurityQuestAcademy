"""CyberQuest wrapper — launches the standalone CyberQuest game."""
import subprocess
import sys
from pathlib import Path

ORIGINAL = Path(__file__).parent.parent / "standalone" / "Cyberquest.py"


def run() -> None:
    if not ORIGINAL.exists():
        print(f"[CyberQuest] Game file not found at: {ORIGINAL}")
        sys.exit(1)
    subprocess.run([sys.executable, str(ORIGINAL)], check=False)
