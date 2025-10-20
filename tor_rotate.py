import os
import subprocess
import time
import requests
from stem import Signal
from stem.control import Controller

TOR_SOCKS = "socks5h://127.0.0.1:9050"
CONTROL_PORT = 9051
CHECK_IP = "https://api.ipify.org"

# Command you normally run manually
AFTER_ROTATE_CMD = ["py", "search_once_google.py", "queries.csv"]

def get_ip_via_tor():
    proxies = {"http": TOR_SOCKS, "https": TOR_SOCKS}
    return requests.get(CHECK_IP, proxies=proxies, timeout=10).text.strip()

def main():
    with Controller.from_port(port=CONTROL_PORT) as c:
        c.authenticate()
        last_ip = None
        while True:
            # Ask Tor for new identity
            c.signal(Signal.NEWNYM)
            time.sleep(5)

            # Get current IP via Tor
            try:
                new_ip = get_ip_via_tor()
            except Exception as e:
                print("[!] Could not get IP:", e)
                time.sleep(10)
                continue

            if new_ip != last_ip:
                print(f"[+] New Tor IP: {new_ip}")
                last_ip = new_ip

                # Run your script through Tor
                env = os.environ.copy()
                env["ALL_PROXY"] = TOR_SOCKS
                env["HTTP_PROXY"] = TOR_SOCKS
                env["HTTPS_PROXY"] = TOR_SOCKS

                try:
                    subprocess.run(AFTER_ROTATE_CMD, env=env, check=True)
                    print("[✓] Script finished.\n")
                except subprocess.CalledProcessError as e:
                    print("[!] Error running script:", e)
            else:
                print("[=] IP unchanged. Skipping run.")

            time.sleep(10)

if __name__ == "__main__":
    main()
