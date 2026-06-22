# Architecture

## Package Structure

```
SecurityQuestAcademy/
├── main.py                  # Legacy launcher (kept for backward compat)
├── securityquest/           # New package entry point
│   ├── __main__.py          # python -m securityquest
│   ├── cli.py               # Menu, game launcher
│   └── config.py            # Game registry, constants
│
├── games/                   # Quest game modules
│   ├── base.py              # Shared engine: progress, executors, UI
│   ├── ciscoquest.py        # Cisco IOS networking (100 levels)
│   ├── cryptoquest.py       # Cryptography (100 levels)
│   ├── reversequest.py      # Reverse engineering (100 levels)
│   ├── webhackquest.py      # Web security (100 levels)
│   ├── cyberquest.py        # Python/Linux wrapper → standalone
│   ├── bashquest.py         # Bash wrapper → standalone
│   └── windowsquest.py      # Windows wrapper → standalone
│
├── standalone/              # Self-contained quest versions
│   ├── Cyberquest.py        # Python & Linux (100 levels)
│   ├── Bashquest.py         # Bash scripting (100 levels)
│   └── Windowsquest.py      # Windows/PowerShell (100 levels)
│
└── tests/
```

## Game Engine (games/base.py)

The shared engine provides:
- **PlayerProgress** — dataclass for level tracking, points, achievements, save/load
- **Execution engines:**
  - `eval_python_level()` — runs user Python code against test assertions
  - `execute_bash()` — runs shell commands in sandboxed temp scripts
  - `match_cisco_command()` — case-insensitive Cisco IOS command matching
- **UI helpers** — level display, stats, rank system, achievement notifications
- **Play functions** — `play_python_level()`, `play_cisco_level()`, `play_bash_level()`

## Data Flow

```
CLI Menu → select quest → importlib.import_module(quest)
                                    │
                                    ▼
                            quest.run() → loads LEVELS list
                                    │
                                    ▼
                        base.py engine loop:
                          show_level_info()
                          user writes code / command
                          execute via appropriate engine
                          update PlayerProgress
                          save to .json
```

Each quest defines a `LEVELS` list of 100 dicts. Each level has: id, title, category, points, description, challenge, hint, and test_code (or accepted_commands for Cisco).
