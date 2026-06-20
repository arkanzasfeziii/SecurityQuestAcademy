#!/usr/bin/env python3
"""
SecurityQuestAcademy — shared base engine
All 7 quest games share this infrastructure: progress tracking,
save/load, rank system, achievement checks, and two execution
engines (Python exec and Cisco command-match).
"""

from __future__ import annotations

import io
import json
import os
import random
import subprocess
import sys
import tempfile
import time
from contextlib import redirect_stdout
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.prompt import Confirm, Prompt
    from rich.syntax import Syntax
    from rich.table import Table
    from rich import box
except ImportError:
    os.system(f"{sys.executable} -m pip install rich --quiet")
    from rich.console import Console
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.prompt import Confirm, Prompt
    from rich.syntax import Syntax
    from rich.table import Table
    from rich import box

console = Console()


# ---------------------------------------------------------------------------
# Player progress
# ---------------------------------------------------------------------------

@dataclass
class PlayerProgress:
    current_level: int = 1
    completed_levels: List[int] = field(default_factory=list)
    total_points: int = 0
    achievements: List[str] = field(default_factory=list)
    start_date: str = field(default_factory=lambda: datetime.now().isoformat())
    last_played: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict:
        return {
            "current_level": self.current_level,
            "completed_levels": self.completed_levels,
            "total_points": self.total_points,
            "achievements": self.achievements,
            "start_date": self.start_date,
            "last_played": self.last_played,
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "PlayerProgress":
        return cls(
            current_level=data.get("current_level", 1),
            completed_levels=data.get("completed_levels", []),
            total_points=data.get("total_points", 0),
            achievements=data.get("achievements", []),
            start_date=data.get("start_date", datetime.now().isoformat()),
            last_played=data.get("last_played", datetime.now().isoformat()),
        )


def save_progress(progress: PlayerProgress, save_file: Path) -> None:
    try:
        with open(save_file, "w") as f:
            json.dump(progress.to_dict(), f, indent=2)
    except Exception as e:
        console.print(f"[red]Save error: {e}[/]")


def load_progress(save_file: Path) -> PlayerProgress:
    if save_file.exists():
        try:
            with open(save_file, "r") as f:
                return PlayerProgress.from_dict(json.load(f))
        except Exception:
            pass
    return PlayerProgress()


# ---------------------------------------------------------------------------
# Ranks & stats
# ---------------------------------------------------------------------------

def get_rank(level: int, ranks: List[Tuple]) -> Tuple[str, str]:
    for min_level, rank_name, description in reversed(ranks):
        if level >= min_level:
            return rank_name, description
    return ranks[0][1], ranks[0][2]


def show_stats(progress: PlayerProgress, ranks: List[Tuple], colors: Dict, title: str = "Your Stats") -> None:
    rank_name, rank_desc = get_rank(progress.current_level, ranks)
    t = Table(title=title, box=box.DOUBLE_EDGE, border_style=colors["primary"])
    t.add_column("Stat", style=colors["secondary"], no_wrap=True)
    t.add_column("Value", style=colors.get("hacker", "bright_green"))
    t.add_row("Current Level", f"{progress.current_level}/100")
    t.add_row("Completed", str(len(progress.completed_levels)))
    t.add_row("Total Points", f"{progress.total_points:,}")
    t.add_row("Rank", rank_name)
    t.add_row("Rank Info", rank_desc)
    t.add_row("Achievements", str(len(progress.achievements)))
    console.print(t)


def check_achievements(
    progress: PlayerProgress,
    colors: Dict,
    thresholds: List[Tuple],
) -> None:
    for threshold, name, desc in thresholds:
        if len(progress.completed_levels) >= threshold and name not in progress.achievements:
            progress.achievements.append(name)
            console.print(f"\n[{colors['success']}]🏆 ACHIEVEMENT UNLOCKED: {name}[/]")
            console.print(f"[{colors['info']}]{desc}[/]\n")
            time.sleep(1.5)


# ---------------------------------------------------------------------------
# Execution engines
# ---------------------------------------------------------------------------

def _exec_python(code: str) -> Tuple[bool, str]:
    buf = io.StringIO()
    try:
        with redirect_stdout(buf):
            exec(code, {})  # noqa: S102
        return True, buf.getvalue().strip()
    except Exception as e:
        return False, f"ERROR: {e}"


def eval_python_level(user_code: str, test_code: str) -> Tuple[bool, str, str]:
    ok, user_out = _exec_python(user_code)
    if not ok:
        return False, user_out, ""
    _, expected_out = _exec_python(test_code)
    return user_out == expected_out, user_out, expected_out


def execute_bash(command: str, expected_output: Optional[str] = None) -> Tuple[bool, str]:
    script_path = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".sh", delete=False) as f:
            f.write("#!/bin/bash\nset +e\n" + command + "\n")
            script_path = f.name
        os.chmod(script_path, 0o755)
        result = subprocess.run(["bash", script_path], capture_output=True, text=True, timeout=5)
        output = result.stdout.strip()
        if expected_output is not None:
            return output == expected_output.strip(), output
        return result.returncode == 0, output
    except subprocess.TimeoutExpired:
        return False, "Command timed out"
    except Exception as e:
        return False, str(e)
    finally:
        if script_path and os.path.exists(script_path):
            os.unlink(script_path)


def match_cisco_command(user_input: str, accepted: List[str]) -> bool:
    normalized = " ".join(user_input.strip().lower().split())
    for a in accepted:
        if normalized == " ".join(a.strip().lower().split()):
            return True
    return False


# ---------------------------------------------------------------------------
# Level displayer
# ---------------------------------------------------------------------------

def show_level_info(level_data: Dict, colors: Dict) -> None:
    color_h = colors.get("hacker", colors["primary"])
    console.print(Panel(
        f"[{color_h}]LEVEL {level_data['id']}: {level_data['title'].upper()}[/]\n\n"
        f"[{colors['info']}]Category:[/] [{colors['secondary']}]{level_data.get('category','').upper()}[/]   "
        f"[{colors['info']}]Points:[/] [{colors['success']}]{level_data['points']}[/]\n\n"
        f"[{colors['warning']}]Description:[/]\n{level_data['description']}\n\n"
        f"[{colors['warning']}]Challenge:[/]\n{level_data['challenge']}",
        border_style=colors["primary"],
        box=box.DOUBLE,
    ))


# ---------------------------------------------------------------------------
# Play-level implementations
# ---------------------------------------------------------------------------

def play_python_level(level_data: Dict, progress: PlayerProgress, colors: Dict) -> bool:
    show_level_info(level_data, colors)
    console.print(f"\n[{colors['info']}]Type your Python code line by line. Type [bold]done[/] to submit, [bold]hint[/] for help, [bold]skip[/] to skip.[/]\n")
    lines: List[str] = []
    while True:
        try:
            line = Prompt.ask(f"[{colors.get('hacker', colors['primary'])}]>>>")
        except (KeyboardInterrupt, EOFError):
            console.print(f"\n[{colors['warning']}]Interrupted.[/]")
            return False
        cmd = line.strip().lower()
        if cmd == "done":
            break
        if cmd == "hint":
            console.print(f"[{colors['warning']}]💡 {level_data['hint']}[/]")
            continue
        if cmd == "skip":
            console.print(f"[{colors['warning']}]Skipped (no points).[/]")
            return False
        if cmd == "solution":
            console.print(f"[{colors['error']}]No cheating! Use the hint instead.[/]")
            continue
        lines.append(line)

    user_code = "\n".join(lines)
    if not user_code.strip():
        console.print(f"[{colors['error']}]No code entered.[/]")
        return False

    console.print(f"\n[{colors['info']}]Your code:[/]")
    console.print(Syntax(user_code, "python", theme="monokai", line_numbers=True))
    console.print(f"\n[{colors['warning']}]Running…[/]")
    time.sleep(0.4)

    success, user_out, expected_out = eval_python_level(user_code, level_data["test_code"])

    if "ERROR:" in user_out:
        console.print(f"[{colors['error']}]❌ Code error: {user_out}[/]")
        return False

    if success:
        _level_pass(level_data, progress, colors)
        return True
    else:
        console.print(f"[{colors['error']}]❌ Output mismatch.[/]")
        console.print(f"[{colors['info']}]Expected:[/] {expected_out}")
        console.print(f"[{colors['info']}]Got:     [/] {user_out}")
        return False


def play_cisco_level(level_data: Dict, progress: PlayerProgress, colors: Dict) -> bool:
    show_level_info(level_data, colors)
    console.print(f"\n[{colors['info']}]Type the Cisco IOS command. [bold]hint[/] for help, [bold]skip[/] to skip.[/]\n")
    while True:
        try:
            user_input = Prompt.ask(f"[{colors.get('hacker', colors['primary'])}]Router#")
        except (KeyboardInterrupt, EOFError):
            return False
        cmd = user_input.strip().lower()
        if cmd == "hint":
            console.print(f"[{colors['warning']}]💡 {level_data['hint']}[/]")
            continue
        if cmd == "skip":
            console.print(f"[{colors['warning']}]Skipped.[/]")
            return False
        break

    console.print(f"\n[{colors['info']}]Your command:[/] [bold]{user_input}[/]")
    time.sleep(0.4)

    accepted = level_data.get("accepted", [level_data["solution"]])
    if match_cisco_command(user_input, accepted):
        _level_pass(level_data, progress, colors)
        return True
    else:
        console.print(f"[{colors['error']}]❌ Not quite right.[/]")
        console.print(f"[{colors['info']}]Expected something like:[/] [bold]{level_data['solution']}[/]")
        return False


def play_bash_level(level_data: Dict, progress: PlayerProgress, colors: Dict) -> bool:
    show_level_info(level_data, colors)
    console.print(f"\n[{colors['info']}]Enter your bash command. [bold]hint[/] for help, [bold]skip[/] to skip.[/]\n")
    while True:
        try:
            user_input = Prompt.ask(f"[{colors.get('terminal', colors['primary'])}]bash$")
        except (KeyboardInterrupt, EOFError):
            return False
        cmd = user_input.strip().lower()
        if cmd == "hint":
            console.print(f"[{colors['warning']}]💡 {level_data['hint']}[/]")
            continue
        if cmd == "skip":
            console.print(f"[{colors['warning']}]Skipped.[/]")
            return False
        break

    console.print(f"\n[{colors['info']}]Command:[/]")
    console.print(Syntax(user_input, "bash", theme="monokai"))
    console.print(f"\n[{colors['warning']}]Executing…[/]")
    time.sleep(0.4)

    success, output = execute_bash(user_input, level_data.get("expected_output"))
    if success:
        if output:
            console.print(f"[{colors['info']}]Output:[/] {output}")
        _level_pass(level_data, progress, colors)
        return True
    else:
        console.print(f"[{colors['error']}]❌ Incorrect.[/]")
        if output:
            console.print(f"[{colors['info']}]Got:[/] {output}")
        if level_data.get("expected_output"):
            console.print(f"[{colors['info']}]Expected:[/] {level_data['expected_output']}")
        return False


def _level_pass(level_data: Dict, progress: PlayerProgress, colors: Dict) -> None:
    console.print(f"\n[{colors['success']}]✅ Correct! Level complete![/]")
    console.print(f"[{colors['info']}]{level_data['explanation']}[/]")
    console.print(f"[{colors['success']}]+{level_data['points']} points![/]")
    if level_data["id"] not in progress.completed_levels:
        progress.completed_levels.append(level_data["id"])
        progress.total_points += level_data["points"]


# ---------------------------------------------------------------------------
# Main game runner (template — all 7 games call this)
# ---------------------------------------------------------------------------

ENGINE_MAP = {
    "python": play_python_level,
    "cisco":  play_cisco_level,
    "bash":   play_bash_level,
}


def run_game(
    levels: List[Dict],
    ranks: List[Tuple],
    colors: Dict,
    save_file: Path,
    game_name: str,
    show_banner_fn: Callable,
    simulate_boot_fn: Callable,
    engine: str,
    achievement_thresholds: List[Tuple],
) -> None:
    play_level_fn = ENGINE_MAP[engine]
    progress = load_progress(save_file)

    try:
        console.clear()
        simulate_boot_fn()
        time.sleep(0.5)
    except Exception:
        pass

    while True:
        console.clear()
        show_banner_fn()
        rank_name, _ = get_rank(progress.current_level, ranks)
        console.print(f"\n[{colors.get('hacker', colors['primary'])}]Welcome back, {rank_name}![/]\n")

        t = Table(box=box.ROUNDED, border_style=colors["secondary"])
        t.add_column("Option", style=colors["primary"], no_wrap=True)
        t.add_column("Description", style=colors["info"])
        t.add_row("1", "Continue Journey")
        t.add_row("2", "View Stats")
        t.add_row("3", "Jump to Level")
        t.add_row("4", "Achievements")
        t.add_row("5", "Reset Progress")
        t.add_row("6", "Exit to Academy")
        console.print(t)

        choice = Prompt.ask(
            f"\n[{colors['secondary']}]Choose", choices=["1", "2", "3", "4", "5", "6"]
        )

        if choice == "1":
            while progress.current_level <= len(levels):
                console.clear()
                level_data = levels[progress.current_level - 1]
                if play_level_fn(level_data, progress, colors):
                    progress.current_level += 1
                    progress.last_played = datetime.now().isoformat()
                    save_progress(progress, save_file)
                    check_achievements(progress, colors, achievement_thresholds)
                    if progress.current_level > len(levels):
                        console.print(f"\n[{colors.get('hacker', colors['primary'])}]🎉 YOU COMPLETED ALL 100 LEVELS! 🎉[/]")
                        console.print(f"[{colors['success']}]Total Points: {progress.total_points:,}[/]")
                        input("\nPress Enter to return…")
                        break
                    if not Confirm.ask(f"\n[{colors['success']}]Continue to next level?"):
                        break
                else:
                    if not Confirm.ask(f"\n[{colors['warning']}]Try again?"):
                        break

        elif choice == "2":
            console.clear()
            show_stats(progress, ranks, colors, f"{game_name} — Stats")
            input("\nPress Enter…")

        elif choice == "3":
            max_lvl = max(progress.completed_levels) + 1 if progress.completed_levels else 1
            try:
                n = int(Prompt.ask(f"Jump to level (1-{min(max_lvl, 100)})"))
                if 1 <= n <= min(max_lvl, len(levels)):
                    progress.current_level = n
                    save_progress(progress, save_file)
                else:
                    console.print(f"[{colors['error']}]Out of range.[/]")
                    time.sleep(1.5)
            except ValueError:
                pass

        elif choice == "4":
            console.clear()
            if progress.achievements:
                t2 = Table(title="🏆 Achievements", box=box.DOUBLE_EDGE, border_style=colors["success"])
                t2.add_column("Achievement", style=colors.get("hacker", colors["primary"]))
                for a in progress.achievements:
                    t2.add_row(a)
                console.print(t2)
            else:
                console.print(f"[{colors['info']}]No achievements yet.[/]")
            input("\nPress Enter…")

        elif choice == "5":
            if Confirm.ask(f"[{colors['error']}]Reset ALL progress?"):
                progress = PlayerProgress()
                save_progress(progress, save_file)
                console.print(f"[{colors['success']}]Reset.[/]")
                time.sleep(1.5)

        elif choice == "6":
            break
