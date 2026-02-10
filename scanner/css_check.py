
import requests
import re

def check_css_exposure(base_url):
    try:
        response = requests.get(base_url)
        css_files = re.findall(r'href=[\'"]?([^\'" >]+\.css)', response.text)
        exposed = []

        for css in css_files:
            full_url = css if css.startswith("http") else base_url.rstrip("/") + "/" + css.lstrip("/")
            r = requests.get(full_url)
            if r.status_code == 200 and "/*" in r.text:
                exposed.append(full_url)
        return exposed
    except:
        return []
