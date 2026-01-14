import os
import time
import json
import uuid
import random
from datetime import datetime, timezone
import pytz
from curl_cffi import requests
from eth_account import Account
from eth_account.messages import encode_defunct
from colorama import Fore, Style, init

os.system('clear' if os.name == 'posix' else 'cls')

import warnings
warnings.filterwarnings('ignore')

import sys
if not sys.warnoptions:
    import os
    os.environ["PYTHONWARNINGS"] = "ignore"

init(autoreset=True)

class VeeraBot:
    def __init__(self, private_key, proxy=None):
        self.account = Account.from_key(private_key)
        self.address = self.account.address
        self.proxy = proxy
        self.session = requests.Session(impersonate="chrome124")
        
        if self.proxy:
            self.session.proxies = {"http": self.proxy, "https": self.proxy}

    def get_wib_time(self):
        wib = pytz.timezone('Asia/Jakarta')
        return datetime.now(wib).strftime('%H:%M:%S')

    def print_banner(self):
        banner = f"""
{Fore.CYAN}VEERA AUTO BOT{Style.RESET_ALL}
{Fore.WHITE}By: FEBRIYAN{Style.RESET_ALL}
{Fore.CYAN}============================================================{Style.RESET_ALL}
"""
        print(banner)

    def log(self, message, level="INFO"):
        time_str = self.get_wib_time()
        
        if level == "INFO":
            color = Fore.CYAN
            symbol = "[INFO]"
        elif level == "SUCCESS":
            color = Fore.GREEN
            symbol = "[SUCCESS]"
        elif level == "ERROR":
            color = Fore.RED
            symbol = "[ERROR]"
        elif level == "WARNING":
            color = Fore.YELLOW
            symbol = "[WARNING]"
        elif level == "CYCLE":
            color = Fore.MAGENTA
            symbol = "[CYCLE]"
        else:
            color = Fore.WHITE
            symbol = "[LOG]"
        
        print(f"[{time_str}] {color}{symbol} {message}{Style.RESET_ALL}")

    def get_headers(self):
        return {
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "origin": "https://hub.veerarewards.com",
            "referer": "https://hub.veerarewards.com/loyalty",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "sec-ch-ua": '"Google Chrome";v="124", "Chromium";v="124", "Not-A.Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin"
        }

    def get_csrf(self):
        url = "https://hub.veerarewards.com/api/auth/csrf"
        try:
            resp = self.session.get(url, headers=self.get_headers())
            if resp.status_code == 200:
                return resp.json().get("csrfToken")
            return None
        except Exception as e:
            self.log(f"Error CSRF: {e}", "ERROR")
            return None

    def login(self):
        csrf_token = self.get_csrf()
        if not csrf_token: return False

        issued_at = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        
        siwe_message = f"""hub.veerarewards.com wants you to sign in with your Ethereum account:
{self.address}

Sign in to the app. Powered by Snag Solutions.

URI: https://hub.veerarewards.com
Version: 1
Chain ID: 97
Nonce: {csrf_token}
Issued At: {issued_at}"""

        signed_msg = self.account.sign_message(encode_defunct(text=siwe_message))
        signature = signed_msg.signature.hex()

        message_json = {
            "domain": "hub.veerarewards.com",
            "address": self.address,
            "statement": "Sign in to the app. Powered by Snag Solutions.",
            "uri": "https://hub.veerarewards.com",
            "version": "1",
            "chainId": 97,
            "nonce": csrf_token,
            "issuedAt": issued_at
        }

        url = "https://hub.veerarewards.com/api/auth/callback/credentials"
        headers = self.get_headers()
        headers["content-type"] = "application/x-www-form-urlencoded"

        payload = {
            "message": json.dumps(message_json, separators=(',', ':')),
            "accessToken": signature,
            "signature": signature,
            "walletConnectorName": "MetaMask",
            "walletAddress": self.address,
            "redirect": "false",
            "callbackUrl": "/protected",
            "chainType": "evm",
            "walletProvider": "undefined",
            "csrfToken": csrf_token,
            "json": "true"
        }

        try:
            resp = self.session.post(url, headers=headers, data=payload)
            if resp.status_code == 200:
                self.log("Login successful!", "SUCCESS")
                return True
            else:
                self.log(f"Login Failed: {resp.text}", "ERROR")
                return False
        except Exception as e:
            self.log(f"Login Error: {e}", "ERROR")
            return False

    def complete_mission(self, quest_id, quest_name="Unknown"):
        url = f"https://hub.veerarewards.com/api/loyalty/rules/{quest_id}/complete"
        
        headers = self.get_headers()
        headers["content-type"] = "application/json"
        
        payload = {}

        try:
            self.log(f"Claiming {quest_name}...", "INFO")
            resp = self.session.post(url, headers=headers, json=payload)
            
            if resp.status_code == 200 or resp.status_code == 201:
                res_json = resp.json()
                msg = res_json.get("message", "Success")
                self.log(f"Claim Success", "SUCCESS")
            elif resp.status_code == 400:
                self.log(f"Already Claimed", "WARNING")
            else:
                self.log(f"Claim Failed {resp.status_code}: {resp.text}", "ERROR")
        except Exception as e:
            self.log(f"Error Claiming: {e}", "ERROR")

    def random_delay(self):
        delay = random.randint(2, 5)
        time.sleep(delay)

    def show_menu(self):
        print(f"{Fore.CYAN}============================================================{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Select Mode:{Style.RESET_ALL}")
        print(f"{Fore.GREEN}1. Run with proxy")
        print(f"2. Run without proxy{Style.RESET_ALL}")
        print(f"{Fore.CYAN}============================================================{Style.RESET_ALL}")
        
        while True:
            try:
                choice = input(f"{Fore.GREEN}Enter your choice (1/2): {Style.RESET_ALL}").strip()
                if choice in ['1', '2']:
                    return choice
                else:
                    print(f"{Fore.RED}Invalid choice! Please enter 1 or 2.{Style.RESET_ALL}")
            except KeyboardInterrupt:
                print(f"\n{Fore.RED}Program terminated by user.{Style.RESET_ALL}")
                exit(0)

    def countdown(self, seconds):
        for i in range(seconds, 0, -1):
            hours = i // 3600
            minutes = (i % 3600) // 60
            secs = i % 60
            print(f"\r[COUNTDOWN] Next cycle in: {hours:02d}:{minutes:02d}:{secs:02d} ", end="", flush=True)
            time.sleep(1)
        print("\r" + " " * 60 + "\r", end="", flush=True)

    def run_account(self, account_num, total_accounts, proxy_info):
        self.log(f"Account #{account_num}/{total_accounts}", "INFO")
        self.log(f"Proxy: {proxy_info}", "INFO")
        self.log(f"{self.address[:6]}...{self.address[-4:]}", "INFO")
        
        self.random_delay()
        
        if self.login():
            missions = [
                {"id": "0c2c81eb-c631-48a8-9f27-a97d192e0039", "name": "Daily Task"},
            ]
            
            for mission in missions:
                self.random_delay()
                self.complete_mission(mission["id"], mission["name"])
            
            return True
        return False

def load_file(filename):
    try:
        with open(filename, 'r') as f:
            return [line.strip() for line in f if line.strip()]
    except: return []

if __name__ == "__main__":
    bot_instance = VeeraBot.__new__(VeeraBot)
    bot_instance.print_banner()
    
    choice = bot_instance.show_menu()
    use_proxy = (choice == '1')
    
    accounts = load_file('accounts.txt')
    proxies = load_file('proxy.txt') if use_proxy else []
    
    if not accounts:
        print(f"{Fore.RED}No accounts found in accounts.txt!{Style.RESET_ALL}")
        exit(1)
    
    bot_instance.log(f"Loaded {len(accounts)} accounts successfully", "INFO")
    
    if use_proxy:
        bot_instance.log(f"Running with proxy", "INFO")
    else:
        bot_instance.log(f"Running without proxy", "INFO")
    
    print(f"\n{Fore.CYAN}============================================================{Style.RESET_ALL}\n")
    
    cycle = 1
    while True:
        bot_instance.log(f"Cycle #{cycle} Started", "CYCLE")
        print(f"{Fore.CYAN}------------------------------------------------------------{Style.RESET_ALL}")
        
        success_count = 0
        total_accounts = len(accounts)
        
        for i, pk in enumerate(accounts):
            proxy = proxies[i % len(proxies)] if proxies else None
            proxy_info = proxy if proxy else "No Proxy"
            
            try:
                bot = VeeraBot(pk, proxy)
                if bot.run_account(i+1, total_accounts, proxy_info):
                    success_count += 1
            except Exception as e:
                bot_instance.log(f"Critical Error Account {i+1}: {e}", "ERROR")
            
            if i < total_accounts - 1:
                print(f"{Fore.WHITE}............................................................{Style.RESET_ALL}")
                time.sleep(2)
        
        print(f"{Fore.CYAN}------------------------------------------------------------{Style.RESET_ALL}")
        bot_instance.log(f"Cycle #{cycle} Complete | Success: {success_count}/{total_accounts}", "CYCLE")
        print(f"{Fore.CYAN}============================================================{Style.RESET_ALL}\n")
        
        cycle += 1
        
        wait_time = 86400
        bot_instance.countdown(wait_time)
