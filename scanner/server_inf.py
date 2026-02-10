import requests
from colorama import Fore

def fetch_server_info(url, timeout=10):
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, headers=headers, timeout=timeout, verify=False)
    info = {
        "status": resp.status_code,
        "headers": dict(resp.headers)
    }
    print(Fore.GREEN + f"[+] HTTP Status {resp.status_code}")
    for h in ["Server","X-Powered-By"]:
        if h in resp.headers:
            print(Fore.GREEN + f"[+] {h}: {resp.headers[h]}")
    # Missing security headers
    sec = ['Content-Security-Policy','X-Frame-Options','X-Content-Type-Options','Strict-Transport-Security']
    miss = [h for h in sec if h not in resp.headers]
    if miss:
        print(Fore.YELLOW + f"[!] Missing security headers: {', '.join(miss)}")
    return info
