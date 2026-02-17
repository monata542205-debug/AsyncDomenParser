import requests
import os
import sys
import zipfile
import base64
from bs4 import BeautifulSoup

def resource_path(rel_path):
    """ Работает и при запуске python Parser.py, и в PyInstaller-бандле """
    base = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, rel_path)
def links_write(links, today):
    with open(resource_path(today + '.txt'), 'a', encoding='utf-8') as f:
        f.write('\n'.join(links))
def bad_links_write(links, today):
    with open(resource_path(today + '.txt'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(links))
def links_read(date):
    with open(resource_path(date + '.txt'), 'r', encoding='utf-8') as f:
        links = [line.strip() for line in f.readlines()]
    return links
def download_url_list(date):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Cache-Control': 'max-age=0',
    }

    b64_part = base64.b64encode(date.encode() + b".zip").decode().rstrip("=")
    url = f"https://www.whoisds.com/whois-database/newly-registered-domains/{b64_part}/nrd"
    print("downloading links...")
    response = requests.get(url, timeout=30, headers=headers)

    if response.status_code == 200:
        filename = f"nrd-{date}.zip"
        with open(resource_path(filename), "wb") as f:
            f.write(response.content)
        print(f"downloaded → {filename}  ({len(response.content) / 1024 / 1024:.1f} MB)")
        with zipfile.ZipFile(resource_path(f"nrd-{date}.zip"), "r") as zip_ref:
            zip_ref.extractall()  # → в текущую директорию
        print(f"nrd-{date}.zip unziped in domain-names.txt")
        os.remove(resource_path(f"nrd-{date}.zip"))
        os.rename(resource_path(f"domain-names.txt"), "new_links.txt")
        print(f"nrd-{date}.zip deleted")
        print("domain-names.txt renamed in new_links.txt")
    else:
        print("error:", response.status_code)
def check_url_list():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Cache-Control': 'max-age=0',
    }

    url = "https://www.whoisds.com/newly-registered-domains"
    response = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")
    date = soup.find(class_='table-bordered').find('td').text[:10]
    print("lust date found: ", date)
    return date

if __name__ == '__main__':
    date = check_url_list()
    date = '2026-02-14'
    download_url_list(date)