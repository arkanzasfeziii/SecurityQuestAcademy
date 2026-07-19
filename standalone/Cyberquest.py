#!/usr/bin/env python3
"""
CyberQuest: Python Security Academy
A comprehensive game to learn Python and cybersecurity from absolute beginner to expert.
Author: arkanzasfeziii
"""

import json
import os
import random
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
SAVE_FILE = Path.home() / ".cyberquest_save.json"
VERSION = "1.0.0"

# Cyberpunk color scheme
COLORS = {
    "primary": "cyan",
    "secondary": "magenta",
    "success": "green",
    "error": "red",
    "warning": "yellow",
    "info": "blue",
    "hacker": "bright_green",
}

# === Rank System ===
RANKS = [
    (0, "👶 Script Newbie", "You're just starting your journey"),
    (5, "🔰 Code Cadet", "Learning the basics"),
    (10, "💻 Terminal Rookie", "Getting comfortable with code"),
    (15, "🎯 Bug Hunter", "Starting to find vulnerabilities"),
    (20, "🔍 Security Scout", "Understanding security concepts"),
    (25, "⚡ Crypto Cracker", "Breaking encryption"),
    (30, "🛡️ Defense Operator", "Protecting systems"),
    (35, "🔓 Access Breacher", "Bypassing security"),
    (40, "📡 Network Phantom", "Mastering network security"),
    (45, "🎭 Social Engineer", "Understanding human vulnerabilities"),
    (50, "💀 Exploit Developer", "Creating exploits"),
    (55, "🌐 Web Infiltrator", "Web application security expert"),
    (60, "🔐 Cryptographer", "Advanced encryption techniques"),
    (65, "🧬 Reverse Engineer", "Deconstructing code"),
    (70, "⚔️ Penetration Tester", "Professional ethical hacker"),
    (75, "🎖️ Security Architect", "Designing secure systems"),
    (80, "👑 Cyber Sensei", "Teaching others"),
    (85, "🔥 Zero-Day Hunter", "Finding unknown vulnerabilities"),
    (90, "🌟 Cyber Samurai", "Master of all domains"),
    (95, "🏆 Elite Guardian", "Protecting the digital realm"),
    (100, "💎 Legendary Hacker", "The ultimate achievement"),
]

# === Level Definitions ===
LEVELS = [
    # === BEGINNER TIER (1-20): Python Basics ===
    {
        "id": 1,
        "title": "Hello, Hacker!",
        "description": "Your first mission: Display a message to the terminal.",
        "challenge": "Write code that prints: Hello, CyberQuest!",
        "hint": "Use the print() function",
        "solution": 'print("Hello, CyberQuest!")',
        "test_code": 'print("Hello, CyberQuest!")',
        "explanation": "The print() function displays text. This is your first step into programming!",
        "points": 10,
        "category": "basics"
    },
    {
        "id": 2,
        "title": "Variable Assignment",
        "description": "Hackers store data in variables. Create your first variable.",
        "challenge": "Create a variable called 'username' with the value 'hacker' and print it.",
        "hint": "Use: variable_name = value",
        "solution": 'username = "hacker"\nprint(username)',
        "test_code": 'username = "hacker"\nprint(username)',
        "explanation": "Variables store data. Use = to assign values.",
        "points": 10,
        "category": "basics"
    },
    {
        "id": 3,
        "title": "String Concatenation",
        "description": "Combine strings to create messages.",
        "challenge": "Create two variables: first_name='Cyber' and last_name='Warrior'. Print them combined with a space.",
        "hint": "Use + to join strings",
        "solution": 'first_name = "Cyber"\nlast_name = "Warrior"\nprint(first_name + " " + last_name)',
        "test_code": 'first_name = "Cyber"\nlast_name = "Warrior"\nprint(first_name + " " + last_name)',
        "explanation": "String concatenation combines text. Use + or f-strings.",
        "points": 15,
        "category": "basics"
    },
    {
        "id": 4,
        "title": "Numbers and Math",
        "description": "Hackers need to calculate. Learn basic arithmetic.",
        "challenge": "Calculate 256 + 512 and print the result.",
        "hint": "Python can do math directly",
        "solution": "print(256 + 512)",
        "test_code": "print(256 + 512)",
        "explanation": "Python handles math: +, -, *, /, //, %, **",
        "points": 15,
        "category": "basics"
    },
    {
        "id": 5,
        "title": "User Input",
        "description": "Interactive programs get input from users.",
        "challenge": "Ask for the user's name using input() and greet them.",
        "hint": "name = input('Prompt: ')",
        "solution": 'name = input("Enter your name: ")\nprint("Welcome, " + name)',
        "test_code": 'name = "Agent"\nprint("Welcome, " + name)',
        "explanation": "input() gets user input as a string.",
        "points": 20,
        "category": "basics"
    },
    {
        "id": 6,
        "title": "Type Conversion",
        "description": "Convert between data types.",
        "challenge": "Convert the string '42' to an integer and add 8 to it. Print the result.",
        "hint": "Use int() to convert strings to integers",
        "solution": 'num = int("42")\nprint(num + 8)',
        "test_code": 'num = int("42")\nprint(num + 8)',
        "explanation": "int(), str(), float() convert between types.",
        "points": 20,
        "category": "basics"
    },
    {
        "id": 7,
        "title": "Conditional Logic",
        "description": "Make decisions with if statements.",
        "challenge": "Create a variable 'password' with value 'secret'. If it equals 'secret', print 'Access Granted'.",
        "hint": "Use: if condition:",
        "solution": 'password = "secret"\nif password == "secret":\n    print("Access Granted")',
        "test_code": 'password = "secret"\nif password == "secret":\n    print("Access Granted")',
        "explanation": "if statements execute code when conditions are true.",
        "points": 25,
        "category": "basics"
    },
    {
        "id": 8,
        "title": "Else Clause",
        "description": "Handle alternative cases.",
        "challenge": "Check if a variable 'port' equals 443. Print 'HTTPS' if true, else 'HTTP'.",
        "hint": "Use: if ... else:",
        "solution": 'port = 443\nif port == 443:\n    print("HTTPS")\nelse:\n    print("HTTP")',
        "test_code": 'port = 443\nif port == 443:\n    print("HTTPS")\nelse:\n    print("HTTP")',
        "explanation": "else provides an alternative when if is false.",
        "points": 25,
        "category": "basics"
    },
    {
        "id": 9,
        "title": "Lists Basics",
        "description": "Store multiple values in lists.",
        "challenge": "Create a list of ports: [80, 443, 22, 21] and print it.",
        "hint": "Use square brackets: [item1, item2, ...]",
        "solution": "ports = [80, 443, 22, 21]\nprint(ports)",
        "test_code": "ports = [80, 443, 22, 21]\nprint(ports)",
        "explanation": "Lists store ordered collections of items.",
        "points": 30,
        "category": "basics"
    },
    {
        "id": 10,
        "title": "List Indexing",
        "description": "Access list items by position.",
        "challenge": "From the list [10, 20, 30, 40], print the first item (10).",
        "hint": "Lists start at index 0",
        "solution": "numbers = [10, 20, 30, 40]\nprint(numbers[0])",
        "test_code": "numbers = [10, 20, 30, 40]\nprint(numbers[0])",
        "explanation": "Access items with list[index]. Python uses 0-based indexing.",
        "points": 30,
        "category": "basics"
    },
    {
        "id": 11,
        "title": "For Loops",
        "description": "Iterate over items.",
        "challenge": "Loop through [1, 2, 3] and print each number.",
        "hint": "for item in list:",
        "solution": "for num in [1, 2, 3]:\n    print(num)",
        "test_code": "for num in [1, 2, 3]:\n    print(num)",
        "explanation": "for loops iterate over sequences.",
        "points": 35,
        "category": "basics"
    },
    {
        "id": 12,
        "title": "Range Function",
        "description": "Generate number sequences.",
        "challenge": "Print numbers 0 to 4 using range().",
        "hint": "range(5) gives 0-4",
        "solution": "for i in range(5):\n    print(i)",
        "test_code": "for i in range(5):\n    print(i)",
        "explanation": "range(n) generates numbers from 0 to n-1.",
        "points": 35,
        "category": "basics"
    },
    {
        "id": 13,
        "title": "While Loops",
        "description": "Loop until a condition is false.",
        "challenge": "Print numbers 1 to 3 using a while loop.",
        "hint": "Initialize counter, loop while condition is true, increment counter",
        "solution": "count = 1\nwhile count <= 3:\n    print(count)\n    count += 1",
        "test_code": "count = 1\nwhile count <= 3:\n    print(count)\n    count += 1",
        "explanation": "while loops continue until the condition becomes false.",
        "points": 40,
        "category": "basics"
    },
    {
        "id": 14,
        "title": "Functions Basics",
        "description": "Create reusable code blocks.",
        "challenge": "Define a function called 'greet' that prints 'Hello, Hacker!'. Then call it.",
        "hint": "def function_name():",
        "solution": 'def greet():\n    print("Hello, Hacker!")\ngreet()',
        "test_code": 'def greet():\n    print("Hello, Hacker!")\ngreet()',
        "explanation": "Functions encapsulate reusable code. def creates them.",
        "points": 40,
        "category": "basics"
    },
    {
        "id": 15,
        "title": "Function Parameters",
        "description": "Pass data to functions.",
        "challenge": "Create a function 'scan_port' that takes a port number and prints it.",
        "hint": "def function_name(parameter):",
        "solution": "def scan_port(port):\n    print(port)\nscan_port(80)",
        "test_code": "def scan_port(port):\n    print(port)\nscan_port(80)",
        "explanation": "Parameters let functions accept input values.",
        "points": 45,
        "category": "basics"
    },
    {
        "id": 16,
        "title": "Return Values",
        "description": "Functions can return data.",
        "challenge": "Create a function that takes two numbers and returns their sum. Print the result of calling it with 5 and 7.",
        "hint": "Use return keyword",
        "solution": "def add(a, b):\n    return a + b\nprint(add(5, 7))",
        "test_code": "def add(a, b):\n    return a + b\nprint(add(5, 7))",
        "explanation": "return sends values back from functions.",
        "points": 45,
        "category": "basics"
    },
    {
        "id": 17,
        "title": "Dictionaries",
        "description": "Store key-value pairs.",
        "challenge": "Create a dictionary with keys 'username' and 'password', values 'admin' and 'secret'. Print it.",
        "hint": "Use curly braces: {key: value}",
        "solution": 'user = {"username": "admin", "password": "secret"}\nprint(user)',
        "test_code": 'user = {"username": "admin", "password": "secret"}\nprint(user)',
        "explanation": "Dictionaries map keys to values.",
        "points": 50,
        "category": "basics"
    },
    {
        "id": 18,
        "title": "Dictionary Access",
        "description": "Get values from dictionaries.",
        "challenge": "From {'ip': '192.168.1.1', 'port': 80}, print the IP address.",
        "hint": "Use dict['key']",
        "solution": "server = {'ip': '192.168.1.1', 'port': 80}\nprint(server['ip'])",
        "test_code": "server = {'ip': '192.168.1.1', 'port': 80}\nprint(server['ip'])",
        "explanation": "Access dictionary values with [key].",
        "points": 50,
        "category": "basics"
    },
    {
        "id": 19,
        "title": "String Methods",
        "description": "Manipulate strings.",
        "challenge": "Convert 'HACKER' to lowercase and print it.",
        "hint": "Use .lower() method",
        "solution": 'text = "HACKER"\nprint(text.lower())',
        "test_code": 'text = "HACKER"\nprint(text.lower())',
        "explanation": "Strings have methods: .lower(), .upper(), .strip(), etc.",
        "points": 55,
        "category": "basics"
    },
    {
        "id": 20,
        "title": "List Methods",
        "description": "Modify lists.",
        "challenge": "Create a list [1, 2], append 3 to it, and print the list.",
        "hint": "Use .append() method",
        "solution": "nums = [1, 2]\nnums.append(3)\nprint(nums)",
        "test_code": "nums = [1, 2]\nnums.append(3)\nprint(nums)",
        "explanation": "Lists have methods: .append(), .remove(), .pop(), etc.",
        "points": 55,
        "category": "basics"
    },

    # === INTERMEDIATE TIER (21-50): Security Concepts ===
    {
        "id": 21,
        "title": "Password Checker",
        "description": "Check password strength.",
        "challenge": "Create a function that checks if a password is at least 8 characters. Return True/False.",
        "hint": "Use len() function",
        "solution": "def check_password(pwd):\n    return len(pwd) >= 8\nprint(check_password('secret123'))",
        "test_code": "def check_password(pwd):\n    return len(pwd) >= 8\nprint(check_password('secret123'))",
        "explanation": "len() returns string length. Good passwords are long!",
        "points": 60,
        "category": "security"
    },
    {
        "id": 22,
        "title": "Caesar Cipher Encoder",
        "description": "Shift letters by a number (basic encryption).",
        "challenge": "Shift 'A' forward by 3 positions in the alphabet (becomes 'D'). Print it.",
        "hint": "Use ord() and chr() functions",
        "solution": "letter = 'A'\nshifted = chr(ord(letter) + 3)\nprint(shifted)",
        "test_code": "letter = 'A'\nshifted = chr(ord(letter) + 3)\nprint(shifted)",
        "explanation": "ord() gets ASCII value, chr() converts back. Caesar cipher basics!",
        "points": 65,
        "category": "crypto"
    },
    {
        "id": 23,
        "title": "Base64 Basics",
        "description": "Understanding encoding (not encryption!).",
        "challenge": "Import base64, encode 'hello' to base64, and print it.",
        "hint": "import base64; base64.b64encode()",
        "solution": "import base64\nencoded = base64.b64encode(b'hello')\nprint(encoded)",
        "test_code": "import base64\nencoded = base64.b64encode(b'hello')\nprint(encoded)",
        "explanation": "Base64 encodes binary data to ASCII. Not secure, just encoding!",
        "points": 70,
        "category": "crypto"
    },
    {
        "id": 24,
        "title": "Hash Function",
        "description": "One-way cryptographic hashing.",
        "challenge": "Import hashlib, create an MD5 hash of 'password', and print the hexdigest.",
        "hint": "hashlib.md5(b'text').hexdigest()",
        "solution": "import hashlib\nhash_obj = hashlib.md5(b'password')\nprint(hash_obj.hexdigest())",
        "test_code": "import hashlib\nhash_obj = hashlib.md5(b'password')\nprint(hash_obj.hexdigest())",
        "explanation": "Hashes are one-way. MD5 is weak, use SHA256 in production!",
        "points": 75,
        "category": "crypto"
    },
    {
        "id": 25,
        "title": "Port Scanner Logic",
        "description": "Check if ports are in common port ranges.",
        "challenge": "Check if port 80 is in the list of common ports [21, 22, 80, 443]. Print True/False.",
        "hint": "Use 'in' operator",
        "solution": "common_ports = [21, 22, 80, 443]\nprint(80 in common_ports)",
        "test_code": "common_ports = [21, 22, 80, 443]\nprint(80 in common_ports)",
        "explanation": "'in' checks membership. Foundation of port scanning!",
        "points": 80,
        "category": "network"
    },
    {
        "id": 26,
        "title": "IP Address Validation",
        "description": "Check if an IP looks valid.",
        "challenge": "Split '192.168.1.1' by '.' and check if it has 4 parts. Print True/False.",
        "hint": "Use .split() method",
        "solution": "ip = '192.168.1.1'\nparts = ip.split('.')\nprint(len(parts) == 4)",
        "test_code": "ip = '192.168.1.1'\nparts = ip.split('.')\nprint(len(parts) == 4)",
        "explanation": "IP validation is crucial. This is a basic check.",
        "points": 85,
        "category": "network"
    },
    {
        "id": 27,
        "title": "Try-Except Basics",
        "description": "Handle errors gracefully.",
        "challenge": "Try to convert 'abc' to int. If it fails, print 'Invalid number'.",
        "hint": "try: ... except: ...",
        "solution": "try:\n    num = int('abc')\nexcept:\n    print('Invalid number')",
        "test_code": "try:\n    num = int('abc')\nexcept:\n    print('Invalid number')",
        "explanation": "try-except prevents crashes. Essential for robust code!",
        "points": 90,
        "category": "basics"
    },
    {
        "id": 28,
        "title": "File Reading",
        "description": "Read data from files.",
        "challenge": "Open a file in read mode using 'with open()' and read its content.",
        "hint": "with open('file.txt', 'r') as f:",
        "solution": "# Simulated - in real scenario:\n# with open('test.txt', 'r') as f:\n#     content = f.read()\n#     print(content)\nprint('File read simulation')",
        "test_code": "print('File read simulation')",
        "explanation": "File I/O is crucial for log analysis and data processing.",
        "points": 95,
        "category": "basics"
    },
    {
        "id": 29,
        "title": "List Comprehension",
        "description": "Create lists efficiently.",
        "challenge": "Create a list of squares of numbers 0-4 using list comprehension.",
        "hint": "[expression for item in iterable]",
        "solution": "squares = [x**2 for x in range(5)]\nprint(squares)",
        "test_code": "squares = [x**2 for x in range(5)]\nprint(squares)",
        "explanation": "List comprehensions are powerful and Pythonic!",
        "points": 100,
        "category": "basics"
    },
    {
        "id": 30,
        "title": "Regular Expressions Intro",
        "description": "Pattern matching in strings.",
        "challenge": "Import re and find all digits in '192.168.1.1'.",
        "hint": "re.findall(r'\\d+', text)",
        "solution": "import re\nip = '192.168.1.1'\ndigits = re.findall(r'\\d+', ip)\nprint(digits)",
        "test_code": "import re\nip = '192.168.1.1'\ndigits = re.findall(r'\\d+', ip)\nprint(digits)",
        "explanation": "Regex is powerful for log parsing and input validation!",
        "points": 110,
        "category": "security"
    },

    # === ADVANCED TIER (31-60): Real Security Tasks ===
    {
        "id": 31,
        "title": "SQL Injection Detection",
        "description": "Find dangerous characters in input.",
        "challenge": "Check if input contains ' OR 1=1 --. Print 'SQLi Detected!' if found.",
        "hint": "Use 'in' operator or .find()",
        "solution": "user_input = \"admin' OR 1=1 --\"\nif \"' OR\" in user_input or '--' in user_input:\n    print('SQLi Detected!')",
        "test_code": "user_input = \"admin' OR 1=1 --\"\nif \"' OR\" in user_input or '--' in user_input:\n    print('SQLi Detected!')",
        "explanation": "Input validation prevents SQL injection attacks!",
        "points": 120,
        "category": "web"
    },
    {
        "id": 32,
        "title": "XSS Filter",
        "description": "Detect cross-site scripting attempts.",
        "challenge": "Check if input contains '<script>' tag. Print warning if found.",
        "hint": "Use .lower() and 'in' operator",
        "solution": "input_data = '<script>alert(1)</script>'\nif '<script>' in input_data.lower():\n    print('XSS Detected!')",
        "test_code": "input_data = '<script>alert(1)</script>'\nif '<script>' in input_data.lower():\n    print('XSS Detected!')",
        "explanation": "XSS detection protects against malicious JavaScript!",
        "points": 125,
        "category": "web"
    },
    {
        "id": 33,
        "title": "Brute Force Counter",
        "description": "Track login attempts.",
        "challenge": "Create a counter that increments failed login attempts. Lock after 3 tries.",
        "hint": "Use a variable and if statement",
        "solution": "attempts = 0\nfor i in range(5):\n    attempts += 1\n    if attempts >= 3:\n        print('Account locked!')\n        break",
        "test_code": "attempts = 0\nfor i in range(5):\n    attempts += 1\n    if attempts >= 3:\n        print('Account locked!')\n        break",
        "explanation": "Rate limiting prevents brute force attacks!",
        "points": 130,
        "category": "security"
    },
    {
        "id": 34,
        "title": "Password Hash Comparison",
        "description": "Secure password verification.",
        "challenge": "Hash 'mypassword' with SHA256 and compare with a stored hash.",
        "hint": "Use hashlib.sha256()",
        "solution": "import hashlib\nstored = hashlib.sha256(b'mypassword').hexdigest()\ninput_hash = hashlib.sha256(b'mypassword').hexdigest()\nprint(stored == input_hash)",
        "test_code": "import hashlib\nstored = hashlib.sha256(b'mypassword').hexdigest()\ninput_hash = hashlib.sha256(b'mypassword').hexdigest()\nprint(stored == input_hash)",
        "explanation": "Never store plaintext passwords! Always hash them.",
        "points": 135,
        "category": "crypto"
    },
    {
        "id": 35,
        "title": "JSON Parsing",
        "description": "Parse API responses.",
        "challenge": "Parse JSON string '{\"status\": \"success\"}' and print the status value.",
        "hint": "import json; json.loads()",
        "solution": "import json\ndata = json.loads('{\"status\": \"success\"}')\nprint(data['status'])",
        "test_code": "import json\ndata = json.loads('{\"status\": \"success\"}')\nprint(data['status'])",
        "explanation": "JSON is everywhere in APIs and web security!",
        "points": 140,
        "category": "web"
    },
    {
        "id": 36,
        "title": "HTTP Status Codes",
        "description": "Understand server responses.",
        "challenge": "Create a dict mapping status codes to meanings. Print meaning of 404.",
        "hint": "Use dictionary",
        "solution": "codes = {200: 'OK', 404: 'Not Found', 500: 'Server Error'}\nprint(codes[404])",
        "test_code": "codes = {200: 'OK', 404: 'Not Found', 500: 'Server Error'}\nprint(codes[404])",
        "explanation": "HTTP status codes tell you what happened in requests!",
        "points": 145,
        "category": "web"
    },
    {
        "id": 37,
        "title": "URL Parsing",
        "description": "Extract parts of URLs.",
        "challenge": "Parse 'https://example.com/path?key=value' and extract the domain.",
        "hint": "Use .split() multiple times",
        "solution": "url = 'https://example.com/path?key=value'\ndomain = url.split('//')[1].split('/')[0]\nprint(domain)",
        "test_code": "url = 'https://example.com/path?key=value'\ndomain = url.split('//')[1].split('/')[0]\nprint(domain)",
        "explanation": "URL parsing is essential for web security analysis!",
        "points": 150,
        "category": "web"
    },
    {
        "id": 38,
        "title": "Directory Traversal Detection",
        "description": "Find path manipulation attacks.",
        "challenge": "Check if a path contains '../'. Print warning if found.",
        "hint": "Use 'in' operator",
        "solution": "path = '../../etc/passwd'\nif '../' in path:\n    print('Directory traversal detected!')",
        "test_code": "path = '../../etc/passwd'\nif '../' in path:\n    print('Directory traversal detected!')",
        "explanation": "Path traversal lets attackers access unauthorized files!",
        "points": 155,
        "category": "web"
    },
    {
        "id": 39,
        "title": "Email Validation",
        "description": "Basic email format checking.",
        "challenge": "Check if email contains '@' and '.'. Print valid/invalid.",
        "hint": "Use 'in' operator twice",
        "solution": "email = 'hacker@example.com'\nif '@' in email and '.' in email:\n    print('Valid format')",
        "test_code": "email = 'hacker@example.com'\nif '@' in email and '.' in email:\n    print('Valid format')",
        "explanation": "Input validation prevents injection and errors!",
        "points": 160,
        "category": "security"
    },
    {
        "id": 40,
        "title": "Command Injection Detection",
        "description": "Find shell command injection.",
        "challenge": "Check if input contains ';' or '|' or '&'. Print warning if found.",
        "hint": "Use multiple 'in' checks",
        "solution": "cmd = 'ls; rm -rf /'\nif ';' in cmd or '|' in cmd or '&' in cmd:\n    print('Command injection detected!')",
        "test_code": "cmd = 'ls; rm -rf /'\nif ';' in cmd or '|' in cmd or '&' in cmd:\n    print('Command injection detected!')",
        "explanation": "Command injection can execute arbitrary system commands!",
        "points": 165,
        "category": "security"
    },
    {
        "id": 41,
        "title": "ROT13 Cipher",
        "description": "Classic letter rotation cipher.",
        "challenge": "Implement ROT13: rotate each letter by 13 positions.",
        "hint": "Use .translate() and str.maketrans()",
        "solution": "import codecs\ntext = 'hello'\nencoded = codecs.encode(text, 'rot_13')\nprint(encoded)",
        "test_code": "import codecs\ntext = 'hello'\nencoded = codecs.encode(text, 'rot_13')\nprint(encoded)",
        "explanation": "ROT13 is a simple substitution cipher. Not secure!",
        "points": 170,
        "category": "crypto"
    },
    {
        "id": 42,
        "title": "Hex Encoding",
        "description": "Convert text to hexadecimal.",
        "challenge": "Convert 'ABC' to hex representation.",
        "hint": "Use .encode().hex()",
        "solution": "text = 'ABC'\nhex_value = text.encode().hex()\nprint(hex_value)",
        "test_code": "text = 'ABC'\nhex_value = text.encode().hex()\nprint(hex_value)",
        "explanation": "Hex encoding is common in security and networking!",
        "points": 175,
        "category": "crypto"
    },
    {
        "id": 43,
        "title": "Rate Limiter",
        "description": "Implement request rate limiting.",
        "challenge": "Count requests in a time window. Allow max 5 requests.",
        "hint": "Use a counter and loop",
        "solution": "requests = 0\nmax_requests = 5\nfor i in range(10):\n    if requests < max_requests:\n        requests += 1\n        print(f'Request {requests} allowed')\n    else:\n        print('Rate limit exceeded!')\n        break",
        "test_code": "requests = 0\nmax_requests = 5\nfor i in range(10):\n    if requests < max_requests:\n        requests += 1\n        print(f'Request {requests} allowed')\n    else:\n        print('Rate limit exceeded!')\n        break",
        "explanation": "Rate limiting prevents DoS and brute force attacks!",
        "points": 180,
        "category": "security"
    },
    {
        "id": 44,
        "title": "JWT Token Structure",
        "description": "Understand JSON Web Tokens.",
        "challenge": "Split a JWT 'header.payload.signature' by '.' and count parts.",
        "hint": "Use .split() and len()",
        "solution": "jwt = 'eyJ0eXAi.eyJzdWIi.SflKxwRJ'\nparts = jwt.split('.')\nprint(f'JWT has {len(parts)} parts')",
        "test_code": "jwt = 'eyJ0eXAi.eyJzdWIi.SflKxwRJ'\nparts = jwt.split('.')\nprint(f'JWT has {len(parts)} parts')",
        "explanation": "JWTs have 3 parts: header, payload, signature!",
        "points": 185,
        "category": "web"
    },
    {
        "id": 45,
        "title": "CORS Headers",
        "description": "Understand Cross-Origin Resource Sharing.",
        "challenge": "Check if 'Access-Control-Allow-Origin' header equals '*' (dangerous!).",
        "hint": "Use dictionary access",
        "solution": "headers = {'Access-Control-Allow-Origin': '*'}\nif headers.get('Access-Control-Allow-Origin') == '*':\n    print('Insecure CORS configuration!')",
        "test_code": "headers = {'Access-Control-Allow-Origin': '*'}\nif headers.get('Access-Control-Allow-Origin') == '*':\n    print('Insecure CORS configuration!')",
        "explanation": "CORS * allows any domain to access resources!",
        "points": 190,
        "category": "web"
    },
    {
        "id": 46,
        "title": "Cookie Security",
        "description": "Check cookie security flags.",
        "challenge": "Check if cookie has 'HttpOnly' and 'Secure' flags.",
        "hint": "Use 'in' operator on cookie string",
        "solution": "cookie = 'session=abc123; HttpOnly; Secure'\nif 'HttpOnly' in cookie and 'Secure' in cookie:\n    print('Cookie is secure!')",
        "test_code": "cookie = 'session=abc123; HttpOnly; Secure'\nif 'HttpOnly' in cookie and 'Secure' in cookie:\n    print('Cookie is secure!')",
        "explanation": "HttpOnly prevents XSS, Secure ensures HTTPS only!",
        "points": 195,
        "category": "web"
    },
    {
        "id": 47,
        "title": "Timing Attack Mitigation",
        "description": "Constant-time string comparison.",
        "challenge": "Use hmac.compare_digest() for secure string comparison.",
        "hint": "import hmac",
        "solution": "import hmac\nstored = 'secret123'\nuser_input = 'secret123'\nif hmac.compare_digest(stored, user_input):\n    print('Match!')",
        "test_code": "import hmac\nstored = 'secret123'\nuser_input = 'secret123'\nif hmac.compare_digest(stored, user_input):\n    print('Match!')",
        "explanation": "Timing attacks can leak information. Use constant-time comparisons!",
        "points": 200,
        "category": "crypto"
    },
    {
        "id": 48,
        "title": "SSRF Detection",
        "description": "Detect Server-Side Request Forgery attempts.",
        "challenge": "Check if URL points to localhost (127.0.0.1 or localhost).",
        "hint": "Use 'in' operator",
        "solution": "url = 'http://localhost/admin'\nif 'localhost' in url or '127.0.0.1' in url:\n    print('SSRF attempt detected!')",
        "test_code": "url = 'http://localhost/admin'\nif 'localhost' in url or '127.0.0.1' in url:\n    print('SSRF attempt detected!')",
        "explanation": "SSRF lets attackers access internal resources!",
        "points": 205,
        "category": "web"
    },
    {
        "id": 49,
        "title": "XXE Detection",
        "description": "Find XML External Entity injection.",
        "challenge": "Check if XML contains '<!ENTITY' or 'SYSTEM'.",
        "hint": "Use 'in' operator",
        "solution": "xml = '<!DOCTYPE foo [<!ENTITY xxe SYSTEM \"file:///etc/passwd\">]>'\nif '<!ENTITY' in xml or 'SYSTEM' in xml:\n    print('XXE detected!')",
        "test_code": "xml = '<!DOCTYPE foo [<!ENTITY xxe SYSTEM \"file:///etc/passwd\">]>'\nif '<!ENTITY' in xml or 'SYSTEM' in xml:\n    print('XXE detected!')",
        "explanation": "XXE can read files and cause denial of service!",
        "points": 210,
        "category": "web"
    },
    {
        "id": 50,
        "title": "Insecure Deserialization",
        "description": "Detect dangerous pickle usage.",
        "challenge": "Warn about using pickle.loads() on untrusted data.",
        "hint": "Check if code contains 'pickle.loads'",
        "solution": "code = 'data = pickle.loads(user_input)'\nif 'pickle.loads' in code:\n    print('Insecure deserialization detected!')",
        "test_code": "code = 'data = pickle.loads(user_input)'\nif 'pickle.loads' in code:\n    print('Insecure deserialization detected!')",
        "explanation": "Deserializing untrusted data can execute arbitrary code!",
        "points": 215,
        "category": "security"
    },

    # === EXPERT TIER (51-75): Advanced Techniques ===
    {
        "id": 51,
        "title": "AES Encryption Basics",
        "description": "Modern symmetric encryption.",
        "challenge": "Understand that AES uses the Crypto library for encryption.",
        "hint": "Research AES-256",
        "solution": "# In real code: from Crypto.Cipher import AES\nprint('AES is a strong symmetric cipher')",
        "test_code": "print('AES is a strong symmetric cipher')",
        "explanation": "AES is the standard for symmetric encryption!",
        "points": 220,
        "category": "crypto"
    },
    {
        "id": 52,
        "title": "RSA Key Concepts",
        "description": "Asymmetric encryption basics.",
        "challenge": "Understand public/private key pairs.",
        "hint": "Public key encrypts, private key decrypts",
        "solution": "print('RSA uses public-private key pairs')",
        "test_code": "print('RSA uses public-private key pairs')",
        "explanation": "RSA enables secure key exchange and digital signatures!",
        "points": 225,
        "category": "crypto"
    },
    {
        "id": 53,
        "title": "HMAC Generation",
        "description": "Hash-based Message Authentication Code.",
        "challenge": "Create HMAC-SHA256 of 'message' with key 'secret'.",
        "hint": "import hmac, hashlib",
        "solution": "import hmac\nimport hashlib\nhmac_value = hmac.new(b'secret', b'message', hashlib.sha256).hexdigest()\nprint(hmac_value)",
        "test_code": "import hmac\nimport hashlib\nhmac_value = hmac.new(b'secret', b'message', hashlib.sha256).hexdigest()\nprint(hmac_value)",
        "explanation": "HMAC ensures message authenticity and integrity!",
        "points": 230,
        "category": "crypto"
    },
    {
        "id": 54,
        "title": "Salt Generation",
        "description": "Generate random salts for password hashing.",
        "challenge": "Generate a random 16-byte salt using os.urandom().",
        "hint": "import os; os.urandom(16)",
        "solution": "import os\nsalt = os.urandom(16)\nprint(len(salt.hex()))",
        "test_code": "import os\nsalt = os.urandom(16)\nprint(len(salt.hex()))",
        "explanation": "Salts prevent rainbow table attacks on password hashes!",
        "points": 235,
        "category": "crypto"
    },
    {
        "id": 55,
        "title": "Bcrypt Password Hashing",
        "description": "Industry-standard password hashing.",
        "challenge": "Understand bcrypt is slow by design (good for passwords!).",
        "hint": "Slow hashing prevents brute force",
        "solution": "# In real code: import bcrypt\nprint('Bcrypt is intentionally slow to prevent brute force')",
        "test_code": "print('Bcrypt is intentionally slow to prevent brute force')",
        "explanation": "Use bcrypt, scrypt, or Argon2 for password hashing!",
        "points": 240,
        "category": "crypto"
    },
    {
        "id": 56,
        "title": "CSRF Token Validation",
        "description": "Prevent Cross-Site Request Forgery.",
        "challenge": "Compare session token with request token.",
        "hint": "Both tokens must match",
        "solution": "session_token = 'abc123'\nrequest_token = 'abc123'\nif session_token == request_token:\n    print('CSRF token valid')",
        "test_code": "session_token = 'abc123'\nrequest_token = 'abc123'\nif session_token == request_token:\n    print('CSRF token valid')",
        "explanation": "CSRF tokens prevent unauthorized actions on behalf of users!",
        "points": 245,
        "category": "web"
    },
    {
        "id": 57,
        "title": "OAuth Flow Understanding",
        "description": "Modern authentication protocol.",
        "challenge": "List the 3 main OAuth components: Client, Resource Server, Authorization Server.",
        "hint": "OAuth has 3 parties",
        "solution": "components = ['Client', 'Resource Server', 'Authorization Server']\nprint(components)",
        "test_code": "components = ['Client', 'Resource Server', 'Authorization Server']\nprint(components)",
        "explanation": "OAuth enables secure delegated access!",
        "points": 250,
        "category": "web"
    },
    {
        "id": 58,
        "title": "SQL Prepared Statements",
        "description": "Prevent SQL injection properly.",
        "challenge": "Understand parameterized queries use placeholders.",
        "hint": "Use ? or %s as placeholders",
        "solution": "# Safe: cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))\nprint('Always use parameterized queries!')",
        "test_code": "print('Always use parameterized queries!')",
        "explanation": "Prepared statements separate code from data!",
        "points": 255,
        "category": "web"
    },
    {
        "id": 59,
        "title": "Content Security Policy",
        "description": "Browser security header.",
        "challenge": "Create a CSP header that blocks inline scripts.",
        "hint": "Use script-src directive",
        "solution": "csp = \"Content-Security-Policy: script-src 'self'\"\nprint(csp)",
        "test_code": "csp = \"Content-Security-Policy: script-src 'self'\"\nprint(csp)",
        "explanation": "CSP prevents XSS by controlling resource loading!",
        "points": 260,
        "category": "web"
    },
    {
        "id": 60,
        "title": "Subresource Integrity",
        "description": "Verify third-party resources.",
        "challenge": "Understand SRI uses hash to verify CDN files.",
        "hint": "integrity='sha384-...'",
        "solution": "print('SRI ensures CDN files are not tampered with')",
        "test_code": "print('SRI ensures CDN files are not tampered with')",
        "explanation": "SRI protects against compromised CDNs!",
        "points": 265,
        "category": "web"
    },
    {
        "id": 61,
        "title": "DNS Rebinding Attack",
        "description": "Advanced network attack.",
        "challenge": "Understand DNS rebinding changes IP after initial lookup.",
        "hint": "DNS response changes over time",
        "solution": "print('DNS rebinding bypasses same-origin policy')",
        "test_code": "print('DNS rebinding bypasses same-origin policy')",
        "explanation": "DNS rebinding can access internal networks!",
        "points": 270,
        "category": "network"
    },
    {
        "id": 62,
        "title": "Race Condition Detection",
        "description": "Time-of-check to time-of-use bugs.",
        "challenge": "Understand race conditions happen with concurrent access.",
        "hint": "Check and use must be atomic",
        "solution": "print('Race conditions occur with concurrent operations')",
        "test_code": "print('Race conditions occur with concurrent operations')",
        "explanation": "Race conditions can lead to security vulnerabilities!",
        "points": 275,
        "category": "security"
    },
    {
        "id": 63,
        "title": "Integer Overflow",
        "description": "Numeric boundary issues.",
        "challenge": "Understand integer overflow wraps around maximum value.",
        "hint": "In some languages, max + 1 = min",
        "solution": "print('Integer overflow can cause unexpected behavior')",
        "test_code": "print('Integer overflow can cause unexpected behavior')",
        "explanation": "Python handles big integers, but other languages don't!",
        "points": 280,
        "category": "security"
    },
    {
        "id": 64,
        "title": "Buffer Overflow Basics",
        "description": "Memory corruption attacks.",
        "challenge": "Understand buffer overflows write beyond allocated memory.",
        "hint": "Writing past buffer end corrupts memory",
        "solution": "print('Buffer overflows can execute arbitrary code')",
        "test_code": "print('Buffer overflows can execute arbitrary code')",
        "explanation": "Not common in Python, but critical in C/C++!",
        "points": 285,
        "category": "security"
    },
    {
        "id": 65,
        "title": "Side Channel Attacks",
        "description": "Information leakage through indirect means.",
        "challenge": "Understand timing, power, and electromagnetic attacks exist.",
        "hint": "Timing attacks measure execution time",
        "solution": "print('Side channels leak information indirectly')",
        "test_code": "print('Side channels leak information indirectly')",
        "explanation": "Side channels bypass cryptographic security!",
        "points": 290,
        "category": "crypto"
    },
    {
        "id": 66,
        "title": "Privilege Escalation",
        "description": "Gaining higher access levels.",
        "challenge": "Understand vertical vs horizontal privilege escalation.",
        "hint": "Vertical = higher role, Horizontal = same role different user",
        "solution": "print('Privilege escalation gains unauthorized access')",
        "test_code": "print('Privilege escalation gains unauthorized access')",
        "explanation": "Always validate authorization, not just authentication!",
        "points": 295,
        "category": "security"
    },
    {
        "id": 67,
        "title": "Zero-Day Vulnerability",
        "description": "Unknown security flaws.",
        "challenge": "Understand zero-days are unknown to vendors.",
        "hint": "No patch exists yet",
        "solution": "print('Zero-days are vulnerabilities without patches')",
        "test_code": "print('Zero-days are vulnerabilities without patches')",
        "explanation": "Zero-days are extremely valuable to attackers!",
        "points": 300,
        "category": "security"
    },
    {
        "id": 68,
        "title": "Threat Modeling",
        "description": "Systematic security analysis.",
        "challenge": "List 4 questions: What are we building? What can go wrong? What are we doing about it? Did we do good?",
        "hint": "STRIDE methodology",
        "solution": "questions = ['What building?', 'What wrong?', 'What doing?', 'Did good?']\nprint(questions)",
        "test_code": "questions = ['What building?', 'What wrong?', 'What doing?', 'Did good?']\nprint(questions)",
        "explanation": "Threat modeling identifies risks early!",
        "points": 305,
        "category": "security"
    },
    {
        "id": 69,
        "title": "Defense in Depth",
        "description": "Layered security approach.",
        "challenge": "Understand multiple security layers are better than one.",
        "hint": "Don't rely on single defense",
        "solution": "print('Defense in depth uses multiple security layers')",
        "test_code": "print('Defense in depth uses multiple security layers')",
        "explanation": "No single defense is perfect. Layer them!",
        "points": 310,
        "category": "security"
    },
    {
        "id": 70,
        "title": "Least Privilege Principle",
        "description": "Minimal access rights.",
        "challenge": "Understand users should have minimum necessary permissions.",
        "hint": "Grant only what's needed",
        "solution": "print('Least privilege limits damage from compromises')",
        "test_code": "print('Least privilege limits damage from compromises')",
        "explanation": "Minimize permissions to reduce attack surface!",
        "points": 315,
        "category": "security"
    },
    {
        "id": 71,
        "title": "Fail Securely",
        "description": "Safe failure modes.",
        "challenge": "Understand errors should deny access, not grant it.",
        "hint": "Default deny on error",
        "solution": "print('Fail securely: deny access on errors')",
        "test_code": "print('Fail securely: deny access on errors')",
        "explanation": "Errors should never grant unintended access!",
        "points": 320,
        "category": "security"
    },
    {
        "id": 72,
        "title": "Security Through Obscurity",
        "description": "Why hiding is not security.",
        "challenge": "Understand obscurity alone is not secure.",
        "hint": "Security should not depend on secrecy of design",
        "solution": "print('Security through obscurity is not real security')",
        "test_code": "print('Security through obscurity is not real security')",
        "explanation": "Assume attacker knows your system. Use strong security!",
        "points": 325,
        "category": "security"
    },
    {
        "id": 73,
        "title": "Open Web Application Security Project",
        "description": "OWASP Top 10.",
        "challenge": "List 3 OWASP Top 10 items: Injection, Broken Auth, XSS.",
        "hint": "OWASP maintains top vulnerability list",
        "solution": "owasp = ['Injection', 'Broken Auth', 'XSS']\nprint(owasp)",
        "test_code": "owasp = ['Injection', 'Broken Auth', 'XSS']\nprint(owasp)",
        "explanation": "OWASP Top 10 guides web application security!",
        "points": 330,
        "category": "security"
    },
    {
        "id": 74,
        "title": "Penetration Testing Phases",
        "description": "Ethical hacking methodology.",
        "challenge": "List phases: Reconnaissance, Scanning, Exploitation, Post-Exploitation.",
        "hint": "Pen testing has structured phases",
        "solution": "phases = ['Recon', 'Scanning', 'Exploitation', 'Post-Exploitation']\nprint(phases)",
        "test_code": "phases = ['Recon', 'Scanning', 'Exploitation', 'Post-Exploitation']\nprint(phases)",
        "explanation": "Systematic approach ensures thorough testing!",
        "points": 335,
        "category": "security"
    },
    {
        "id": 75,
        "title": "Bug Bounty Programs",
        "description": "Responsible disclosure.",
        "challenge": "Understand bug bounties reward ethical hackers.",
        "hint": "Report vulnerabilities responsibly",
        "solution": "print('Bug bounties encourage responsible disclosure')",
        "test_code": "print('Bug bounties encourage responsible disclosure')",
        "explanation": "Report bugs to vendors, get rewarded!",
        "points": 340,
        "category": "security"
    },

    # === MASTER TIER (76-100): Professional Security Engineering ===
    {
        "id": 76,
        "title": "Secure Random Numbers",
        "description": "Cryptographically secure randomness.",
        "challenge": "Use secrets module to generate secure random token.",
        "hint": "import secrets; secrets.token_hex()",
        "solution": "import secrets\ntoken = secrets.token_hex(16)\nprint(len(token))",
        "test_code": "import secrets\ntoken = secrets.token_hex(16)\nprint(len(token))",
        "explanation": "Never use random module for security! Use secrets!",
        "points": 345,
        "category": "crypto"
    },
    {
        "id": 77,
        "title": "Key Derivation Function",
        "description": "Derive keys from passwords.",
        "challenge": "Understand PBKDF2 strengthens passwords into encryption keys.",
        "hint": "Multiple iterations slow down attacks",
        "solution": "print('PBKDF2 derives strong keys from passwords')",
        "test_code": "print('PBKDF2 derives strong keys from passwords')",
        "explanation": "KDFs make brute forcing passwords expensive!",
        "points": 350,
        "category": "crypto"
    },
    {
        "id": 78,
        "title": "Digital Signatures",
        "description": "Cryptographic proof of authenticity.",
        "challenge": "Understand signatures prove message origin and integrity.",
        "hint": "Sign with private key, verify with public key",
        "solution": "print('Digital signatures ensure authenticity and integrity')",
        "test_code": "print('Digital signatures ensure authenticity and integrity')",
        "explanation": "Signatures prevent tampering and impersonation!",
        "points": 355,
        "category": "crypto"
    },
    {
        "id": 79,
        "title": "Certificate Pinning",
        "description": "Prevent man-in-the-middle attacks.",
        "challenge": "Understand pinning validates specific certificates.",
        "hint": "Don't trust all CAs",
        "solution": "print('Certificate pinning validates specific certs')",
        "test_code": "print('Certificate pinning validates specific certs')",
        "explanation": "Pinning prevents rogue CA certificates!",
        "points": 360,
        "category": "network"
    },
    {
        "id": 80,
        "title": "Perfect Forward Secrecy",
        "description": "Long-term key compromise protection.",
        "challenge": "Understand PFS uses ephemeral keys for each session.",
        "hint": "Session keys not derived from long-term keys",
        "solution": "print('PFS protects past sessions even if key compromised')",
        "test_code": "print('PFS protects past sessions even if key compromised')",
        "explanation": "PFS ensures past traffic stays secure!",
        "points": 365,
        "category": "crypto"
    },
    {
        "id": 81,
        "title": "API Rate Limiting Advanced",
        "description": "Token bucket algorithm.",
        "challenge": "Implement token bucket: refill tokens over time.",
        "hint": "Tokens regenerate at fixed rate",
        "solution": "tokens = 10\nmax_tokens = 10\nrefill_rate = 1  # per second\nprint('Token bucket allows burst with smooth refill')",
        "test_code": "print('Token bucket allows burst with smooth refill')",
        "explanation": "Token bucket balances burst and sustained rate!",
        "points": 370,
        "category": "security"
    },
    {
        "id": 82,
        "title": "Mutual TLS",
        "description": "Two-way certificate authentication.",
        "challenge": "Understand mTLS requires both client and server certificates.",
        "hint": "Both parties verify each other",
        "solution": "print('mTLS provides strong mutual authentication')",
        "test_code": "print('mTLS provides strong mutual authentication')",
        "explanation": "mTLS is stronger than password authentication!",
        "points": 375,
        "category": "network"
    },
    {
        "id": 83,
        "title": "Security Headers Analysis",
        "description": "Comprehensive header security.",
        "challenge": "List 5 security headers: CSP, HSTS, X-Frame-Options, X-Content-Type-Options, Referrer-Policy.",
        "hint": "Modern browsers support many security headers",
        "solution": "headers = ['CSP', 'HSTS', 'X-Frame-Options', 'X-Content-Type-Options', 'Referrer-Policy']\nprint(headers)",
        "test_code": "headers = ['CSP', 'HSTS', 'X-Frame-Options', 'X-Content-Type-Options', 'Referrer-Policy']\nprint(headers)",
        "explanation": "Security headers provide defense in depth!",
        "points": 380,
        "category": "web"
    },
    {
        "id": 84,
        "title": "WebAuthn/FIDO2",
        "description": "Passwordless authentication.",
        "challenge": "Understand WebAuthn uses hardware tokens for auth.",
        "hint": "YubiKey, TouchID are WebAuthn authenticators",
        "solution": "print('WebAuthn enables passwordless authentication')",
        "test_code": "print('WebAuthn enables passwordless authentication')",
        "explanation": "Hardware keys are phishing-resistant!",
        "points": 385,
        "category": "security"
    },
    {
        "id": 85,
        "title": "Supply Chain Security",
        "description": "Dependency vulnerability management.",
        "challenge": "Understand third-party code can contain vulnerabilities.",
        "hint": "Audit dependencies regularly",
        "solution": "print('Supply chain attacks target dependencies')",
        "test_code": "print('Supply chain attacks target dependencies')",
        "explanation": "Modern apps have hundreds of dependencies!",
        "points": 390,
        "category": "security"
    },
    {
        "id": 86,
        "title": "Container Security",
        "description": "Docker/Kubernetes security.",
        "challenge": "Understand containers need security: least privilege, scanning, isolation.",
        "hint": "Don't run as root in containers",
        "solution": "print('Container security requires multiple controls')",
        "test_code": "print('Container security requires multiple controls')",
        "explanation": "Containers share kernel, need careful isolation!",
        "points": 395,
        "category": "security"
    },
    {
        "id": 87,
        "title": "Zero Trust Architecture",
        "description": "Never trust, always verify.",
        "challenge": "Understand zero trust assumes breach and verifies everything.",
        "hint": "No implicit trust based on network location",
        "solution": "print('Zero trust verifies every request')",
        "test_code": "print('Zero trust verifies every request')",
        "explanation": "Modern security doesn't trust internal networks!",
        "points": 400,
        "category": "security"
    },
    {
        "id": 88,
        "title": "Secure Development Lifecycle",
        "description": "Security in every phase.",
        "challenge": "List SDL phases: Requirements, Design, Implementation, Testing, Deployment, Maintenance.",
        "hint": "Security at every SDLC stage",
        "solution": "phases = ['Requirements', 'Design', 'Implementation', 'Testing', 'Deployment', 'Maintenance']\nprint(phases)",
        "test_code": "phases = ['Requirements', 'Design', 'Implementation', 'Testing', 'Deployment', 'Maintenance']\nprint(phases)",
        "explanation": "Integrate security from day one!",
        "points": 405,
        "category": "security"
    },
    {
        "id": 89,
        "title": "Incident Response Plan",
        "description": "Handling security incidents.",
        "challenge": "List IR phases: Preparation, Detection, Containment, Eradication, Recovery, Lessons Learned.",
        "hint": "Have a plan before incidents happen",
        "solution": "ir = ['Preparation', 'Detection', 'Containment', 'Eradication', 'Recovery', 'Lessons']\nprint(ir)",
        "test_code": "ir = ['Preparation', 'Detection', 'Containment', 'Eradication', 'Recovery', 'Lessons']\nprint(ir)",
        "explanation": "Good IR minimizes damage and recovery time!",
        "points": 410,
        "category": "security"
    },
    {
        "id": 90,
        "title": "Security Metrics",
        "description": "Measuring security posture.",
        "challenge": "Understand metrics: MTTR, vulnerability count, patch cadence, incident frequency.",
        "hint": "What gets measured gets managed",
        "solution": "metrics = ['MTTR', 'Vuln Count', 'Patch Cadence', 'Incident Rate']\nprint(metrics)",
        "test_code": "metrics = ['MTTR', 'Vuln Count', 'Patch Cadence', 'Incident Rate']\nprint(metrics)",
        "explanation": "Metrics drive security improvements!",
        "points": 415,
        "category": "security"
    },
    {
        "id": 91,
        "title": "Compliance Frameworks",
        "description": "Regulatory requirements.",
        "challenge": "List frameworks: PCI-DSS, HIPAA, GDPR, SOC 2, ISO 27001.",
        "hint": "Different industries have different requirements",
        "solution": "frameworks = ['PCI-DSS', 'HIPAA', 'GDPR', 'SOC 2', 'ISO 27001']\nprint(frameworks)",
        "test_code": "frameworks = ['PCI-DSS', 'HIPAA', 'GDPR', 'SOC 2', 'ISO 27001']\nprint(frameworks)",
        "explanation": "Compliance is minimum baseline, not maximum security!",
        "points": 420,
        "category": "security"
    },
    {
        "id": 92,
        "title": "Red Team vs Blue Team",
        "description": "Adversarial security testing.",
        "challenge": "Understand Red Team attacks, Blue Team defends.",
        "hint": "Purple Team collaborates",
        "solution": "print('Red Team: Attack. Blue Team: Defend. Purple Team: Collaborate.')",
        "test_code": "print('Red Team: Attack. Blue Team: Defend. Purple Team: Collaborate.')",
        "explanation": "Team exercises improve both offense and defense!",
        "points": 425,
        "category": "security"
    },
    {
        "id": 93,
        "title": "SIEM and Log Analysis",
        "description": "Security Information and Event Management.",
        "challenge": "Understand SIEMs aggregate and correlate security logs.",
        "hint": "Centralized logging for security monitoring",
        "solution": "print('SIEMs detect threats through log correlation')",
        "test_code": "print('SIEMs detect threats through log correlation')",
        "explanation": "Log everything, analyze patterns, detect anomalies!",
        "points": 430,
        "category": "security"
    },
    {
        "id": 94,
        "title": "Threat Intelligence",
        "description": "Proactive threat awareness.",
        "challenge": "Understand threat intel provides indicators of compromise (IOCs).",
        "hint": "Know what attackers are doing",
        "solution": "print('Threat intelligence enables proactive defense')",
        "test_code": "print('Threat intelligence enables proactive defense')",
        "explanation": "Use IOCs to detect attacks before they succeed!",
        "points": 435,
        "category": "security"
    },
    {
        "id": 95,
        "title": "Security Automation",
        "description": "SOAR platforms.",
        "challenge": "Understand Security Orchestration, Automation, Response improves efficiency.",
        "hint": "Automate repetitive security tasks",
        "solution": "print('SOAR automates security operations')",
        "test_code": "print('SOAR automates security operations')",
        "explanation": "Automation frees analysts for complex investigations!",
        "points": 440,
        "category": "security"
    },
    {
        "id": 96,
        "title": "Cloud Security Posture Management",
        "description": "Multi-cloud security.",
        "challenge": "Understand CSPM monitors cloud configurations for security issues.",
        "hint": "Cloud misconfigurations are common",
        "solution": "print('CSPM detects cloud misconfigurations')",
        "test_code": "print('CSPM detects cloud misconfigurations')",
        "explanation": "Cloud security requires continuous monitoring!",
        "points": 445,
        "category": "security"
    },
    {
        "id": 97,
        "title": "DevSecOps Culture",
        "description": "Security in CI/CD.",
        "challenge": "Understand DevSecOps integrates security into development pipeline.",
        "hint": "Shift left: security early in development",
        "solution": "print('DevSecOps makes security everyone\\'s responsibility')",
        "test_code": "print('DevSecOps makes security everyone\\'s responsibility')",
        "explanation": "Automate security testing in CI/CD!",
        "points": 450,
        "category": "security"
    },
    {
        "id": 98,
        "title": "Blockchain Security",
        "description": "Distributed ledger security.",
        "challenge": "Understand blockchain security: 51% attacks, smart contract bugs, private key management.",
        "hint": "Immutability doesn't mean secure",
        "solution": "print('Blockchain has unique security challenges')",
        "test_code": "print('Blockchain has unique security challenges')",
        "explanation": "Smart contracts need auditing like any code!",
        "points": 455,
        "category": "security"
    },
    {
        "id": 99,
        "title": "AI/ML Security",
        "description": "Securing machine learning systems.",
        "challenge": "Understand adversarial ML: poisoning, evasion, model theft.",
        "hint": "ML models can be attacked too",
        "solution": "print('AI/ML systems need security too')",
        "test_code": "print('AI/ML systems need security too')",
        "explanation": "Adversarial examples can fool ML models!",
        "points": 460,
        "category": "security"
    },
    {
        "id": 100,
        "title": "The Legendary Challenge",
        "description": "Complete all-in-one security script.",
        "challenge": "Create a script that: 1) Hashes a password with SHA256, 2) Checks if input contains SQLi patterns, 3) Validates an email format. Show mastery!",
        "hint": "Combine everything you've learned",
        "solution": """import hashlib
import re

# 1. Hash password
password = "secure123"
hashed = hashlib.sha256(password.encode()).hexdigest()
print(f"Hashed: {hashed}")

# 2. SQLi detection
user_input = "admin' OR 1=1--"
if "' OR" in user_input or "--" in user_input:
    print("SQLi detected!")

# 3. Email validation
email = "hacker@cyberquest.com"
if re.match(r'^[\\w\\.-]+@[\\w\\.-]+\\.\\w+$', email):
    print("Valid email!")

print("Congratulations, Legendary Hacker!")""",
        "test_code": """import hashlib
import re

password = "secure123"
hashed = hashlib.sha256(password.encode()).hexdigest()
print(f"Hashed: {hashed}")

user_input = "admin' OR 1=1--"
if "' OR" in user_input or "--" in user_input:
    print("SQLi detected!")

email = "hacker@cyberquest.com"
if re.match(r'^[\\w\\.-]+@[\\w\\.-]+\\.\\w+$', email):
    print("Valid email!")

print("Congratulations, Legendary Hacker!")""",
        "explanation": "You've mastered Python security! You're now a Legendary Hacker! 🏆",
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
    ║   ██████╗██╗   ██╗██████╗ ███████╗██████╗  ██████╗ ██╗   ██╗ ║
    ║  ██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗██╔═══██╗██║   ██║ ║
    ║  ██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝██║   ██║██║   ██║ ║
    ║  ██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗██║▄▄ ██║██║   ██║ ║
    ║  ╚██████╗   ██║   ██████╔╝███████╗██║  ██║╚██████╔╝╚██████╔╝ ║
    ║   ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚══▀▀═╝  ╚═════╝  ║
    ║                                                               ║
    ║              🎮 Python Security Academy 🎮                    ║
    ║                                                               ║
    ║           Learn Python & Cybersecurity from Zero              ║
    ║                  Author: arkanzasfeziii                       ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    """
    console.print(f"[{COLORS['hacker']}]{banner}[/]")
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
    table.add_column("Value", style=COLORS['hacker'])

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
        f"""[{COLORS['hacker']}]LEVEL {level_data['id']}: {level_data['title'].upper()}[/]

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


def simulate_hacking():
    """Show a cool hacking animation."""
    messages = [
        "Initializing neural network...",
        "Connecting to mainframe...",
        "Bypassing firewall...",
        "Decrypting protocols...",
        "Accessing secure terminal...",
        "System ready!",
    ]

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("[cyan]Booting up...", total=len(messages))
        for msg in messages:
            progress.update(task, description=f"[{COLORS['hacker']}]{msg}")
            time.sleep(random.uniform(0.3, 0.7))
            progress.advance(task)


# === Core Game Logic ===
def play_level(level_data: dict, progress: PlayerProgress) -> bool:
    """
    Play a single level.
    Returns True if completed successfully.
    """
    show_level_info(level_data)
    console.print()

    # Show hint option
    console.print(f"[{COLORS['info']}]💡 Type 'hint' for a hint, 'skip' to skip (no points), or write your code:[/]")
    console.print()

    # Get user code
    code_lines = []
    console.print(f"[{COLORS['secondary']}]Enter your Python code (type 'done' on a new line when finished):[/]")

    while True:
        try:
            line = Prompt.ask(f"[{COLORS['hacker']}]>>>")

            if line.lower() == 'done':
                break
            elif line.lower() == 'hint':
                console.print(f"[{COLORS['warning']}]💡 Hint: {level_data['hint']}[/]")
                continue
            elif line.lower() == 'skip':
                console.print(f"[{COLORS['warning']}]⏭️  Skipping level (no points awarded)[/]")
                return False
            elif line.lower() == 'solution':
                console.print(f"[{COLORS['error']}]🚫 No cheating! Try using the hint instead.[/]")
                continue
            else:
                code_lines.append(line)
        except (KeyboardInterrupt, EOFError):
            console.print(f"\n[{COLORS['warning']}]Level interrupted.[/]")
            return False

    user_code = "\n".join(code_lines)

    if not user_code.strip():
        console.print(f"[{COLORS['error']}]❌ No code entered![/]")
        return False

    # Show what they wrote
    console.print(f"\n[{COLORS['info']}]Your code:[/]")
    syntax = Syntax(user_code, "python", theme="monokai", line_numbers=True)
    console.print(syntax)
    console.print()

    # Test the code
    console.print(f"[{COLORS['warning']}]Testing your code...[/]")
    time.sleep(1)

    try:
        # Capture output
        import io
        from contextlib import redirect_stdout

        user_output = io.StringIO()
        with redirect_stdout(user_output):
            exec(user_code, {})
        user_result = user_output.getvalue().strip()

        expected_output = io.StringIO()
        with redirect_stdout(expected_output):
            exec(level_data['test_code'], {})
        expected_result = expected_output.getvalue().strip()

        # Compare outputs
        if user_result == expected_result:
            console.print(f"[{COLORS['success']}]✅ CORRECT! Level completed![/]")
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
            console.print(f"[{COLORS['info']}]Expected output:[/] {expected_result}")
            console.print(f"[{COLORS['info']}]Your output:[/] {user_result}")
            return False

    except Exception as e:
        console.print(f"[{COLORS['error']}]❌ Error in your code: {e}[/]")
        console.print(f"[{COLORS['info']}]Check for syntax errors and try again![/]")
        return False


def check_achievements(progress: PlayerProgress):
    """Check and award achievements."""
    achievements = [
        (5, "🌟 First Steps", "Completed 5 levels"),
        (10, "💻 Code Warrior", "Completed 10 levels"),
        (25, "🔐 Security Aware", "Completed 25 levels"),
        (50, "⚡ Halfway Master", "Completed 50 levels"),
        (75, "🎖️ Elite Hacker", "Completed 75 levels"),
        (100, "👑 Legendary Status", "Completed ALL levels!"),
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
        console.print(f"\n[{COLORS['hacker']}]Welcome back, {rank_name}![/]\n")

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
                        console.print(f"\n[{COLORS['hacker']}]🎉 CONGRATULATIONS! You've completed ALL 100 levels! 🎉[/]")
                        console.print(f"[{COLORS['success']}]You are now a LEGENDARY HACKER! 👑[/]")
                        console.print(f"[{COLORS['info']}]Total Points: {progress.total_points}[/]")
                        input("\nPress Enter to return to menu...")
                        break
                else:
                    if Confirm.ask(f"\n[{COLORS['warning']}]Try again?"):
                        continue
                    else:
                        break

        elif choice == "2":
            console.clear()
            show_stats(progress)
            input("\nPress Enter to continue...")

        elif choice == "3":
            max_level = max(progress.completed_levels) + 1 if progress.completed_levels else 1
            try:
                level_num = int(Prompt.ask(f"Jump to level (1-{min(max_level, 100)})"))
                if 1 <= level_num <= min(max_level, 100):
                    progress.current_level = level_num
                    save_progress(progress)
                else:
                    console.print(f"[{COLORS['error']}]Invalid level number![/]")
                    time.sleep(2)
            except ValueError:
                console.print(f"[{COLORS['error']}]Invalid level number![/]")
                time.sleep(2)

        elif choice == "4":
            console.clear()
            if progress.achievements:
                table = Table(title="🏆 Your Achievements", box=box.DOUBLE_EDGE, border_style=COLORS['success'])
                table.add_column("Achievement", style=COLORS['hacker'])
                for achievement in progress.achievements:
                    table.add_row(achievement)
                console.print(table)
            else:
                console.print(f"[{COLORS['info']}]No achievements yet. Keep playing![/]")
            input("\nPress Enter to continue...")

        elif choice == "5":
            if Confirm.ask(f"[{COLORS['error']}]Are you sure you want to reset ALL progress?"):
                progress = PlayerProgress()
                save_progress(progress)
                console.print(f"[{COLORS['success']}]Progress reset![/]")
                time.sleep(2)

        elif choice == "6":
            console.print(f"\n[{COLORS['hacker']}]Thanks for playing CyberQuest! See you next time, hacker! 👋[/]")
            break


# === Entry Point ===
def main():
    """Main entry point."""
    try:
        console.clear()
        simulate_hacking()
        time.sleep(1)
        main_menu()
    except KeyboardInterrupt:
        console.print(f"\n\n[{COLORS['warning']}]Game interrupted. Progress saved. Goodbye! 👋[/]")
    except Exception as e:
        console.print(f"\n[{COLORS['error']}]An error occurred: {e}[/]")
        console.print(f"[{COLORS['info']}]Please report this bug to arkanzasfeziii[/]")


if __name__ == "__main__":
    main()
