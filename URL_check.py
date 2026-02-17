import time
import requests

def check_items(url):
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
    print('Checking ', url)
    try:
        response = requests.get('https://' + url, timeout=5, headers=headers)
        code = response.status_code
        print('result: ',code)
        return code
    except requests.exceptions.ConnectionError:
        print("Ошибка подключения")
        return None
    except requests.exceptions.Timeout:
        print("Таймаут")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Ошибка: {e}")
        return None
    time.sleep(1)

if __name__ == '__main__':
    code = check_items('ya.ru')