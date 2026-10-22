#!/usr/bin/env python3
import os
import sys
import phonenumbers
from phonenumbers import geocoder, carrier, timezone
import requests
import socket
import webbrowser
import dns.resolver
import concurrent.futures

# ==========================================
# ANSI COLOR CODES
# ==========================================
RED = '\033[1;31m'
BLUE = '\033[1;34m'
CYAN = '\033[1;36m'
GREEN = '\033[1;32m'
YELLOW = '\033[1;33m'
MAGENTA = '\033[1;35m'
WHITE = '\033[1;37m'
NC = '\033[0m'

def clear_screen():
    os.system('clear')

def print_banner():
    print(f"""{RED}
    ██████╗ ███████╗ █████╗ ██╗██████╗ 
    ██╔═══██╗██╔════╝██╔══██╗██║██╔══██╗
    ██║   ██║███████╗███████║██║██║  ██║
    ██║   ██║╚════██║██╔══██║██║██║  ██║
    ╚██████╔╝███████║██║  ██║██║██████╔╝
     ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝╚═════╝ 
{BLUE}          [ O S I N T   T O O L ]{RED}
    {YELLOW}        👁️ Created by: ØSÄÎD HAK 👁️{NC}
{MAGENTA}    ═══════════════════════════════════════════════════════════{NC}
{GREEN}        🇵🇸  FREE PALESTINE  🇵🇸{NC}
{MAGENTA}    ═══════════════════════════════════════════════════════════{NC}
    """)

def open_url(url):
    # Open URL silently without printing it
    if os.system(f'termux-open-url "{url}" > /dev/null 2>&1') != 0:
        webbrowser.open(url)

# ==========================================
# MODULE 1: PHONE LOOKUP
# ==========================================
def lookup_phone(phone_number):
    print(f"\n{CYAN}[⚡] Analyzing Phone Number: {phone_number}{NC}")
    print(f"{BLUE}=================================================={NC}")
    
    try:
        parsed_number = phonenumbers.parse(phone_number, None)
        if not phonenumbers.is_valid_number(parsed_number):
            print(f"{RED}[✖] Invalid phone number format!{NC}")
            return

        country = geocoder.description_for_number(parsed_number, "en")
        carrier_name = carrier.name_for_number(parsed_number, "en")
        region_code = phonenumbers.region_code_for_number(parsed_number)
        time_zones = timezone.time_zones_for_number(parsed_number)
        
        print(f"{GREEN}[✔] Country/Region   : {country if country else 'Unknown'} ({region_code}){NC}")
        print(f"{GREEN}[✔] Carrier/Provider : {carrier_name if carrier_name else 'Unknown'}{NC}")
        print(f"{GREEN}[✔] Timezone         : {', '.join(time_zones)}{NC}")
        
        print(f"\n{YELLOW}[?] 👁️ Do you want to open the Telegram account linked to this number? (y/n){NC}")
        choice = input(f"{MAGENTA}osaid > {NC}").strip().lower()
        
        if choice == 'y':
            clean_number = phone_number.replace("+", "").replace(" ", "").replace("-", "")
            telegram_url = f"https://t.me/+{clean_number}"
            print(f"{GREEN}[✔] Opening Telegram...{NC}")
            open_url(telegram_url)
        else:
            print(f"{YELLOW}[-] Cancelled.{NC}")
                
    except Exception as e:
        print(f"{RED}[✖] Error: {e}{NC}")

# ==========================================
# MODULE 2: IP LOOKUP
# ==========================================
def lookup_ip(ip_address):
    print(f"\n{CYAN}[⚡] Analyzing IP Address: {ip_address}{NC}")
    print(f"{BLUE}=================================================={NC}")
    
    try:
        url = f"http://ip-api.com/json/{ip_address}?fields=status,message,continent,country,countryCode,region,regionName,city,district,zip,lat,lon,timezone,offset,currency,isp,org,as,asname,reverse,mobile,proxy,hosting,query"
        response = requests.get(url, timeout=10)
        data = response.json()

        if data["status"] == "fail":
            print(f"{RED}[✖] Error: {data['message']}{NC}")
            return

        print(f"{GREEN}[✔] IP Address       : {data.get('query', 'N/A')}{NC}")
        print(f"{GREEN}[✔] Continent        : {data.get('continent', 'N/A')}{NC}")
        print(f"{GREEN}[✔] Country          : {data.get('country', 'N/A')} ({data.get('countryCode', 'N/A')}){NC}")
        print(f"{GREEN}[✔] Region/State     : {data.get('regionName', 'N/A')}{NC}")
        print(f"{GREEN}[✔] City             : {data.get('city', 'N/A')}{NC}")
        print(f"{GREEN}[✔] ISP / Provider   : {data.get('isp', 'N/A')}{NC}")
        print(f"{GREEN}[✔] Organization     : {data.get('org', 'N/A')}{NC}")
        print(f"{GREEN}[✔] Is Proxy/VPN     : {'Yes' if data.get('proxy') or data.get('hosting') else 'No'}{NC}")

        lat, lon = data.get('lat'), data.get('lon')
        if lat and lon:
            print(f"\n{YELLOW}[?] 👁️ Do you want to open the location on Google Maps? (y/n){NC}")
            choice = input(f"{MAGENTA}osaid > {NC}").strip().lower()
            if choice == 'y':
                map_url = f"https://www.google.com/maps?q={lat},{lon}"
                print(f"{GREEN}[✔] Opening Maps...{NC}")
                open_url(map_url)

    except Exception as e:
        print(f"{RED}[✖] Error: {e}{NC}")

# ==========================================
# MODULE 3 & 4: USERNAME / EMAIL HUNT
# ==========================================
def check_site(target, site_info, target_type):
    site_name = site_info['name']
    url = site_info['url'].format(target)
    
    if target_type == 'email':
        url = f"https://www.google.com/search?q=%22{target}%22+site:{site_info['domain']}"
        
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            return (site_name, url)
    except:
        pass
    return None

def search_target(target, target_type):
    print(f"\n{CYAN}[⚡] Searching for {target_type.upper()}: '{target}' across platforms...{NC}")
    print(f"{BLUE}=================================================={NC}")
    print(f"{YELLOW}[!] 🔥 This might take 10-20 seconds...{NC}\n")

    sites = [
        {"name": "Instagram", "url": "https://www.instagram.com/{}/", "domain": "instagram.com"},
        {"name": "Facebook", "url": "https://www.facebook.com/{}", "domain": "facebook.com"},
        {"name": "Twitter/X", "url": "https://twitter.com/{}", "domain": "twitter.com"},
        {"name": "TikTok", "url": "https://www.tiktok.com/@{}", "domain": "tiktok.com"},
        {"name": "Snapchat", "url": "https://www.snapchat.com/add/{}", "domain": "snapchat.com"},
        {"name": "GitHub", "url": "https://github.com/{}", "domain": "github.com"},
        {"name": "Reddit", "url": "https://www.reddit.com/user/{}", "domain": "reddit.com"},
        {"name": "Pinterest", "url": "https://www.pinterest.com/{}/", "domain": "pinterest.com"},
        {"name": "YouTube", "url": "https://www.youtube.com/@{}", "domain": "youtube.com"},
        {"name": "Twitch", "url": "https://www.twitch.tv/{}", "domain": "twitch.tv"},
        {"name": "Telegram", "url": "https://t.me/{}", "domain": "t.me"},
        {"name": "Medium", "url": "https://medium.com/@{}", "domain": "medium.com"},
        {"name": "GitLab", "url": "https://gitlab.com/{}", "domain": "gitlab.com"},
        {"name": "Steam", "url": "https://steamcommunity.com/id/{}", "domain": "steamcommunity.com"},
        {"name": "SoundCloud", "url": "https://soundcloud.com/{}", "domain": "soundcloud.com"},
        {"name": "Spotify", "url": "https://open.spotify.com/user/{}", "domain": "spotify.com"},
        {"name": "Flickr", "url": "https://www.flickr.com/people/{}/", "domain": "flickr.com"},
        {"name": "Tumblr", "url": "https://{}.tumblr.com", "domain": "tumblr.com"},
        {"name": "DeviantArt", "url": "https://www.deviantart.com/{}", "domain": "deviantart.com"},
        {"name": "Behance", "url": "https://www.behance.net/{}", "domain": "behance.net"},
        {"name": "Dribbble", "url": "https://dribbble.com/{}", "domain": "dribbble.com"},
        {"name": "Patreon", "url": "https://www.patreon.com/{}", "domain": "patreon.com"},
        {"name": "Goodreads", "url": "https://www.goodreads.com/{}", "domain": "goodreads.com"},
        {"name": "WordPress", "url": "https://{}.wordpress.com", "domain": "wordpress.com"},
        {"name": "Linktree", "url": "https://linktr.ee/{}", "domain": "linktr.ee"},
        {"name": "Keybase", "url": "https://keybase.io/{}", "domain": "keybase.io"},
        {"name": "Mastodon", "url": "https://mastodon.social/@{}", "domain": "mastodon.social"},
        {"name": "Quora", "url": "https://www.quora.com/profile/{}", "domain": "quora.com"},
        {"name": "Imgur", "url": "https://imgur.com/user/{}", "domain": "imgur.com"},
        {"name": "9GAG", "url": "https://9gag.com/u/{}", "domain": "9gag.com"},
        {"name": "AskFM", "url": "https://ask.fm/{}", "domain": "ask.fm"},
        {"name": "Discord", "url": "https://discord.com/users/{}", "domain": "discord.com"},
        {"name": "HackerRank", "url": "https://www.hackerrank.com/{}", "domain": "hackerrank.com"},
        {"name": "Codepen", "url": "https://codepen.io/{}", "domain": "codepen.io"},
        {"name": "Replit", "url": "https://replit.com/@{}", "domain": "replit.com"},
        {"name": "DockerHub", "url": "https://hub.docker.com/u/{}", "domain": "hub.docker.com"},
        {"name": "Pastebin", "url": "https://pastebin.com/u/{}", "domain": "pastebin.com"},
        {"name": "VK", "url": "https://vk.com/{}", "domain": "vk.com"},
        {"name": "OK", "url": "https://ok.ru/{}", "domain": "ok.ru"},
        {"name": "Weibo", "url": "https://weibo.com/{}", "domain": "weibo.com"},
        {"name": "Line", "url": "https://line.me/ti/p/~{}", "domain": "line.me"},
        {"name": "LinkedIn", "url": "https://www.linkedin.com/in/{}", "domain": "linkedin.com"},
        {"name": "Google Search", "url": "https://www.google.com/search?q=%22{}%22", "domain": "google.com"},
        {"name": "Bing Search", "url": "https://www.bing.com/search?q=%22{}%22", "domain": "bing.com"},
        {"name": "Yandex Search", "url": "https://yandex.com/search/?text=%22{}%22", "domain": "yandex.com"},
        {"name": "DuckDuckGo", "url": "https://duckduckgo.com/?q=%22{}%22", "domain": "duckduckgo.com"},
        {"name": "GitHub Gists", "url": "https://gist.github.com/{}", "domain": "gist.github.com"},
        {"name": "Mastodon (Alt)", "url": "https://mstdn.social/@{}", "domain": "mstdn.social"},
        {"name": "Threads", "url": "https://www.threads.net/@{}", "domain": "threads.net"},
        {"name": "Bluesky", "url": "https://bsky.app/profile/{}.bsky.social", "domain": "bsky.app"}
    ]

    found_links = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        futures = [executor.submit(check_site, target, site, target_type) for site in sites]
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                found_links.append(result)

    unique_links = list(set(found_links))
    
    print(f"\n{BLUE}=================================================={NC}")
    print(f"{YELLOW}[!] ⚡ Total Found: {len(unique_links)} / {len(sites)} platforms{NC}")
    print(f"{BLUE}=================================================={NC}")
    
    if not unique_links:
        print(f"{RED}[✖] {target_type.capitalize()} not found on any platform.{NC}")
        return

    print(f"\n{MAGENTA}Select a number to open the link:{NC}")
    for idx, (name, url) in enumerate(unique_links, 1):
        print(f" {CYAN}[{idx}]{NC} {GREEN}{name}{NC}")

    try:
        choice = int(input(f"\n{MAGENTA}osaid > {NC}"))
        if 1 <= choice <= len(unique_links):
            selected_name, selected_url = unique_links[choice - 1]
            print(f"{GREEN}[✔] Opening {selected_name}...{NC}")
            open_url(selected_url)
        else:
            print(f"{RED}[✖] Invalid number!{NC}")
    except ValueError:
        print(f"{RED}[✖] Please enter a valid number.{NC}")

def main():
    clear_screen()
    print_banner()
    
    while True:
        print(f"\n{BLUE}Choose a Target Type:{NC}")
        print(f"{CYAN}[1]{NC} 📱 Phone Number (Lookup + Telegram)")
        print(f"{CYAN}[2]{NC} 🌐 IP Address (Deep Lookup)")
        print(f"{CYAN}[3]{NC} 👤 Username (Hunt across platforms)")
        print(f"{CYAN}[4]{NC} 📧 Email / Gmail (Hunt across platforms)")
        print(f"{CYAN}[0]{NC} ❌ Exit")
        
        choice = input(f"\n{MAGENTA}osaid > {NC}")
        
        if choice == '1':
            phone = input(f"{CYAN}Enter phone number (e.g., +970599123456): {NC}")
            lookup_phone(phone)
            input(f"\n{YELLOW}Press Enter to continue...{NC}")
            clear_screen()
            print_banner()
        elif choice == '2':
            ip = input(f"{CYAN}Enter IP address (e.g., 8.8.8.8): {NC}")
            lookup_ip(ip)
            input(f"\n{YELLOW}Press Enter to continue...{NC}")
            clear_screen()
            print_banner()
        elif choice == '3':
            username = input(f"{CYAN}Enter username (e.g., osaid): {NC}")
            search_target(username, "username")
            input(f"\n{YELLOW}Press Enter to continue...{NC}")
            clear_screen()
            print_banner()
        elif choice == '4':
            email = input(f"{CYAN}Enter email (e.g., example@gmail.com): {NC}")
            search_target(email, "email")
            input(f"\n{YELLOW}Press Enter to continue...{NC}")
            clear_screen()
            print_banner()
        elif choice == '0':
            print(f"{RED}Exiting... Stay safe! ☠{NC}")
            break
        else:
            print(f"{RED}[✖] Invalid choice!{NC}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{RED}Exiting...{NC}")