# Extreme-Web_Attack

## Features
- Automated form brute-force attacks
- Cross-site scripting (XSS) payload injection
- Session cookie theft
- Admin panel discovery
- Web spidering with depth control
- Stealth mode with random user agents
- Payload obfuscation (Base64 encoding)

## Installation

pip install -r requirements.txt

Usage
1: Run the script for linux: 
python3 extreme-linux.py

1: Run the script for Termux: 
python3 extreme-termux.py


Enter target URL when prompted

View attack results in console

Attack Workflow
Spider target website (5 levels deep)

Inject payloads into all discovered forms

Attempt common credential combinations

Scan for admin panels

Extract session cookies

Warning This tool:

Ignores SSL certificate verification

Sends malicious payloads

Modifies website content

Attempts credential brute-forcing

Use only on unauthorized systems!

