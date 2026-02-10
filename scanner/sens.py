import requests
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore

ENDPOINTS = ["phpinfo.php","test.php",".env","config.php","backup.zip"]

def check_sensitive(url):
    found = []
    with ThreadPoolExecutor(max_workers=10) as exe:
        futures = [exe.submit(requests.head, urljoin(url,e), timeout=5, verify=False) for e in ENDPOINTS]
        for f,e in zip(futures, ENDPOINTS):
            try:
                resp = f.result()
                if resp.status_code < 400:
                    found.append(e)
                    print(Fore.RED + f"[!] Sensitive: {e}")
            except:
                pass
    if not found:
        print(Fore.GREEN + "[+] No sensitive files")
    return found
