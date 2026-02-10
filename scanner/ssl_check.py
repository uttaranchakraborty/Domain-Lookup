import ssl, socket
from datetime import datetime
from colorama import Fore

def check_ssl(url, domain):
    if not url.startswith("https://"):
        print(Fore.YELLOW + "[!] HTTPS not enabled")
        return None
    try:
        ctx = ssl.create_default_context()
        with socket.create_connection((domain,443)) as sock:
            with ctx.wrap_socket(sock, server_hostname=domain) as ss:
                cert = ss.getpeercert()
                not_before = datetime.strptime(cert['notBefore'], "%b %d %H:%M:%S %Y %Z")
                not_after = datetime.strptime(cert['notAfter'], "%b %d %H:%M:%S %Y %Z")
                days = (not_after - datetime.now()).days
                print(Fore.GREEN + f"[+] SSL valid until {not_after} ({days} days left)")
                if days < 30:
                    print(Fore.RED + "[!] Certificate expiring soon!")
                return cert
    except Exception as e:
        print(Fore.RED + f"[-] SSL check failed: {e}")
        return None
