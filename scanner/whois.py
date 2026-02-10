import whois
from colorama import Fore

def lookup_whois(domain):
    try:
        w = whois.whois(domain)
        print(Fore.GREEN + "[+] WHOIS:")
        print(Fore.GREEN + f"  Registrar: {w.registrar}")
        print(Fore.GREEN + f"  Created: {w.creation_date}")
        print(Fore.GREEN + f"  Expires: {w.expiration_date}")
        return w
    except Exception as e:
        print(Fore.RED + f"[-] WHOIS error: {e}")
        return None
