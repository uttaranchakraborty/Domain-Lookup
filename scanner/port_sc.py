import socket
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore

def scan_ports(ip, ports=[80,443,8080,8443]):
    open_ports = []
    with ThreadPoolExecutor(max_workers=10) as exe:
        futures = {exe.submit(socket_connect, ip,p):p for p in ports}
        for f,p in futures.items():
            if f.result():
                open_ports.append(p)
                print(Fore.GREEN + f"[+] Port {p} is open")
    if not open_ports:
        print(Fore.YELLOW + "[!] No open ports")
    return open_ports

def socket_connect(ip, port):
    s = socket.socket()
    s.settimeout(1)
    try:
        s.connect((ip,port))
        s.close()
        return True
    except:
        return False
