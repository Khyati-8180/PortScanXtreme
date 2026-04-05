import socket
import requests
import threading
from colorama import Fore, init

# Initialize colorama
init()

# 🔐 Banner Grabbing
def banner_grab(ip, port):
    try:
        s = socket.socket()
        s.settimeout(2)
        s.connect((ip, port))
        banner = s.recv(1024)
        return banner.decode().strip()
    except:
        return None

# 🔍 Scan each port (THREAD FUNCTION)
def scan_port(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)

    result = s.connect_ex((target, port))

    if result == 0:
        print(Fore.GREEN + f"[OPEN] Port {port}")

        banner = banner_grab(target, port)
        if banner:
            print(Fore.YELLOW + f"   → Service: {banner}")
    else:
        print(Fore.RED + f"[CLOSED] Port {port}")

    s.close()

# 🌐 Header Check
def check_headers(url):
    try:
        response = requests.get(url)
        headers = response.headers

        print(Fore.CYAN + "\n[+] Checking Security Headers...\n")

        if "X-Frame-Options" not in headers:
            print(Fore.YELLOW + "[WARNING] Missing X-Frame-Options")

        if "Content-Security-Policy" not in headers:
            print(Fore.YELLOW + "[WARNING] Missing Content-Security-Policy")

        if "Strict-Transport-Security" not in headers:
            print(Fore.YELLOW + "[WARNING] Missing HSTS")

    except:
        print(Fore.RED + "Could not check headers")

# 🎯 Input
target = input("Enter target IP or domain: ")

ports = [21, 22, 23, 25, 53, 80, 110, 139, 143, 443, 445, 8080]

print(Fore.CYAN + f"\nScanning target: {target}\n")

# ⚡ THREADING STARTS HERE
threads = []

for port in ports:
    t = threading.Thread(target=scan_port, args=(port,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

# 🌐 Header check
if "http" not in target:
    target_url = "http://" + target
else:
    target_url = target

check_headers(target_url)   