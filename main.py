import os
import sys
import streams
import day_check
import URL_check
import URL_download
import discord
import signal

def links_division():
    links = URL_download.links_read('links')
    if len(links) < 100:
        print('НЕДОСТАТОЧНО ДАННЫХ ДЛЯ ПРОВЕРКИ. ОТСУТСВУЮТ НОВЫЕ ДОМЕНЫ!!!')
        sys.exit()
    else:
        lenght = int(len(links)/10) + 1
        little_links = []
        i = 0
        j = lenght
        while i < len(links):
            little_links.append(links[i:j])
            i += lenght
            j += lenght

        return little_links
def function_for_stream(links, thread_id):
    filename = f"thread_{thread_id}.txt"
    for url in links:
        try:
            code = URL_check.check_items(url)
            if code == 200:
                file = open(filename, 'a')
                file.write(f"{url}\n")
                file.close()
                discord.discord_message('https://' + url)
            else:
                pass
        except:
            pass

    return links
def signal_handler(signum, frame):
    global running
    running = False
def main():
    # Проверяем вчерашнюю дату
    yesterday = day_check.dates()
    day = day_check.days_read()
    if day == yesterday:
        print('day is respond')
    else:
        day_check.days_write(yesterday)
        date = URL_download.check_url_list()
        if yesterday == date:
            # Загружаем новые ссылки и записываем их в общий список
            URL_download.download_url_list(date)
            new_links = URL_download.links_read('new_links')
            URL_download.links_write(new_links, 'links')
            print('new_links appended to links')
            os.remove('new_links.txt')
            print('new_links deleted')
        else:
            print('data does not download on website')

    little_links = links_division()
    streams.streams(function_for_stream, little_links)

if __name__ == '__main__':
    running = True
    signal.signal(signal.SIGINT, signal_handler)
    while running:
        try:
            links = URL_download.links_read('links')
            good_links = []
            for i in range(1, 11):
                k = URL_download.links_read('thread_' + str(i))
                print(len(k))
                for t in k:
                    good_links.append(t)
            print(len(good_links))
            print(len(links))
            result = [x for x in links if x not in good_links]
            URL_download.bad_links_write(result, 'links')
        except:
            pass
        for i in range(1, 11):
            k = open('thread_' + str(i) + '.txt', 'w')
            k.close()
        main()