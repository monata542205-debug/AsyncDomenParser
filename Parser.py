import requests

import time
import os
import signal
import sys

def resource_path(rel_path):
    """ Работает и при запуске python Parser.py, и в PyInstaller-бандле """
    base = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, rel_path)
def read_files():
    current_dir = resource_path('.')
    files = [f for f in os.listdir(current_dir) if os.path.isfile(os.path.join(current_dir, f))]
    return files
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
def signal_handler(signum, frame):
    global running
    running = False
def main():
    # Чтение записанных дней
    days = days_read()
    print(days)
    # Получаем сегодня, вчера и позавчера
    today, yesterday, beforeyesterday = dates()
    # Проверяем есть ли сегодняшний день в файле
    for day in days:
        if day in [today, yesterday, beforeyesterday]:
            pass
        else:
            os.remove(day + '.txt')
    # перезаписали файл с датами
    days_write(today, yesterday, beforeyesterday)
    # записывам новые файлы с датами которых нет
    files = read_files()
    days = days_read()
    print("Файлы в текущей директории:", files)
    for day in days:
        if day + '.txt' in files:
            pass
        else:
            print(day)
            links = download_url_list(day)
            links_write(links, day)

    # проверяем ссылки в файлах
    days = days_read()
    for day in days:
        links = links_read(day)
        good_links = []
        for domen in links:
            print(domen)
            code, message = check_url('https://' + domen)
            print(f"Статус: {code or 'Нет ответа'}, {message}")
            if code == 200:
                discord_message('https://' + domen)
                links.remove(domen)
                links_write(links, day)
            else:
                pass
        # После чтения всех ссылок перезаписываем файл
        links_write(links, day)

if __name__ == '__main__':
    running = True
    signal.signal(signal.SIGINT, signal_handler)
    while running:
        main()
    print("✅ Цикл завершен")