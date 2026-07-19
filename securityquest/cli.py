"""Main menu and game launcher for SecurityQuestAcademy."""

from __future__ import annotations

import importlib
import time

try:
    from rich import box
    from rich.console import Console
    from rich.table import Table
    from rich.text import Text

    HAS_RICH = True
except ImportError:
    HAS_RICH = False

from securityquest.config import ACADEMY_BANNER, GAMES

console = Console() if HAS_RICH else None


def _print(msg: str) -> None:
    if console:
        console.print(msg)
    else:
        print(msg)


def show_banner() -> None:
    if console:
        console.print(Text(ACADEMY_BANNER, style="bold bright_cyan"))
        console.print(Text("  Your journey to cybersecurity mastery starts here.\n", style="italic cyan"))
    else:
        print(ACADEMY_BANNER)


def show_boot() -> None:
    steps = [
        "Loading security modules...",
        "Initializing game engines...",
        "Calibrating challenge levels...",
        "Academy ready!",
    ]
    for msg in steps:
        _print(f"  > {msg}")
        time.sleep(0.1)
    print()


def show_menu() -> None:
    if not console:
        for g in GAMES:
            print(f"  {g['id']}. {g['name']} — {g['description']} ({g['levels']} levels)")
        print("\n  Enter quest number or Q to quit.\n")
        return

    table = Table(
        title="[bold bright_cyan]── SELECT YOUR QUEST ──[/bold bright_cyan]",
        box=box.ROUNDED,
        border_style="bright_cyan",
        header_style="bold bright_cyan",
        show_lines=True,
    )
    table.add_column("#", style="bold white", width=4, justify="center")
    table.add_column("Game", style="bold", width=16)
    table.add_column("Description", width=34)
    table.add_column("Levels", style="cyan", width=8, justify="center")
    table.add_column("Topics", style="dim", width=38)

    for g in GAMES:
        table.add_row(
            str(g["id"]),
            f"[{g['color']}]{g['name']}[/{g['color']}]",
            g["description"],
            g["levels"],
            g["topics"],
        )
    console.print(table)
    console.print("\n  [dim]Enter the number of the quest, or [bold]Q[/bold] to quit.[/dim]\n")


def launch_game(game: dict) -> None:
    _print(f"\n  Launching {game['name']}...\n")
    time.sleep(0.3)
    try:
        mod = importlib.import_module(game["module"])
        mod.run()
    except ImportError as e:
        _print(f"  Failed to load {game['name']}: {e}")
    except Exception as e:
        _print(f"  Error in {game['name']}: {e}")


def main() -> None:
    show_banner()
    show_boot()

    while True:
        show_menu()
        try:
            choice = input("  Select quest [1-7 / Q]: ").strip().upper()
        except (EOFError, KeyboardInterrupt):
            _print("\n  Goodbye, hacker. Keep learning!\n")
            break

        if choice == "Q":
            _print("\n  Goodbye, hacker. Keep learning!\n")
            break

        if choice.isdigit() and 1 <= int(choice) <= len(GAMES):
            launch_game(GAMES[int(choice) - 1])
            _print("\n  Returned to SecurityQuestAcademy main menu.\n")
        else:
            _print(f"  Invalid choice: {choice!r}. Enter 1-{len(GAMES)} or Q.\n")
