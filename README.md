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

pip3 install -r requirements.txt

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

Technical Notes Security Warnings:

Disables SSL verification (verify=False)

Ignores security warnings (warnings.filterwarnings)

Uses insecure HTTP callbacks to "evil.site"

Evasion Techniques:

Random user-agent rotation

Base64 payload obfuscation

Session persistence

Delayed requests (timeout=5)

Brute-force Credentials Tested:

admin/admin123

root/toor

user/123456

Ethical Considerations

This tool demonstrates:

Importance of form validation

Need for input sanitization

Session cookie security risks

Password policy vulnerabilities

Web spidering dangers

Always obtain written permission before testing any website. Check local laws regarding security research.

8. Suggested Improvements
Add command-line arguments for target URL

Implement threading for faster scanning

Add proxy support

Include vulnerability reporting feature

-----------------Use only on unauthorized systems!--------------------
