import socket
import requests
from colorama import Fore

def get_ip(domain):
    try:
        ip = socket.gethostbyname(domain)
        print(Fore.GREEN + f"[+] IP Address: {ip}")
        return ip
    except Exception as e:
        print(Fore.RED + f"[-] IP resolution error: {e}")
        return None

def get_ip_info(ip, timeout=10):
    try:
        resp = requests.get(f"http://ip-api.com/json/{ip}", timeout=timeout)
        resp.raise_for_status()
        data = resp.json()
        print(Fore.GREEN + f"[+] IP Location: {data.get('city','')} {data.get('country','')}")
        print(Fore.GREEN + f"[+] ISP: {data.get('isp','')}")
        return data
    except Exception:
        print(Fore.YELLOW + "[!] IP info unavailable")
        return {}
