import re
from colorama import Fore

def find_leaks(text: str):
    leaks = []
    emails = set(re.findall(r'[\w\.-]+@[\w\.-]+', text))
    if emails:
        print(Fore.RED + f"[!] Emails: {', '.join(emails)}")
        leaks += list(emails)
    keys = re.findall(r'AKIA[0-9A-Z]{16}', text)
    if keys:
        print(Fore.RED + f"[!] AWS keys: {', '.join(keys)}")
        leaks += keys
    return leaks
