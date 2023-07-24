from cryptography.hazmat.primitives.asymmetric import ed25519
import base64
import hashlib
import re
import requests
import sys
import threading
import time

def tor_v3():
    tor_agent = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; rv:102.0) Gecko/20100101 Firefox/102.0"}
    tor_proxy = {"http": "socks5h://localhost:9050", "https": "socks5h://localhost:9050"}

    while True:
        repeat = False

        public = ed25519.Ed25519PrivateKey.generate().sign(b"")[:32]
        checksum = hashlib.sha3_256(b".onion checksum" + public + b"\x03").digest()[:2]
        result = "http://" + base64.b32encode(public + checksum + b"\x03").decode().lower() + ".onion"

        print(f"checking: {result}\n")
        try:
            my_request = requests.get(result, headers=tor_agent, proxies=tor_proxy, verify=False).text
            title = re.findall("<title>(.+)</title>", my_request)

        except:
            continue

        try:
            with open("tor_links.txt", "r") as f:
                for i in f:
                    if result in i:
                        repeat = True
                        break

        except FileNotFoundError:
            pass

        if not repeat:
            print(True)
            with open("tor_links.txt", "a") as f:
                f.write(result + "\n")

for _ in range(8):
    my_thread = threading.Thread(target=tor_v3).start()
