# Usage Guide

## Quick Start

```bash
pip install -r requirements.txt
python -m securityquest
```

Or with the legacy launcher:
```bash
python main.py
```

## Playing a Quest

1. Launch the academy
2. Select a quest (1-7) from the menu
3. Read the challenge description
4. Write your solution:
   - **Python quests**: type code line by line, then `done` to submit
   - **Bash quests**: type the shell command
   - **Cisco quests**: type the IOS command
5. Type `hint` for help, `skip` to skip

## The 7 Quests

| # | Quest | Domain | Engine |
|---|-------|--------|--------|
| 1 | CyberQuest | Python & Linux Security | Python exec |
| 2 | BashQuest | Bash & Shell Security | Bash exec |
| 3 | WindowsQuest | Windows & PowerShell | Command match |
| 4 | CiscoQuest | Cisco IOS Networking | Command match |
| 5 | CryptoQuest | Cryptography | Python exec |
| 6 | ReverseQuest | Reverse Engineering | Python exec |
| 7 | WebHackQuest | Web Security | Python exec |

## Progress

Progress auto-saves to `~/.securityquest/` or the working directory. Each quest has its own save file. You earn points, unlock ranks, and collect achievements as you progress.

## Running Individual Quests

```bash
# Direct quest launch (standalone)
python standalone/Cyberquest.py
python standalone/Bashquest.py

# Or via the menu
python -m securityquest
```
