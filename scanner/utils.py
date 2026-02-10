import sys
from urllib.parse import urlparse

def normalize_url(url: str) -> str:
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    return url.rstrip('/')

def is_valid_url(url: str) -> bool:
    p = urlparse(url)
    return bool(p.scheme and p.netloc)

def exit_error(msg: str):
    print(f"[ERROR] {msg}")
    sys.exit(1)
