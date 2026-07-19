"""Constants and game registry for SecurityQuestAcademy."""

from __future__ import annotations

from securityquest import __version__

TOOL_NAME = "SecurityQuestAcademy"
VERSION = __version__

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
        "description": "Python & Linux Security Fundamentals",
        "levels": "100",
        "topics": "Linux, Python, Networking, System Security",
    },
    {
        "id": 2,
        "name": "BashQuest",
        "module": "games.bashquest",
        "color": "bright_yellow",
        "description": "Bash Scripting & Shell Security",
        "levels": "100",
        "topics": "Bash, Shell Scripting, Automation, Security Scripts",
    },
    {
        "id": 3,
        "name": "WindowsQuest",
        "module": "games.windowsquest",
        "color": "bright_blue",
        "description": "Windows Security & PowerShell",
        "levels": "100",
        "topics": "PowerShell, Active Directory, Windows Hardening, Forensics",
    },
    {
        "id": 4,
        "name": "CiscoQuest",
        "module": "games.ciscoquest",
        "color": "bright_white",
        "description": "Cisco IOS Networking & Security",
        "levels": "100",
        "topics": "Routing, Switching, ACLs, VPNs, Firewalls, IOS Commands",
    },
    {
        "id": 5,
        "name": "CryptoQuest",
        "module": "games.cryptoquest",
        "color": "bright_magenta",
        "description": "Cryptography from Classical to Modern",
        "levels": "100",
        "topics": "Classical Ciphers, AES, RSA, Hashing, TLS, PKI",
    },
    {
        "id": 6,
        "name": "ReverseQuest",
        "module": "games.reversequest",
        "color": "bright_red",
        "description": "Reverse Engineering & Malware Analysis",
        "levels": "100",
        "topics": "x86 ASM, ELF/PE, GDB, IDA, Malware, Exploitation, Fuzzing",
    },
    {
        "id": 7,
        "name": "WebHackQuest",
        "module": "games.webhackquest",
        "color": "bright_green",
        "description": "Web Application Security & Pentesting",
        "levels": "100",
        "topics": "XSS, SQLi, SSRF, SSTI, JWT, OAuth, OWASP Top 10",
    },
]
