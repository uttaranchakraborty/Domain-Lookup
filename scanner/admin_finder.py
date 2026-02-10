



import requests

COMMON_ADMIN_PATHS = [
    'admin/', 'admin.php', 'admin/login.php', 'administrator/', 'cpanel/', 'admin123/'
]

def find_admin_pages(url):
    found = []
    for path in COMMON_ADMIN_PATHS:
        full_url = url.rstrip('/') + '/' + path
        try:
            r = requests.get(full_url, timeout=5)
            if r.status_code in [200, 301, 302]:
                found.append(full_url)
        except:
            continue
    return found
