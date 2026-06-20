#!/usr/bin/env python3
"""SecurityQuestAcademy — Unified launcher for all security training games."""
import sys
import time
from pathlib import Path

try:
    from rich.console import Console
    from rich.text import Text
    from rich.panel import Panel
    from rich.table import Table
    from rich import box
except ImportError:
    print("Missing dependency: pip install rich")
    sys.exit(1)

# ── Add package root to path ──────────────────────────────────────────────────
sys.path.insert(0, str(Path(__file__).parent))

con = Console()

ACADEMY_BANNER = """
╔═══════════════════════════════════════════════════════════════════╗
║   ███████╗███████╗ ██████╗ ██╗   ██╗██████╗ ██╗████████╗██╗   ██╗║
║   ██╔════╝██╔════╝██╔════╝ ██║   ██║██╔══██╗██║╚══██╔══╝╚██╗ ██╔╝║
║   ███████╗█████╗  ██║      ██║   ██║██████╔╝██║   ██║    ╚████╔╝ ║
║   ╚════██║██╔══╝  ██║      ██║   ██║██╔══██╗██║   ██║     ╚██╔╝  ║
║   ███████║███████╗╚██████╗ ╚██████╔╝██║  ██║██║   ██║      ██║   ║
║   ╚══════╝╚══════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝   ╚═╝      ╚═╝   ║
║              Q U E S T   A C A D E M Y                            ║
╚═══════════════════════════════════════════════════════════════════╝
"""

GAMES = [
    {
        "id": 1,
        "name": "CyberQuest",
        "module": "games.cyberquest",
        "color": "bright_cyan",
        "icon": "🖥️",
        "description": "Python & Linux Security Fundamentals",
        "levels": "100",
        "topics": "Linux, Python, Networking, System Security",
    },
    {
        "id": 2,
        "name": "BashQuest",
        "module": "games.bashquest",
        "color": "bright_yellow",
        "icon": "🐚",
        "description": "Bash Scripting & Shell Security",
        "levels": "100",
        "topics": "Bash, Shell Scripting, Automation, Security Scripts",
    },
    {
        "id": 3,
        "name": "WindowsQuest",
        "module": "games.windowsquest",
        "color": "bright_blue",
        "icon": "🪟",
        "description": "Windows Security & PowerShell",
        "levels": "100",
        "topics": "PowerShell, Active Directory, Windows Hardening, Forensics",
    },
    {
        "id": 4,
        "name": "CiscoQuest",
        "module": "games.ciscoquest",
        "color": "bright_white",
        "icon": "🌐",
        "description": "Cisco IOS Networking & Security",
        "levels": "100",
        "topics": "Routing, Switching, ACLs, VPNs, Firewalls, IOS Commands",
    },
    {
        "id": 5,
        "name": "CryptoQuest",
        "module": "games.cryptoquest",
        "color": "bright_magenta",
        "icon": "🔐",
        "description": "Cryptography from Classical to Modern",
        "levels": "100",
        "topics": "Classical Ciphers, AES, RSA, Hashing, TLS, PKI",
    },
    {
        "id": 6,
        "name": "ReverseQuest",
        "module": "games.reversequest",
        "color": "bright_red",
        "icon": "🔍",
        "description": "Reverse Engineering & Malware Analysis",
        "levels": "100",
        "topics": "x86 ASM, ELF/PE, GDB, IDA, Malware, Exploitation, Fuzzing",
    },
    {
        "id": 7,
        "name": "WebHackQuest",
        "module": "games.webhackquest",
        "color": "bright_green",
        "icon": "🕸️",
        "description": "Web Application Security & Pentesting",
        "levels": "100",
        "topics": "XSS, SQLi, SSRF, SSTI, JWT, OAuth, OWASP Top 10",
    },
]


def show_academy_banner() -> None:
    con.print(Text(ACADEMY_BANNER, style="bold bright_cyan"))
    con.print(Text("  Your journey to cybersecurity mastery starts here.\n", style="italic cyan"))


def show_academy_boot() -> None:
    steps = [
        ("Loading security modules...",   0.12),
        ("Initializing game engines...",  0.10),
        ("Calibrating challenge levels...", 0.10),
        ("Establishing secure channel...", 0.12),
        ("Academy ready!",                0.08),
    ]
    for msg, delay in steps:
        con.print(f"  [bright_cyan]>[/bright_cyan] {msg}")
        time.sleep(delay)
    con.print()


def show_game_menu() -> None:
    table = Table(
        title="[bold bright_cyan]── SELECT YOUR QUEST ──[/bold bright_cyan]",
        box=box.ROUNDED,
        border_style="bright_cyan",
        header_style="bold bright_cyan",
        show_lines=True,
    )
    table.add_column("#",        style="bold white",   width=4,  justify="center")
    table.add_column("Game",     style="bold",         width=16)
    table.add_column("Description",                    width=34)
    table.add_column("Levels",   style="cyan",         width=8,  justify="center")
    table.add_column("Topics",   style="dim",          width=38)

    for g in GAMES:
        table.add_row(
            str(g["id"]),
            f"[{g['color']}]{g['icon']} {g['name']}[/{g['color']}]",
            g["description"],
            g["levels"],
            g["topics"],
        )

    con.print(table)
    con.print()
    con.print("  [dim]Enter the number of the quest you want to play, or [bold]Q[/bold] to quit.[/dim]")
    con.print()


def launch_game(game: dict) -> None:
    con.print(f"\n  [bold {game['color']}]Launching {game['name']}...[/bold {game['color']}]\n")
    time.sleep(0.3)
    try:
        import importlib
        mod = importlib.import_module(game["module"])
        mod.run()
    except ImportError as e:
        con.print(f"  [red]Failed to load {game['name']}: {e}[/red]")
        con.print(f"  [yellow]Make sure all dependencies are installed: pip install -r requirements.txt[/yellow]")
    except Exception as e:
        con.print(f"  [red]Error in {game['name']}: {e}[/red]")


def main() -> None:
    show_academy_banner()
    show_academy_boot()

    while True:
        show_game_menu()
        try:
            choice = input("  Select quest [1-7 / Q]: ").strip().upper()
        except (EOFError, KeyboardInterrupt):
            con.print("\n\n  [bold cyan]Goodbye, hacker. Keep learning![/bold cyan]\n")
            break

        if choice == "Q":
            con.print("\n  [bold cyan]Goodbye, hacker. Keep learning![/bold cyan]\n")
            break

        if choice.isdigit() and 1 <= int(choice) <= len(GAMES):
            game = GAMES[int(choice) - 1]
            launch_game(game)
            con.print(f"\n  [dim]Returned to SecurityQuestAcademy main menu.[/dim]\n")
        else:
            con.print(f"  [red]Invalid choice: {choice!r}. Enter 1-{len(GAMES)} or Q.[/red]\n")


if __name__ == "__main__":
    main()
