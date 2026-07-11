#!/usr/bin/env python3
"""
BashQuest: Linux Terminal Mastery
A comprehensive game to learn Bash scripting and Linux commands from absolute beginner to expert.
Author: arkanzasfeziii
"""

import json
import os
import random
import subprocess
import sys
import tempfile
import time
from datetime import datetime
from pathlib import Path

# === Rich imports for beautiful CLI ===
try:
    from rich import box
    from rich.console import Console
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.prompt import Confirm, Prompt
    from rich.syntax import Syntax
    from rich.table import Table
except ImportError:
    print("Installing required dependencies...")
    os.system(f"{sys.executable} -m pip install rich --quiet")
    from rich import box
    from rich.console import Console
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.prompt import Confirm, Prompt
    from rich.syntax import Syntax
    from rich.table import Table

console = Console()

# === Constants ===
SAVE_FILE = Path.home() / ".bashquest_save.json"
VERSION = "1.0.0"

# Terminal color scheme
COLORS = {
    "primary": "bright_blue",
    "secondary": "bright_yellow",
    "success": "bright_green",
    "error": "bright_red",
    "warning": "yellow",
    "info": "cyan",
    "terminal": "bright_green",
}

# === Rank System ===
RANKS = [
    (0, "🐣 Terminal Newbie", "You're taking your first steps in the terminal"),
    (5, "📁 File Explorer", "Learning to navigate directories"),
    (10, "📝 Text Wizard", "Mastering text manipulation"),
    (15, "🔍 Command Seeker", "Discovering powerful commands"),
    (20, "⚙️ Script Apprentice", "Writing basic scripts"),
    (25, "🔧 Tool Crafter", "Building useful tools"),
    (30, "🌊 Stream Master", "Mastering pipes and redirects"),
    (35, "🎯 Regex Ninja", "Pattern matching expert"),
    (40, "📊 Process Watcher", "Understanding system processes"),
    (45, "🔐 Permission Guardian", "Security and permissions expert"),
    (50, "🌐 Network Scout", "Network commands mastery"),
    (55, "💾 Data Architect", "Advanced file operations"),
    (60, "⚡ Performance Tuner", "Optimization techniques"),
    (65, "🎭 Variable Virtuoso", "Advanced scripting concepts"),
    (70, "🔄 Loop Legend", "Control flow mastery"),
    (75, "🛡️ Error Handler", "Robust script writing"),
    (80, "📦 Package Master", "System administration"),
    (85, "🚀 Automation Expert", "Complete workflow automation"),
    (90, "👑 Shell Samurai", "Advanced shell techniques"),
    (95, "💎 Terminal Sensei", "Teaching others"),
    (100, "🏆 Bash Grandmaster", "The ultimate achievement"),
]

# === Level Definitions ===
LEVELS = [
    # === BEGINNER TIER (1-20): Basic Commands ===
    {
        "id": 1,
        "title": "Echo Hello World",
        "description": "Your first command: display text on the terminal.",
        "challenge": "Use the echo command to print: Hello, BashQuest!",
        "hint": "echo 'text here'",
        "solution": "echo 'Hello, BashQuest!'",
        "expected_output": "Hello, BashQuest!",
        "explanation": "echo displays text to the terminal. It's the most basic output command!",
        "points": 10,
        "category": "basics"
    },
    {
        "id": 2,
        "title": "Present Working Directory",
        "description": "Find out where you are in the filesystem.",
        "challenge": "Use the command that prints the current working directory.",
        "hint": "pwd stands for Print Working Directory",
        "solution": "pwd",
        "expected_output": None,  # Output varies by system
        "check_command": True,
        "explanation": "pwd shows your current location in the directory tree.",
        "points": 10,
        "category": "basics"
    },
    {
        "id": 3,
        "title": "List Files",
        "description": "See what's in your current directory.",
        "challenge": "List all files in the current directory.",
        "hint": "ls lists directory contents",
        "solution": "ls",
        "expected_output": None,
        "check_command": True,
        "explanation": "ls shows files and directories. Use ls -l for detailed view, ls -a to show hidden files.",
        "points": 15,
        "category": "basics"
    },
    {
        "id": 4,
        "title": "Create a Directory",
        "description": "Make a new folder.",
        "challenge": "Create a directory named 'testdir' using mkdir.",
        "hint": "mkdir directory_name",
        "solution": "mkdir testdir",
        "expected_output": None,
        "check_command": True,
        "explanation": "mkdir creates new directories. Use -p to create parent directories too.",
        "points": 15,
        "category": "basics"
    },
    {
        "id": 5,
        "title": "Change Directory",
        "description": "Navigate to different folders.",
        "challenge": "Change into the 'testdir' directory you just created.",
        "hint": "cd directory_name",
        "solution": "cd testdir",
        "expected_output": None,
        "check_command": True,
        "explanation": "cd changes your current directory. Use 'cd ..' to go up one level, 'cd ~' for home.",
        "points": 20,
        "category": "basics"
    },
    {
        "id": 6,
        "title": "Create a File",
        "description": "Make a new empty file.",
        "challenge": "Create an empty file named 'test.txt' using touch.",
        "hint": "touch filename",
        "solution": "touch test.txt",
        "expected_output": None,
        "check_command": True,
        "explanation": "touch creates new empty files or updates timestamps of existing files.",
        "points": 20,
        "category": "basics"
    },
    {
        "id": 7,
        "title": "Write to a File",
        "description": "Put text into a file.",
        "challenge": "Write 'Hello Bash' into a file called output.txt using echo and redirection.",
        "hint": "Use > to redirect output to a file",
        "solution": "echo 'Hello Bash' > output.txt",
        "expected_output": None,
        "check_command": True,
        "explanation": "> redirects output to a file (overwrites). Use >> to append instead.",
        "points": 25,
        "category": "basics"
    },
    {
        "id": 8,
        "title": "Read a File",
        "description": "Display file contents.",
        "challenge": "Display the contents of output.txt using cat.",
        "hint": "cat filename",
        "solution": "cat output.txt",
        "expected_output": "Hello Bash",
        "explanation": "cat displays file contents. For large files, use less or more for paging.",
        "points": 25,
        "category": "basics"
    },
    {
        "id": 9,
        "title": "Copy Files",
        "description": "Duplicate files.",
        "challenge": "Copy output.txt to backup.txt using cp.",
        "hint": "cp source destination",
        "solution": "cp output.txt backup.txt",
        "expected_output": None,
        "check_command": True,
        "explanation": "cp copies files. Use -r for directories, -i to prompt before overwriting.",
        "points": 30,
        "category": "basics"
    },
    {
        "id": 10,
        "title": "Move/Rename Files",
        "description": "Relocate or rename files.",
        "challenge": "Rename backup.txt to old.txt using mv.",
        "hint": "mv old_name new_name",
        "solution": "mv backup.txt old.txt",
        "expected_output": None,
        "check_command": True,
        "explanation": "mv moves or renames files. It can also move files between directories.",
        "points": 30,
        "category": "basics"
    },
    {
        "id": 11,
        "title": "Remove Files",
        "description": "Delete files carefully!",
        "challenge": "Remove the file old.txt using rm.",
        "hint": "rm filename (be careful!)",
        "solution": "rm old.txt",
        "expected_output": None,
        "check_command": True,
        "explanation": "rm deletes files permanently! Use -i for confirmation, -r for directories.",
        "points": 35,
        "category": "basics"
    },
    {
        "id": 12,
        "title": "Count Lines",
        "description": "Count lines in a file.",
        "challenge": "Count the number of lines in output.txt using wc -l.",
        "hint": "wc -l filename",
        "solution": "wc -l output.txt",
        "expected_output": "1 output.txt",
        "explanation": "wc counts lines (-l), words (-w), and characters (-c) in files.",
        "points": 35,
        "category": "basics"
    },
    {
        "id": 13,
        "title": "Find Command Location",
        "description": "Locate where commands are stored.",
        "challenge": "Find the location of the 'ls' command using which.",
        "hint": "which command_name",
        "solution": "which ls",
        "expected_output": None,
        "check_command": True,
        "explanation": "which shows the full path of commands. Useful for checking what you'll execute.",
        "points": 40,
        "category": "basics"
    },
    {
        "id": 14,
        "title": "Command Manual",
        "description": "Read command documentation.",
        "challenge": "Open the manual page for the ls command.",
        "hint": "man command_name",
        "solution": "man ls",
        "expected_output": None,
        "check_command": True,
        "explanation": "man shows manual pages. Press 'q' to quit. Use 'man man' to learn about man!",
        "points": 40,
        "category": "basics"
    },
    {
        "id": 15,
        "title": "Disk Usage",
        "description": "Check file and directory sizes.",
        "challenge": "Show disk usage of the current directory in human-readable format.",
        "hint": "du -h",
        "solution": "du -h",
        "expected_output": None,
        "check_command": True,
        "explanation": "du shows disk usage. Use -h for human-readable sizes, -s for summary.",
        "points": 45,
        "category": "basics"
    },
    {
        "id": 16,
        "title": "Disk Space",
        "description": "Check available disk space.",
        "challenge": "Show filesystem disk space in human-readable format.",
        "hint": "df -h",
        "solution": "df -h",
        "expected_output": None,
        "check_command": True,
        "explanation": "df shows free disk space on filesystems. Essential for monitoring.",
        "points": 45,
        "category": "basics"
    },
    {
        "id": 17,
        "title": "Head of File",
        "description": "View the beginning of files.",
        "challenge": "Display the first 5 lines of /etc/passwd using head.",
        "hint": "head -n 5 filename",
        "solution": "head -n 5 /etc/passwd",
        "expected_output": None,
        "check_command": True,
        "explanation": "head shows the first lines of a file. Default is 10 lines.",
        "points": 50,
        "category": "basics"
    },
    {
        "id": 18,
        "title": "Tail of File",
        "description": "View the end of files.",
        "challenge": "Display the last 5 lines of /etc/passwd using tail.",
        "hint": "tail -n 5 filename",
        "solution": "tail -n 5 /etc/passwd",
        "expected_output": None,
        "check_command": True,
        "explanation": "tail shows the last lines. Use -f to follow files (great for logs!).",
        "points": 50,
        "category": "basics"
    },
    {
        "id": 19,
        "title": "Search in Files",
        "description": "Find text patterns in files.",
        "challenge": "Search for 'root' in /etc/passwd using grep.",
        "hint": "grep 'pattern' filename",
        "solution": "grep 'root' /etc/passwd",
        "expected_output": None,
        "check_command": True,
        "explanation": "grep searches for patterns. Use -i for case-insensitive, -r for recursive.",
        "points": 55,
        "category": "basics"
    },
    {
        "id": 20,
        "title": "Pipe Commands",
        "description": "Chain commands together.",
        "challenge": "List files and count them using ls | wc -l.",
        "hint": "command1 | command2",
        "solution": "ls | wc -l",
        "expected_output": None,
        "check_command": True,
        "explanation": "Pipes (|) send output of one command to another. Very powerful!",
        "points": 55,
        "category": "basics"
    },

    # === INTERMEDIATE TIER (21-50): Scripting Basics ===
    {
        "id": 21,
        "title": "Variables",
        "description": "Store data in variables.",
        "challenge": "Create a variable NAME='Hacker' and echo it with $NAME.",
        "hint": "variable=value (no spaces!), then echo $variable",
        "solution": "NAME='Hacker'; echo $NAME",
        "expected_output": "Hacker",
        "explanation": "Variables store values. Access with $. No spaces around =!",
        "points": 60,
        "category": "scripting"
    },
    {
        "id": 22,
        "title": "Command Substitution",
        "description": "Use command output as a variable.",
        "challenge": "Store the current date in a variable and echo it: TODAY=$(date).",
        "hint": "variable=$(command)",
        "solution": "TODAY=$(date); echo $TODAY",
        "expected_output": None,
        "check_command": True,
        "explanation": "$() captures command output. Backticks `` also work but $() is preferred.",
        "points": 65,
        "category": "scripting"
    },
    {
        "id": 23,
        "title": "If Statement",
        "description": "Conditional execution.",
        "challenge": "Write: if [ 5 -gt 3 ]; then echo 'Greater'; fi",
        "hint": "if [ condition ]; then commands; fi",
        "solution": "if [ 5 -gt 3 ]; then echo 'Greater'; fi",
        "expected_output": "Greater",
        "explanation": "if tests conditions. -gt is greater than, -eq equals, -lt less than.",
        "points": 70,
        "category": "scripting"
    },
    {
        "id": 24,
        "title": "For Loop",
        "description": "Iterate over items.",
        "challenge": "Loop through 1 2 3 and echo each: for i in 1 2 3; do echo $i; done",
        "hint": "for var in list; do commands; done",
        "solution": "for i in 1 2 3; do echo $i; done",
        "expected_output": "1\n2\n3",
        "explanation": "for loops iterate over lists or ranges. Very useful for automation!",
        "points": 75,
        "category": "scripting"
    },
    {
        "id": 25,
        "title": "While Loop",
        "description": "Loop while condition is true.",
        "challenge": "Count from 1 to 3: i=1; while [ $i -le 3 ]; do echo $i; i=$((i+1)); done",
        "hint": "while [ condition ]; do commands; done",
        "solution": "i=1; while [ $i -le 3 ]; do echo $i; i=$((i+1)); done",
        "expected_output": "1\n2\n3",
        "explanation": "while loops continue while condition is true. Great for monitoring!",
        "points": 80,
        "category": "scripting"
    },
    {
        "id": 26,
        "title": "Arithmetic",
        "description": "Perform math operations.",
        "challenge": "Calculate 10 + 5 and echo the result: echo $((10 + 5))",
        "hint": "echo $((expression))",
        "solution": "echo $((10 + 5))",
        "expected_output": "15",
        "explanation": "$(()) performs arithmetic. Supports +, -, *, /, %, **.",
        "points": 85,
        "category": "scripting"
    },
    {
        "id": 27,
        "title": "String Length",
        "description": "Get length of strings.",
        "challenge": "Get length of 'hello': TEXT='hello'; echo ${#TEXT}",
        "hint": "${#variable}",
        "solution": "TEXT='hello'; echo ${#TEXT}",
        "expected_output": "5",
        "explanation": "${#var} returns string length. Useful for validation!",
        "points": 90,
        "category": "scripting"
    },
    {
        "id": 28,
        "title": "String Substitution",
        "description": "Replace parts of strings.",
        "challenge": "Replace 'world' with 'bash': TEXT='hello world'; echo ${TEXT/world/bash}",
        "hint": "${variable/old/new}",
        "solution": "TEXT='hello world'; echo ${TEXT/world/bash}",
        "expected_output": "hello bash",
        "explanation": "${var/old/new} replaces first occurrence. Use // for all occurrences.",
        "points": 95,
        "category": "scripting"
    },
    {
        "id": 29,
        "title": "Array Basics",
        "description": "Store multiple values.",
        "challenge": "Create array: FRUITS=(apple banana orange); echo ${FRUITS[1]}",
        "hint": "array=(item1 item2); echo ${array[index]}",
        "solution": "FRUITS=(apple banana orange); echo ${FRUITS[1]}",
        "expected_output": "banana",
        "explanation": "Arrays store multiple values. Index starts at 0!",
        "points": 100,
        "category": "scripting"
    },
    {
        "id": 30,
        "title": "Array Length",
        "description": "Count array elements.",
        "challenge": "Get array length: NUMS=(1 2 3 4 5); echo ${#NUMS[@]}",
        "hint": "${#array[@]}",
        "solution": "NUMS=(1 2 3 4 5); echo ${#NUMS[@]}",
        "expected_output": "5",
        "explanation": "${#array[@]} returns number of elements. [@] means all elements.",
        "points": 110,
        "category": "scripting"
    },
    {
        "id": 31,
        "title": "Function Definition",
        "description": "Create reusable functions.",
        "challenge": "Define and call: greet() { echo 'Hello!'; }; greet",
        "hint": "function_name() { commands; }; function_name",
        "solution": "greet() { echo 'Hello!'; }; greet",
        "expected_output": "Hello!",
        "explanation": "Functions encapsulate code. Define once, use many times!",
        "points": 120,
        "category": "scripting"
    },
    {
        "id": 32,
        "title": "Function Parameters",
        "description": "Pass arguments to functions.",
        "challenge": "Function with params: say() { echo $1; }; say 'Hi'",
        "hint": "$1, $2, etc. are positional parameters",
        "solution": "say() { echo $1; }; say 'Hi'",
        "expected_output": "Hi",
        "explanation": "$1 is first argument, $2 second, etc. $@ is all arguments.",
        "points": 125,
        "category": "scripting"
    },
    {
        "id": 33,
        "title": "Exit Status",
        "description": "Check if commands succeeded.",
        "challenge": "Run ls and check status: ls > /dev/null; echo $?",
        "hint": "$? holds exit status of last command",
        "solution": "ls > /dev/null; echo $?",
        "expected_output": "0",
        "explanation": "$? is 0 for success, non-zero for failure. Essential for error handling!",
        "points": 130,
        "category": "scripting"
    },
    {
        "id": 34,
        "title": "AND Operator",
        "description": "Execute if previous succeeded.",
        "challenge": "Chain commands: echo 'First' && echo 'Second'",
        "hint": "command1 && command2",
        "solution": "echo 'First' && echo 'Second'",
        "expected_output": "First\nSecond",
        "explanation": "&& executes second command only if first succeeds.",
        "points": 135,
        "category": "scripting"
    },
    {
        "id": 35,
        "title": "OR Operator",
        "description": "Execute if previous failed.",
        "challenge": "Fallback: false || echo 'Failed'",
        "hint": "command1 || command2",
        "solution": "false || echo 'Failed'",
        "expected_output": "Failed",
        "explanation": "|| executes second command only if first fails. Great for error messages!",
        "points": 140,
        "category": "scripting"
    },
    {
        "id": 36,
        "title": "Case Statement",
        "description": "Multiple condition matching.",
        "challenge": "case 2 in 1) echo 'One';; 2) echo 'Two';; esac",
        "hint": "case $var in pattern) commands;; esac",
        "solution": "case 2 in 1) echo 'One';; 2) echo 'Two';; esac",
        "expected_output": "Two",
        "explanation": "case is like switch in other languages. Great for menu systems!",
        "points": 145,
        "category": "scripting"
    },
    {
        "id": 37,
        "title": "Read User Input",
        "description": "Get input interactively.",
        "challenge": "Simulate: echo 'test' | { read NAME; echo $NAME; }",
        "hint": "read variable",
        "solution": "echo 'test' | { read NAME; echo $NAME; }",
        "expected_output": "test",
        "explanation": "read gets user input. Use -p for prompt, -s for silent (passwords).",
        "points": 150,
        "category": "scripting"
    },
    {
        "id": 38,
        "title": "Here Document",
        "description": "Multi-line input.",
        "challenge": "cat << EOF\nLine 1\nLine 2\nEOF",
        "hint": "command << DELIMITER ... DELIMITER",
        "solution": "cat << EOF\nLine 1\nLine 2\nEOF",
        "expected_output": "Line 1\nLine 2",
        "explanation": "Here documents provide multi-line input. EOF is common delimiter.",
        "points": 155,
        "category": "scripting"
    },
    {
        "id": 39,
        "title": "Background Jobs",
        "description": "Run commands in background.",
        "challenge": "Run sleep in background: sleep 1 &",
        "hint": "command &",
        "solution": "sleep 1 &",
        "expected_output": None,
        "check_command": True,
        "explanation": "& runs commands in background. Use 'jobs' to list, 'fg' to foreground.",
        "points": 160,
        "category": "scripting"
    },
    {
        "id": 40,
        "title": "Process ID",
        "description": "Get current shell PID.",
        "challenge": "Echo the current shell process ID: echo $$",
        "hint": "$$ is current shell PID",
        "solution": "echo $$",
        "expected_output": None,
        "check_command": True,
        "explanation": "$$ is current shell's PID. $! is last background process PID.",
        "points": 165,
        "category": "scripting"
    },
    {
        "id": 41,
        "title": "Find Files",
        "description": "Search for files by name.",
        "challenge": "Find all .txt files: find . -name '*.txt'",
        "hint": "find path -name pattern",
        "solution": "find . -name '*.txt'",
        "expected_output": None,
        "check_command": True,
        "explanation": "find searches filesystem. Very powerful with -type, -size, -mtime options.",
        "points": 170,
        "category": "files"
    },
    {
        "id": 42,
        "title": "File Permissions",
        "description": "Change file permissions.",
        "challenge": "Make script executable: chmod +x script.sh",
        "hint": "chmod permissions file",
        "solution": "touch script.sh; chmod +x script.sh",
        "expected_output": None,
        "check_command": True,
        "explanation": "chmod changes permissions. +x adds execute, 755 is common for scripts.",
        "points": 175,
        "category": "files"
    },
    {
        "id": 43,
        "title": "File Ownership",
        "description": "Change file owner.",
        "challenge": "Understand chown syntax: chown user:group file",
        "hint": "chown changes ownership (needs sudo usually)",
        "solution": "echo 'chown user:group file'",
        "expected_output": "chown user:group file",
        "explanation": "chown changes file owner. Usually requires root/sudo privileges.",
        "points": 180,
        "category": "files"
    },
    {
        "id": 44,
        "title": "Symbolic Links",
        "description": "Create file shortcuts.",
        "challenge": "Create symlink: ln -s /etc/passwd link.txt",
        "hint": "ln -s target linkname",
        "solution": "ln -s /etc/passwd link.txt",
        "expected_output": None,
        "check_command": True,
        "explanation": "ln -s creates symbolic links (shortcuts). Without -s creates hard links.",
        "points": 185,
        "category": "files"
    },
    {
        "id": 45,
        "title": "Archive Files",
        "description": "Create tar archives.",
        "challenge": "Create tar archive: tar -czf archive.tar.gz file.txt",
        "hint": "tar -czf archive.tar.gz files",
        "solution": "touch file.txt; tar -czf archive.tar.gz file.txt",
        "expected_output": None,
        "check_command": True,
        "explanation": "tar archives files. -c create, -z compress, -f filename, -x extract.",
        "points": 190,
        "category": "files"
    },
    {
        "id": 46,
        "title": "Extract Archives",
        "description": "Decompress tar files.",
        "challenge": "Extract tar.gz: tar -xzf archive.tar.gz",
        "hint": "tar -xzf archive",
        "solution": "tar -xzf archive.tar.gz",
        "expected_output": None,
        "check_command": True,
        "explanation": "tar -xzf extracts compressed archives. -x extract, -z gunzip.",
        "points": 195,
        "category": "files"
    },
    {
        "id": 47,
        "title": "Sort Output",
        "description": "Sort lines of text.",
        "challenge": "Sort lines: echo -e '3\\n1\\n2' | sort",
        "hint": "sort [options] file or command | sort",
        "solution": "echo -e '3\\n1\\n2' | sort",
        "expected_output": "1\n2\n3",
        "explanation": "sort orders lines. Use -r for reverse, -n for numeric sort.",
        "points": 200,
        "category": "text"
    },
    {
        "id": 48,
        "title": "Unique Lines",
        "description": "Remove duplicate lines.",
        "challenge": "Get unique: echo -e 'a\\na\\nb' | sort | uniq",
        "hint": "sort | uniq (needs sorted input)",
        "solution": "echo -e 'a\\na\\nb' | sort | uniq",
        "expected_output": "a\nb",
        "explanation": "uniq removes adjacent duplicates. Always sort first! Use -c to count.",
        "points": 205,
        "category": "text"
    },
    {
        "id": 49,
        "title": "Cut Columns",
        "description": "Extract specific fields.",
        "challenge": "Get first field: echo 'a:b:c' | cut -d':' -f1",
        "hint": "cut -d'delimiter' -f field_number",
        "solution": "echo 'a:b:c' | cut -d':' -f1",
        "expected_output": "a",
        "explanation": "cut extracts columns. -d sets delimiter, -f selects fields.",
        "points": 210,
        "category": "text"
    },
    {
        "id": 50,
        "title": "AWK Basics",
        "description": "Pattern scanning and processing.",
        "challenge": "Print 2nd column: echo 'a b c' | awk '{print $2}'",
        "hint": "awk '{print $field_number}'",
        "solution": "echo 'a b c' | awk '{print $2}'",
        "expected_output": "b",
        "explanation": "awk is powerful for text processing. $1, $2 are columns (space-separated).",
        "points": 215,
        "category": "text"
    },

    # === ADVANCED TIER (51-75): System Administration ===
    {
        "id": 51,
        "title": "SED Substitution",
        "description": "Stream editor for text transformation.",
        "challenge": "Replace text: echo 'hello world' | sed 's/world/bash/'",
        "hint": "sed 's/old/new/'",
        "solution": "echo 'hello world' | sed 's/world/bash/'",
        "expected_output": "hello bash",
        "explanation": "sed edits streams. s/old/new/ substitutes. Use g for global replacement.",
        "points": 220,
        "category": "advanced"
    },
    {
        "id": 52,
        "title": "Process List",
        "description": "View running processes.",
        "challenge": "List all processes: ps aux",
        "hint": "ps with options shows processes",
        "solution": "ps aux",
        "expected_output": None,
        "check_command": True,
        "explanation": "ps shows processes. aux shows all users' processes with details.",
        "points": 225,
        "category": "system"
    },
    {
        "id": 53,
        "title": "Kill Process",
        "description": "Terminate processes.",
        "challenge": "Understand kill: echo 'kill PID' (sends SIGTERM)",
        "hint": "kill PID or kill -9 PID for force",
        "solution": "echo 'kill PID'",
        "expected_output": "kill PID",
        "explanation": "kill sends signals to processes. Default is SIGTERM, -9 is SIGKILL (force).",
        "points": 230,
        "category": "system"
    },
    {
        "id": 54,
        "title": "Top Command",
        "description": "Monitor system resources.",
        "challenge": "Know top shows real-time processes: echo 'top'",
        "hint": "top for interactive process viewer",
        "solution": "echo 'top'",
        "expected_output": "top",
        "explanation": "top shows live system resources. Press 'q' to quit. htop is enhanced version.",
        "points": 235,
        "category": "system"
    },
    {
        "id": 55,
        "title": "Environment Variables",
        "description": "View environment.",
        "challenge": "Show all environment variables: env",
        "hint": "env or printenv",
        "solution": "env",
        "expected_output": None,
        "check_command": True,
        "explanation": "env shows environment variables. export sets them for child processes.",
        "points": 240,
        "category": "system"
    },
    {
        "id": 56,
        "title": "PATH Variable",
        "description": "Command search path.",
        "challenge": "Echo PATH: echo $PATH",
        "hint": "echo $PATH",
        "solution": "echo $PATH",
        "expected_output": None,
        "check_command": True,
        "explanation": "PATH lists directories searched for commands. Add dirs with export PATH=$PATH:/new/dir",
        "points": 245,
        "category": "system"
    },
    {
        "id": 57,
        "title": "Cron Jobs",
        "description": "Schedule recurring tasks.",
        "challenge": "Know crontab syntax: echo '0 * * * * command'",
        "hint": "minute hour day month weekday command",
        "solution": "echo '0 * * * * command'",
        "expected_output": "0 * * * * command",
        "explanation": "crontab schedules tasks. Format: min hour day month weekday command.",
        "points": 250,
        "category": "automation"
    },
    {
        "id": 58,
        "title": "Network Interfaces",
        "description": "View network configuration.",
        "challenge": "Show network interfaces: ip addr or ifconfig",
        "hint": "ip addr show or ifconfig",
        "solution": "ip addr",
        "expected_output": None,
        "check_command": True,
        "explanation": "ip addr shows network interfaces. ifconfig is older but still common.",
        "points": 255,
        "category": "network"
    },
    {
        "id": 59,
        "title": "Ping Host",
        "description": "Test network connectivity.",
        "challenge": "Ping localhost: ping -c 1 localhost",
        "hint": "ping -c count hostname",
        "solution": "ping -c 1 localhost",
        "expected_output": None,
        "check_command": True,
        "explanation": "ping tests connectivity. -c limits count. Sends ICMP echo requests.",
        "points": 260,
        "category": "network"
    },
    {
        "id": 60,
        "title": "Download Files",
        "description": "Fetch files from URLs.",
        "challenge": "Know wget downloads: echo 'wget URL'",
        "hint": "wget URL or curl -O URL",
        "solution": "echo 'wget URL'",
        "expected_output": "wget URL",
        "explanation": "wget downloads files. curl can too with -O. Both are essential tools.",
        "points": 265,
        "category": "network"
    },
    {
        "id": 61,
        "title": "SSH Connection",
        "description": "Secure remote shell.",
        "challenge": "Know SSH syntax: echo 'ssh user@host'",
        "hint": "ssh user@hostname",
        "solution": "echo 'ssh user@host'",
        "expected_output": "ssh user@host",
        "explanation": "ssh connects securely to remote systems. Essential for remote admin.",
        "points": 270,
        "category": "network"
    },
    {
        "id": 62,
        "title": "SCP File Transfer",
        "description": "Secure copy files.",
        "challenge": "Know SCP syntax: echo 'scp file user@host:path'",
        "hint": "scp source destination",
        "solution": "echo 'scp file user@host:path'",
        "expected_output": "scp file user@host:path",
        "explanation": "scp copies files over SSH. Use -r for directories.",
        "points": 275,
        "category": "network"
    },
    {
        "id": 63,
        "title": "Netstat Connections",
        "description": "View network connections.",
        "challenge": "Know netstat shows connections: echo 'netstat -tuln'",
        "hint": "netstat -tuln shows listening ports",
        "solution": "echo 'netstat -tuln'",
        "expected_output": "netstat -tuln",
        "explanation": "netstat shows network connections. -t TCP, -u UDP, -l listening, -n numeric.",
        "points": 280,
        "category": "network"
    },
    {
        "id": 64,
        "title": "System Logs",
        "description": "View system logs.",
        "challenge": "Read syslog: tail /var/log/syslog (if exists) or journalctl",
        "hint": "Logs in /var/log/ or journalctl for systemd",
        "solution": "echo 'tail /var/log/syslog'",
        "expected_output": "tail /var/log/syslog",
        "explanation": "System logs in /var/log/. journalctl for systemd. Essential for troubleshooting!",
        "points": 285,
        "category": "system"
    },
    {
        "id": 65,
        "title": "Disk Check",
        "description": "Check filesystem for errors.",
        "challenge": "Know fsck checks filesystems: echo 'fsck /dev/sdX'",
        "hint": "fsck (filesystem check, needs unmounted disk)",
        "solution": "echo 'fsck /dev/sdX'",
        "expected_output": "fsck /dev/sdX",
        "explanation": "fsck checks and repairs filesystems. Must be unmounted! Use carefully.",
        "points": 290,
        "category": "system"
    },
    {
        "id": 66,
        "title": "Mount Filesystem",
        "description": "Attach filesystems.",
        "challenge": "Know mount syntax: echo 'mount /dev/sdX /mnt'",
        "hint": "mount device mountpoint",
        "solution": "echo 'mount /dev/sdX /mnt'",
        "expected_output": "mount /dev/sdX /mnt",
        "explanation": "mount attaches filesystems. umount detaches. /etc/fstab for permanent mounts.",
        "points": 295,
        "category": "system"
    },
    {
        "id": 67,
        "title": "Regex Pattern",
        "description": "Regular expression matching.",
        "challenge": "Match emails: echo 'test@example.com' | grep -E '[a-z]+@[a-z]+\\.[a-z]+'",
        "hint": "grep -E for extended regex",
        "solution": "echo 'test@example.com' | grep -E '[a-z]+@[a-z]+\\.[a-z]+'",
        "expected_output": "test@example.com",
        "explanation": "Regex matches patterns. -E enables extended regex. Essential for text processing!",
        "points": 300,
        "category": "advanced"
    },
    {
        "id": 68,
        "title": "Xargs Command",
        "description": "Build commands from input.",
        "challenge": "Use xargs: echo -e 'a\\nb\\nc' | xargs echo",
        "hint": "xargs converts input to arguments",
        "solution": "echo -e 'a\\nb\\nc' | xargs echo",
        "expected_output": "a b c",
        "explanation": "xargs builds command lines from input. Great with find!",
        "points": 305,
        "category": "advanced"
    },
    {
        "id": 69,
        "title": "Parallel Execution",
        "description": "Run commands concurrently.",
        "challenge": "Background tasks: echo 'cmd1 & cmd2 & wait'",
        "hint": "Use & for background, wait for completion",
        "solution": "echo 'cmd1 & cmd2 & wait'",
        "expected_output": "cmd1 & cmd2 & wait",
        "explanation": "& backgrounds tasks. wait waits for all. GNU parallel is more advanced.",
        "points": 310,
        "category": "advanced"
    },
    {
        "id": 70,
        "title": "Signal Trapping",
        "description": "Handle signals in scripts.",
        "challenge": "Trap signal: trap 'echo Caught' SIGINT",
        "hint": "trap 'commands' SIGNAL",
        "solution": "trap 'echo Caught' SIGINT",
        "expected_output": None,
        "check_command": True,
        "explanation": "trap catches signals. Use for cleanup on script exit or interruption.",
        "points": 315,
        "category": "advanced"
    },
    {
        "id": 71,
        "title": "Set Options",
        "description": "Script execution modes.",
        "challenge": "Exit on error: set -e",
        "hint": "set -e exits on error, -u on undefined vars",
        "solution": "set -e",
        "expected_output": None,
        "check_command": True,
        "explanation": "set -e exits on errors. set -u errors on undefined vars. Use for robust scripts!",
        "points": 320,
        "category": "advanced"
    },
    {
        "id": 72,
        "title": "Debugging Scripts",
        "description": "Debug bash scripts.",
        "challenge": "Debug mode: set -x",
        "hint": "set -x prints commands before executing",
        "solution": "set -x",
        "expected_output": None,
        "check_command": True,
        "explanation": "set -x shows commands being executed. Essential for debugging!",
        "points": 325,
        "category": "advanced"
    },
    {
        "id": 73,
        "title": "Process Substitution",
        "description": "Use process output as file.",
        "challenge": "Compare outputs: diff <(echo 'a') <(echo 'b')",
        "hint": "<(command) treats output as file",
        "solution": "diff <(echo 'a') <(echo 'b')",
        "expected_output": None,
        "check_command": True,
        "explanation": "<() process substitution treats command output as file. Very powerful!",
        "points": 330,
        "category": "advanced"
    },
    {
        "id": 74,
        "title": "Brace Expansion",
        "description": "Generate sequences.",
        "challenge": "Create sequence: echo {1..5}",
        "hint": "{start..end} or {a,b,c}",
        "solution": "echo {1..5}",
        "expected_output": "1 2 3 4 5",
        "explanation": "Brace expansion generates sequences. {1..10}, {a..z}, {file1,file2}.",
        "points": 335,
        "category": "advanced"
    },
    {
        "id": 75,
        "title": "Associative Arrays",
        "description": "Key-value pairs in bash.",
        "challenge": "Declare hash: declare -A hash; hash[key]=value; echo ${hash[key]}",
        "hint": "declare -A for associative arrays",
        "solution": "declare -A hash; hash[key]=value; echo ${hash[key]}",
        "expected_output": "value",
        "explanation": "declare -A creates associative arrays (hashes/dicts). Bash 4+ only.",
        "points": 340,
        "category": "advanced"
    },

    # === EXPERT TIER (76-100): Advanced Scripting & Automation ===
    {
        "id": 76,
        "title": "Script Template",
        "description": "Professional script structure.",
        "challenge": "Know good script starts with: #!/bin/bash and set -euo pipefail",
        "hint": "Shebang + safety flags",
        "solution": "echo '#!/bin/bash\nset -euo pipefail'",
        "expected_output": "#!/bin/bash\nset -euo pipefail",
        "explanation": "#!/bin/bash (shebang) + set -euo pipefail ensures robust scripts.",
        "points": 345,
        "category": "expert"
    },
    {
        "id": 77,
        "title": "Getopts Parsing",
        "description": "Parse command-line options.",
        "challenge": "Know getopts parses options: getopts 'a:b' opt",
        "hint": "getopts optstring variable",
        "solution": "echo 'while getopts \"a:b\" opt; do case $opt in a) ;; esac; done'",
        "expected_output": "while getopts \"a:b\" opt; do case $opt in a) ;; esac; done",
        "explanation": "getopts parses -a value -b style options. Essential for professional scripts.",
        "points": 350,
        "category": "expert"
    },
    {
        "id": 78,
        "title": "Logging Function",
        "description": "Structured logging.",
        "challenge": "Create logger: log() { echo \"[$(date +%Y-%m-%d\\ %H:%M:%S)] $*\"; }; log 'test'",
        "hint": "Function that timestamps messages",
        "solution": "log() { echo \"[$(date +%Y-%m-%d\\ %H:%M:%S)] $*\"; }; log 'test'",
        "expected_output": None,
        "check_command": True,
        "explanation": "Logging functions add timestamps and structure. Essential for production scripts!",
        "points": 355,
        "category": "expert"
    },
    {
        "id": 79,
        "title": "Lock Files",
        "description": "Prevent concurrent execution.",
        "challenge": "Know lock pattern: LOCKFILE=/tmp/script.lock; if mkdir $LOCKFILE 2>/dev/null; then ...",
        "hint": "mkdir is atomic for locks",
        "solution": "echo 'mkdir /tmp/script.lock 2>/dev/null'",
        "expected_output": "mkdir /tmp/script.lock 2>/dev/null",
        "explanation": "mkdir is atomic, perfect for lock files. Prevents script race conditions.",
        "points": 360,
        "category": "expert"
    },
    {
        "id": 80,
        "title": "Error Handling",
        "description": "Robust error management.",
        "challenge": "Error function: err() { echo \"ERROR: $*\" >&2; exit 1; }; err 'test' || true",
        "hint": ">&2 sends to stderr, exit 1 for errors",
        "solution": "err() { echo \"ERROR: $*\" >&2; exit 1; }; err 'test' || true",
        "expected_output": None,
        "check_command": True,
        "explanation": "Send errors to stderr (>&2), exit with non-zero for failures.",
        "points": 365,
        "category": "expert"
    },
    {
        "id": 81,
        "title": "Config Files",
        "description": "Source configuration files.",
        "challenge": "Source config: echo 'VAR=value' > /tmp/config; source /tmp/config; echo $VAR",
        "hint": "source or . loads files",
        "solution": "echo 'VAR=value' > /tmp/config; source /tmp/config; echo $VAR",
        "expected_output": "value",
        "explanation": "source (or .) loads config files. Keep configs separate from code!",
        "points": 370,
        "category": "expert"
    },
    {
        "id": 82,
        "title": "Temporary Files",
        "description": "Safe temp file creation.",
        "challenge": "Create temp file: TMPFILE=$(mktemp); echo $TMPFILE",
        "hint": "mktemp creates unique temp files",
        "solution": "TMPFILE=$(mktemp); echo $TMPFILE",
        "expected_output": None,
        "check_command": True,
        "explanation": "mktemp creates unique temp files safely. Always clean up with trap!",
        "points": 375,
        "category": "expert"
    },
    {
        "id": 83,
        "title": "Cleanup Traps",
        "description": "Always clean up resources.",
        "challenge": "Cleanup on exit: trap 'rm -f /tmp/file' EXIT",
        "hint": "trap cleanup EXIT ensures cleanup",
        "solution": "trap 'rm -f /tmp/test$$' EXIT",
        "expected_output": None,
        "check_command": True,
        "explanation": "trap EXIT ensures cleanup happens even on errors. Critical for production!",
        "points": 380,
        "category": "expert"
    },
    {
        "id": 84,
        "title": "Timeout Command",
        "description": "Limit command execution time.",
        "challenge": "Timeout after 1s: timeout 1 sleep 5 || echo 'Timed out'",
        "hint": "timeout SECONDS command",
        "solution": "timeout 1 sleep 5 || echo 'Timed out'",
        "expected_output": "Timed out",
        "explanation": "timeout prevents commands from hanging. Essential for automation!",
        "points": 385,
        "category": "expert"
    },
    {
        "id": 85,
        "title": "Watch Command",
        "description": "Monitor command output.",
        "challenge": "Know watch reruns commands: echo 'watch -n 1 date'",
        "hint": "watch -n seconds command",
        "solution": "echo 'watch -n 1 date'",
        "expected_output": "watch -n 1 date",
        "explanation": "watch runs command repeatedly. Great for monitoring!",
        "points": 390,
        "category": "expert"
    },
    {
        "id": 86,
        "title": "Version Check",
        "description": "Check software versions in scripts.",
        "challenge": "Check bash version: echo $BASH_VERSION",
        "hint": "$BASH_VERSION variable",
        "solution": "echo $BASH_VERSION",
        "expected_output": None,
        "check_command": True,
        "explanation": "$BASH_VERSION shows bash version. Check for required features!",
        "points": 395,
        "category": "expert"
    },
    {
        "id": 87,
        "title": "Conditional Compilation",
        "description": "OS-specific code in scripts.",
        "challenge": "Detect OS: if [[ \"$OSTYPE\" == \"linux-gnu\"* ]]; then echo 'Linux'; fi",
        "hint": "$OSTYPE variable",
        "solution": "if [[ \"$OSTYPE\" == \"linux-gnu\"* ]]; then echo 'Linux'; fi",
        "expected_output": "Linux",
        "explanation": "$OSTYPE shows OS. Write portable scripts checking this!",
        "points": 400,
        "category": "expert"
    },
    {
        "id": 88,
        "title": "Performance Timing",
        "description": "Measure script execution time.",
        "challenge": "Time command: time sleep 0.1",
        "hint": "time command shows execution time",
        "solution": "time sleep 0.1",
        "expected_output": None,
        "check_command": True,
        "explanation": "time measures execution. Use for performance optimization!",
        "points": 405,
        "category": "expert"
    },
    {
        "id": 89,
        "title": "Backup Script Pattern",
        "description": "Safe backup with timestamps.",
        "challenge": "Backup: cp file.txt file.txt.$(date +%Y%m%d_%H%M%S).bak",
        "hint": "Add timestamp to backups",
        "solution": "touch file.txt; cp file.txt file.txt.$(date +%Y%m%d_%H%M%S).bak",
        "expected_output": None,
        "check_command": True,
        "explanation": "Timestamped backups prevent overwrites. Essential pattern!",
        "points": 410,
        "category": "expert"
    },
    {
        "id": 90,
        "title": "Input Validation",
        "description": "Validate user input.",
        "challenge": "Check if number: if [[ \"5\" =~ ^[0-9]+$ ]]; then echo 'Valid'; fi",
        "hint": "=~ for regex matching in [[]]",
        "solution": "if [[ \"5\" =~ ^[0-9]+$ ]]; then echo 'Valid'; fi",
        "expected_output": "Valid",
        "explanation": "Always validate input! =~ does regex matching in [[ ]].",
        "points": 415,
        "category": "expert"
    },
    {
        "id": 91,
        "title": "Retry Logic",
        "description": "Retry failed commands.",
        "challenge": "Retry pattern: for i in {1..3}; do command && break || sleep 1; done",
        "hint": "Loop with break on success",
        "solution": "for i in {1..3}; do true && break || sleep 0.1; done; echo 'Done'",
        "expected_output": "Done",
        "explanation": "Retry logic handles transient failures. Essential for reliability!",
        "points": 420,
        "category": "expert"
    },
    {
        "id": 92,
        "title": "Colored Output",
        "description": "Add colors to terminal output.",
        "challenge": "Red text: echo -e '\\033[31mRed\\033[0m'",
        "hint": "ANSI escape codes: \\033[31m for red",
        "solution": "echo -e '\\033[31mRed\\033[0m'",
        "expected_output": None,
        "check_command": True,
        "explanation": "ANSI codes add color. \\033[31m red, \\033[32m green, \\033[0m reset.",
        "points": 425,
        "category": "expert"
    },
    {
        "id": 93,
        "title": "Progress Bar",
        "description": "Show progress in scripts.",
        "challenge": "Simple progress: for i in {1..5}; do echo -ne \"#\"; sleep 0.1; done; echo",
        "hint": "echo -ne for same line",
        "solution": "for i in {1..5}; do echo -ne \"#\"; sleep 0.1; done; echo",
        "expected_output": "#####",
        "explanation": "echo -ne stays on same line. Build progress bars for long operations!",
        "points": 430,
        "category": "expert"
    },
    {
        "id": 94,
        "title": "Menu System",
        "description": "Interactive menu in scripts.",
        "challenge": "Select menu: select opt in A B Quit; do case $opt in Quit) break;; esac; done",
        "hint": "select creates numbered menus",
        "solution": "echo 'select opt in A B; do break; done'",
        "expected_output": "select opt in A B; do break; done",
        "explanation": "select creates interactive menus. Great for user-friendly scripts!",
        "points": 435,
        "category": "expert"
    },
    {
        "id": 95,
        "title": "Heredoc with Variables",
        "description": "Template generation with variable expansion.",
        "challenge": "Expand vars in heredoc: NAME=World; cat << EOF\nHello $NAME\nEOF",
        "hint": "Heredoc expands variables by default",
        "solution": "NAME=World; cat << EOF\nHello $NAME\nEOF",
        "expected_output": "Hello World",
        "explanation": "Heredocs expand variables. Use << 'EOF' to prevent expansion.",
        "points": 440,
        "category": "expert"
    },
    {
        "id": 96,
        "title": "Shell Best Practices",
        "description": "Professional script standards.",
        "challenge": "List best practices: echo 'set -euo pipefail, quote vars, check exit codes'",
        "hint": "Safety flags, quoting, error checking",
        "solution": "echo 'set -euo pipefail, quote vars, check exit codes'",
        "expected_output": "set -euo pipefail, quote vars, check exit codes",
        "explanation": "Best practices: set -euo pipefail, quote variables, check exit codes, validate input!",
        "points": 445,
        "category": "expert"
    },
    {
        "id": 97,
        "title": "Systemd Service",
        "description": "Create systemd unit files.",
        "challenge": "Know systemd unit structure: [Unit], [Service], [Install] sections",
        "hint": "systemd uses INI-style config",
        "solution": "echo '[Unit]\\n[Service]\\n[Install]'",
        "expected_output": "[Unit]\n[Service]\n[Install]",
        "explanation": "systemd services have Unit, Service, Install sections. Modern Linux init!",
        "points": 450,
        "category": "expert"
    },
    {
        "id": 98,
        "title": "Ansible Integration",
        "description": "Use bash scripts with ansible.",
        "challenge": "Know ansible can run bash: echo 'ansible host -m shell -a \"command\"'",
        "hint": "Ansible shell module runs commands",
        "solution": "echo 'ansible host -m shell -a \"command\"'",
        "expected_output": "ansible host -m shell -a \"command\"",
        "explanation": "Ansible shell module runs bash commands. Combine bash and automation!",
        "points": 455,
        "category": "expert"
    },
    {
        "id": 99,
        "title": "Docker Bash",
        "description": "Bash in containers.",
        "challenge": "Run bash in container: echo 'docker run -it ubuntu bash'",
        "hint": "docker run -it image bash",
        "solution": "echo 'docker run -it ubuntu bash'",
        "expected_output": "docker run -it ubuntu bash",
        "explanation": "Docker containers often use bash. Essential for modern DevOps!",
        "points": 460,
        "category": "expert"
    },
    {
        "id": 100,
        "title": "The Grand Challenge",
        "description": "Complete bash automation script.",
        "challenge": "Write a script that: 1) Takes filename as arg, 2) Checks if exists, 3) Backs it up with timestamp, 4) Logs action",
        "hint": "Combine everything you've learned!",
        "solution": """#!/bin/bash
set -euo pipefail
FILE=${1:-}
[[ -z "$FILE" ]] && { echo "Usage: $0 filename" >&2; exit 1; }
[[ ! -f "$FILE" ]] && { echo "File not found!" >&2; exit 1; }
BACKUP="${FILE}.$(date +%Y%m%d_%H%M%S).bak"
cp "$FILE" "$BACKUP"
echo "[$(date)] Backed up $FILE to $BACKUP"
""",
        "expected_output": None,
        "check_command": True,
        "explanation": "You've mastered Bash! You combined safety flags, validation, functions, timestamps, and logging. You're a Bash Grandmaster! 🏆",
        "points": 500,
        "category": "final"
    },
]


# === Player Progress ===
class PlayerProgress:
    def __init__(self):
        self.current_level = 1
        self.completed_levels = []
        self.total_points = 0
        self.achievements = []
        self.start_date = datetime.now().isoformat()
        self.last_played = datetime.now().isoformat()

    def to_dict(self) -> dict:
        return {
            "current_level": self.current_level,
            "completed_levels": self.completed_levels,
            "total_points": self.total_points,
            "achievements": self.achievements,
            "start_date": self.start_date,
            "last_played": self.last_played,
        }

    @classmethod
    def from_dict(cls, data: dict):
        progress = cls()
        progress.current_level = data.get("current_level", 1)
        progress.completed_levels = data.get("completed_levels", [])
        progress.total_points = data.get("total_points", 0)
        progress.achievements = data.get("achievements", [])
        progress.start_date = data.get("start_date", datetime.now().isoformat())
        progress.last_played = data.get("last_played", datetime.now().isoformat())
        return progress


# === Save/Load Functions ===
def save_progress(progress: PlayerProgress):
    """Save player progress to file."""
    try:
        with open(SAVE_FILE, 'w') as f:
            json.dump(progress.to_dict(), f, indent=2)
    except Exception as e:
        console.print(f"[{COLORS['error']}]Error saving progress: {e}[/]")


def load_progress() -> PlayerProgress:
    """Load player progress from file."""
    if SAVE_FILE.exists():
        try:
            with open(SAVE_FILE) as f:
                data = json.load(f)
                return PlayerProgress.from_dict(data)
        except Exception as e:
            console.print(f"[{COLORS['warning']}]Could not load save file: {e}[/]")
    return PlayerProgress()


# === UI Functions ===
def show_banner():
    """Display the game banner."""
    banner = """
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║   ██████╗  █████╗ ███████╗██╗  ██╗ ██████╗ ██╗   ██╗███████╗║
    ║   ██╔══██╗██╔══██╗██╔════╝██║  ██║██╔═══██╗██║   ██║██╔════╝║
    ║   ██████╔╝███████║███████╗███████║██║   ██║██║   ██║█████╗  ║
    ║   ██╔══██╗██╔══██║╚════██║██╔══██║██║▄▄ ██║██║   ██║██╔══╝  ║
    ║   ██████╔╝██║  ██║███████║██║  ██║╚██████╔╝╚██████╔╝███████╗║
    ║   ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ╚══▀▀═╝  ╚═════╝ ╚══════╝║
    ║                                                               ║
    ║              🐧 Linux Terminal Mastery 🐧                     ║
    ║                                                               ║
    ║           Learn Bash Scripting from Zero to Expert           ║
    ║                  Author: arkanzasfeziii                       ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    """
    console.print(f"[{COLORS['terminal']}]{banner}[/]")
    time.sleep(1)


def get_rank(level: int) -> tuple[str, str]:
    """Get player rank based on current level."""
    for min_level, rank_name, description in reversed(RANKS):
        if level >= min_level:
            return rank_name, description
    return RANKS[0][1], RANKS[0][2]


def show_stats(progress: PlayerProgress):
    """Display player statistics."""
    rank_name, rank_desc = get_rank(progress.current_level)

    table = Table(title="Your Stats", box=box.DOUBLE_EDGE, border_style=COLORS['primary'])
    table.add_column("Stat", style=COLORS['secondary'], no_wrap=True)
    table.add_column("Value", style=COLORS['terminal'])

    table.add_row("Current Level", f"{progress.current_level}/100")
    table.add_row("Completed Levels", str(len(progress.completed_levels)))
    table.add_row("Total Points", str(progress.total_points))
    table.add_row("Current Rank", rank_name)
    table.add_row("Rank Description", rank_desc)
    table.add_row("Achievements", str(len(progress.achievements)))

    console.print(table)


def show_level_info(level_data: dict):
    """Display information about a level."""
    panel = Panel(
        f"""[{COLORS['terminal']}]LEVEL {level_data['id']}: {level_data['title'].upper()}[/]

[{COLORS['info']}]Category:[/] [{COLORS['secondary']}]{level_data['category'].upper()}[/]
[{COLORS['info']}]Points:[/] [{COLORS['success']}]{level_data['points']}[/]

[{COLORS['warning']}]Description:[/]
{level_data['description']}

[{COLORS['warning']}]Challenge:[/]
{level_data['challenge']}
""",
        border_style=COLORS['primary'],
        box=box.DOUBLE
    )
    console.print(panel)


def simulate_terminal_boot():
    """Show a cool terminal boot animation."""
    messages = [
        "Initializing bash environment...",
        "Loading shell configuration...",
        "Mounting filesystems...",
        "Starting terminal services...",
        "System ready!",
    ]

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("[cyan]Booting...", total=len(messages))
        for msg in messages:
            progress.update(task, description=f"[{COLORS['terminal']}]{msg}")
            time.sleep(random.uniform(0.3, 0.7))
            progress.advance(task)


# === Core Game Logic ===
def execute_bash_command(command: str, expected_output: str | None = None) -> tuple[bool, str]:
    """
    Execute a bash command and return success status and output.
    """
    try:
        # Create a temporary script file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.sh', delete=False) as f:
            f.write("#!/bin/bash\n")
            f.write("set +e\n")  # Don't exit on errors for testing
            f.write(command + "\n")
            script_path = f.name

        # Make executable
        os.chmod(script_path, 0o755)

        # Execute
        result = subprocess.run(
            ['bash', script_path],
            capture_output=True,
            text=True,
            timeout=5
        )

        # Cleanup
        os.unlink(script_path)

        output = result.stdout.strip()

        # If we have expected output, check it
        if expected_output is not None:
            # Normalize outputs for comparison
            expected_normalized = expected_output.strip()
            output_normalized = output.strip()
            return (output_normalized == expected_normalized, output)
        else:
            # Just check if command executed without error
            return (result.returncode == 0, output)

    except subprocess.TimeoutExpired:
        if script_path and os.path.exists(script_path):
            os.unlink(script_path)
        return (False, "Command timed out (>5 seconds)")
    except Exception as e:
        if script_path and os.path.exists(script_path):
            os.unlink(script_path)
        return (False, f"Error: {str(e)}")


def play_level(level_data: dict, progress: PlayerProgress) -> bool:
    """
    Play a single level.
    Returns True if completed successfully.
    """
    show_level_info(level_data)
    console.print()

    # Show hint option
    console.print(f"[{COLORS['info']}]💡 Type 'hint' for a hint, 'skip' to skip (no points), or enter your bash command:[/]")
    console.print()

    while True:
        try:
            user_input = Prompt.ask(f"[{COLORS['terminal']}]bash$")

            if user_input.lower() == 'hint':
                console.print(f"[{COLORS['warning']}]💡 Hint: {level_data['hint']}[/]")
                continue
            elif user_input.lower() == 'skip':
                console.print(f"[{COLORS['warning']}]⏭️  Skipping level (no points awarded)[/]")
                return False
            elif user_input.lower() == 'solution':
                console.print(f"[{COLORS['error']}]🚫 No cheating! Try using the hint instead.[/]")
                continue
            elif not user_input.strip():
                console.print(f"[{COLORS['error']}]Please enter a command![/]")
                continue

            break
        except (KeyboardInterrupt, EOFError):
            console.print(f"\n[{COLORS['warning']}]Level interrupted.[/]")
            return False

    # Show what they entered
    console.print(f"\n[{COLORS['info']}]Your command:[/]")
    syntax = Syntax(user_input, "bash", theme="monokai", line_numbers=False)
    console.print(syntax)
    console.print()

    # Execute the command
    console.print(f"[{COLORS['warning']}]Executing command...[/]")
    time.sleep(0.5)

    success, output = execute_bash_command(user_input, level_data.get('expected_output'))

    if success:
        console.print(f"[{COLORS['success']}]✅ CORRECT! Level completed![/]")
        if output:
            console.print(f"[{COLORS['info']}]Output:[/] {output}")
        console.print(f"[{COLORS['info']}]{level_data['explanation']}[/]")
        console.print(f"[{COLORS['success']}]+{level_data['points']} points![/]")

        # Update progress
        if level_data['id'] not in progress.completed_levels:
            progress.completed_levels.append(level_data['id'])
            progress.total_points += level_data['points']

        # Check for achievements
        check_achievements(progress)

        return True
    else:
        console.print(f"[{COLORS['error']}]❌ Not quite right. Try again![/]")
        if output:
            console.print(f"[{COLORS['info']}]Output:[/] {output}")
        if level_data.get('expected_output'):
            console.print(f"[{COLORS['info']}]Expected:[/] {level_data['expected_output']}")

        if Confirm.ask(f"[{COLORS['warning']}]Try again?"):
            return play_level(level_data, progress)
        return False


def check_achievements(progress: PlayerProgress):
    """Check and award achievements."""
    achievements = [
        (5, "🌟 First Steps", "Completed 5 levels"),
        (10, "📁 Directory Master", "Completed 10 levels"),
        (25, "⚙️ Script Writer", "Completed 25 levels"),
        (50, "🚀 Automation King", "Completed 50 levels"),
        (75, "👑 Shell Sensei", "Completed 75 levels"),
        (100, "🏆 Bash Grandmaster", "Completed ALL levels!"),
    ]

    for threshold, name, desc in achievements:
        if len(progress.completed_levels) >= threshold and name not in progress.achievements:
            progress.achievements.append(name)
            console.print(f"\n[{COLORS['success']}]🏆 ACHIEVEMENT UNLOCKED: {name}[/]")
            console.print(f"[{COLORS['info']}]{desc}[/]\n")
            time.sleep(2)


# === Main Menu ===
def main_menu():
    """Display main menu and handle user choices."""
    progress = load_progress()

    while True:
        console.clear()
        show_banner()

        rank_name, _ = get_rank(progress.current_level)
        console.print(f"\n[{COLORS['terminal']}]Welcome back, {rank_name}![/]\n")

        table = Table(box=box.ROUNDED, border_style=COLORS['secondary'])
        table.add_column("Option", style=COLORS['primary'], no_wrap=True)
        table.add_column("Description", style=COLORS['info'])

        table.add_row("1", "Continue Journey")
        table.add_row("2", "View Stats")
        table.add_row("3", "Jump to Level")
        table.add_row("4", "View Achievements")
        table.add_row("5", "Reset Progress")
        table.add_row("6", "Exit")

        console.print(table)

        choice = Prompt.ask(f"\n[{COLORS['secondary']}]Choose an option", choices=["1", "2", "3", "4", "5", "6"])

        if choice == "1":
            # Continue playing
            while progress.current_level <= 100:
                console.clear()
                level_data = LEVELS[progress.current_level - 1]

                if play_level(level_data, progress):
                    progress.current_level += 1
                    progress.last_played = datetime.now().isoformat()
                    save_progress(progress)

                    if progress.current_level <= 100:
                        if Confirm.ask(f"\n[{COLORS['success']}]Continue to next level?"):
                            continue
                        else:
                            break
                    else:
                        console.print(f"\n[{COLORS['terminal']}]🎉 CONGRATULATIONS! You've completed ALL 100 levels! 🎉[/]")
                        console.print(f"[{COLORS['success']}]You are now a BASH GRANDMASTER! 🏆[/]")
                        console.print(f"[{COLORS['info']}]Total Points: {progress.total_points}[/]")
                        input("\nPress Enter to return to menu...")
                        break
                else:
                    break

        elif choice == "2":
            console.clear()
            show_stats(progress)
            input("\nPress Enter to continue...")

        elif choice == "3":
            max_level = max(progress.completed_levels) + 1 if progress.completed_levels else 1
            level_num = int(Prompt.ask(f"Jump to level (1-{min(max_level, 100)})"))
            if 1 <= level_num <= min(max_level, 100):
                progress.current_level = level_num
                save_progress(progress)
            else:
                console.print(f"[{COLORS['error']}]Invalid level number![/]")
                time.sleep(2)

        elif choice == "4":
            console.clear()
            if progress.achievements:
                table = Table(title="🏆 Your Achievements", box=box.DOUBLE_EDGE, border_style=COLORS['success'])
                table.add_column("Achievement", style=COLORS['terminal'])
                for achievement in progress.achievements:
                    table.add_row(achievement)
                console.print(table)
            else:
                console.print(f"[{COLORS['info']}]No achievements yet. Keep learning![/]")
            input("\nPress Enter to continue...")

        elif choice == "5":
            if Confirm.ask(f"[{COLORS['error']}]Are you sure you want to reset ALL progress?"):
                progress = PlayerProgress()
                save_progress(progress)
                console.print(f"[{COLORS['success']}]Progress reset![/]")
                time.sleep(2)

        elif choice == "6":
            console.print(f"\n[{COLORS['terminal']}]Thanks for playing BashQuest! Happy scripting! 👋[/]")
            break


# === Entry Point ===
def main():
    """Main entry point."""
    try:
        console.clear()
        simulate_terminal_boot()
        time.sleep(1)
        main_menu()
    except KeyboardInterrupt:
        console.print(f"\n\n[{COLORS['warning']}]Game interrupted. Progress saved. Goodbye! 👋[/]")
    except Exception as e:
        console.print(f"\n[{COLORS['error']}]An error occurred: {e}[/]")
        console.print(f"[{COLORS['info']}]Please report this bug to arkanzasfeziii[/]")


if __name__ == "__main__":
    main()
