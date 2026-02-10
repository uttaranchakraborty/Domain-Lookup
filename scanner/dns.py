import dns.resolver
from colorama import Fore

def check_dns(domain):
    recs = {}
    types = ["A","AAAA","MX","NS","TXT","CNAME"]
    print(Fore.CYAN + "[*] DNS records...")
    for t in types:
        try:
            answers = dns.resolver.resolve(domain, t)
            recs[t] = [str(r) for r in answers]
            print(Fore.GREEN + f"[+] {t}: {', '.join(recs[t])}")
        except Exception:
            pass
    # DMARC
    try:
        answers = dns.resolver.resolve(f"_dmarc.{domain}", "TXT")
        recs["DMARC"] = [str(r) for r in answers]
        print(Fore.GREEN + "[+] DMARC found")
    except:
        print(Fore.YELLOW + "[!] No DMARC record")
    return recs
