from subprocess import Popen, PIPE, STDOUT, run
import urllib.request
import json
import datetime
import random
import string
import time
import os
import sys
from concurrent.futures import ThreadPoolExecutor
import socks
import socket


def genString(stringLength):
    try:
        letters = string.ascii_letters + string.digits
        return ''.join(random.choice(letters) for i in range(stringLength))
    except Exception as error:
        print(error)


def digitString(stringLength):
    try:
        digit = string.digits
        return ''.join((random.choice(digit) for i in range(stringLength)))
    except Exception as error:
        print(error)


def send_request(device_id: str, *addr: str):
    print(device_id)
    try:
        install_id = genString(22)
        body = {"key": "{}=".format(genString(43)),
                "install_id": install_id,
                "fcm_token": "{}:APA91b{}".format(install_id, genString(134)),
                "referrer": device_id,
                "warp_enabled": False,
                "tos": datetime.datetime.now().isoformat()[:-3] + "+02:00",
                "type": "Android",
                "locale": "es_ES"}
        data = json.dumps(body).encode('utf8')
        headers = {'Content-Type': 'application/json; charset=UTF-8',
                   'Host': 'api.cloudflareclient.com',
                   'Connection': 'Keep-Alive',
                   'Accept-Encoding': 'gzip',
                   'User-Agent': 'okhttp/3.12.1'
                   }
        req = urllib.request.Request(url, data, headers)
        response = urllib.request.urlopen(req)
        status_code = response.getcode()
        return status_code
    except Exception as error:
        print(error)


def generate_account(filename: str):
    run(["bin/wgcf", "register", "--accept-tos", "--config", f"conf/{filename}"])


def process_account(filename: str, *addr):
    device_id = ''
    with open(f"conf/{filename}", "r") as f:
        lines = f.readlines()
        for line in lines:
            data = line.split('=')
            if data[0] == 'device_id ':
                device_id = data[1].replace('\n', '').replace(' ', '').replace("'", '')
                break
    time.sleep(5)

    g = 0
    b = 0
    while g < 3 and b < 5:
        result = send_request(device_id, *addr)
        if result == 200:
            g = g + 1
            # os.system('cls' if os.name == 'nt' else 'clear')
            print("")
            print("                  WARP-PLUS-CLOUDFLARE (script)" + " By ALIILAPRO")
            print("")
            animation = ["[■□□□□□□□□□] 10%", "[■■□□□□□□□□] 20%", "[■■■□□□□□□□] 30%", "[■■■■□□□□□□] 40%",
                         "[■■■■■□□□□□] 50%",
                         "[■■■■■■□□□□] 60%", "[■■■■■■■□□□] 70%", "[■■■■■■■■□□] 80%", "[■■■■■■■■■□] 90%",
                         "[■■■■■■■■■■] 100%"]
            for i in range(len(animation)):
                time.sleep(0.5)
                sys.stdout.write("\r[+] Preparing... " + animation[i % len(animation)])
                sys.stdout.flush()
            print(f"\n[-] WORK ON ID: {device_id}")
            print(f"[:)] {g} GB has been successfully added to your account.")
            print(f"[#] Total: {g} Good {b} Bad")
            print("[*] After 5 seconds, a new request will be sent.")

        else:
            b = b + 1
            # os.system('cls' if os.name == 'nt' else 'clear')
            print("")
            print("                  WARP-PLUS-CLOUDFLARE (script)" + " By ALIILAPRO")
            print("")
            print("[:(] Error when connecting to server.")
            print(f"[#] Total: {g} Good {b} Bad")
        time.sleep(5)


def proxy_validate(addr: str) -> str:
    try:
        print(addr.replace('\n', ''))
        req = urllib.request.Request("http://httpbin.org/ip")
        socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, addr)
        socket.socket = socks.socksocket

        response = urllib.request.urlopen(req, timeout=2)
        status_code = response.getcode()
        if status_code == 200:
            return addr
        else:
            return ""
    except Exception as error:
        print(error)
        return ""


def proxy_prepare() -> []:
    proxies = []
    run(["/usr/bin/wget",
         "https://raw.githubusercontent.com/ALIILAPRO/Proxy/main/socks5.txt", "-O",
         "proxy.txt"])
    with open("proxy.txt", "r") as f:
        lines = f.readlines()
        # Create a ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=10) as executor:
            # Start a thread for each state
            futures = [executor.submit(proxy_validate, line) for line in lines]
            # Wait for all threads to finish
            for future in futures:
                if future.result() != "":
                    proxies.append(future.result())

    with open('proxy_tested.txt', 'w') as f:
        for proxy in proxies:
            f.write(f'{proxy}')
    return proxies


if __name__ == "__main__":
    if not os.path.exists("bin"):
        os.mkdir("bin")
        print("bin folder created")

    if not os.path.exists("conf"):
        os.mkdir("conf")
        print("conf folder created")

    if not os.path.exists("bin/wgcf"):
        run(["/usr/bin/wget",
             "https://github.com/ViRb3/wgcf/releases/download/v2.2.19/wgcf_2.2.19_linux_amd64", "-O",
             "bin/wgcf"])
        print("wgcf downloaded")

        run(["/usr/bin/chmod", "+x", "bin/wgcf"])
        print("wgcf chmoded")

    # filename = f"wgcf-account_{time.time()}.toml"
    # generate_account(filename)

    if not os.path.exists("proxy_tested.txt"):
        proxies = proxy_prepare()
        print("proxy prepared")

    files = []
    for file in os.listdir("conf"):
        if file.startswith("wgcf"):
            filename = file
            files.append(filename)
        # with open("proxy_tested.txt", "r") as f:
        #     lines = f.readlines()
        #     if len(lines) > 0:
        #         random.shuffle(lines)
        #         process_account(filename, lines[0].replace('\n', ''))

    random.shuffle(files)
    for filename in files:
        url = f'https://api.cloudflareclient.com/v0a{digitString(3)}/reg'
        process_account(filename)
