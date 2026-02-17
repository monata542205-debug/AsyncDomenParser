import requests
import os
import sys

def resource_path(rel_path):
    """ Работает и при запуске python Parser.py, и в PyInstaller-бандле """
    base = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, rel_path)
def discord_message(url):
    file = open(resource_path('webhook.txt'), 'r')
    WEBHOOK_URL = file.read()
    file.close()

    payload = {
        "content": f"✅ **Новый зарегистрированный домен:** {url}"
    }

    # Отправляем POST-запрос
    response = requests.post(WEBHOOK_URL, json=payload)

    if response.status_code == 204:
        print("Сообщение успешно отправлено в Discord!")
    else:
        print(f"Ошибка: {response.status_code}")

