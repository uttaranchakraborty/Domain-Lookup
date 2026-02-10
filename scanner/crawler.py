import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from colorama import Fore

def crawl(url, domain):
    resp = requests.get(url, timeout=10, verify=False)
    soup = BeautifulSoup(resp.text, 'html.parser')
    links = set()
    forms = []
    for a in soup.find_all("a", href=True):
        href = a['href']
        if href.startswith('http') and domain in href:
            links.add(href)
        elif href.startswith('/'):
            links.add(urljoin(url, href))
    print(Fore.GREEN + f"[+] Links: {len(links)}")
    for f in soup.find_all('form'):
        forms.append({
            "action": f.get('action',''),
            "method": f.get('method','').upper(),
            "inputs": [i.get('name','') for i in f.find_all('input')]
        })
    print(Fore.GREEN + f"[+] Forms: {len(forms)}")
    return links, forms
