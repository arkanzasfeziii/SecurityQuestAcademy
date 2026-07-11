# SecurityQuestAcademy

> **700 hands-on challenges across 7 cybersecurity domains — learn by writing real code, typing real commands, and solving real problems in an interactive terminal game.**

---

## What This Is

SecurityQuestAcademy is an interactive, gamified training platform that teaches cybersecurity through hands-on challenges. No slides. No multiple choice. You write actual Python exploits, type actual Cisco IOS commands, craft actual Bash scripts, and build actual attack payloads — all inside a terminal-based game engine with progress tracking, ranks, and achievements.

7 quest games. 100 levels each. 700 challenges total. From absolute beginner to expert.

---

## The 7 Quests

| # | Quest | Domain | What You Build |
|---|---|---|---|
| 1 | **CyberQuest** | Python & Linux Security | Python scripts for networking, crypto, system security, forensics, web scraping, malware analysis |
| 2 | **BashQuest** | Bash & Shell Security | File operations, text processing, pipes/redirects, regex, process management, automation scripts |
| 3 | **WindowsQuest** | Windows & PowerShell | CMD commands, PowerShell cmdlets, registry, services, Active Directory, Group Policy, forensics |
| 4 | **CiscoQuest** | Cisco IOS & Networking | CLI navigation, interface config, routing (OSPF/BGP/EIGRP), switching (VLANs/STP), ACLs, VPNs, NAT |
| 5 | **CryptoQuest** | Cryptography | Caesar/Vigenere/Enigma, AES/DES, RSA/ECC/Diffie-Hellman, SHA/HMAC, TLS handshake, PKI, post-quantum |
| 6 | **ReverseQuest** | Reverse Engineering | Binary/hex, x86 assembly, ELF/PE parsing, GDB debugging, IDA/Ghidra, anti-debug, buffer overflow, ROP |
| 7 | **WebHackQuest** | Web Security & Pentesting | HTTP parsing, XSS, SQLi, SSRF, SSTI, IDOR, JWT attacks, OAuth bypass, GraphQL, deserialization |

---

## How Challenges Work

Each quest uses one of three execution engines depending on the domain:

### Python Engine — Write and Execute
CyberQuest, CryptoQuest, ReverseQuest, and WebHackQuest present a problem and expect you to write a Python function that produces the correct output. Your code is executed and tested against assertions.

```
LEVEL 1: Caesar Cipher — Encrypt

Category: CLASSICAL  |  Points: 10

Description:
The Caesar cipher shifts each letter by a fixed number.
Julius Caesar used a shift of 3.

Challenge:
Write caesar_encrypt(text, shift) that encrypts uppercase letters only.
Example: caesar_encrypt('HELLO', 3) → 'KHOOR'

>>> def caesar_encrypt(text, shift):
>>>     result = ''
>>>     for c in text:
>>>         if c.isupper():
>>>             result += chr((ord(c) - ord('A') + shift) % 26 + ord('A'))
>>>         else:
>>>             result += c
>>>     return result
>>> done

✅ Correct! Level complete!
+10 points!
```

### Cisco Engine — Type the Command
CiscoQuest presents a network scenario and expects the exact Cisco IOS command. Abbreviations accepted (`conf t` for `configure terminal`).

```
LEVEL 5: Save Configuration

You've made changes to the running-config.
Save them so they survive a reload.

Router# copy running-config startup-config

✅ Correct! Level complete!
```

### Bash Engine — Execute on Your System
BashQuest and WindowsQuest challenges run your commands in a sandboxed shell and compare output against expected results.

```
LEVEL 12: Count Lines in a File

bash$ wc -l < /etc/passwd

✅ Correct! Level complete!
```

---

## Progression System

### Ranks
Each quest has 21 ranks that reflect your expertise level. Your rank updates as you complete levels:

```
Level  1-4    Script Newbie        →  Just starting
Level  5-9    Code Cadet           →  Learning the basics
Level 10-14   Terminal Rookie      →  Getting comfortable
  ...
Level 50-54   Exploit Developer    →  Creating exploits
  ...
Level 90-94   Cyber Samurai        →  Master of all domains
Level 95-99   Elite Guardian       →  Protecting the digital realm
Level 100     Legendary Hacker     →  The ultimate achievement
```

### Achievements
Milestone badges unlock as you hit level thresholds — 5, 10, 25, 50, 75, and 100 levels completed per quest.

### Progress Persistence
Progress is saved automatically to `~/.{quest}_save.json` after every completed level. Close and reopen anytime — your rank, points, completed levels, and achievements persist.

---

## Architecture

```
main.py                          ← Academy launcher — game selection menu
│
├── games/
│   ├── base.py                  ← Shared engine: progress, ranks, achievements,
│   │                               3 execution engines (Python/Cisco/Bash),
│   │                               level display, save/load
│   │
│   ├── ciscoquest.py            ← 100 Cisco IOS levels (cisco engine)
│   ├── cryptoquest.py           ← 100 Cryptography levels (python engine)
│   ├── reversequest.py          ← 100 Reverse Engineering levels (python engine)
│   ├── webhackquest.py          ← 100 Web Security levels (python engine)
│   │
│   ├── cyberquest.py            ← Launcher → standalone/Cyberquest.py
│   ├── bashquest.py             ← Launcher → standalone/Bashquest.py
│   └── windowsquest.py          ← Launcher → standalone/Windowsquest.py
│
└── standalone/
    ├── Cyberquest.py            ← 100 Python & Linux Security levels
    ├── Bashquest.py             ← 100 Bash & Shell levels
    └── Windowsquest.py          ← 100 Windows & PowerShell levels
```

The 4 integrated quests (Cisco, Crypto, Reverse, WebHack) share `base.py`'s game loop, execution engines, and progress infrastructure. The 3 standalone quests (Cyber, Bash, Windows) have their own self-contained engines with the same feature set.

---

## Level Coverage by Domain

### CyberQuest (100 levels)
`Python basics` → `data structures` → `file I/O` → `networking (sockets, HTTP)` → `system security` → `cryptography fundamentals` → `web scraping` → `forensics` → `malware analysis` → `exploit development`

### BashQuest (100 levels)
`Navigation & files` → `text processing (grep/sed/awk)` → `pipes & redirects` → `regex` → `scripting fundamentals` → `process management` → `permissions & security` → `networking commands` → `system administration` → `automation workflows`

### WindowsQuest (100 levels)
`CMD basics` → `file operations` → `PowerShell introduction` → `cmdlets & pipeline` → `registry editing` → `services & processes` → `Active Directory` → `Group Policy` → `security & forensics` → `advanced automation`

### CiscoQuest (100 levels)
`CLI modes (User/Priv/Global)` → `interface configuration` → `static routing` → `VLANs & trunking` → `STP` → `OSPF` → `EIGRP` → `BGP` → `ACLs` → `NAT/PAT` → `VPN/IPsec` → `device hardening` → `QoS`

### CryptoQuest (100 levels)
`Caesar/ROT13` → `Vigenere/Playfair` → `Enigma simulation` → `XOR` → `DES/3DES` → `AES (ECB/CBC/CTR/GCM)` → `RSA` → `Diffie-Hellman` → `ECC` → `SHA/HMAC` → `PBKDF2/bcrypt/Argon2` → `TLS handshake` → `PKI/X.509` → `post-quantum`

### ReverseQuest (100 levels)
`Binary/hex conversion` → `x86 registers & instructions` → `stack frames & calling conventions` → `ELF/PE format parsing` → `GDB commands` → `static analysis (IDA/Ghidra)` → `dynamic analysis` → `anti-debugging` → `unpacking` → `buffer overflow` → `ROP chains` → `format strings` → `malware analysis` → `fuzzing`

### WebHackQuest (100 levels)
`HTTP request parsing` → `URL/HTML encoding` → `cookies & sessions` → `XSS (reflected/stored/DOM)` → `SQL injection (error/blind/UNION)` → `CSRF` → `SSRF` → `file upload/inclusion` → `SSTI` → `IDOR` → `JWT attacks` → `OAuth bypass` → `GraphQL` → `deserialization` → `race conditions` → `CSP bypass`

---

## Usage

```bash
# Install dependencies
pip install -r requirements.txt

# Launch the Academy — select any quest from the menu
python main.py
```

Installed as a package (`pip install -e .`), the same launcher is also
available as a console script:

```bash
securityquest
# or: python -m securityquest
```

The launcher presents a game selection menu. Pick a quest number (1-7) to start.

Inside each quest:
- **Continue Journey** — play from your current level
- **View Stats** — see rank, points, completed levels
- **Jump to Level** — replay any completed level
- **Achievements** — view unlocked badges
- **Reset Progress** — start over

During a level:
- Type `hint` for a clue
- Type `skip` to skip (no points awarded)
- Type `done` to submit your code (Python engine)

---

## Output

```
╔═══════════════════════════════════════════════════════════════════╗
║   ███████╗███████╗ ██████╗ ██╗   ██╗██████╗ ██╗████████╗██╗   ██╗║
║   ██╔════╝██╔════╝██╔════╝ ██║   ██║██╔══██╗██║╚══██╔══╝╚██╗ ██╔╝║
║   ███████╗█████╗  ██║      ██║   ██║██████╔╝██║   ██║    ╚████╔╝ ║
║   ╚════██║██╔══╝  ██║      ██║   ██║██╔══██╗██║   ██║     ╚██╔╝  ║
║   ███████║███████╗╚██████╗ ╚██████╔╝██║  ██║██║   ██║      ██║   ║
║   ╚══════╝╚══════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝   ╚═╝      ╚═╝   ║
║              Q U E S T   A C A D E M Y                            ║
╚═══════════════════════════════════════════════════════════════════╝

  ── SELECT YOUR QUEST ──
╭──────┬──────────────────┬────────────────────────────────────┬──────────┬──────────────────────────────────────────╮
│  #   │ Game             │ Description                        │  Levels  │ Topics                                   │
├──────┼──────────────────┼────────────────────────────────────┼──────────┼──────────────────────────────────────────┤
│  1   │ 🖥️ CyberQuest    │ Python & Linux Security            │   100    │ Linux, Python, Networking, System...      │
│  2   │ 🐚 BashQuest     │ Bash Scripting & Shell Security    │   100    │ Bash, Shell Scripting, Automation...      │
│  3   │ 🪟 WindowsQuest  │ Windows Security & PowerShell      │   100    │ PowerShell, Active Directory...           │
│  4   │ 🌐 CiscoQuest    │ Cisco IOS Networking & Security    │   100    │ Routing, Switching, ACLs, VPNs...        │
│  5   │ 🔐 CryptoQuest   │ Cryptography Classical to Modern   │   100    │ Classical Ciphers, AES, RSA, TLS...      │
│  6   │ 🔍 ReverseQuest  │ Reverse Engineering & Malware      │   100    │ x86 ASM, ELF/PE, GDB, IDA...             │
│  7   │ 🕸️ WebHackQuest  │ Web App Security & Pentesting      │   100    │ XSS, SQLi, SSRF, SSTI, JWT...            │
╰──────┴──────────────────┴────────────────────────────────────┴──────────┴──────────────────────────────────────────╯

  Enter the number of the quest you want to play, or Q to quit.
```

---

## Topics Covered

```
Offensive Security          Defensive Concepts          Infrastructure
─────────────────           ──────────────────          ──────────────
XSS / SQLi / SSRF          Input validation            Cisco IOS
SSTI / IDOR / CSRF          Cookie security flags       OSPF / BGP / EIGRP
JWT forging                 CSP / CORS policy           VLANs / ACLs / NAT
Buffer overflow             Password hashing            VPN / IPsec
ROP chains                  TLS/PKI                     Active Directory
Format string exploits      AES-GCM / RSA padding       Group Policy
Malware reverse eng.        Anti-debugging detection    PowerShell remoting
Binary exploitation         Secure coding patterns      Registry hardening
```

---

## Requirements

- Python 3.10+
- Terminal with Unicode support (for the UI)
- Dependencies: `rich`, `pycryptodome`, `cryptography`, `bcrypt`, `argon2-cffi`

```bash
pip install -r requirements.txt
```
