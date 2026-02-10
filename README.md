# 🦂 Seto1 Bruter

**Seto1 Bruter** is a powerful Python-based ethical hacking tool for performing full-scope recon and brute-force attacks against websites. It automates reconnaissance and initial exploitation techniques, making it perfect for red team ops, bug bounty hunters, and CTF players.

---
screenshots : 

<img width="790" height="671" alt="Screenshot 2025-07-18 054002" src="https://github.com/user-attachments/assets/68ef4518-f7c8-41eb-b3f7-c0ba7674f596" />


<img width="872" height="681" alt="Screenshot 2025-07-18 054037" src="https://github.com/user-attachments/assets/9e9f395a-7d86-4ff4-bb9b-5d23a426e85e" />

## 🚀 Features

- 🌐 Target scanning (IP, WHOIS, location, DNS, headers, SSL info)
- 🔍 Admin panel discovery
- 🔐 WordPress login bruteforcer (optional)
- 💉 SQL Injection detection on URLs and forms
- 📤 Form enumeration
- 🔎 Exposed file discovery (CSS, backups, sensitive paths)
- ⚡ Port scanner (80, 443)
- 🧠 Smart detection of WordPress, themes, and plugins
- 📥 JSON report output
- 💣 Integration-ready for Hydra/WPScan

---

## 🛠️ Usage

```bash
sudo apt update && apt upgrade -y

sudo apt install git

git clone https://github.com/Phoenix-sudo-tech/seto1-bruter.git

sudo apt install python3-venv

python3 -m venv venv

source venv/bin/activate

pip install requests beautifulsoup4 dnspython python-whois colorama

python3 launch.py https://target.com
