#!/usr/bin/env python3
"""
WindowsQuest: CMD & PowerShell Mastery
A comprehensive game to learn Windows command-line and PowerShell from absolute beginner to expert.
Author: arkanzasfeziii
"""

import json
import os
import platform
import random
import subprocess
import sys
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
SAVE_FILE = Path.home() / ".windowsquest_save.json"
VERSION = "1.0.0"

# Windows color scheme
COLORS = {
    "primary": "bright_cyan",
    "secondary": "bright_magenta",
    "success": "bright_green",
    "error": "bright_red",
    "warning": "bright_yellow",
    "info": "blue",
    "windows": "bright_blue",
}

# === Rank System ===
RANKS = [
    (0, "🪟 CMD Rookie", "Just opened your first command prompt"),
    (5, "📂 Explorer Novice", "Learning to navigate folders"),
    (10, "⌨️ Command Cadet", "Getting comfortable with commands"),
    (15, "🔍 Search Specialist", "Finding files like a pro"),
    (20, "📝 Batch Beginner", "Writing your first scripts"),
    (25, "⚡ PowerShell Padawan", "Discovering PowerShell"),
    (30, "🎯 Cmdlet Commander", "Mastering cmdlets"),
    (35, "🔧 Tool Craftsman", "Building useful utilities"),
    (40, "📊 Object Warrior", "Understanding the pipeline"),
    (45, "🔐 Security Sentinel", "Managing permissions"),
    (50, "🌐 Network Navigator", "Network command mastery"),
    (55, "💾 Registry Ranger", "Editing the registry safely"),
    (60, "⚙️ Service Specialist", "Managing Windows services"),
    (65, "📦 Module Master", "Working with modules"),
    (70, "🎭 Script Architect", "Advanced scripting"),
    (75, "🛡️ Admin Ace", "System administration expert"),
    (80, "🚀 Automation Guru", "Full workflow automation"),
    (85, "👑 PowerShell Pro", "PowerShell expert"),
    (90, "💎 Windows Wizard", "Command-line master"),
    (95, "🏆 Terminal Titan", "Almost legendary"),
    (100, "⭐ Windows Grandmaster", "The ultimate achievement"),
]

# === Level Definitions ===
LEVELS = [
    # === BEGINNER TIER (1-20): CMD Basics ===
    {
        "id": 1,
        "title": "Echo Hello World",
        "description": "Your first command: display text in the console.",
        "challenge": "Use echo to print: Hello, WindowsQuest!",
        "hint": "echo text",
        "solution": "echo Hello, WindowsQuest!",
        "expected_output": "Hello, WindowsQuest!",
        "shell": "cmd",
        "explanation": "echo displays text. It's the most basic output command in CMD!",
        "points": 10,
        "category": "basics"
    },
    {
        "id": 2,
        "title": "Current Directory",
        "description": "Find out where you are in the filesystem.",
        "challenge": "Use the command that shows the current directory path.",
        "hint": "cd without arguments shows current directory",
        "solution": "cd",
        "expected_output": None,
        "shell": "cmd",
        "check_command": True,
        "explanation": "cd without arguments displays current directory. cd with path changes directory.",
        "points": 10,
        "category": "basics"
    },
    {
        "id": 3,
        "title": "List Files",
        "description": "See what files are in your directory.",
        "challenge": "List all files and folders in the current directory.",
        "hint": "dir lists directory contents",
        "solution": "dir",
        "expected_output": None,
        "shell": "cmd",
        "check_command": True,
        "explanation": "dir shows files and directories. Use dir /w for wide format, dir /p for paged.",
        "points": 15,
        "category": "basics"
    },
    {
        "id": 4,
        "title": "Create a Directory",
        "description": "Make a new folder.",
        "challenge": "Create a directory named 'testfolder' using mkdir or md.",
        "hint": "mkdir foldername",
        "solution": "mkdir testfolder",
        "expected_output": None,
        "shell": "cmd",
        "check_command": True,
        "explanation": "mkdir or md creates new directories. Both commands work identically.",
        "points": 15,
        "category": "basics"
    },
    {
        "id": 5,
        "title": "Change Directory",
        "description": "Navigate to different folders.",
        "challenge": "Change into the 'testfolder' directory you just created.",
        "hint": "cd foldername",
        "solution": "cd testfolder",
        "expected_output": None,
        "shell": "cmd",
        "check_command": True,
        "explanation": "cd changes directory. Use 'cd ..' to go up one level, 'cd \\' for root.",
        "points": 20,
        "category": "basics"
    },
    {
        "id": 6,
        "title": "Create a File",
        "description": "Make a new empty file.",
        "challenge": "Create an empty file named 'test.txt' using type nul.",
        "hint": "type nul > filename",
        "solution": "type nul > test.txt",
        "expected_output": None,
        "shell": "cmd",
        "check_command": True,
        "explanation": "type nul > creates empty files. In PowerShell, use New-Item.",
        "points": 20,
        "category": "basics"
    },
    {
        "id": 7,
        "title": "Write to a File",
        "description": "Put text into a file.",
        "challenge": "Write 'Hello Windows' into a file called output.txt using echo.",
        "hint": "Use > to redirect output to a file",
        "solution": "echo Hello Windows > output.txt",
        "expected_output": None,
        "shell": "cmd",
        "check_command": True,
        "explanation": "> redirects output to a file (overwrites). Use >> to append.",
        "points": 25,
        "category": "basics"
    },
    {
        "id": 8,
        "title": "Read a File",
        "description": "Display file contents.",
        "challenge": "Display the contents of output.txt using type.",
        "hint": "type filename",
        "solution": "type output.txt",
        "expected_output": "Hello Windows",
        "shell": "cmd",
        "explanation": "type displays file contents. Similar to cat in Linux.",
        "points": 25,
        "category": "basics"
    },
    {
        "id": 9,
        "title": "Copy Files",
        "description": "Duplicate files.",
        "challenge": "Copy output.txt to backup.txt using copy.",
        "hint": "copy source destination",
        "solution": "copy output.txt backup.txt",
        "expected_output": None,
        "shell": "cmd",
        "check_command": True,
        "explanation": "copy duplicates files. Use xcopy for directories.",
        "points": 30,
        "category": "basics"
    },
    {
        "id": 10,
        "title": "Rename Files",
        "description": "Change file names.",
        "challenge": "Rename backup.txt to old.txt using ren.",
        "hint": "ren oldname newname",
        "solution": "ren backup.txt old.txt",
        "expected_output": None,
        "shell": "cmd",
        "check_command": True,
        "explanation": "ren or rename changes file names. Use move to relocate files.",
        "points": 30,
        "category": "basics"
    },
    {
        "id": 11,
        "title": "Delete Files",
        "description": "Remove files carefully!",
        "challenge": "Delete the file old.txt using del.",
        "hint": "del filename (be careful!)",
        "solution": "del old.txt",
        "expected_output": None,
        "shell": "cmd",
        "check_command": True,
        "explanation": "del deletes files. Use /p for confirmation prompt. Be very careful!",
        "points": 35,
        "category": "basics"
    },
    {
        "id": 12,
        "title": "Clear Screen",
        "description": "Clean up the console.",
        "challenge": "Clear the screen using cls.",
        "hint": "cls clears the console",
        "solution": "cls",
        "expected_output": None,
        "shell": "cmd",
        "check_command": True,
        "explanation": "cls clears the screen. Useful when console gets cluttered!",
        "points": 35,
        "category": "basics"
    },
    {
        "id": 13,
        "title": "System Information",
        "description": "View system details.",
        "challenge": "Display system information using systeminfo.",
        "hint": "systeminfo shows detailed system info",
        "solution": "systeminfo",
        "expected_output": None,
        "shell": "cmd",
        "check_command": True,
        "explanation": "systeminfo shows OS version, hardware, network config, and more!",
        "points": 40,
        "category": "basics"
    },
    {
        "id": 14,
        "title": "IP Configuration",
        "description": "View network settings.",
        "challenge": "Display IP configuration using ipconfig.",
        "hint": "ipconfig shows network adapter info",
        "solution": "ipconfig",
        "expected_output": None,
        "shell": "cmd",
        "check_command": True,
        "explanation": "ipconfig shows IP addresses. Use /all for detailed info, /release and /renew for DHCP.",
        "points": 40,
        "category": "basics"
    },
    {
        "id": 15,
        "title": "Find Command Help",
        "description": "Learn about commands.",
        "challenge": "Get help for the dir command using /?.",
        "hint": "command /?",
        "solution": "dir /?",
        "expected_output": None,
        "shell": "cmd",
        "check_command": True,
        "explanation": "/? shows command help. Use 'help command' or 'command /?' for documentation.",
        "points": 45,
        "category": "basics"
    },
    {
        "id": 16,
        "title": "Ping Test",
        "description": "Test network connectivity.",
        "challenge": "Ping localhost once using ping -n 1.",
        "hint": "ping -n count hostname",
        "solution": "ping -n 1 localhost",
        "expected_output": None,
        "shell": "cmd",
        "check_command": True,
        "explanation": "ping tests connectivity. -n limits count. Useful for troubleshooting!",
        "points": 45,
        "category": "basics"
    },
    {
        "id": 17,
        "title": "Tree Structure",
        "description": "Visualize directory structure.",
        "challenge": "Show directory tree using tree.",
        "hint": "tree shows folder structure",
        "solution": "tree",
        "expected_output": None,
        "shell": "cmd",
        "check_command": True,
        "explanation": "tree displays folder structure graphically. Use /f to include files.",
        "points": 50,
        "category": "basics"
    },
    {
        "id": 18,
        "title": "Find Files",
        "description": "Search for files.",
        "challenge": "Find all .txt files using dir *.txt.",
        "hint": "dir pattern or dir /s pattern for subdirectories",
        "solution": "dir *.txt",
        "expected_output": None,
        "shell": "cmd",
        "check_command": True,
        "explanation": "Use wildcards: * (any characters) and ? (single character). /s searches subdirectories.",
        "points": 50,
        "category": "basics"
    },
    {
        "id": 19,
        "title": "Pipe Commands",
        "description": "Chain commands together.",
        "challenge": "List files and count them: dir | find /c \".\"",
        "hint": "command1 | command2",
        "solution": "dir | find /c \".\"",
        "expected_output": None,
        "shell": "cmd",
        "check_command": True,
        "explanation": "Pipes (|) send output of one command to another. Very powerful!",
        "points": 55,
        "category": "basics"
    },
    {
        "id": 20,
        "title": "Environment Variables",
        "description": "View system variables.",
        "challenge": "Display the USERNAME environment variable using echo %USERNAME%.",
        "hint": "echo %VARIABLE%",
        "solution": "echo %USERNAME%",
        "expected_output": None,
        "shell": "cmd",
        "check_command": True,
        "explanation": "Environment variables store system info. Use %VAR% in CMD, $env:VAR in PowerShell.",
        "points": 55,
        "category": "basics"
    },

    # === INTERMEDIATE TIER (21-50): Batch & PowerShell Intro ===
    {
        "id": 21,
        "title": "PowerShell Hello",
        "description": "First PowerShell command!",
        "challenge": "Use Write-Host to print: Hello PowerShell!",
        "hint": "Write-Host 'text'",
        "solution": "Write-Host 'Hello PowerShell!'",
        "expected_output": "Hello PowerShell!",
        "shell": "powershell",
        "explanation": "Write-Host outputs text in PowerShell. Write-Output is for pipeline output.",
        "points": 60,
        "category": "powershell"
    },
    {
        "id": 22,
        "title": "Get Location",
        "description": "PowerShell current directory.",
        "challenge": "Get current location using Get-Location.",
        "hint": "Get-Location or pwd (alias)",
        "solution": "Get-Location",
        "expected_output": None,
        "shell": "powershell",
        "check_command": True,
        "explanation": "Get-Location shows current path. pwd is an alias. gl is the shortest alias!",
        "points": 65,
        "category": "powershell"
    },
    {
        "id": 23,
        "title": "List Items",
        "description": "PowerShell directory listing.",
        "challenge": "Get child items using Get-ChildItem.",
        "hint": "Get-ChildItem or ls (alias)",
        "solution": "Get-ChildItem",
        "expected_output": None,
        "shell": "powershell",
        "check_command": True,
        "explanation": "Get-ChildItem lists items. Aliases: ls, dir, gci. Returns objects, not text!",
        "points": 70,
        "category": "powershell"
    },
    {
        "id": 24,
        "title": "Variables in PowerShell",
        "description": "Store data in variables.",
        "challenge": "Create variable $name = 'Admin' and write it.",
        "hint": "$variable = value; Write-Host $variable",
        "solution": "$name = 'Admin'; Write-Host $name",
        "expected_output": "Admin",
        "shell": "powershell",
        "explanation": "Variables start with $. PowerShell is strongly typed but flexible.",
        "points": 75,
        "category": "powershell"
    },
    {
        "id": 25,
        "title": "PowerShell Pipeline",
        "description": "Object pipeline basics.",
        "challenge": "Get processes and select first 5: Get-Process | Select-Object -First 5",
        "hint": "cmdlet | Select-Object -First n",
        "solution": "Get-Process | Select-Object -First 5",
        "expected_output": None,
        "shell": "powershell",
        "check_command": True,
        "explanation": "PowerShell pipeline passes objects, not text. Much more powerful!",
        "points": 80,
        "category": "powershell"
    },
    {
        "id": 26,
        "title": "Get Service",
        "description": "View Windows services.",
        "challenge": "Get all services using Get-Service.",
        "hint": "Get-Service lists Windows services",
        "solution": "Get-Service",
        "expected_output": None,
        "shell": "powershell",
        "check_command": True,
        "explanation": "Get-Service shows Windows services. Use -Name to filter specific services.",
        "points": 85,
        "category": "powershell"
    },
    {
        "id": 27,
        "title": "Where-Object Filter",
        "description": "Filter objects in pipeline.",
        "challenge": "Get running services: Get-Service | Where-Object {$_.Status -eq 'Running'}",
        "hint": "Where-Object {condition}",
        "solution": "Get-Service | Where-Object {$_.Status -eq 'Running'}",
        "expected_output": None,
        "shell": "powershell",
        "check_command": True,
        "explanation": "Where-Object filters objects. $_ is current object. Alias: where or ?",
        "points": 90,
        "category": "powershell"
    },
    {
        "id": 28,
        "title": "Select Properties",
        "description": "Choose specific object properties.",
        "challenge": "Get services showing only Name and Status: Get-Service | Select-Object Name,Status",
        "hint": "Select-Object Property1,Property2",
        "solution": "Get-Service | Select-Object Name,Status -First 1",
        "expected_output": None,
        "shell": "powershell",
        "check_command": True,
        "explanation": "Select-Object chooses properties. Great for formatting output!",
        "points": 95,
        "category": "powershell"
    },
    {
        "id": 29,
        "title": "Measure Objects",
        "description": "Count and calculate.",
        "challenge": "Count running services: Get-Service | Where-Object {$_.Status -eq 'Running'} | Measure-Object",
        "hint": "Measure-Object counts objects",
        "solution": "Get-Service | Where-Object {$_.Status -eq 'Running'} | Measure-Object",
        "expected_output": None,
        "shell": "powershell",
        "check_command": True,
        "explanation": "Measure-Object counts, sums, averages. Essential for statistics!",
        "points": 100,
        "category": "powershell"
    },
    {
        "id": 30,
        "title": "Sort Objects",
        "description": "Order objects by properties.",
        "challenge": "Sort processes by CPU: Get-Process | Sort-Object CPU -Descending | Select-Object -First 5",
        "hint": "Sort-Object PropertyName -Descending",
        "solution": "Get-Process | Sort-Object CPU -Descending | Select-Object -First 5",
        "expected_output": None,
        "shell": "powershell",
        "check_command": True,
        "explanation": "Sort-Object orders by properties. Use -Descending for reverse order.",
        "points": 110,
        "category": "powershell"
    },
    {
        "id": 31,
        "title": "Get-Member",
        "description": "Discover object properties and methods.",
        "challenge": "See Get-Service members: Get-Service | Get-Member",
        "hint": "cmdlet | Get-Member shows available properties/methods",
        "solution": "Get-Service | Get-Member",
        "expected_output": None,
        "shell": "powershell",
        "check_command": True,
        "explanation": "Get-Member reveals object structure. Essential for learning cmdlets!",
        "points": 120,
        "category": "powershell"
    },
    {
        "id": 32,
        "title": "Format Table",
        "description": "Format output as table.",
        "challenge": "Format processes as table: Get-Process | Format-Table Name,CPU,Memory -AutoSize",
        "hint": "Format-Table Property1,Property2",
        "solution": "Get-Process | Format-Table Name,CPU -AutoSize | Out-String",
        "expected_output": None,
        "shell": "powershell",
        "check_command": True,
        "explanation": "Format-Table creates tabular output. Use -AutoSize for best fit.",
        "points": 125,
        "category": "powershell"
    },
    {
        "id": 33,
        "title": "If Statement",
        "description": "Conditional execution.",
        "challenge": "Write: if (5 -gt 3) { Write-Host 'Greater' }",
        "hint": "if (condition) { commands }",
        "solution": "if (5 -gt 3) { Write-Host 'Greater' }",
        "expected_output": "Greater",
        "shell": "powershell",
        "explanation": "if tests conditions. -gt greater, -lt less, -eq equals, -ne not equals.",
        "points": 130,
        "category": "powershell"
    },
    {
        "id": 34,
        "title": "ForEach Loop",
        "description": "Iterate over items.",
        "challenge": "Loop: 1..3 | ForEach-Object { Write-Host $_ }",
        "hint": "collection | ForEach-Object { $_ is current item }",
        "solution": "1..3 | ForEach-Object { Write-Host $_ }",
        "expected_output": "1\n2\n3",
        "shell": "powershell",
        "explanation": "ForEach-Object iterates. 1..3 creates range. $_ is current item.",
        "points": 135,
        "category": "powershell"
    },
    {
        "id": 35,
        "title": "Arrays in PowerShell",
        "description": "Store multiple values.",
        "challenge": "Create array: $colors = @('red','blue'); Write-Host $colors[0]",
        "hint": "@(item1, item2) creates arrays",
        "solution": "$colors = @('red','blue'); Write-Host $colors[0]",
        "expected_output": "red",
        "shell": "powershell",
        "explanation": "Arrays use @(). Index from 0. Use .Count property for length.",
        "points": 140,
        "category": "powershell"
    },
    {
        "id": 36,
        "title": "Hash Tables",
        "description": "Key-value pairs.",
        "challenge": "Create hashtable: $user = @{Name='Alice'; Age=30}; Write-Host $user.Name",
        "hint": "@{Key=Value; Key2=Value2}",
        "solution": "$user = @{Name='Alice'; Age=30}; Write-Host $user.Name",
        "expected_output": "Alice",
        "shell": "powershell",
        "explanation": "Hashtables are key-value pairs. Access with .Key or ['Key'].",
        "points": 145,
        "category": "powershell"
    },
    {
        "id": 37,
        "title": "Get-Content",
        "description": "Read file contents.",
        "challenge": "Read file: Get-Content output.txt",
        "hint": "Get-Content filename",
        "solution": "Get-Content output.txt",
        "expected_output": None,
        "shell": "powershell",
        "check_command": True,
        "explanation": "Get-Content reads files. Returns array of lines. Alias: gc, type, cat.",
        "points": 150,
        "category": "powershell"
    },
    {
        "id": 38,
        "title": "Set-Content",
        "description": "Write to files.",
        "challenge": "Write to file: 'PowerShell Data' | Set-Content psfile.txt",
        "hint": "'text' | Set-Content filename",
        "solution": "'PowerShell Data' | Set-Content psfile.txt",
        "expected_output": None,
        "shell": "powershell",
        "check_command": True,
        "explanation": "Set-Content writes to files. Add-Content appends. Out-File also works.",
        "points": 155,
        "category": "powershell"
    },
    {
        "id": 39,
        "title": "Test-Path",
        "description": "Check if files exist.",
        "challenge": "Test file existence: Test-Path psfile.txt",
        "hint": "Test-Path returns $true or $false",
        "solution": "Test-Path psfile.txt",
        "expected_output": None,
        "shell": "powershell",
        "check_command": True,
        "explanation": "Test-Path checks existence. Returns boolean. Essential for validation!",
        "points": 160,
        "category": "powershell"
    },
    {
        "id": 40,
        "title": "New-Item",
        "description": "Create files and folders.",
        "challenge": "Create folder: New-Item -ItemType Directory -Name PSFolder",
        "hint": "New-Item -ItemType Directory/File -Name name",
        "solution": "New-Item -ItemType Directory -Name PSFolder",
        "expected_output": None,
        "shell": "powershell",
        "check_command": True,
        "explanation": "New-Item creates files and folders. Very versatile cmdlet!",
        "points": 165,
        "category": "powershell"
    },
    {
        "id": 41,
        "title": "Remove-Item",
        "description": "Delete items.",
        "challenge": "Remove folder: Remove-Item PSFolder",
        "hint": "Remove-Item path",
        "solution": "Remove-Item PSFolder -Force",
        "expected_output": None,
        "shell": "powershell",
        "check_command": True,
        "explanation": "Remove-Item deletes files/folders. Use -Recurse for directories, -Force to skip prompts.",
        "points": 170,
        "category": "powershell"
    },
    {
        "id": 42,
        "title": "Copy-Item",
        "description": "Copy files and folders.",
        "challenge": "Copy file: Copy-Item psfile.txt -Destination pscopy.txt",
        "hint": "Copy-Item source -Destination dest",
        "solution": "Copy-Item psfile.txt -Destination pscopy.txt",
        "expected_output": None,
        "shell": "powershell",
        "check_command": True,
        "explanation": "Copy-Item copies files/folders. Use -Recurse for directories.",
        "points": 175,
        "category": "powershell"
    },
    {
        "id": 43,
        "title": "Move-Item",
        "description": "Move or rename items.",
        "challenge": "Rename file: Move-Item pscopy.txt -Destination renamed.txt",
        "hint": "Move-Item source -Destination dest",
        "solution": "Move-Item pscopy.txt -Destination renamed.txt",
        "expected_output": None,
        "shell": "powershell",
        "check_command": True,
        "explanation": "Move-Item moves or renames. Same item, different name = rename!",
        "points": 180,
        "category": "powershell"
    },
    {
        "id": 44,
        "title": "Get-Date",
        "description": "Work with dates.",
        "challenge": "Get current date: Get-Date",
        "hint": "Get-Date with -Format for custom format",
        "solution": "Get-Date",
        "expected_output": None,
        "shell": "powershell",
        "check_command": True,
        "explanation": "Get-Date gets current date/time. Use -Format for custom formatting!",
        "points": 185,
        "category": "powershell"
    },
    {
        "id": 45,
        "title": "Start-Process",
        "description": "Launch applications.",
        "challenge": "Know Start-Process launches apps: Write-Host 'Start-Process notepad.exe'",
        "hint": "Start-Process application",
        "solution": "Write-Host 'Start-Process notepad.exe'",
        "expected_output": "Start-Process notepad.exe",
        "shell": "powershell",
        "explanation": "Start-Process starts applications. Use -Wait to wait for completion.",
        "points": 190,
        "category": "powershell"
    },
    {
        "id": 46,
        "title": "Stop-Process",
        "description": "Terminate processes.",
        "challenge": "Know Stop-Process kills processes: Write-Host 'Stop-Process -Name notepad'",
        "hint": "Stop-Process -Name name or -Id id",
        "solution": "Write-Host 'Stop-Process -Name notepad'",
        "expected_output": "Stop-Process -Name notepad",
        "shell": "powershell",
        "explanation": "Stop-Process terminates processes. Use -Force for stubborn processes.",
        "points": 195,
        "category": "powershell"
    },
    {
        "id": 47,
        "title": "Get-Command",
        "description": "Discover available commands.",
        "challenge": "Find all Get commands: Get-Command Get-*",
        "hint": "Get-Command pattern",
        "solution": "Get-Command Get-* | Select-Object -First 5",
        "expected_output": None,
        "shell": "powershell",
        "check_command": True,
        "explanation": "Get-Command finds cmdlets. Essential for discovery!",
        "points": 200,
        "category": "powershell"
    },
    {
        "id": 48,
        "title": "Get-Help",
        "description": "Get command documentation.",
        "challenge": "Get help: Get-Help Get-Process",
        "hint": "Get-Help cmdlet",
        "solution": "Get-Help Get-Process",
        "expected_output": None,
        "shell": "powershell",
        "check_command": True,
        "explanation": "Get-Help shows documentation. Use -Examples for examples, -Full for complete help.",
        "points": 205,
        "category": "powershell"
    },
    {
        "id": 49,
        "title": "Select-String",
        "description": "Search text patterns.",
        "challenge": "Search in file: Select-String 'pattern' -Path file.txt (simulation)",
        "hint": "Select-String -Pattern pattern -Path file",
        "solution": "Write-Host 'Select-String pattern file.txt'",
        "expected_output": "Select-String pattern file.txt",
        "shell": "powershell",
        "explanation": "Select-String is like grep. Searches for patterns in files.",
        "points": 210,
        "category": "powershell"
    },
    {
        "id": 50,
        "title": "Export-CSV",
        "description": "Save data to CSV.",
        "challenge": "Know Export-Csv saves to CSV: Write-Host 'cmdlet | Export-Csv file.csv'",
        "hint": "objects | Export-Csv filename",
        "solution": "Write-Host 'cmdlet | Export-Csv file.csv'",
        "expected_output": "cmdlet | Export-Csv file.csv",
        "shell": "powershell",
        "explanation": "Export-Csv saves pipeline output to CSV. Use Import-Csv to read back!",
        "points": 215,
        "category": "powershell"
    },

    # === ADVANCED TIER (51-75): Advanced PowerShell & Administration ===
    {
        "id": 51,
        "title": "Functions in PowerShell",
        "description": "Create reusable functions.",
        "challenge": "Define function: function Say-Hello { Write-Host 'Hello!' }; Say-Hello",
        "hint": "function Name { commands }",
        "solution": "function Say-Hello { Write-Host 'Hello!' }; Say-Hello",
        "expected_output": "Hello!",
        "shell": "powershell",
        "explanation": "Functions encapsulate code. Use Verb-Noun naming convention!",
        "points": 220,
        "category": "advanced"
    },
    {
        "id": 52,
        "title": "Function Parameters",
        "description": "Functions with arguments.",
        "challenge": "Function with param: function Greet($name) { Write-Host \"Hello $name\" }; Greet 'World'",
        "hint": "function Name($param) { use $param }",
        "solution": "function Greet($name) { Write-Host \"Hello $name\" }; Greet 'World'",
        "expected_output": "Hello World",
        "shell": "powershell",
        "explanation": "Parameters make functions flexible. Use param() block for advanced parameters!",
        "points": 225,
        "category": "advanced"
    },
    {
        "id": 53,
        "title": "Try-Catch",
        "description": "Error handling.",
        "challenge": "Handle errors: try { 1/0 } catch { Write-Host 'Error caught' }",
        "hint": "try { risky code } catch { handle error }",
        "solution": "try { Get-Item NonExistent -ErrorAction Stop } catch { Write-Host 'Error caught' }",
        "expected_output": "Error caught",
        "shell": "powershell",
        "explanation": "try-catch handles errors gracefully. Essential for robust scripts!",
        "points": 230,
        "category": "advanced"
    },
    {
        "id": 54,
        "title": "Error Variables",
        "description": "Access error information.",
        "challenge": "Know $Error contains errors: Write-Host '$Error[0] shows last error'",
        "hint": "$Error automatic variable",
        "solution": "Write-Host '$Error[0] shows last error'",
        "expected_output": "$Error[0] shows last error",
        "shell": "powershell",
        "explanation": "$Error array holds all errors. $Error[0] is most recent.",
        "points": 235,
        "category": "advanced"
    },
    {
        "id": 55,
        "title": "Execution Policy",
        "description": "Script execution security.",
        "challenge": "Get execution policy: Get-ExecutionPolicy",
        "hint": "Get-ExecutionPolicy shows current policy",
        "solution": "Get-ExecutionPolicy",
        "expected_output": None,
        "shell": "powershell",
        "check_command": True,
        "explanation": "ExecutionPolicy controls script running. RemoteSigned is common for development.",
        "points": 240,
        "category": "advanced"
    },
    {
        "id": 56,
        "title": "Modules",
        "description": "Import PowerShell modules.",
        "challenge": "Know Import-Module loads modules: Write-Host 'Import-Module ModuleName'",
        "hint": "Import-Module name",
        "solution": "Write-Host 'Import-Module ModuleName'",
        "expected_output": "Import-Module ModuleName",
        "shell": "powershell",
        "explanation": "Modules extend PowerShell. Use Get-Module to list loaded modules.",
        "points": 245,
        "category": "advanced"
    },
    {
        "id": 57,
        "title": "Registry Access",
        "description": "Read Windows Registry.",
        "challenge": "Get registry value: Get-ItemProperty 'HKLM:\\Software\\Microsoft\\Windows\\CurrentVersion'",
        "hint": "Get-ItemProperty registry-path",
        "solution": "Write-Host 'Get-ItemProperty HKLM:\\Software'",
        "expected_output": "Get-ItemProperty HKLM:\\Software",
        "shell": "powershell",
        "explanation": "PowerShell treats registry like filesystem. HKLM: and HKCU: are drives!",
        "points": 250,
        "category": "advanced"
    },
    {
        "id": 58,
        "title": "WMI Queries",
        "description": "Windows Management Instrumentation.",
        "challenge": "Get OS info: Get-WmiObject Win32_OperatingSystem | Select-Object Caption",
        "hint": "Get-WmiObject Win32_ClassName",
        "solution": "Get-WmiObject Win32_OperatingSystem | Select-Object Caption",
        "expected_output": None,
        "shell": "powershell",
        "check_command": True,
        "explanation": "WMI provides system information. Get-CimInstance is modern replacement.",
        "points": 255,
        "category": "advanced"
    },
    {
        "id": 59,
        "title": "CIM Instance",
        "description": "Modern WMI alternative.",
        "challenge": "Get computer info: Get-CimInstance Win32_ComputerSystem | Select-Object Name",
        "hint": "Get-CimInstance Win32_Class",
        "solution": "Get-CimInstance Win32_ComputerSystem | Select-Object Name",
        "expected_output": None,
        "shell": "powershell",
        "check_command": True,
        "explanation": "Get-CimInstance is faster and better than Get-WmiObject. Use it!",
        "points": 260,
        "category": "advanced"
    },
    {
        "id": 60,
        "title": "Event Logs",
        "description": "Read Windows event logs.",
        "challenge": "Get recent events: Get-EventLog Application -Newest 5",
        "hint": "Get-EventLog LogName -Newest n",
        "solution": "Get-EventLog Application -Newest 5",
        "expected_output": None,
        "shell": "powershell",
        "check_command": True,
        "explanation": "Get-EventLog reads Windows event logs. Essential for troubleshooting!",
        "points": 265,
        "category": "advanced"
    },
    {
        "id": 61,
        "title": "Scheduled Tasks",
        "description": "View scheduled tasks.",
        "challenge": "Know Get-ScheduledTask lists tasks: Write-Host 'Get-ScheduledTask'",
        "hint": "Get-ScheduledTask",
        "solution": "Write-Host 'Get-ScheduledTask'",
        "expected_output": "Get-ScheduledTask",
        "shell": "powershell",
        "explanation": "Get-ScheduledTask manages scheduled tasks. Windows task automation!",
        "points": 270,
        "category": "advanced"
    },
    {
        "id": 62,
        "title": "Network Adapter",
        "description": "Manage network adapters.",
        "challenge": "Get adapters: Get-NetAdapter",
        "hint": "Get-NetAdapter shows network adapters",
        "solution": "Get-NetAdapter",
        "expected_output": None,
        "shell": "powershell",
        "check_command": True,
        "explanation": "Get-NetAdapter manages network interfaces. Part of NetAdapter module.",
        "points": 275,
        "category": "advanced"
    },
    {
        "id": 63,
        "title": "IP Address",
        "description": "Get IP configuration.",
        "challenge": "Get IP: Get-NetIPAddress",
        "hint": "Get-NetIPAddress",
        "solution": "Get-NetIPAddress | Select-Object -First 1",
        "expected_output": None,
        "shell": "powershell",
        "check_command": True,
        "explanation": "Get-NetIPAddress shows IP addresses. PowerShell way of ipconfig!",
        "points": 280,
        "category": "advanced"
    },
    {
        "id": 64,
        "title": "Firewall Rules",
        "description": "View firewall configuration.",
        "challenge": "Know Get-NetFirewallRule shows firewall: Write-Host 'Get-NetFirewallRule'",
        "hint": "Get-NetFirewallRule",
        "solution": "Write-Host 'Get-NetFirewallRule'",
        "expected_output": "Get-NetFirewallRule",
        "shell": "powershell",
        "explanation": "Get-NetFirewallRule manages Windows Firewall. Powerful automation!",
        "points": 285,
        "category": "advanced"
    },
    {
        "id": 65,
        "title": "Measure-Command",
        "description": "Benchmark command execution.",
        "challenge": "Time command: Measure-Command { Get-Process } | Select-Object TotalMilliseconds",
        "hint": "Measure-Command { commands }",
        "solution": "Measure-Command { Get-Process } | Select-Object TotalMilliseconds",
        "expected_output": None,
        "shell": "powershell",
        "check_command": True,
        "explanation": "Measure-Command times execution. Essential for optimization!",
        "points": 290,
        "category": "advanced"
    },
    {
        "id": 66,
        "title": "Start-Job",
        "description": "Background jobs.",
        "challenge": "Know Start-Job runs in background: Write-Host 'Start-Job { commands }'",
        "hint": "Start-Job { scriptblock }",
        "solution": "Write-Host 'Start-Job { commands }'",
        "expected_output": "Start-Job { commands }",
        "shell": "powershell",
        "explanation": "Start-Job runs commands in background. Use Get-Job and Receive-Job!",
        "points": 295,
        "category": "advanced"
    },
    {
        "id": 67,
        "title": "Invoke-WebRequest",
        "description": "Make HTTP requests.",
        "challenge": "Know Invoke-WebRequest downloads: Write-Host 'Invoke-WebRequest URL'",
        "hint": "Invoke-WebRequest -Uri url",
        "solution": "Write-Host 'Invoke-WebRequest URL'",
        "expected_output": "Invoke-WebRequest URL",
        "shell": "powershell",
        "explanation": "Invoke-WebRequest makes HTTP requests. wget/curl for PowerShell!",
        "points": 300,
        "category": "advanced"
    },
    {
        "id": 68,
        "title": "ConvertTo-Json",
        "description": "Convert objects to JSON.",
        "challenge": "Convert to JSON: @{Name='Test'} | ConvertTo-Json",
        "hint": "object | ConvertTo-Json",
        "solution": "@{Name='Test'} | ConvertTo-Json",
        "expected_output": None,
        "shell": "powershell",
        "check_command": True,
        "explanation": "ConvertTo-Json serializes objects. ConvertFrom-Json deserializes!",
        "points": 305,
        "category": "advanced"
    },
    {
        "id": 69,
        "title": "Advanced Functions",
        "description": "Cmdlet-style functions.",
        "challenge": "Know [CmdletBinding()] makes advanced functions: Write-Host 'function F { [CmdletBinding()] param() }'",
        "hint": "[CmdletBinding()] enables advanced features",
        "solution": "Write-Host 'function F { [CmdletBinding()] param() }'",
        "expected_output": "function F { [CmdletBinding()] param() }",
        "shell": "powershell",
        "explanation": "[CmdletBinding()] adds -Verbose, -Debug, etc. Professional functions!",
        "points": 310,
        "category": "advanced"
    },
    {
        "id": 70,
        "title": "Parameter Validation",
        "description": "Validate function parameters.",
        "challenge": "Know [ValidateNotNullOrEmpty()] validates: Write-Host '[ValidateNotNullOrEmpty()]'",
        "hint": "Validation attributes ensure data quality",
        "solution": "Write-Host '[ValidateNotNullOrEmpty()]'",
        "expected_output": "[ValidateNotNullOrEmpty()]",
        "shell": "powershell",
        "explanation": "Validation attributes ensure parameters meet requirements. Many types available!",
        "points": 315,
        "category": "advanced"
    },
    {
        "id": 71,
        "title": "Splatting",
        "description": "Pass parameters as hashtable.",
        "challenge": "Splat parameters: $params = @{Name='test'}; Write-Host @params",
        "hint": "$params = @{Key=Value}; Cmdlet @params",
        "solution": "$params = @{Object='test'}; Write-Host @params",
        "expected_output": "test",
        "shell": "powershell",
        "explanation": "Splatting (@params) passes hashtable as parameters. Cleaner code!",
        "points": 320,
        "category": "advanced"
    },
    {
        "id": 72,
        "title": "Remoting Basics",
        "description": "PowerShell remoting.",
        "challenge": "Know Enter-PSSession connects remote: Write-Host 'Enter-PSSession -ComputerName PC'",
        "hint": "Enter-PSSession for interactive, Invoke-Command for one-off",
        "solution": "Write-Host 'Enter-PSSession -ComputerName PC'",
        "expected_output": "Enter-PSSession -ComputerName PC",
        "shell": "powershell",
        "explanation": "PowerShell Remoting uses WinRM. Powerful remote management!",
        "points": 325,
        "category": "advanced"
    },
    {
        "id": 73,
        "title": "Script Blocks",
        "description": "Code as data.",
        "challenge": "Create scriptblock: $code = { Write-Host 'Hello' }; & $code",
        "hint": "$var = { commands }; & $var to execute",
        "solution": "$code = { Write-Host 'Hello' }; & $code",
        "expected_output": "Hello",
        "shell": "powershell",
        "explanation": "ScriptBlocks are code objects. Use & to execute. Very powerful!",
        "points": 330,
        "category": "advanced"
    },
    {
        "id": 74,
        "title": "String Interpolation",
        "description": "Variables in strings.",
        "challenge": "Interpolate: $name = 'World'; Write-Host \"Hello $name\"",
        "hint": "Double quotes allow variable expansion",
        "solution": "$name = 'World'; Write-Host \"Hello $name\"",
        "expected_output": "Hello World",
        "shell": "powershell",
        "explanation": "Double quotes expand variables. Single quotes don't. Use $() for expressions!",
        "points": 335,
        "category": "advanced"
    },
    {
        "id": 75,
        "title": "Comparison Operators",
        "description": "Advanced comparisons.",
        "challenge": "Pattern match: 'test' -match 't.*t'; Write-Host $Matches[0]",
        "hint": "-match for regex, -like for wildcards",
        "solution": "'test' -match 't.*t'; Write-Host $Matches[0]",
        "expected_output": "test",
        "shell": "powershell",
        "explanation": "-match uses regex. $Matches contains matches. -like uses wildcards.",
        "points": 340,
        "category": "advanced"
    },

    # === EXPERT TIER (76-100): Professional Automation ===
    {
        "id": 76,
        "title": "Profile Scripts",
        "description": "Customize PowerShell startup.",
        "challenge": "Know $PROFILE contains profile path: Write-Host '$PROFILE'",
        "hint": "$PROFILE variable",
        "solution": "Write-Host '$PROFILE'",
        "expected_output": "$PROFILE",
        "shell": "powershell",
        "explanation": "$PROFILE script runs at startup. Customize your environment!",
        "points": 345,
        "category": "expert"
    },
    {
        "id": 77,
        "title": "PSCustomObject",
        "description": "Create custom objects.",
        "challenge": "Create object: [PSCustomObject]@{Name='Test'; Value=123} | Format-Table",
        "hint": "[PSCustomObject]@{Property=Value}",
        "solution": "[PSCustomObject]@{Name='Test'; Value=123}",
        "expected_output": None,
        "shell": "powershell",
        "check_command": True,
        "explanation": "PSCustomObject creates structured data. Essential for output!",
        "points": 350,
        "category": "expert"
    },
    {
        "id": 78,
        "title": "Group-Object",
        "description": "Group objects by property.",
        "challenge": "Group services: Get-Service | Group-Object Status",
        "hint": "Group-Object PropertyName",
        "solution": "Get-Service | Group-Object Status",
        "expected_output": None,
        "shell": "powershell",
        "check_command": True,
        "explanation": "Group-Object groups by properties. Great for analysis!",
        "points": 355,
        "category": "expert"
    },
    {
        "id": 79,
        "title": "Compare-Object",
        "description": "Compare two sets of objects.",
        "challenge": "Know Compare-Object diffs: Write-Host 'Compare-Object $a $b'",
        "hint": "Compare-Object -ReferenceObject $a -DifferenceObject $b",
        "solution": "Write-Host 'Compare-Object $a $b'",
        "expected_output": "Compare-Object $a $b",
        "shell": "powershell",
        "explanation": "Compare-Object finds differences. Essential for validation!",
        "points": 360,
        "category": "expert"
    },
    {
        "id": 80,
        "title": "Calculated Properties",
        "description": "Add computed properties.",
        "challenge": "Add property: Get-Process | Select-Object Name, @{Name='MB';Expression={$_.WS/1MB}} | Select-Object -First 1",
        "hint": "Select-Object Name, @{Name='X';Expression={calculation}}",
        "solution": "Get-Process | Select-Object Name, @{Name='MB';Expression={$_.WS/1MB}} -First 1",
        "expected_output": None,
        "shell": "powershell",
        "check_command": True,
        "explanation": "Calculated properties add computed values. Very powerful!",
        "points": 365,
        "category": "expert"
    },
    {
        "id": 81,
        "title": "Progress Bars",
        "description": "Show script progress.",
        "challenge": "Show progress: 1..3 | ForEach-Object { Write-Progress -Activity 'Processing' -Status $_ -PercentComplete ($_/3*100); Start-Sleep -Milliseconds 100 }",
        "hint": "Write-Progress -Activity name -PercentComplete %",
        "solution": "1..3 | ForEach-Object { Write-Progress -Activity 'Test' -PercentComplete ($_/3*100) }",
        "expected_output": None,
        "shell": "powershell",
        "check_command": True,
        "explanation": "Write-Progress shows progress bars. Professional scripts!",
        "points": 370,
        "category": "expert"
    },
    {
        "id": 82,
        "title": "Logging Functions",
        "description": "Professional logging.",
        "challenge": "Create logger: function Write-Log($msg) { \"$(Get-Date) - $msg\" | Out-File log.txt -Append }; Write-Log 'Test'",
        "hint": "Timestamp and append to log file",
        "solution": "function Write-Log($msg) { \"$(Get-Date) - $msg\" | Out-File log.txt -Append }; Write-Log 'Test'",
        "expected_output": None,
        "shell": "powershell",
        "check_command": True,
        "explanation": "Logging is essential for production scripts. Always log important actions!",
        "points": 375,
        "category": "expert"
    },
    {
        "id": 83,
        "title": "Pipeline Functions",
        "description": "Process pipeline input.",
        "challenge": "Know process{} handles pipeline: Write-Host 'function F { process { $_ } }'",
        "hint": "function Name { begin{} process{} end{} }",
        "solution": "Write-Host 'function F { process { $_ } }'",
        "expected_output": "function F { process { $_ } }",
        "shell": "powershell",
        "explanation": "begin/process/end blocks handle pipeline input. Advanced functions!",
        "points": 380,
        "category": "expert"
    },
    {
        "id": 84,
        "title": "Credential Management",
        "description": "Handle credentials securely.",
        "challenge": "Know Get-Credential prompts securely: Write-Host 'Get-Credential'",
        "hint": "Get-Credential for secure password input",
        "solution": "Write-Host 'Get-Credential'",
        "expected_output": "Get-Credential",
        "shell": "powershell",
        "explanation": "Get-Credential prompts for credentials securely. Never hardcode passwords!",
        "points": 385,
        "category": "expert"
    },
    {
        "id": 85,
        "title": "Secure Strings",
        "description": "Encrypt sensitive data.",
        "challenge": "Know ConvertTo-SecureString encrypts: Write-Host 'ConvertTo-SecureString'",
        "hint": "ConvertTo-SecureString for passwords",
        "solution": "Write-Host 'ConvertTo-SecureString'",
        "expected_output": "ConvertTo-SecureString",
        "shell": "powershell",
        "explanation": "SecureString encrypts passwords in memory. Security best practice!",
        "points": 390,
        "category": "expert"
    },
    {
        "id": 86,
        "title": "Comment-Based Help",
        "description": "Document functions properly.",
        "challenge": "Know <# .SYNOPSIS #> creates help: Write-Host '<# .SYNOPSIS Description #>'",
        "hint": "Comment-based help in functions",
        "solution": "Write-Host '<# .SYNOPSIS Description #>'",
        "expected_output": "<# .SYNOPSIS Description #>",
        "shell": "powershell",
        "explanation": "Comment-based help makes functions professional. Use .SYNOPSIS, .DESCRIPTION, etc!",
        "points": 395,
        "category": "expert"
    },
    {
        "id": 87,
        "title": "Regular Expressions",
        "description": "Pattern matching mastery.",
        "challenge": "Extract pattern: 'Email: test@example.com' -match '([\\w.-]+@[\\w.-]+)'; Write-Host $Matches[1]",
        "hint": "-match with capture groups ()",
        "solution": "'Email: test@example.com' -match '([\\w.-]+@[\\w.-]+)'; Write-Host $Matches[1]",
        "expected_output": "test@example.com",
        "shell": "powershell",
        "explanation": "Regex captures with (). $Matches contains captured groups. Powerful!",
        "points": 400,
        "category": "expert"
    },
    {
        "id": 88,
        "title": "DSC Basics",
        "description": "Desired State Configuration.",
        "challenge": "Know DSC enforces configuration: Write-Host 'configuration ConfigName { }'",
        "hint": "DSC for declarative configuration",
        "solution": "Write-Host 'configuration ConfigName { }'",
        "expected_output": "configuration ConfigName { }",
        "shell": "powershell",
        "explanation": "DSC ensures systems stay configured. Infrastructure as code!",
        "points": 405,
        "category": "expert"
    },
    {
        "id": 89,
        "title": "Class Definitions",
        "description": "Object-oriented PowerShell.",
        "challenge": "Define class: class Person { [string]$Name }; $p = [Person]::new(); $p.Name = 'Alice'; Write-Host $p.Name",
        "hint": "class ClassName { [type]$Property }",
        "solution": "class Person { [string]$Name }; $p = [Person]::new(); $p.Name = 'Alice'; Write-Host $p.Name",
        "expected_output": "Alice",
        "shell": "powershell",
        "explanation": "PowerShell 5+ supports classes. Full OOP capabilities!",
        "points": 410,
        "category": "expert"
    },
    {
        "id": 90,
        "title": "Runspaces",
        "description": "True multithreading.",
        "challenge": "Know Runspaces enable parallel execution: Write-Host 'Runspace for true parallelism'",
        "hint": "Runspaces run code in parallel",
        "solution": "Write-Host 'Runspace for true parallelism'",
        "expected_output": "Runspace for true parallelism",
        "shell": "powershell",
        "explanation": "Runspaces provide real parallelism. Much faster than jobs!",
        "points": 415,
        "category": "expert"
    },
    {
        "id": 91,
        "title": "Error Action Preference",
        "description": "Control error handling globally.",
        "challenge": "Set preference: $ErrorActionPreference = 'Stop'; Write-Host $ErrorActionPreference",
        "hint": "$ErrorActionPreference = 'Stop'/'Continue'/'SilentlyContinue'",
        "solution": "$ErrorActionPreference = 'Stop'; Write-Host $ErrorActionPreference",
        "expected_output": "Stop",
        "shell": "powershell",
        "explanation": "$ErrorActionPreference controls error behavior globally. Stop makes errors terminating!",
        "points": 420,
        "category": "expert"
    },
    {
        "id": 92,
        "title": "Verbose Output",
        "description": "Debugging and detailed output.",
        "challenge": "Write verbose: Write-Verbose 'Detailed info' -Verbose",
        "hint": "Write-Verbose with -Verbose parameter",
        "solution": "Write-Verbose 'Detailed info' -Verbose",
        "expected_output": None,
        "shell": "powershell",
        "check_command": True,
        "explanation": "Write-Verbose for debugging output. Controlled by -Verbose parameter!",
        "points": 425,
        "category": "expert"
    },
    {
        "id": 93,
        "title": "Module Manifests",
        "description": "Professional module packaging.",
        "challenge": "Know .psd1 is module manifest: Write-Host 'New-ModuleManifest creates .psd1'",
        "hint": "New-ModuleManifest for module metadata",
        "solution": "Write-Host 'New-ModuleManifest creates .psd1'",
        "expected_output": "New-ModuleManifest creates .psd1",
        "shell": "powershell",
        "explanation": "Module manifests (.psd1) describe modules. Professional packaging!",
        "points": 430,
        "category": "expert"
    },
    {
        "id": 94,
        "title": "Pester Testing",
        "description": "Unit testing for PowerShell.",
        "challenge": "Know Pester is testing framework: Write-Host 'Describe, It, Should for testing'",
        "hint": "Pester: Describe, Context, It, Should",
        "solution": "Write-Host 'Describe, It, Should for testing'",
        "expected_output": "Describe, It, Should for testing",
        "shell": "powershell",
        "explanation": "Pester is PowerShell testing framework. Professional development!",
        "points": 435,
        "category": "expert"
    },
    {
        "id": 95,
        "title": "Best Practices",
        "description": "Professional PowerShell standards.",
        "challenge": "List best practices: Write-Host 'Verb-Noun naming, approved verbs, comment help, error handling'",
        "hint": "Naming, documentation, error handling",
        "solution": "Write-Host 'Verb-Noun naming, approved verbs, comment help, error handling'",
        "expected_output": "Verb-Noun naming, approved verbs, comment help, error handling",
        "shell": "powershell",
        "explanation": "Best practices: approved verbs (Get-Verb), Verb-Noun, comments, error handling!",
        "points": 440,
        "category": "expert"
    },
    {
        "id": 96,
        "title": "Performance Optimization",
        "description": "Write faster scripts.",
        "challenge": "Know ArrayList is faster than +=: Write-Host '[System.Collections.ArrayList] faster than +='",
        "hint": "Use .NET collections, avoid +=",
        "solution": "Write-Host '[System.Collections.ArrayList] faster than +='",
        "expected_output": "[System.Collections.ArrayList] faster than +=",
        "shell": "powershell",
        "explanation": "Use .NET collections, avoid array +=, filter left, select properties early!",
        "points": 445,
        "category": "expert"
    },
    {
        "id": 97,
        "title": "PowerShell Gallery",
        "description": "Share and install modules.",
        "challenge": "Know Install-Module installs from gallery: Write-Host 'Install-Module from PSGallery'",
        "hint": "Install-Module, Publish-Module",
        "solution": "Write-Host 'Install-Module from PSGallery'",
        "expected_output": "Install-Module from PSGallery",
        "shell": "powershell",
        "explanation": "PowerShell Gallery is module repository. Install-Module to get, Publish-Module to share!",
        "points": 450,
        "category": "expert"
    },
    {
        "id": 98,
        "title": "Cross-Platform PowerShell",
        "description": "PowerShell Core for Linux/Mac.",
        "challenge": "Know PowerShell Core is cross-platform: Write-Host 'PowerShell 7+ on Linux/Mac/Windows'",
        "hint": "PowerShell Core/7+ is cross-platform",
        "solution": "Write-Host 'PowerShell 7+ on Linux/Mac/Windows'",
        "expected_output": "PowerShell 7+ on Linux/Mac/Windows",
        "shell": "powershell",
        "explanation": "PowerShell 7+ runs everywhere! Open-source and cross-platform!",
        "points": 455,
        "category": "expert"
    },
    {
        "id": 99,
        "title": "Azure Automation",
        "description": "Cloud automation with PowerShell.",
        "challenge": "Know Azure PowerShell module: Write-Host 'Connect-AzAccount, Get-AzVM for Azure'",
        "hint": "Az module for Azure automation",
        "solution": "Write-Host 'Connect-AzAccount, Get-AzVM for Azure'",
        "expected_output": "Connect-AzAccount, Get-AzVM for Azure",
        "shell": "powershell",
        "explanation": "Az module automates Azure. Cloud automation with PowerShell!",
        "points": 460,
        "category": "expert"
    },
    {
        "id": 100,
        "title": "The Ultimate Challenge",
        "description": "Complete PowerShell automation script.",
        "challenge": "Create a function that: 1) Takes computername parameter, 2) Validates input, 3) Gets system info, 4) Exports to CSV, 5) Includes error handling and logging.",
        "hint": "Combine everything you've learned!",
        "solution": """function Get-SystemReport {
    [CmdletBinding()]
    param([Parameter(Mandatory)][ValidateNotNullOrEmpty()][string]$ComputerName)
    
    try {
        Write-Verbose "Getting info from $ComputerName"
        $info = Get-CimInstance Win32_OperatingSystem -ComputerName $ComputerName |
                Select-Object CSName, Caption, Version
        $info | Export-Csv "report_$(Get-Date -Format yyyyMMdd).csv" -NoTypeInformation
        Write-Host "Report generated successfully"
    }
    catch {
        Write-Error "Failed: $_"
        Write-Log "Error: $_"
    }
}
Write-Host 'Function created!'""",
        "expected_output": None,
        "shell": "powershell",
        "check_command": True,
        "explanation": "You've mastered PowerShell! Parameters, validation, error handling, logging, CIM queries, CSV export. You're a Windows Grandmaster! 🏆",
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
    ║  ██╗    ██╗██╗███╗   ██╗██████╗  ██████╗ ██╗    ██╗███████╗  ║
    ║  ██║    ██║██║████╗  ██║██╔══██╗██╔═══██╗██║    ██║██╔════╝  ║
    ║  ██║ █╗ ██║██║██╔██╗ ██║██║  ██║██║   ██║██║ █╗ ██║███████╗  ║
    ║  ██║███╗██║██║██║╚██╗██║██║  ██║██║   ██║██║███╗██║╚════██║  ║
    ║  ╚███╔███╔╝██║██║ ╚████║██████╔╝╚██████╔╝╚███╔███╔╝███████║  ║
    ║   ╚══╝╚══╝ ╚═╝╚═╝  ╚═══╝╚═════╝  ╚═════╝  ╚══╝╚══╝ ╚══════╝  ║
    ║                                                               ║
    ║            🪟 CMD & PowerShell Mastery 🪟                     ║
    ║                                                               ║
    ║        Learn Windows Command-Line from Zero to Expert        ║
    ║                  Author: arkanzasfeziii                       ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    """
    console.print(f"[{COLORS['windows']}]{banner}[/]")
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
    table.add_column("Value", style=COLORS['windows'])

    table.add_row("Current Level", f"{progress.current_level}/100")
    table.add_row("Completed Levels", str(len(progress.completed_levels)))
    table.add_row("Total Points", str(progress.total_points))
    table.add_row("Current Rank", rank_name)
    table.add_row("Rank Description", rank_desc)
    table.add_row("Achievements", str(len(progress.achievements)))

    console.print(table)


def show_level_info(level_data: dict):
    """Display information about a level."""
    shell_name = "PowerShell" if level_data['shell'] == 'powershell' else "CMD"
    panel = Panel(
        f"""[{COLORS['windows']}]LEVEL {level_data['id']}: {level_data['title'].upper()}[/]

[{COLORS['info']}]Shell:[/] [{COLORS['secondary']}]{shell_name}[/]
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


def simulate_windows_boot():
    """Show a Windows-style boot animation."""
    messages = [
        "Initializing Windows environment...",
        "Loading command processor...",
        "Starting PowerShell engine...",
        "Mounting system drives...",
        "System ready!",
    ]

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("[cyan]Booting...", total=len(messages))
        for msg in messages:
            progress.update(task, description=f"[{COLORS['windows']}]{msg}")
            time.sleep(random.uniform(0.3, 0.7))
            progress.advance(task)


# === Core Game Logic ===
def execute_windows_command(command: str, shell: str, expected_output: str | None = None) -> tuple[bool, str]:
    """
    Execute a Windows command and return success status and output.
    """
    try:
        if shell == 'cmd':
            # Execute with CMD
            result = subprocess.run(
                ['cmd', '/c', command],
                capture_output=True,
                text=True,
                timeout=10,
                shell=False
            )
        else:  # powershell
            # Execute with PowerShell
            result = subprocess.run(
                ['powershell', '-NoProfile', '-Command', command],
                capture_output=True,
                text=True,
                timeout=10,
                shell=False
            )

        output = result.stdout.strip()

        # If we have expected output, check it
        if expected_output is not None:
            expected_normalized = expected_output.strip()
            output_normalized = output.strip()
            # Allow partial match for flexibility
            return (expected_normalized in output_normalized or output_normalized in expected_normalized, output)
        else:
            # Just check if command executed without error
            return (result.returncode == 0, output)

    except subprocess.TimeoutExpired:
        return (False, "Command timed out (>10 seconds)")
    except FileNotFoundError:
        if shell == 'powershell':
            return (False, "PowerShell not found. Make sure PowerShell is installed.")
        return (False, "CMD not available")
    except Exception as e:
        return (False, f"Error: {str(e)}")


def play_level(level_data: dict, progress: PlayerProgress) -> bool:
    """
    Play a single level.
    Returns True if completed successfully.
    """
    show_level_info(level_data)
    console.print()

    shell_prompt = "PS>" if level_data['shell'] == 'powershell' else "C:\\>"

    # Show hint option
    console.print(f"[{COLORS['info']}]💡 Type 'hint' for a hint, 'skip' to skip (no points), or enter your command:[/]")
    console.print()

    while True:
        try:
            user_input = Prompt.ask(f"[{COLORS['windows']}]{shell_prompt}")

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
    syntax = Syntax(user_input, "powershell" if level_data['shell'] == 'powershell' else "batch", theme="monokai", line_numbers=False)
    console.print(syntax)
    console.print()

    # Execute the command
    console.print(f"[{COLORS['warning']}]Executing command...[/]")
    time.sleep(0.5)

    success, output = execute_windows_command(user_input, level_data['shell'], level_data.get('expected_output'))

    if success:
        console.print(f"[{COLORS['success']}]✅ CORRECT! Level completed![/]")
        if output and len(output) < 500:
            console.print(f"[{COLORS['info']}]Output:[/] {output[:200]}...")
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
            console.print(f"[{COLORS['info']}]Output/Error:[/] {output[:200]}")
        if level_data.get('expected_output'):
            console.print(f"[{COLORS['info']}]Expected:[/] {level_data['expected_output']}")

        if Confirm.ask(f"[{COLORS['warning']}]Try again?"):
            return play_level(level_data, progress)
        return False


def check_achievements(progress: PlayerProgress):
    """Check and award achievements."""
    achievements = [
        (5, "🌟 First Commands", "Completed 5 levels"),
        (10, "⌨️ Command Master", "Completed 10 levels"),
        (25, "⚡ PowerShell Awakened", "Completed 25 levels"),
        (50, "🚀 Automation Expert", "Completed 50 levels"),
        (75, "👑 Windows Wizard", "Completed 75 levels"),
        (100, "⭐ Windows Grandmaster", "Completed ALL levels!"),
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
        console.print(f"\n[{COLORS['windows']}]Welcome back, {rank_name}![/]\n")

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
                        console.print(f"\n[{COLORS['windows']}]🎉 CONGRATULATIONS! You've completed ALL 100 levels! 🎉[/]")
                        console.print(f"[{COLORS['success']}]You are now a WINDOWS GRANDMASTER! ⭐[/]")
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
                table.add_column("Achievement", style=COLORS['windows'])
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
            console.print(f"\n[{COLORS['windows']}]Thanks for playing WindowsQuest! Happy scripting! 👋[/]")
            break


# === Entry Point ===
def main():
    """Main entry point."""
    try:
        # Check platform
        if platform.system() != 'Windows':
            console.print(f"[{COLORS['warning']}]Warning: This game is designed for Windows. Some commands may not work on {platform.system()}.[/]")
            if not Confirm.ask("Continue anyway?"):
                return

        console.clear()
        simulate_windows_boot()
        time.sleep(1)
        main_menu()
    except KeyboardInterrupt:
        console.print(f"\n\n[{COLORS['warning']}]Game interrupted. Progress saved. Goodbye! 👋[/]")
    except Exception as e:
        console.print(f"\n[{COLORS['error']}]An error occurred: {e}[/]")
        console.print(f"[{COLORS['info']}]Please report this bug to arkanzasfeziii[/]")


if __name__ == "__main__":
    main()
