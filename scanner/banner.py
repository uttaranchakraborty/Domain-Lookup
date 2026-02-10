from datetime import datetime
from colorama import Fore, Style

def print_banner(url, domain):
    print(Fore.RED + r"""
   _____      _       __     ____             _
  / ____|    | |     /_ |   |  _ \           | |
 | (___   ___| |_ ___ | |   | |_) |_ __ _   _| |_ ___ _ __
  \___ \ / _ \ __/ _ \| |   |  _ <| '__| | | | __/ _ \ '__|
  ____) |  __/ || (_) | |   | |_) | |  | |_| | ||  __/ |
 |_____/ \___|\__\___/|_|   |____/|_|   \__,_|\__\___|_|
    """ + Style.RESET_ALL)
    print(Fore.YELLOW + f"[*] Scanning target: {url}")
    print(Fore.YELLOW + f"[*] Domain: {domain}")
    print(Fore.YELLOW + f"[*] Start time: {datetime.now():%Y-%m-%d %H:%M:%S}")
    print("-" * 60)
