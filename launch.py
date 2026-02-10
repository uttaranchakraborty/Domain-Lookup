
import argparse
import json
from pathlib import Path
from urllib.parse import urlparse
from scanner import (
    banner,
    crawler,
    dns,
    leaks,
    network,
    port_sc,
    sens,
    server_inf,
    ssl_check,
    whois,
    sql_attack,
    admin_finder,
    css_check,
)
import requests

def normalize_url(url: str) -> str:
    if not url.startswith(("http://", "https://")):
        url = "http://" + url
    return url.rstrip("/")

def run_scan(target_url: str):
    url = normalize_url(target_url)
    domain = urlparse(url).netloc

    results = {
        "basic": {},
        "vulnerabilities": {},
    }

    try:
        banner.print_banner(url, domain)
    except Exception:
        print("[!] Skipping banner")

    ip = network.get_ip(domain)
    results["basic"]["ip"] = ip
    if ip:
        results["basic"]["ip_info"] = network.get_ip_info(ip)

    results["basic"]["whois"] = whois.lookup_whois(domain)
    results["basic"]["dns"] = dns.check_dns(domain)
    results["server_info"] = server_inf.fetch_server_info(url)
    results["ssl"] = ssl_check.check_ssl(url, domain)

    links, forms = crawler.crawl(url, domain)
    results["crawl"] = {"links": list(links), "forms": forms}
    results["vulnerabilities"]["sensitive_files"] = sens.check_sensitive(url)

    try:
        print("[*] Scanning for admin pages...")
        admin_pages = admin_finder.find_admin_pages(url)
        results["vulnerabilities"]["admin_pages"] = admin_pages
        for page in admin_pages:
            print(f"[+] Found admin page: {page}")
    except Exception as e:
        print(f"[!] Error in admin finder: {e}")

    try:
        print("[*] Testing for SQL Injection...")
        sqli_results = sql_attack.test_sql_injection(url)
        results["vulnerabilities"]["sql_injection"] = sqli_results
        for vuln in sqli_results:
            print(f"[!] SQL Injection vulnerability found: {vuln}")
    except Exception as e:
        print(f"[!] Error in SQL Injection module: {e}")

    try:
        print("[*] Checking for exposed CSS files...")
        css_results = css_check.check_css_exposure(url)
        results["vulnerabilities"]["css_exposure"] = css_results
        for css in css_results:
            print(f"[!] Exposed CSS file: {css}")
    except Exception as e:
        print(f"[!] Error in CSS module: {e}")

    try:
        body = requests.get(url, timeout=10, verify=False).text
        results["vulnerabilities"]["leaks"] = leaks.find_leaks(body)
    except Exception:
        results["vulnerabilities"]["leaks"] = []

    if ip:
        results["basic"]["open_ports"] = port_sc.scan_ports(ip)

    out_file = Path(f"scan_{domain.replace(':', '_')}.json")
    out_file.write_text(json.dumps(results, indent=2, default=str))
    print(f"\n[+] Scan report saved to {out_file}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Modular Website Vulnerability Scanner")
    parser.add_argument("url", help="Target URL (e.g. https://example.com)")
    args = parser.parse_args()
    run_scan(args.url)
